import os
import json
import shutil
import time
from datetime import datetime
from brain import analyze_document
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Folders same rahenge
PENDING, APPROVED, REJECTED = "Pending_Approval", "Approved", "Rejected"
TASK_PENDING, TASK_PROCESSING, TASK_COMPLETED, TASK_FAILED = "Tasks/Pending", "Tasks/Processing", "Tasks/Completed", "Tasks/Failed"
LOG_DIR = "Logs"
DATABASE_URL = os.getenv("NEON_DB_URL")

for folder in [PENDING, APPROVED, REJECTED, TASK_PENDING, TASK_PROCESSING, TASK_COMPLETED, TASK_FAILED, LOG_DIR]:
    os.makedirs(folder, exist_ok=True)

def update_neon_db(file_name, result):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        decision = result.get('decision', 'Rejected')
        confidence = result.get('confidence', 0.0)
        reasoning = result.get('reasoning', 'No reasoning provided')
        filename = os.path.basename(file_name)

        cur.execute('''
            INSERT INTO decisions (filename, decision, confidence, reasoning)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (filename) DO UPDATE SET
            decision = EXCLUDED.decision, confidence = EXCLUDED.confidence, reasoning = EXCLUDED.reasoning
        ''', (filename, decision, confidence, reasoning))
        conn.commit()
        cur.close()
        conn.close()
        print(f"[DB] Synced {filename}")
    except Exception as e:
        print(f"[DB Error] {e}")

def task_log(msg):
    with open("Logs/task_engine.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {msg}\n")

# AI Analysis with Retry Mechanism (Naya Feature)
def safe_analyze(content):
    for attempt in range(3): # 3 baar koshish karega
        try:
            return analyze_document(content)
        except Exception as e:
            print(f"[Retry {attempt+1}] Gemini API Busy, waiting...")
            time.sleep(2)
    return {"decision": "Rejected", "confidence": 0, "reasoning": "API Timeout after 3 retries"}

def process_task(file_path):
    try:
        filename = os.path.basename(file_path)
        print(f"[Task] Processing {filename}")
        with open(file_path, "r", encoding="utf-8") as f:
            task = json.load(f)

        processing_path = os.path.join(TASK_PROCESSING, filename)
        shutil.move(file_path, processing_path)

        result = safe_analyze(task["content"]) # Safe call use kiya
        decision = result.get("decision", "Rejected")
        task["status"] = decision.lower()
        task["decision"] = result

        update_neon_db(filename, result)
        target = TASK_COMPLETED if decision == "Approved" else TASK_FAILED
        final_path = os.path.join(target, filename)

        with open(final_path, "w", encoding="utf-8") as f:
            json.dump(task, f, indent=2)

        os.remove(processing_path)
        task_log(f"{task.get('task_id', 'Unknown')} -> {decision}")
        print(f"[Task] Done {filename} → {decision}")
    except Exception as e:
        task_log(f"ERROR {file_path}: {e}")
        print(f"[Task ERROR] {e}")

if __name__ == "__main__":
    print("Watcher running: Priority Mode Active")

    while True:
        try:
            # Priority Sorting: Pehle wo files uthayega jinme 'urgent' likha ho
            files = os.listdir(PENDING)
            files.sort(key=lambda x: 'urgent' not in x.lower()) # Urgent files first

            for f in files:
                file_path = os.path.join(PENDING, f)
                if os.path.isfile(file_path) and not f.startswith('.'):
                    with open(file_path, 'r', encoding="utf-8") as file:
                        res = safe_analyze(file.read())
                    update_neon_db(f, res)
                    dest = APPROVED if res['decision'] == "Approved" else REJECTED
                    shutil.move(file_path, os.path.join(dest, f))
                    print(f"[Legacy] Processed {f} -> {res['decision']}")

            # Task Processing
            task_files = os.listdir(TASK_PENDING)
            for f in task_files:
                process_task(os.path.join(TASK_PENDING, f))

        except Exception as e:
            print("Watcher crash:", e)
        time.sleep(5)