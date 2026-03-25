from mcp_servers.social_media_mcp import SocialMediaMCP
import os

def test_social():
    print("--- Starting Social Media Integration Test ---")
    
    social_engine = SocialMediaMCP()
    
    # Test Post Content
    content = """🚀 Big News! Our AI Employee Vault is now integrated with Odoo and Neon DB. 
    Efficiency is 100% on autopilot! #AI #Automation #Hackathon2026"""
    
    print("Attempting to create a LinkedIn draft...")
    success = social_engine.post_to_linkedin_draft(content)
    
    if success:
        # Check if the file exists
        draft_dir = os.path.join(os.getcwd(), "Vault", "Pending_Approval", "Social")
        files = os.listdir(draft_dir)
        print(f"✅ SUCCESS: Social Media draft created!")
        print(f"Files in draft folder: {files}")
    else:
        print("❌ FAILED: Could not create social media draft.")

if __name__ == "__main__":
    test_social()