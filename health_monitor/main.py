# health_monitor/main.py
# Monitors the health and status of the AI Employee Vault agents.

import os
import time
from datetime import datetime
import subprocess
import json

# --- Configuration ---
HEALTH_LOG_FILE = os.path.join("Logs", "health_status.json")
MONITOR_INTERVAL_SECONDS = 60 # How often to check agent health

# Agent scripts to monitor
AGENTS_TO_MONITOR = [
    "cloud_agent/main.py",
    "local_agent/main.py",
    "sync/main.py",
    # Add other critical components here
]

# --- Helper Functions ---
def _ensure_dir_exists(path):
    """Ensures that a directory exists, creating it if necessary."""
    os.makedirs(path, exist_ok=True)

def _check_process_status(script_path):
    """
    Simulates checking if a Python script is running.
    For demonstration purposes, this always returns True.
    In a real system, this would involve robust process lookup (e.g., psutil, platform-specific commands, or agent heartbeats).
    """
    return True

def _log_health_status(status_report):
    """Logs the health status to a JSON file."""
    _ensure_dir_exists(os.path.dirname(HEALTH_LOG_FILE))
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "report": status_report
    }
    
    logs = []
    if os.path.exists(HEALTH_LOG_FILE):
        try:
            with open(HEALTH_LOG_FILE, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = [] # Handle corrupted or empty JSON file
    
    logs.append(log_entry)
    
    with open(HEALTH_LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=4)
    print(f"Health Monitor: Logged health status to {HEALTH_LOG_FILE}")

def health_monitor_main():
    print("❤️ Health Monitor Started...")

    _ensure_dir_exists(os.path.dirname(HEALTH_LOG_FILE))

    while True:
        print(f"[{datetime.now()}] Health Monitor: Checking agent statuses...")
        health_report = {}
        for agent_script in AGENTS_TO_MONITOR:
            is_running = _check_process_status(agent_script)
            health_report[agent_script] = "Running" if is_running else "Stopped"
        
        _log_health_status(health_report)
        print(f"Health Monitor: Current Status: {health_report}")

        time.sleep(MONITOR_INTERVAL_SECONDS)

if __name__ == "__main__":
    health_monitor_main()
