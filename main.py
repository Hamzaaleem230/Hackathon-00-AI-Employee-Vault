import os
import json
import shutil
import time
from datetime import datetime
from brain import analyze_document

PENDING = "Pending_Approval"
APPROVED = "Approved"
REJECTED = "Rejected"
LOG_DIR = "Logs"

os.makedirs(PENDING, exist_ok=True)
os.makedirs(APPROVED, exist_ok=True)
os.makedirs(REJECTED, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# --- Helper Functions ---

def move_file(file_path, destination_folder):
    filename = os.path.basename(file_path)
    dest = os.path.join(destination_folder, filename)
    shutil.move(file_path, dest)

def log_decision(file_name, result):
    log_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "file": os.path.basename(file_name),
        "decision": result.get('decision', 'N/A'),
        "confidence": result.get('confidence', 0),
        "reasoning": result.get('reasoning', 'No reasoning provided')
    }

    with open("Logs/decisions.json", "a") as f:
        f.write(json.dumps(log_data) + "\n")

def log_action(file_path, decision, reasoning):
    with open("Logs/log.txt", "a") as f:
        timestamp = datetime.now()
        f.write(f"{timestamp} - AI {decision.upper()}: {os.path.basename(file_path)} - {reasoning}\n")

# --- Core Processor ---

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            content = f.read()

        result = analyze_document(content)

        decision = result.get('decision', 'Rejected')
        reasoning = result.get('reasoning', 'No reasoning')

        print(f"\n[+] Processing: {os.path.basename(file_path)}")
        print(f"Decision: {decision} | Confidence: {result.get('confidence')}")
        print(f"Reason: {reasoning}")

        log_decision(file_path, result)
        log_action(file_path, decision, reasoning)

        if decision == "Approved":
            move_file(file_path, APPROVED)
            print("Moved to Approved.")
        else:
            move_file(file_path, REJECTED)
            print("Moved to Rejected.")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# --- Watcher Loop ---

print("Watching Pending_Approval folder...")

while True:
    try:
        files = os.listdir(PENDING)

        for f in files:
            file_path = os.path.join(PENDING, f)

            if os.path.isfile(file_path):
                process_file(file_path)

        time.sleep(5)

    except Exception as e:
        print("Watcher error:", e)
        time.sleep(5)
