import os
import logging
import traceback
import requests
import psutil
from dotenv import load_dotenv
import time
from mss import mss

load_dotenv()

# Setup logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def capture_screenshot():
    with mss() as sct:
        filename = f"screenshots/screenshot_{int(time.time())}.png"
        os.makedirs('screenshots', exist_ok=True)
        sct.shot(output=filename)
        logging.info(f"Screenshot saved: {filename}")

def run_app():
    logging.info("Application started")
    try:
        # Your app code here
        for i in range(10):  # Simulate some work
            time.sleep(1)
            if i % 3 == 0:  # Capture screenshot every 3 seconds
                capture_screenshot()
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        logging.error(traceback.format_exc())
        capture_screenshot()
    finally:
        capture_screenshot()  # Final screenshot

def edit_github_file(file_path, new_content):
    github_token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('GITHUB_REPO')
    url = f"https://api.github.com/repos/{repo_name}/contents/{file_path}"

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Get the current file content and SHA
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    current_file = response.json()

    # Update the file
    import base64
    data = {
        "message": "Update via Claude API",
        "content": base64.b64encode(new_content.encode()).decode(),
        "sha": current_file["sha"]
    }

    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()
    logging.info(f"File {file_path} updated on GitHub")

def get_claude_suggestions(file_content):
    claude_api_key = os.getenv('CLAUDE_API_KEY')
    claude_api_url = os.getenv('CLAUDE_API_URL')

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {claude_api_key}"
    }

    data = {
        "prompt": f"Please review and suggest improvements for the following code:\n\n{file_content}\n\nSuggestions:",
        "max_tokens_to_sample": 300,
        "temperature": 0.7
    }

    response = requests.post(claude_api_url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()['completion']

if __name__ == "__main__":
    run_app()