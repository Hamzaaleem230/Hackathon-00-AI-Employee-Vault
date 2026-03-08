import os
import time
from datetime import datetime
# from watcher.email_service import EmailService # Removed for local agent's specific role
# from config import NOTIFY_EMAIL # Removed for local agent's specific role
from local_agent.local_brain import LocalBrain # Will import the local brain
from utils.audit_logger import AuditLogger
from utils.error_handler import robust_watcher_process

PENDING_APPROVAL_FOLDER = "Pending_Approval" # This will eventually be Pending_Approval/<domain>
APPROVED_FOLDER = "Approved"
REJECTED_FOLDER = "Rejected"
DONE_FOLDER = "Done"
AWAITING_HUMAN_REVIEW_FOLDER = "Awaiting_Human_Review" # This is where Cloud Agent might place sensitive files for Local Agent review
IN_PROGRESS_FOLDER = "In_Progress" # For claim-by-move
# LOG_FILE is now handled by AuditLogger

class LocalApprovalWatcher:
    def __init__(self):
        self.local_brain = LocalBrain() # Initialize LocalBrain
        AuditLogger.log(
            event_type="WATCHER_START",
            agent="LocalApprovalWatcher",
            description="Local Approval Watcher initialized, monitoring Pending_Approval folder."
        )
        print("🏠 Local Approval Watcher: Monitoring Pending_Approval for tasks...")

    def move_file(self, source, destination_folder):
        file_name = os.path.basename(source)
        dest_path = os.path.join(destination_folder, file_name)
        os.rename(source, dest_path)
        return dest_path

    @robust_watcher_process(fallback_action_description="File processing skipped due to error in LocalApprovalWatcher.")
    def process_pending_file(self, file_path): # Changed to take full file_path
        file_name = os.path.basename(file_path)
        
        # Platinum Tier: Claim-by-move logic - move to In_Progress/local_agent/
        local_agent_in_progress_folder = os.path.join(IN_PROGRESS_FOLDER, "local_agent")
        os.makedirs(local_agent_in_progress_folder, exist_ok=True)
        in_progress_path = self.move_file(file_path, local_agent_in_progress_folder)
        
        AuditLogger.log_action(
            agent="LocalApprovalWatcher",
            action="CLAIMED_TASK",
            file_name=file_name,
            details={"moved_to": in_progress_path}
        )
        print(f"🏠 Local Approval Watcher: Claimed {file_name}. Moving to In_Progress/local_agent.")

        # Evaluate the file (which might trigger further local actions)
        decision = self.local_brain.evaluate(in_progress_path)

        # Move out of In_Progress based on decision
        if decision == "approved":
            final_dest_path = self.move_file(in_progress_path, APPROVED_FOLDER) # Or straight to Done/ after final send
            AuditLogger.log_action(
                agent="LocalApprovalWatcher",
                action="AI APPROVED (LOCAL)",
                file_name=file_name,
                decision="approved",
                details={"moved_to": final_dest_path}
            )
            # Placeholder for final send/post action by Local Agent
            print(f"🏠 Local Approval Watcher: {file_name} approved and moved to Approved folder. Final send/post should occur.")

        elif decision == "rejected":
            final_dest_path = self.move_file(in_progress_path, REJECTED_FOLDER)
            AuditLogger.log_action(
                agent="LocalApprovalWatcher",
                action="AI REJECTED (LOCAL)",
                file_name=file_name,
                decision="rejected",
                details={"moved_to": final_dest_path}
            )
            print(f"🏠 Local Approval Watcher: {file_name} rejected and moved to Rejected folder.")

        elif decision == "human_review":
            final_dest_path = self.move_file(in_progress_path, AWAITING_HUMAN_REVIEW_FOLDER)
            AuditLogger.log_action(
                agent="LocalApprovalWatcher",
                action="FLAGGED FOR HUMAN REVIEW (LOCAL)",
                file_name=file_name,
                decision="human_review",
                details={"moved_to": final_dest_path}
            )
            print(f"🏠 Local Approval Watcher: {file_name} flagged for human review and moved to Awaiting_Human_Review.")
        else:
            # Fallback for unexpected decisions - move to rejected
            final_dest_path = self.move_file(in_progress_path, REJECTED_FOLDER)
            AuditLogger.log_action(
                agent="LocalApprovalWatcher",
                action="UNKNOWN DECISION - FALLBACK TO REJECTED (LOCAL)",
                file_name=file_name,
                decision=decision,
                details={"moved_to": final_dest_path}
            )
            print(f"🏠 Local Approval Watcher: {file_name} received unknown decision '{decision}'. Moved to Rejected folder.")

    def watch(self):
        while True:
            try:
                # Platinum Tier: Monitor Pending_Approval/<domain>/ (will implement domain later)
                # For now, monitor top-level Pending_Approval
                files = os.listdir(PENDING_APPROVAL_FOLDER)

                for file_name in files:
                    if file_name.startswith('.'): # Ignore hidden files
                        continue
                    file_path = os.path.join(PENDING_APPROVAL_FOLDER, file_name)
                    self.process_pending_file(file_path)

                time.sleep(5)

            except Exception as e:
                AuditLogger.log(
                    event_type="WATCHER_ERROR",
                    agent="LocalApprovalWatcher",
                    description=f"An error occurred in watch loop: {e}",
                    details={"error_message": str(e)}
                )
                print(f"🏠 Local Approval Watcher Error: {e}")
                time.sleep(5)

if __name__ == "__main__":
    watcher = LocalApprovalWatcher()
    watcher.watch()