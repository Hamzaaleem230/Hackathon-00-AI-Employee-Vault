from mcp_servers.social_media_mcp import SocialMediaMCP
import os
from utils.error_handler import robust_skill_execution

class SocialMediaManagerSkill:
    def __init__(self):
        self.sm_mcp = SocialMediaMCP()

    @robust_skill_execution(fallback_return_value="Social media post failed.", skill_name="SocialMediaManagerSkill")
    def handle_social_media_post(self, file_path: str, platform: str) -> str:
        """
        Generates content from a file and posts it to the specified social media platform.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        file_name = os.path.basename(file_path)
        post_message = f"New update from AI Employee Vault: {content[:150]}... #AIEmployeeVault #{platform.capitalize()}"
        success = self.sm_mcp.post_message(platform, post_message)
        if success:
            print(f"[Social Media Manager Skill]: Posted to {platform} from '{file_name}'.")
            return f"Successfully posted to {platform}."
        else:
            print(f"[Social Media Manager Skill]: Failed to post to {platform} from '{file_name}'.")
            return f"Failed to post to {platform}."

    @robust_skill_execution(fallback_return_value="Social media briefing failed.", skill_name="SocialMediaManagerSkill")
    def generate_social_media_briefing(self, platform: str, period: str = "daily") -> str:
        """
        Generates a summary of activity for a given social media platform.
        """
        briefing = self.sm_mcp.get_activity_summary(platform, period)
        print(f"[Social Media Manager Skill]: Generated {platform} briefing: {briefing}")
        return briefing
