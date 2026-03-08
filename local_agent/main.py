# local_agent/main.py
# This is the entry point for the Local AI Agent, focusing on approvals and final actions.

import os
import time
from datetime import datetime
import shutil
import json

# Define vault directories
PENDING_APPROVAL_DIR = "Pending_Approval"
PENDING_APPROVAL_EMAIL_DIR = os.path.join(PENDING_APPROVAL_DIR, "email")
DONE_DIR = "Done"
LOGS_DIR = "Logs"
DECISIONS_LOG_FILE = os.path.join(LOGS_DIR, "decisions.json")

# --- Helper Functions ---
def _ensure_dir_exists(path):
    """Ensures that a directory exists, creating it if necessary."""
    os.makedirs(path, exist_ok=True)

def _read_approval_request(file_path):
    """Reads an approval request from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        task_data = {"full_content": content}
        for line in content.split('\n'):
            if line.startswith("Approval Type:"):
                task_data["approval_type"] = line.split(":", 1)[1].strip()
            elif line.startswith("Original File:"):
                task_data["original_file"] = line.split(":", 1)[1].strip()
            elif line.startswith("Subject:"):
                task_data["subject"] = line.split(":", 1)[1].strip()
        return task_data
    except Exception as e:
        print(f"Error reading approval request {file_path}: {e}")
        return None

def _simulate_user_approval(task_data):
    """Simulates a user approving the task."""
    # In a real scenario, this would involve a UI or explicit user input.
    # For the demo, we'll auto-approve.
    print(f"Local Agent: Simulating user approval for task: {task_data.get('subject', 'N/A')}")
    return True # Always approve for simulation

def _execute_send_action(task_data):
    """Simulates executing the final send/post action."""
    print(f"Local Agent: Executing send action for '{task_data.get('subject', 'N/A')}' (Original file: {task_data.get('original_file', 'N/A')})")
    # This is where integration with external systems (e.g., email API, social media API) would go.
    # For now, it's a print statement.
    return True

def _log_action(action_details):
    """Logs the action to a JSON file."""
    _ensure_dir_exists(LOGS_DIR)
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": "local_agent",
        "details": action_details
    }
    
    logs = []
    if os.path.exists(DECISIONS_LOG_FILE):
        try:
            with open(DECISIONS_LOG_FILE, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = [] # Handle corrupted or empty JSON file
    
    logs.append(log_entry)
    
    with open(DECISIONS_LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=4)
    print(f"Local Agent: Logged action to {DECISIONS_LOG_FILE}")

def local_agent_main():
    print("🏠 Local AI Agent Started...")

    _ensure_dir_exists(PENDING_APPROVAL_EMAIL_DIR)
    _ensure_dir_exists(DONE_DIR)
    _ensure_dir_exists(LOGS_DIR)

    while True:
        print(f"[{datetime.now()}] Local Agent: Watching for pending approvals in {PENDING_APPROVAL_EMAIL_DIR}...")
        
        pending_approvals = [f for f in os.listdir(PENDING_APPROVAL_EMAIL_DIR) if f.endswith('.txt') and os.path.isfile(os.path.join(PENDING_APPROVAL_EMAIL_DIR, f))]
        
        if pending_approvals:
            print(f"Local Agent: Found {len(pending_approvals)} pending approval(s).")
            for approval_file in pending_approvals:
                approval_path = os.path.join(PENDING_APPROVAL_EMAIL_DIR, approval_file)
                
                print(f"Local Agent: Processing approval request: {approval_file}")
                task_data = _read_approval_request(approval_path)
                
                if task_data:
                    if _simulate_user_approval(task_data):
                        if _execute_send_action(task_data):
                            _log_action({
                                "task_id": os.path.splitext(approval_file)[0],
                                "action": "email_sent",
                                "subject": task_data.get("subject", "N/A"),
                                "original_file": task_data.get("original_file", "N/A")
                            })
                            # Move processed approval request to DONE_DIR
                            shutil.move(approval_path, os.path.join(DONE_DIR, approval_file))
                            print(f"Local Agent: Moved {approval_file} to {DONE_DIR}")
                        else:
                            print(f"Local Agent: Failed to execute send action for {approval_file}.")
                    else:
                        print(f"Local Agent: User denied approval for {approval_file}.")
                else:
                    print(f"Local Agent: Failed to read approval request {approval_file}. Skipping.")
        else:
            print(f"[{datetime.now()}] Local Agent: No pending approvals found.")

        time.sleep(10) # Wait before checking again

if __name__ == "__main__":
    local_agent_main()
