import os
from mcp_servers.odoo_mcp import OdooMCP
from dotenv import load_dotenv

# Environment variables load karein
load_dotenv()

def test_integration():
    print("--- Starting Gold Tier Integration Test ---")
    
    # Odoo MCP ka instance banayein
    agent = OdooMCP()
    
    # Test Data
    customer = "Hackathon Test User"
    amount = 750.0
    task_id = "TASK-GOLD-001"
    
    print(f"Attempting to create invoice for {customer}...")
    
    # Invoice create karne ki koshish
    result = agent.create_invoice(customer, amount, task_id)
    
    if result:
        print(f"✅ SUCCESS: Invoice generated with ID: {result}")
        print("Now check your Odoo Dashboard (Invoicing) and Neon DB Console!")
    else:
        print("❌ FAILED: Could not create invoice. Check your .env settings and Odoo status.")

if __name__ == "__main__":
    test_integration()