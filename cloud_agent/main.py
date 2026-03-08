# cloud_agent/main.py
# This is the entry point for the Cloud AI Agent, focusing on email triage and drafting.

import os
import time
from datetime import datetime
import uuid
import shutil

# Define vault directories
INBOX_DIR = "Inbox"
INBOX_PROCESSED_DIR = os.path.join(INBOX_DIR, "Processed")
PENDING_APPROVAL_DIR = "Pending_Approval"
PENDING_APPROVAL_EMAIL_DIR = os.path.join(PENDING_APPROVAL_DIR, "email")
NEEDS_ACTION_DIR = "Needs_Action"
NEEDS_ACTION_EMAIL_DIR = os.path.join(NEEDS_ACTION_DIR, "email")

# --- Helper Functions ---
def _ensure_dir_exists(path):
    """Ensures that a directory exists, creating it if necessary."""
    os.makedirs(path, exist_ok=True)

def _read_email_task(file_path):
    """Reads a simulated email task from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # A very basic parser for demonstration.
        # In a real scenario, this would be more robust.
        subject_line = ""
        body = ""
        lines = content.split('\n')
        if lines:
            if lines[0].startswith("Subject:"):
                subject_line = lines[0][len("Subject:"):].strip()
            body = "\n".join(lines[1:]).strip()
        return {"subject": subject_line, "body": body, "full_content": content}
    except Exception as e:
        print(f"Error reading email task {file_path}: {e}")
        return None

def _draft_reply(email_content):
    """Simulates drafting a reply based on email content."""
    # This is a placeholder for actual AI drafting logic.
    subject = email_content.get("subject", "No Subject")
    body = email_content.get("body", "")
    
    draft_subject = f"Draft Reply: {subject}"
    draft_body = (
        f"Hi,\n\n"
        f"Thank you for your email regarding '{subject}'.\n\n"
        f"We are looking into this and will get back to you shortly.\n\n"
        f"Best regards,\nCloud Agent (Draft)\n\n"
        f"--- Original Email ---\n{email_content.get('full_content', '')}"
    )
    return {"subject": draft_subject, "body": draft_body}

def _create_pending_approval_file(domain, task_id, draft_data, original_task_file_name):
    """Creates a file in the Pending_Approval directory."""
    _ensure_dir_exists(os.path.join(PENDING_APPROVAL_DIR, domain))
    file_name = f"{task_id}.txt"
    file_path = os.path.join(PENDING_APPROVAL_DIR, domain, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"Approval Type: {domain.upper()} Draft\n")
        f.write(f"Original File: {original_task_file_name}\n")
        f.write(f"Subject: {draft_data['subject']}\n\n")
        f.write(f"{draft_data['body']}\n")
    print(f"Cloud Agent: Created pending approval file: {file_path}")
    return file_path

def cloud_agent_main():
    print("🚀 Cloud AI Agent Started...")

    _ensure_dir_exists(INBOX_DIR)
    _ensure_dir_exists(INBOX_PROCESSED_DIR)
    _ensure_dir_exists(PENDING_APPROVAL_EMAIL_DIR)
    _ensure_dir_exists(NEEDS_ACTION_EMAIL_DIR)

    while True:
        print(f"[{datetime.now()}] Cloud Agent: Watching for new tasks in {INBOX_DIR}...")
        
        new_emails = [f for f in os.listdir(INBOX_DIR) if f.endswith('.txt') and os.path.isfile(os.path.join(INBOX_DIR, f))]
        
        if new_emails:
            print(f"Cloud Agent: Found {len(new_emails)} new email(s).")
            for email_file in new_emails:
                email_path = os.path.join(INBOX_DIR, email_file)
                task_id = str(uuid.uuid4())
                
                print(f"Cloud Agent: Processing email: {email_file}")
                email_content = _read_email_task(email_path)
                
                if email_content:
                    # Simulate drafting a reply
                    draft = _draft_reply(email_content)
                    
                    # Create pending approval file
                    _create_pending_approval_file("email", task_id, draft, email_file)
                    
                    # Move processed email to INBOX_PROCESSED_DIR
                    shutil.move(email_path, os.path.join(INBOX_PROCESSED_DIR, email_file))
                    print(f"Cloud Agent: Moved {email_file} to {INBOX_PROCESSED_DIR}")
                else:
                    print(f"Cloud Agent: Failed to process email {email_file}. Skipping.")
        else:
            print(f"[{datetime.now()}] Cloud Agent: No new emails found.")

        time.sleep(10) # Wait before checking again

if __name__ == "__main__":
    cloud_agent_main()
