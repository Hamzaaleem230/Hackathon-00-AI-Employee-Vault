from mcp_servers.odoo_mcp import OdooMCP
import os
from utils.error_handler import robust_skill_execution

class OdooIntegratorSkill:
    def __init__(self):
        self.odoo_mcp = OdooMCP()

    @robust_skill_execution(fallback_return_value="Odoo integration failed.", skill_name="OdooIntegratorSkill")
    def process_accounting_document(self, file_path: str) -> str:
        """
        Processes an accounting-related document and interacts with Odoo MCP.
        For demonstration, it will check for keywords and call mock Odoo functions.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().lower()

        file_name = os.path.basename(file_path)

        if "invoice" in content:
            # Mock extraction of info
            customer_name = "Mock Customer"
            amount = 100.00
            if "urgent" in content:
                amount = 500.00 # Example of AI reasoning affecting action
            invoice_id = self.odoo_mcp.create_invoice({"name": customer_name}, [], amount)
            print(f"[Odoo Integrator Skill]: Processed invoice from '{file_name}'. Odoo ID: {invoice_id}")
            return f"Invoice {invoice_id} created in Odoo."
        elif "expense" in content:
            employee_id = "EMP001"
            amount = 50.00
            expense_id = self.odoo_mcp.process_expense(employee_id, f"Expense from {file_name}", amount)
            print(f"[Odoo Integrator Skill]: Processed expense from '{file_name}'. Odoo ID: {expense_id}")
            return f"Expense {expense_id} processed in Odoo."
        else:
            print(f"[Odoo Integrator Skill]: No specific accounting action for '{file_name}'.")
            return "No Odoo action taken."

