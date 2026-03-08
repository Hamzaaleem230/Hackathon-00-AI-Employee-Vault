import os
from agent_skills.evaluate_document import evaluate_document # Can be used by local for final approvals
from agent_skills.odoo_integrator import OdooIntegratorSkill
from agent_skills.social_media_manager import SocialMediaManagerSkill
from agent_skills.personal_assistant import PersonalAssistantSkill
from utils.audit_logger import AuditLogger
from utils.error_handler import robust_skill_execution

# Placeholder for new Local-only skills
class WhatsAppSkill:
    @robust_skill_execution(fallback_return_value="WhatsApp action failed.", skill_name="WhatsAppSkill")
    def process_whatsapp_message(self, file_path: str, message: str) -> str:
        AuditLogger.log(
            event_type="WHATSAPP_ACTION",
            agent="LocalBrain",
            description=f"Processing WhatsApp message from file: {os.path.basename(file_path)}",
            details={"message": message}
        )
        print(f"[WHATSAPP SKILL]: Processing WhatsApp message for {os.path.basename(file_path)}: {message}")
        return f"WhatsApp message '{message[:50]}...' processed."

class LocalBrain:
    odoo_integrator = OdooIntegratorSkill()
    social_media_manager = SocialMediaManagerSkill()
    personal_assistant = PersonalAssistantSkill()
    whatsapp_skill = WhatsAppSkill()

    @robust_skill_execution(fallback_return_value="rejected", skill_name="LocalBrainEvaluate")
    def evaluate(self, file_path: str) -> str:
        """
        Local Agent's AI evaluation for final approvals and execution of sensitive tasks.
        """
        AuditLogger.log(
            event_type="LOCAL_BRAIN_EVALUATION",
            agent="LocalBrain",
            description=f"Evaluating document for local action: {os.path.basename(file_path)}",
            details={"file_path": file_path}
        )
        print(f"🏠 Local Brain: Evaluating {os.path.basename(file_path)} for final action.")

        # Read content (file_path here is the In_Progress path)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().lower()
        except Exception as e:
            AuditLogger.log(
                event_type="LOCAL_BRAIN_FILE_READ_ERROR",
                agent="LocalBrain",
                description=f"Error reading file for local evaluation: {file_path}",
                details={"error_message": str(e)}
            )
            content = ""
            # Fallback to rejected if content can't be read for safety
            return "rejected" 
        
        # Platinum Tier: Local agent responsibilities
        # Approvals (final decision, often based on Cloud's initial decision)
        # For simplicity, we'll run evaluate_document again here as a "final check"
        # In a more complex scenario, LocalBrain might have its own evaluate_document variant
        # or read a decision from the file itself (e.g., from Cloud Agent).
        decision = evaluate_document(file_path) # Uses the shared evaluate_document skill

        # Payments / banking (Odoo integration)
        if "invoice" in content or "expense" in content or "accounting" in content:
            AuditLogger.log(
                event_type="LOCAL_BRAIN_ODOO_TRIGGER",
                agent="LocalBrain",
                description=f"Triggering Odoo integration for {os.path.basename(file_path)}"
            )
            self.odoo_integrator.process_accounting_document(file_path) # Triggers mock Odoo action

        # Final send/post actions (Social media, WhatsApp)
        if ("social media final post" in content or "facebook final post" in content or "instagram final post" in content or "twitter final post" in content or "x final post" in content) and decision == "approved":
            platform = "facebook"
            if "facebook" in content:
                platform = "facebook"
            elif "instagram" in content:
                platform = "instagram"
            elif "twitter" in content or "x final post" in content:
                platform = "twitter"
            AuditLogger.log(
                event_type="LOCAL_BRAIN_SM_FINAL_POST_TRIGGER",
                agent="LocalBrain",
                description=f"Triggering Social Media FINAL post for {os.path.basename(file_path)} on {platform}"
            )
            self.social_media_manager.handle_social_media_post(file_path, platform) # Triggers mock social media post
        
        if "whatsapp message" in content and decision == "approved":
            message_to_send = f"Final message from AI for {os.path.basename(file_path)}."
            self.whatsapp_skill.process_whatsapp_message(file_path, message_to_send)

        # Personal / cross-domain integration
        if "personal final action" in content or "grocery list completed" in content or "reminder executed" in content:
            AuditLogger.log(
                event_type="LOCAL_BRAIN_PERSONAL_FINAL_ACTION",
                agent="LocalBrain",
                description=f"Executing final personal action for {os.path.basename(file_path)}"
            )
            self.personal_assistant.handle_personal_request(file_path) # Triggers mock personal action

        # The returned decision will be used by the watcher to move the file
        return decision
