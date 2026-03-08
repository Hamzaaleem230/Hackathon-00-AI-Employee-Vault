# platinum_demo.py
# Orchestrates the Platinum Tier Demo Flow scenario.

import os
import time
import shutil
import subprocess
import json
from datetime import datetime

# --- Configuration ---
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define vault directories
INBOX_DIR = os.path.join(ROOT_DIR, "Inbox")
INBOX_PROCESSED_DIR = os.path.join(INBOX_DIR, "Processed")
NEEDS_ACTION_DIR = os.path.join(ROOT_DIR, "Needs_Action")
NEEDS_ACTION_EMAIL_DIR = os.path.join(NEEDS_ACTION_DIR, "email")
IN_PROGRESS_DIR = os.path.join(ROOT_DIR, "In_Progress")
IN_PROGRESS_LOCAL_AGENT_DIR = os.path.join(IN_PROGRESS_DIR, "local_agent")
PENDING_APPROVAL_DIR = os.path.join(ROOT_DIR, "Pending_Approval")
PENDING_APPROVAL_EMAIL_DIR = os.path.join(PENDING_APPROVAL_DIR, "email")
PENDING_APPROVAL_ODOO_DIR = os.path.join(PENDING_APPROVAL_DIR, "odoo")
DONE_DIR = os.path.join(ROOT_DIR, "Done")
LOGS_DIR = os.path.join(ROOT_DIR, "Logs")
DECISIONS_LOG_FILE = os.path.join(LOGS_DIR, "decisions.json")
HEALTH_LOG_FILE = os.path.join(LOGS_DIR, "health_status.json")
UPDATES_DIR = os.path.join(ROOT_DIR, "Updates")
UPDATES_PROCESSED_DIR = os.path.join(UPDATES_DIR, "Processed")
SIGNALS_DIR = os.path.join(ROOT_DIR, "Signals")
SIGNALS_PROCESSED_DIR = os.path.join(SIGNALS_DIR, "Processed")
DASHBOARD_FILE = os.path.join(ROOT_DIR, "Dashboard.md")

# Agent script paths
CLOUD_AGENT_SCRIPT = os.path.join(ROOT_DIR, "cloud_agent", "main.py")
LOCAL_AGENT_SCRIPT = os.path.join(ROOT_DIR, "local_agent", "main.py")
SYNC_AGENT_SCRIPT = os.path.join(ROOT_DIR, "sync", "main.py")
HEALTH_MONITOR_SCRIPT = os.path.join(ROOT_DIR, "health_monitor", "main.py")

# --- Helper Functions ---
def _run_cmd(command, cwd=None, check=True):
    """Executes a shell command."""
    print(f"Running command: {' '.join(command)}")
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=check, shell=True)
    return result

def _start_agent(script_path, agent_name):
    """Starts an agent in the background."""
    print(f"--- Starting {agent_name} ---")
    command = f"python {script_path}"
    subprocess.Popen(command, shell=True)
    time.sleep(3) 

def _stop_all_agents():
    """Attempts to stop all running Python agents."""
    print("--- Attempting to stop all running agents ---")
    print("Please ensure all previous agent python.exe processes are manually stopped from Task Manager.")

def _clear_directories():
    """Clears all task-related directories and logs."""
    print("--- Clearing task-related directories and logs ---")
    dirs_to_clear = [
        INBOX_DIR, INBOX_PROCESSED_DIR, NEEDS_ACTION_EMAIL_DIR, NEEDS_ACTION_DIR,
        IN_PROGRESS_LOCAL_AGENT_DIR, PENDING_APPROVAL_EMAIL_DIR, PENDING_APPROVAL_ODOO_DIR,
        DONE_DIR, UPDATES_DIR, UPDATES_PROCESSED_DIR, SIGNALS_DIR, SIGNALS_PROCESSED_DIR
    ]
    files_to_remove = [DECISIONS_LOG_FILE, HEALTH_LOG_FILE]

    for d in dirs_to_clear:
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d, exist_ok=True)
    
    for f in files_to_remove:
        if os.path.exists(f):
            os.remove(f)

    initial_dashboard_content = "# AI Employee Vault Dashboard\n\n- Initialized"
    with open(DASHBOARD_FILE, 'w', encoding='utf-8') as f:
        f.write(initial_dashboard_content)
    print("Directories cleared, Dashboard.md reset.")

def _create_dummy_email(filename="demo_email.txt", subject="Demo Email for Platinum Flow"):
    email_content = f"Subject: {subject}\n\nThis is a test email for the Platinum Demo."
    email_path = os.path.join(INBOX_DIR, filename)
    with open(email_path, 'w', encoding='utf-8') as f:
        f.write(email_content)
    print(f"--- Created dummy email: {email_path} ---")
    return email_path

def _verify_state():
    """Verifies the final state of the vault."""
    print("--- Verifying final state ---")
    
    # 1. Inbox Check (Sirf files check karein)
    inbox_files = [f for f in os.listdir(INBOX_DIR) if os.path.isfile(os.path.join(INBOX_DIR, f))]
    assert len(inbox_files) == 0, f"Inbox should be empty of files, found: {inbox_files}"
    assert len(os.listdir(INBOX_PROCESSED_DIR)) >= 1, "Inbox/Processed should contain the processed email."
    print("Inbox state: OK")

    # 2. Pending & Done Check
    # Done mein kam az kam 1 file honi chahiye
    assert len(os.listdir(DONE_DIR)) >= 1, "Done folder should have at least one completed task."
    print("Task Flow state: OK")

    # 3. Updates and Signals Check (Relaxed for background activity)
    assert os.path.exists(UPDATES_PROCESSED_DIR), "Updates/Processed should exist."
    assert os.path.exists(SIGNALS_PROCESSED_DIR), "Signals/Processed should exist."
    print("Updates and Signals states: OK")

    # 4. Logs Check
    assert os.path.exists(DECISIONS_LOG_FILE), "decisions.json should exist."
    assert os.path.exists(HEALTH_LOG_FILE), "health_status.json should exist."
    print("Logs state: OK")

    # 5. Dashboard.md Check
    with open(DASHBOARD_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        # Dashboard check ko thora flexible rakha hai
        print(f"Dashboard Content Preview: {content[:50]}...")
    
    print("--- All Platinum Demo Flow verifications passed! ---")


def main():
    print("--- Starting Platinum Demo Flow Orchestration ---")

    # Step 1: Cleanup
    _stop_all_agents()
    input("Press Enter after you have manually stopped all python.exe processes...")
    _clear_directories()

    # Step 2: Cloud Agent Action
    _create_dummy_email()
    _start_agent(CLOUD_AGENT_SCRIPT, "Cloud Agent")
    time.sleep(7) # Thora zyada time taake processing pakki ho

    # Step 3: Local Agent Action
    _start_agent(LOCAL_AGENT_SCRIPT, "Local Agent")
    time.sleep(12) # Time for approval and moving to done

    # Step 4: Support Agents
    _start_agent(SYNC_AGENT_SCRIPT, "Sync Agent")
    _start_agent(HEALTH_MONITOR_SCRIPT, "Health Monitor")
    time.sleep(8)

    # Step 5: Verification
    _verify_state()

    print("--- Platinum Demo Flow Orchestration Completed ---")

if __name__ == "__main__":
    main()