import os
from agent_skills.evaluate_document import evaluate_document
from agent_skills.linkedin_poster import post_to_linkedin, generate_linkedin_post_content
from agent_skills.plan_generator import generate_plan
from agent_skills.odoo_integrator import OdooIntegratorSkill
from agent_skills.social_media_manager import SocialMediaManagerSkill
from agent_skills.task_orchestrator import TaskOrchestratorSkill
from agent_skills.personal_assistant import PersonalAssistantSkill


class AIBrain:
    odoo_integrator = OdooIntegratorSkill() # Initialize Odoo Integrator Skill
    social_media_manager = SocialMediaManagerSkill() # Initialize Social Media Manager Skill
    task_orchestrator = TaskOrchestratorSkill() # Initialize Task Orchestrator Skill
    personal_assistant = PersonalAssistantSkill() # Initialize Personal Assistant Skill


    @staticmethod
    def evaluate(file_path: str) -> str:
        """
        Delegates document evaluation to the evaluate_document skill
        and potentially triggers other skills based on content.
        Returns: 'approved', 'rejected', or 'human_review' (for Silver Tier)
        """
        decision = evaluate_document(file_path)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().lower()
        except Exception as e:
            print(f"[AIBrain File Read Error]: {e}")
            content = "" # Ensure content is always a string

        # Silver Tier: LinkedIn Posting Logic
        if "sales" in content or "marketing" in content:
            post_content = generate_linkedin_post_content(file_path)
            post_to_linkedin(post_content)

        # Silver Tier: Plan Generation Logic
        if decision == "approved" and ("task" in content or "project" in content):
            generate_plan(file_path)

        # Gold Tier: Odoo Integration Logic
        if "invoice" in content or "expense" in content or "accounting" in content:
            AIBrain.odoo_integrator.process_accounting_document(file_path)

        # Gold Tier: Social Media Integration Logic
        if "social media post" in content or "facebook post" in content or "instagram post" in content or "twitter post" in content or "x post" in content or "social media campaign" in content:
            platform = "facebook" # Default platform for general "social media post"
            if "facebook" in content:
                platform = "facebook"
            elif "instagram" in content:
                platform = "instagram"
            elif "twitter" in content or "x post" in content:
                platform = "twitter"
            
            AIBrain.social_media_manager.handle_social_media_post(file_path, platform)
        
        if "social media summary" in content or "facebook summary" in content or "instagram summary" in content or "twitter summary" in content or "x summary" in content:
            platform = "facebook" # Default platform
            if "facebook" in content:
                platform = "facebook"
            elif "instagram" in content:
                platform = "instagram"
            elif "twitter" in content or "x summary" in content:
                platform = "twitter"
            
            AIBrain.social_media_manager.generate_social_media_briefing(platform)

        # Gold Tier: Ralph Wiggum Loop / Task Orchestrator Logic
        if "goal:" in content or "complex task:" in content:
            goal_start_index = content.find("goal:")
            if goal_start_index == -1:
                goal_start_index = content.find("complex task:")
            
            if goal_start_index != -1:
                goal_text = content[goal_start_index:].split('\n')[0].strip()
                AIBrain.task_orchestrator.orchestrate_task(goal_text, file_path)
        
        # Gold Tier: Personal Assistant / Cross-Domain Integration Logic
        if "personal" in content or "grocery" in content or "reminder" in content:
            AIBrain.personal_assistant.handle_personal_request(file_path)


        return decision
