import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- Email Service ---
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
EMAIL_FROM = os.getenv("EMAIL_FROM")
NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL")

# --- Odoo Integration ---
ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USERNAME = os.getenv("ODOO_USERNAME")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")

# --- Social Media APIs ---
FACEBOOK_API_KEY = os.getenv("FACEBOOK_API_KEY")
FACEBOOK_API_SECRET = os.getenv("FACEBOOK_API_SECRET")
INSTAGRAM_API_KEY = os.getenv("INSTAGRAM_API_KEY")
INSTAGRAM_API_SECRET = os.getenv("INSTAGRAM_API_SECRET")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
LINKEDIN_API_KEY = os.getenv("LINKEDIN_API_KEY")
LINKEDIN_API_SECRET = os.getenv("LINKEDIN_API_SECRET")

# --- Vault Sync ---
VAULT_SYNC_REPO = os.getenv("VAULT_SYNC_REPO")

# --- Agent Configuration ---
# Define which agent this is running as. This could be set as an environment variable itself.
# 'cloud' or 'local'
AGENT_TYPE = os.getenv("AGENT_TYPE", "local") 
