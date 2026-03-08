import os
from datetime import datetime
import json

AUDIT_LOG_FILE = "Logs/audit.log"

class AuditLogger:
    @staticmethod
    def log(event_type: str, agent: str, description: str, details: dict = None):
        """
        Logs an audit event with detailed information.
        """
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "event_type": event_type,
            "agent": agent,
            "description": description,
            "details": details if details is not None else {}
        }

        os.makedirs("Logs", exist_ok=True) # Ensure Logs directory exists

        with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "
")

        # For immediate feedback in console
        print(f"[AUDIT LOG]: {event_type} by {agent}: {description}")

    @staticmethod
    def log_action(agent: str, action: str, file_name: str = None, decision: str = None):
        """
        Convenience method for logging file-related actions.
        """
        details = {}
        if file_name:
            details["file_name"] = file_name
        if decision:
            details["decision"] = decision

        AuditLogger.log(
            event_type="FILE_ACTION",
            agent=agent,
            description=action,
            details=details
        )
