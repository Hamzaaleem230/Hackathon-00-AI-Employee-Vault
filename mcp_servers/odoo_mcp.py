import xmlrpc.client
import psycopg2 # Neon DB ke liye (pip install psycopg2-binary)
import os
from dotenv import load_dotenv

load_dotenv()

class OdooMCP:
    def __init__(self):
        self.url = os.getenv("ODOO_URL")
        self.db = os.getenv("ODOO_DB")
        self.username = os.getenv("ODOO_USER")
        self.password = os.getenv("ODOO_PASS")
        self.neon_url = os.getenv("NEON_DB_URL")

    def create_invoice(self, customer_name, amount, task_id="DEMO-001"):
        try:
            # 1. Odoo Connection
            common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            uid = common.authenticate(self.db, self.username, self.password, {})
            models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')

            # 2. Odoo mein Invoice banana
            partner_id = models.execute_kw(self.db, uid, self.password, 'res.partner', 'name_create', [customer_name])[0]
            inv_id = models.execute_kw(self.db, uid, self.password, 'account.move', 'create', [{
                'partner_id': partner_id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [(0, 0, {'name': 'AI Service', 'price_unit': amount, 'quantity': 1})]
            }])
            
            # 3. Neon DB mein Audit Log daalna (Zaroori for Gold Tier)
            conn = psycopg2.connect(self.neon_url)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO odoo_audit_logs (task_id, action_type, odoo_invoice_id, amount) VALUES (%s, %s, %s, %s)",
                (task_id, 'Invoice Created', str(inv_id), amount)
            )
            conn.commit()
            cur.close()
            conn.close()

            print(f"✅ Success! Invoice #{inv_id} created and logged to Neon.")
            return f"INV-{inv_id}"
        except Exception as e:
            print(f"❌ Error in Integration: {e}")
            return None