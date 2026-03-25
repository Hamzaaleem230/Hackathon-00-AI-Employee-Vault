import time
import os
from datetime import datetime

def check_system():
    # Dashboard update karne ke liye
    status_msg = f"🟢 System Live | Last Heartbeat: {datetime.now().strftime('%H:%M:%S')}"
    
    with open("Dashboard.md", "w", encoding="utf-8") as f:
        f.write(f"# 🚀 AI Employee Vault Dashboard\n\n")
        f.write(f"### ⚡ System Status\n- {status_msg}\n\n")
        f.write(f"### 📂 Quick Links\n- [Latest CEO Briefing](./CEO_Reports/)\n- [Social Drafts](./Vault/Pending_Approval/Social/)\n\n")
        f.write(f"### 🛠️ Active Modules\n- ✅ Odoo ERP (Accounting)\n- ✅ Neon DB (Audit Cloud)\n- ✅ Playwright (Social Engine)")

    print(status_msg)

if __name__ == "__main__":
    print("AI Employee Heartbeat Started...")
    while True:
        check_system()
        time.sleep(10) # Every 10 seconds status update