import os
import time
from datetime import datetime
from watcher.email_service import EmailService
from watcher.ai_brain import AIBrain
from watcher.config import NOTIFY_EMAIL

PENDING_FOLDER = "Pending_Approval"
APPROVED_FOLDER = "Approved"
REJECTED_FOLDER = "Rejected"
DONE_FOLDER = "Done"
LOG_FILE = "Logs/log.txt"

print("🚀 AI Employee Watcher Started...")


def log_action(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - {message}\n")


def move_file(source, destination_folder):
    file_name = os.path.basename(source)
    dest_path = os.path.join(destination_folder, file_name)
    os.rename(source, dest_path)
    return dest_path


def process_pending_file(file_name):
    source_path = os.path.join(PENDING_FOLDER, file_name)

    decision = AIBrain.evaluate(source_path)

    if decision == "approved":
        new_path = move_file(source_path, APPROVED_FOLDER)

        log_action(f"AI APPROVED: {file_name}")

        EmailService.send_email(
            to_email=NOTIFY_EMAIL,
            subject=f"AI Approved: {file_name}",
            body=f"File {file_name} has been approved by AI."
        )

        # Execute action after approval
        final_path = move_file(new_path, DONE_FOLDER)
        log_action(f"Executed action for {file_name}")

    else:
        move_file(source_path, REJECTED_FOLDER)

        log_action(f"AI REJECTED: {file_name}")

        EmailService.send_email(
            to_email=NOTIFY_EMAIL,
            subject=f"AI Rejected: {file_name}",
            body=f"File {file_name} has been rejected by AI."
        )


def watch_pending():
    while True:
        try:
            files = os.listdir(PENDING_FOLDER)

            for file in files:
                process_pending_file(file)

            time.sleep(5)

        except Exception as e:
            print("Watcher Error:", e)
            time.sleep(5)


if __name__ == "__main__":
    watch_pending()
