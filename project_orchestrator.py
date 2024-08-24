import os
import subprocess
import logging
from dotenv import load_dotenv
from main import edit_github_file, get_claude_suggestions, run_app

load_dotenv()

def clone_or_pull_repo():
    repo_name = os.getenv('GITHUB_REPO')
    if not os.path.exists(repo_name.split('/')[-1]):
        subprocess.run(['git', 'clone', f'https://github.com/{repo_name}.git'])
    else:
        subprocess.run(['git', 'pull'], cwd=repo_name.split('/')[-1])

def push_changes():
    repo_name = os.getenv('GITHUB_REPO')
    subprocess.run(['git', 'add', '.'], cwd=repo_name.split('/')[-1])
    subprocess.run(['git', 'commit', '-m', "Applied Claude's suggestions"], cwd=repo_name.split('/')[-1])
    subprocess.run(['git', 'push'], cwd=repo_name.split('/')[-1])

def main():
    # Clone or pull the latest changes
    clone_or_pull_repo()

    # Get the content of main.py
    repo_name = os.getenv('GITHUB_REPO')
    with open(f"{repo_name.split('/')[-1]}/main.py", 'r') as file:
        content = file.read()

    # Get suggestions from Claude
    suggestions = get_claude_suggestions(content)

    # Apply suggestions (in a real scenario, you'd want to review these)
    new_content = content + "\n# Claude's suggestions:\n" + suggestions

    # Update the file on GitHub
    edit_github_file('main.py', new_content)

    # Pull the changes
    clone_or_pull_repo()

    # Run the app and capture logs, errors, screenshots, and video
    run_app()

    # Push any changes (like new log files or screenshots)
    push_changes()

    logging.info("Orchestration complete")

if __name__ == "__main__":
    main()