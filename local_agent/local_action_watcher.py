import os
import time
from datetime import datetime
from utils.audit_logger import AuditLogger # Use the central AuditLogger
from utils.error_handler import robust_watcher_process # For error handling

APPROVED_FOLDER = "Approved"
DONE_FOLDER = "Done"

class LocalActionWatcher:
    def __init__(self):
        AuditLogger.log(
            event_type="WATCHER_START",
            agent="LocalActionWatcher",
            description="Local Action Watcher initialized, watching Approved folder."
        )
        print("🏠 Local Action Watcher: Watching Approved folder...")

    @robust_watcher_process(fallback_action_description="Skipping processing for a file in Approved folder due to error.")
    def process_approved_file(self, file_name):
        source_path = os.path.join(APPROVED_FOLDER, file_name)
        
        # Simulate final action here (e.g., logging, actual execution)
        AuditLogger.log_action(
            agent="LocalActionWatcher",
            action="EXECUTING FINAL ACTION",
            file_name=file_name
        )
        print(f"🏠 Local Action Watcher: Executing final action for {file_name}")

        # Move to Done folder after action
        os.rename(source_path, os.path.join(DONE_FOLDER, file_name))
        AuditLogger.log_action(
            agent="LocalActionWatcher",
            action="MOVED TO DONE",
            file_name=file_name
        )
        print(f"🏠 Local Action Watcher: Moved {file_name} to Done folder.")

    def watch(self):
        while True:
            try:
                # Platinum Tier: Claim-by-move logic will be added here if this was an In_Progress folder
                # For Approved -> Done, it's a direct move after action.

                files = os.listdir(APPROVED_FOLDER)
                for file_name in files:
                    if file_name.startswith('.'): # Ignore hidden files
                        continue
                    self.process_approved_file(file_name)

                time.sleep(5)
            except Exception as e:
                AuditLogger.log(
                    event_type="WATCHER_ERROR",
                    agent="LocalActionWatcher",
                    description=f"Error in LocalActionWatcher loop: {e}",
                    details={"error_message": str(e)}
                )
                time.sleep(5)

if __name__ == "__main__":
    watcher = LocalActionWatcher()
    watcher.watch()
