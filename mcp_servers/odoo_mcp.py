class OdooMCP:
    """
    Mock MCP for Odoo Community (JSON-RPC APIs).
    Simulates integration with Odoo for accounting tasks.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OdooMCP, cls).__new__(cls)
            print("[ODoo MCP]: Initializing mock Odoo MCP.")
            # In a real scenario, this would establish connection to Odoo
        return cls._instance

    def create_invoice(self, customer_info: dict, items: list, amount: float) -> str:
        print(f"[ODoo MCP]: Mock: Creating invoice for {customer_info.get('name', 'N/A')} for ${amount}.")
        # Simulate Odoo API call
        return f"invoice_Odoo_ID_12345_{customer_info.get('name', 'N/A')}"

    def get_account_balance(self, account_name: str) -> float:
        print(f"[ODoo MCP]: Mock: Getting balance for account '{account_name}'.")
        # Simulate Odoo API call
        return 15000.00 # Mock balance

    def process_expense(self, employee_id: str, description: str, amount: float) -> str:
        print(f"[ODoo MCP]: Mock: Processing expense for employee {employee_id}: {description} - ${amount}.")
        # Simulate Odoo API call
        return f"expense_Odoo_ID_67890_{employee_id}"

    # Add more mock methods as needed for Odoo integration
