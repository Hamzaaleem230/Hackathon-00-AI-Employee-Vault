import os
import json
import shutil
import time
from datetime import datetime
from brain import analyze_document
import psycopg2
from dotenv import load_dotenv
# Naya Integration Import
from mcp_servers.odoo_mcp import OdooMCP

load_dotenv()

# Folders configuration
PENDING, APPROVED, REJECTED = "Pending_Approval", "Approved", "Rejected"
TASK_PENDING, TASK_PROCESSING, TASK_COMPLETED, TASK_FAILED = "Tasks/Pending", "Tasks/Processing", "Tasks/Completed", "Tasks/Failed"
LOG_DIR = "Logs"
DATABASE_URL = os.getenv("NEON_DB_URL")

# Odoo Initialize
odoo_engine = OdooMCP()

for folder in [PENDING, APPROVED, REJECTED, TASK_PENDING, TASK_PROCESSING, TASK_COMPLETED, TASK_FAILED, LOG_DIR]:
    os.makedirs(folder, exist_ok=True)

def update_neon_db(file_name, result, odoo_inv_id=None):
    """Naya Table 'odoo_audit_logs' use karne ke liye updated function"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        decision = result.get('decision', 'Rejected')
        reasoning = result.get('reasoning', 'No reasoning provided')
        # Amount extract karne ki koshish (Simple logic)
        amount = 0.0
        if "$" in reasoning:
            try: amount = float(reasoning.split("$")[1].split()[0])
            except: amount = 0.0

        filename = os.path.basename(file_name)

        # Updated Query for Gold Tier Table
        cur.execute('''
            INSERT INTO public.odoo_audit_logs (task_id, action_type, odoo_invoice_id, amount)
            VALUES (%s, %s, %s, %s)
        ''', (filename, f"Decision: {decision}", str(odoo_inv_id) if odoo_inv_id else "N/A", amount))
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"[Neon DB] Audit Log Synced for {filename}")
    except Exception as e:
        print(f"[Neon DB Error] {e}")

def task_log(msg):
    with open("Logs/task_engine.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {msg}\n")

def safe_analyze(content):
    for attempt in range(3):
        try:
            return analyze_document(content)
        except Exception as e:
            print(f"[Retry {attempt+1}] Gemini API Busy, waiting...")
            time.sleep(2)
    return {"decision": "Rejected", "confidence": 0, "reasoning": "API Timeout after 3 retries"}

def process_file_logic(f, file_path):
    """File processing with Odoo Sync"""
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            res = safe_analyze(content)
        
        odoo_id = None
        # Agar AI kehta hai Approve hai aur content invoice jaisa hai
        if res['decision'] == "Approved":
            print(f"[Odoo] Syncing {f} to ERP...")
            # Default values agar AI details na de sakay
            odoo_id = odoo_engine.create_invoice("Automated AI Customer", 500.0)
            if odoo_id:
                print(f"✅ Odoo Invoice Created: {odoo_id}")

        # Neon DB Update
        update_neon_db(f, res, odoo_id)
        
        # File Movement
        dest = APPROVED if res['decision'] == "Approved" else REJECTED
        shutil.move(file_path, os.path.join(dest, f))
        print(f"[Vault] {f} moved to {dest}")
        
    except Exception as e:
        print(f"[Process Error] {e}")

if __name__ == "__main__":
    print("🚀 AI Employee Watcher: Active & Odoo-Linked")

    while True:
        try:
            # 1. Main Pending Folder Watcher
            files = os.listdir(PENDING)
            # Sort files (urgent first)
            files.sort(key=lambda x: 'urgent' not in x.lower())

            for f in files:
                file_path = os.path.join(PENDING, f)
                # Ensure it's a file and not a sub-folder
                if os.path.isfile(file_path) and not f.startswith('.'):
                    process_file_logic(f, file_path)

            # 2. Tasks Folder Watcher (JSON tasks)
            if os.path.exists(TASK_PENDING):
                task_files = os.listdir(TASK_PENDING)
                for tf in task_files:
                    # Yahan aap apna purana process_task function call kar sakte hain
                    pass

        except Exception as e:
            print("Watcher loop crash:", e)
        
        time.sleep(5)