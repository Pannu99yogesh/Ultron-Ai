import cohere
from rich import print
from dotenv import dotenv_values
from difflib import get_close_matches

# Load environment variables
env_vars = dotenv_values(".env")
CohereAPIKey = env_vars.get("CohereAPIKey")

if not CohereAPIKey:
    raise ValueError("Cohere API Key not found in the .env file!")

co = cohere.Client(api_key=CohereAPIKey)

# All valid function prefixes
funcs = [
    "exit", "general", "realtime", "open", "close", "play",
    "generate image", "system", "content", "google search",
    "youtube search", "reminder"
]

# Instruction for the model
preamble = """
You are a very accurate Decision-Making Model. Your job is to classify the query into one or more categories:
- general
- realtime
- open
- close
- play
- generate image
- reminder
- system
- content
- google search
- youtube search
- exit

Respond strictly in the format: category query
Examples:
- "who was akbar?" → general who was akbar?
- "what is today's news?" → realtime what is today's news?
- "open chrome and notepad" → open chrome, open notepad
- "bye" → exit

*** Never answer the query. Just classify it. If unsure, fallback to 'general (query)'. ***
"""

# Few-shot examples for context
ChatHistory = [
    {"role": "User", "message": "how are you?"},
    {"role": "Chatbot", "message": "general how are you?"},
    {"role": "User", "message": "open chrome and tell me about mahatma gandhi"},
    {"role": "Chatbot", "message": "open chrome, general tell me about mahatma gandhi"},
    {"role": "User", "message": "what is today's date and remind me of exam on 5th June at 9am"},
    {"role": "Chatbot", "message": "general what is today's date, reminder 9:00am 5th June exam"},
    {"role": "User", "message": "generate image of a flying car"},
    {"role": "Chatbot", "message": "generate image of a flying car"}
]

# --- Normalizer ---
def normalize_and_correct(raw_tasks: list[str]) -> list[str]:
    cleaned = []
    for task in raw_tasks:
        task = task.strip().lower()

        if not task:
            continue

        # Get the prefix (first 2 words to support multi-word categories)
        prefix = " ".join(task.split()[:2]) if len(task.split()) >= 2 else task.split()[0]
        match = get_close_matches(prefix, funcs, n=1, cutoff=0.8)

        if match:
            if match[0] in task:
                corrected = task
            else:
                corrected = match[0] + " " + " ".join(task.split()[1:])
            cleaned.append(corrected.strip())

        elif any(task.startswith(f) for f in funcs):
            cleaned.append(task)

        else:
            print(f"[yellow]⚠ Unrecognized task:[/yellow] '{task}', defaulting to general")
            cleaned.append(f"general {task}")

    return cleaned

# --- Main Decision Model ---
def FirstLayerDMM(prompt: str = "test", retries: int = 1) -> list[str]:
    print(f"[blue]🧠 Classifying:[/blue] {prompt}")
    try:
        stream = co.chat_stream(
            model='command-r-plus',
            message=prompt,
            temperature=0.3,
            chat_history=ChatHistory,
            prompt_truncation='OFF',
            connectors=[],
            preamble=preamble
        )

        raw_output = ""
        for event in stream:
            if event.event_type == "text-generation":
                raw_output += event.text

        raw_output = raw_output.strip()
        print(f"[green]🧾 Raw model output:[/green] {raw_output}")

        if not raw_output:
            raise ValueError("Empty response from model.")

        raw_list = [r.strip() for r in raw_output.replace("\n", "").split(",") if r.strip()]

        # Normalize & correct
        tasks = normalize_and_correct(raw_list)

        if not tasks and retries > 0:
            print("[red]❌ Empty classification, retrying...[/red]")
            return FirstLayerDMM(prompt, retries=retries - 1)

        return tasks

    except Exception as e:
        print(f"[bold red]🚨 Model error:[/bold red] {e}")
        print(f"[yellow]⚠ Fallback: enforcing 'general {prompt}'[/yellow]")
        return [f"general {prompt}"]

# --- CLI Test Mode ---
if __name__ == "__main__":
    while True:
        user_input = input(">>> ")
        result = FirstLayerDMM(user_input)
        print("[bold cyan]Decision →[/bold cyan]", result)



        



