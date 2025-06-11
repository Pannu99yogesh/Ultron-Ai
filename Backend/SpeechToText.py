
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt
import time

# Load environment variables from the .env file
env_vars = dotenv_values(".env")

# Get the input language setting from the environment variables (default to 'en' if not set)
InputLanguage = env_vars.get("InputLanguage", "en")

# Define the HTML code for the speech recognition interface
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = '';
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;

            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                output.textContent = transcript;
            };

            recognition.onerror = function(event) {
                console.error('Speech recognition error:', event.error);
            };

            recognition.onend = function() {
                // Don't automatically restart
            };
            
            recognition.start();
        }

        function stopRecognition() {
            if (recognition) {
                recognition.stop();
            }
        }
    </script>
</body>
</html>'''

# Ensure Data directory exists
os.makedirs("Data", exist_ok=True)
os.makedirs("Frontend/Files", exist_ok=True)

# Replace the language setting in the HTML code with the input language
HtmlCode = str(HtmlCode).replace("recognition.lang = ''", f"recognition.lang = '{InputLanguage}';")

# Write the modified HTML code to a file
with open("Data/Voice.html", "w", encoding="utf-8") as f:
    f.write(HtmlCode)

# Get the current working directory
current_dir = os.getcwd()

# Generate the file path for the HTML file
Link = f"file:///{current_dir}/Data/Voice.html"

# Set Chrome options for the WebDriver
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
# Remove headless mode for testing; add back "--headless=new" if desired
# chrome_options.add_argument("--headless=new")

# Initialize the Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define the path for temporary files
TempDirPath = f"{current_dir}/Frontend/Files"

# Function to set the assistant's status
def SetAssistantStatus(Status):
    try:
        with open(f"{TempDirPath}/Status.data", "w", encoding="utf-8") as file:
            file.write(Status)
    except Exception as e:
        print(f"Error setting status: {e}")

# Function to modify a query
def QueryModifier(Query):
    if not Query:
        return ""
    new_query = Query.lower().strip()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's"]
    query_words = new_query.split()
    
    if any(word in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    
    return new_query.capitalize()

# Function to translate text into English
def UniversalTranslator(Text):
    try:
        english_translation = mt.translate(Text, "en", "auto")
        return english_translation.capitalize()
    except Exception as e:
        print(f"Translation error: {e}")
        return Text

# Function to perform speech recognition
def SpeechRecognition():
    try:
        driver.get(Link)
        
        # Wait for page to load
        time.sleep(1)
        
        # Start speech recognition
        driver.find_element(by=By.ID, value="start").click()
        
        # Wait for some speech input
        timeout = time.time() + 5  # 5 seconds timeout
        while True:
            try:
                text = driver.find_element(by=By.ID, value="output").text
                if text and text.strip():
                    driver.find_element(by=By.ID, value="end").click()
                    
                    if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                        return QueryModifier(text)
                    else:
                        SetAssistantStatus("Translating...")
                        return QueryModifier(UniversalTranslator(text))
                    
                if time.time() > timeout:
                    driver.find_element(by=By.ID, value="end").click()
                    return "No speech detected."
                    
                time.sleep(0.1)
            except Exception as e:
                time.sleep(0.1)
                continue
                
    except Exception as e:
        print(f"Speech recognition error: {e}")
        return ""

# Main execution block
if __name__ == "__main__":
    try:
        while True:
            text = SpeechRecognition()
            if text:
                print(f"Recognized: {text}")
            time.sleep(1)  # Small delay between recognitions
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        driver.quit()


        





