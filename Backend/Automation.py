from AppOpener import close, open as appopen  # Functions to open and close apps
from webbrowser import open as webopen  # Browser functionality
from pywhatkit import search, playonyt  # Functions for Google search and YouTube playback
from dotenv import dotenv_values  # Manage environment variables
from bs4 import BeautifulSoup  # Parse HTML content
from rich import print  # Rich for styled console output
from groq import Groq  # Groq API for chat functionalities
import webbrowser  # Web browser for opening URLs
import subprocess  # For interacting with the system
import requests  # For HTTP requests
import keyboard  # For keyboard-related actions
import asyncio  # For asynchronous programming
import os  # For operating system functionalities

# Load environment variables from the .env file
env_vars = dotenv_values(".env")

GroqAPIKey = env_vars.get("GroqAPIKey")  # Retrieve the Groq API key

# Define CSS classes for parsing specific elements in HTML content
classes = ["zCubwf", "hgKElc", "LTKOO", "SY7ric", "Z0LcW", "gsrt", "vk_bk", "FzvWSb", "YwPhnf", "pclqee", 
           "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "05uR6d", "LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table", 
           "dDoNo", "Ikb48b", "gart", "sklade", "LWkfke", "VQF4g", "qv3wpe", "kno-rdesc", "SPZz6h"]

# Define a user agent for making web requests
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"

# Initialize the Groq client with the API key
client = Groq(api_key=GroqAPIKey)

# Predefined professional responses
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need — don't hesitate to ask."
]

# Store chatbot messages
messages = []

# System message to provide context to the chatbot
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['USERNAME']}. You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems, etc."}]

# Function to perform a Google search
def GoogleSearch(Topic):
    search(Topic)  # Use pywhatkit's search function to perform a Google search
    return True  # Indicate success




# Function to summarize content, write it to a file, and open in Notepad
def Content(Topic):
    # Nested function to open a file in Notepad
    def OpenNotepad(File):
        default_text_editor = "notepad.exe"  # Default text editor (Notepad)
        subprocess.Popen([default_text_editor, File])  # Open the file in Notepad

    # Nested function to generate content using the AI
    def ContentByAI(prompt):
        messages.append({"role": "user", "content": prompt})  # Add the user's prompt to messages

        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Specify the AI model
            messages=SystemChatBot + messages,  # Include system instructions and chat history
            max_tokens=2048,  # Limit the maximum tokens in the response
            temperature=0.7,  # Adjust response randomness
            top_p=1,  # Use nucleus sampling for response diversity
            stream=True,  # Enable streaming response
            stop=None  # Allow the model to determine stopping conditions
        )

        # Initialize an empty string for the response
        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:  # Check for content in the current chunk
                Answer += chunk.choices[0].delta.content  # Append the content to the answer

        Answer = Answer.replace("</s>", "")  # Remove unwanted tokens from the response
        messages.append({"role": "assistant", "content": Answer})  # Add the AI's response to messages
        return Answer

    Topic = Topic.replace("Content", "")  # Remove "Content" from the topic
    generated_content = ContentByAI(Topic)  # Generate content using AI

    # Save the generated content to a text file
    with open(rf"Data\{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as file:
        file.write(generated_content)  # Write the content to the file

    # Open the file in Notepad
    OpenNotepad(rf"Data\{Topic.lower().replace(' ', '')}.txt")

    return True  # Indicate success

# Function to search for a topic on YouTube
def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"  # Construct the YouTube search URL
    webbrowser.open(Url4Search)  # Open the search URL in a web browser
    return True  # Indicate success

# Function to play a video on YouTube
def PlayYoutube(query):
    
    playonyt(query)  # Use pywhatkit's playonyt function to play the video
    return True  # Indicate success


# Function to open an application or relevant webpage
def OpenApp(app):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)  # Open the app
        return True  # Indicate success
    except:
        return False  # Indicate failure

# Function to extract links from HTML content
def extract_links(html):
    if html is None:
        return []

    soup = BeautifulSoup(html, 'html.parser')  # Parse the HTML content
    links = soup.find_all('a', {'jsname': 'UWckNb'})  # Find relevant links
    return [link.get('href') for link in links]  # Return the links

# Function to perform a Google search and retrieve HTML content
def search_google(query):
    url = f"https://www.google.com/search?q={query}"  # Construct the Google search URL
    headers = {"User-Agent": useragent}  # Use the predefined user-agent
    response = requests.get(url, headers=headers)  # Perform the GET request

    if response.status_code == 200:
        return response.text  # Return the HTML content
    else:
        print("Failed to retrieve search results.")  # Print an error message
        return None

# Function to open a URL based on a Google search
def OpenLinkFromGoogle(query):
    html = search_google(query)  # Perform the Google search
    if html:
        link = extract_links(html)[0]  # Extract the first link from the search results
        webopen(link)  # Open the link in a web browser
        return True  # Indicate success
    return False  # Indicate failure

# Function to close an application
def CloseApp(app):
    if "chrome" in app:
        pass  # Skip if the app is Chrome
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)  # Attempt to close the app
            return True  # Indicate success
        except:
            return False  # Indicate failure

# Function to execute system-level commands
def System(command):
    # Nested function to mute the system volume
    def mute():
        keyboard.press_and_release("volume mute")  # Simulate the mute key press

    # Nested function to unmute the system volume
    def unmute():
        keyboard.press_and_release("volume mute")  # Simulate the unmute key press

    # Nested function to increase the system volume
    def volume_up():
        keyboard.press_and_release("volume up")  # Simulate the volume up key press

    # Nested function to decrease the system volume
    def volume_down():
        keyboard.press_and_release("volume down")  # Simulate the volume down key press

    # Execute the appropriate command
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()

    return True  # Indicate success

# Asynchronous function to translate and execute user commands
async def TranslateAndExecute(commands: list[str]):
    funcs = []  # List to store asynchronous tasks

    for command in commands:
        if command.startswith("open"):
            if "open it" in command:  # Ignore "open it" commands
                continue
            elif "open file" in command:  # Ignore open file commands
                continue
            else:
                func = asyncio.to_thread(OpenApp, command.removeprefix("open"))  # Schedule app opening
                funcs.append(func)

        elif command.startswith("close"):
            func = asyncio.to_thread(CloseApp, command.removeprefix("close"))  # Schedule app closing
            funcs.append(func)

        elif command.startswith("play"):
            func = asyncio.to_thread(PlayYoutube, command.removeprefix("play"))  # Schedule YouTube playback
            funcs.append(func)

        elif command.startswith("content"):
            func = asyncio.to_thread(Content, command.removeprefix("content"))  # Schedule content creation
            funcs.append(func)

        elif command.startswith("google search"):
            func = asyncio.to_thread(GoogleSearch, command.removeprefix("google search"))  # Schedule Google search
            funcs.append(func)

        elif command.startswith("youtube search"):
            func = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search"))  # Schedule YouTube search
            funcs.append(func)

        elif command.startswith("system"):
            func = asyncio.to_thread(System, command.removeprefix("system"))  # Schedule system command
            funcs.append(func)

        else:
            print(f"No Function Found for {command}")  # Print an error for unrecognized commands

    results = await asyncio.gather(*funcs)  # Execute all tasks concurrently
    for result in results:  # Process the results
        if isinstance(result, str):
            yield result
        else:
            yield result

# Asynchronous function to automate command execution
async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass  # Execute commands
    return True  # Indicate success
