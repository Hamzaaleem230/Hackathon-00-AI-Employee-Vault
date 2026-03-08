# sync/main.py
# Handles Git-based synchronization for the AI Employee Vault.

import os
import subprocess
import time
from datetime import datetime

# --- Configuration ---
VAULT_PATH = os.getcwd() # The root of the AI Employee Vault
REMOTE_REPO_URL = "https://github.com/Hamzaaleem230/Hackathon-00-AI-Employee-Vault.git" # TODO: Configure your remote Git repository URL here
SYNC_INTERVAL_SECONDS = 30 # How often to attempt synchronization

# --- Helper Functions ---
def _run_git_command(command, cwd=None):
    """Executes a git command and returns its output."""
    if cwd is None:
        cwd = VAULT_PATH
    
    full_command = ["git"] + command
    try:
        result = subprocess.run(
            full_command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing git command: {' '.join(full_command)}")
        print(f"Stderr: {e.stderr.strip()}")
        return None
    except FileNotFoundError:
        print("Error: Git command not found. Please ensure Git is installed and in your PATH.")
        return None

def _initialize_git_repo(repo_path):
    """Initializes the vault as a Git repository and sets up the remote."""
    if not os.path.exists(os.path.join(repo_path, '.git')):
        print(f"Initializing Git repository in {repo_path}...")
        _run_git_command(["init"], cwd=repo_path)
        _run_git_command(["branch", "-M", "main"], cwd=repo_path)
        if REMOTE_REPO_URL != "YOUR_REMOTE_GIT_REPO_URL":
            _run_git_command(["remote", "add", "origin", REMOTE_REPO_URL], cwd=repo_path)
            print(f"Added remote origin: {REMOTE_REPO_URL}")
        else:
            print("WARNING: Remote Git repository URL not configured. Please update REMOTE_REPO_URL in sync/main.py")
        # Add a default .gitignore if not present
        if not os.path.exists(os.path.join(repo_path, '.gitignore')):
            with open(os.path.join(repo_path, '.gitignore'), 'w') as f:
                f.write("""__pycache__/
*.pyc
.env
Logs/ # Exclude Logs directory from sync
*.session # Example for WhatsApp sessions
# TODO: Add more specific exclusions based on security rules
""")
    else:
        print(f"Git repository already initialized in {repo_path}.")
        # Ensure remote is set if it's a fresh run and REMOTE_REPO_URL is updated
        remotes = _run_git_command(["remote", "-v"], cwd=repo_path)
        if REMOTE_REPO_URL != "YOUR_REMOTE_GIT_REPO_URL" and REMOTE_REPO_URL not in (remotes or ""):
             print(f"Adding/updating remote origin to: {REMOTE_REPO_URL}")
             _run_git_command(["remote", "set-url", "origin", REMOTE_REPO_URL], cwd=repo_path)
             # If set-url fails (e.g. no origin exists), try add
             if _run_git_command(["remote", "set-url", "origin", REMOTE_REPO_URL], cwd=repo_path) is None:
                 _run_git_command(["remote", "add", "origin", REMOTE_REPO_URL], cwd=repo_path)

def _perform_sync(repo_path):
    """Performs a Git add, commit, pull --rebase, and push operation."""
    print(f"[{datetime.now()}] Sync Agent: Performing synchronization...")
    
    # Add all changes
    _run_git_command(["add", "."], cwd=repo_path)
    
    # Check for changes to commit
    status_output = _run_git_command(["status", "--porcelain"], cwd=repo_path)
    if status_output:
        commit_message = f"Vault sync: Automated commit at {datetime.now().isoformat()}"
        print(f"Sync Agent: Committing changes with message: '{commit_message}'")
        _run_git_command(["commit", "-m", commit_message], cwd=repo_path)
        
        # Pull with rebase to integrate remote changes
        print("Sync Agent: Pulling latest changes (rebase)...")
        _run_git_command(["pull", "--rebase", "origin", "main"], cwd=repo_path) # Assumes 'main' branch
        
        # Push local changes
        print("Sync Agent: Pushing changes...")
        _run_git_command(["push", "origin", "main"], cwd=repo_path) # Assumes 'main' branch
    else:
        print("Sync Agent: No changes to commit.")
        # Still attempt pull/push to ensure local is up-to-date and remote gets any changes
        print("Sync Agent: Pulling latest changes (rebase)...")
        _run_git_command(["pull", "--rebase", "origin", "main"], cwd=repo_path)
        print("Sync Agent: Pushing changes...")
        _run_git_command(["push", "origin", "main"], cwd=repo_path)


def sync_main():
    print("🔄 Sync Agent Started...")

    _initialize_git_repo(VAULT_PATH)

    while True:
        try:
            _perform_sync(VAULT_PATH)
        except Exception as e:
            print(f"Sync Agent: An error occurred during synchronization: {e}")
        time.sleep(SYNC_INTERVAL_SECONDS)

if __name__ == "__main__":
    sync_main()
