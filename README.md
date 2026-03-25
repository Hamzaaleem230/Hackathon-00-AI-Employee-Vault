# 🤖 AI Employee Vault (Autonomous Digital FTE)

> **"Transforming unstructured corporate data into actionable intelligence through autonomous AI governance and business automation."**

---

## 📌 Problem Statement 📝

Modern enterprises face overwhelming volumes of documents and operational tasks—ranging from invoices and payroll to compliance and marketing workflows. Traditional systems suffer from:

- ⏳ **High Latency:** Slow approvals and delayed decision-making  
- 🧩 **Context Fragmentation:** Disconnected systems (ERP, files, reports)  
- 🔍 **Lack of Auditability:** No clear reasoning behind approvals/rejections  
- 🔄 **Manual Overhead:** Human dependency in repetitive operational workflows  

---

## 💡 Solution Overview 🌟

The **AI Employee Vault** is an **Autonomous Digital FTE (Full-Time Employee)** that acts as a **compliance officer + operations manager**.

It intelligently:
- Monitors incoming documents  
- Understands context using LLMs (Gemini / Claude)  
- Executes decisions (Approve / Reject / Act)  
- Automates business workflows (ERP + Social Media)  
- Maintains a **real-time cloud audit trail**

---

## 🚀 Key Features ✨

### 🕵️ Autonomous Watcher Engine
- Real-time monitoring of file systems and task directories  
- Detects new documents and triggers AI processing  

### 🧠 Context-Aware AI Auditing
- Uses LLMs to interpret **intent**, not just keywords  
- Returns structured JSON decisions with:
  - Confidence Score  
  - Reasoning  
  - Action  

### ⚙️ Dynamic Task Engine
- Processes JSON-based operational tasks  
- Supports state transitions: Pending → Processing → Completed / Failed  

### 🧾 Proactive Accounting (Odoo Integration)
- Automatically generates invoices via **Odoo JSON-RPC API**  
- Syncs financial operations without manual input  

### 📣 Social Media Automation
- Generates marketing content using AI  
- Automates posting workflows via **Playwright browser automation**  

### 📊 Enterprise Dashboard
- Real-time monitoring with analytics and file previews  
- Instant search and filtering  
- Optimized for sub-second responses  

### 📜 Governance Audit History
- Every decision logged in **Neon PostgreSQL**  
- Fully searchable audit trail  
- CSV export for compliance reporting  

### 🧠 CEO Briefing Engine
- Generates **"Monday Morning CEO Briefing"**  
- Summarizes:
  - Revenue insights  
  - Task bottlenecks  
  - Operational performance  

### 🛡️ Resilient Architecture
- API retry logic  
- Priority-based task queuing  
- Fault-tolerant processing system  

---

## 🛠 Tech Stack 💻

| Layer | Technology |
|------|-----------|
| **AI Brain** | Gemini API / Claude |
| **Backend** | FastAPI (Python 3.10+) |
| **Database** | Neon PostgreSQL |
| **ERP Integration** | Odoo Community Edition (JSON-RPC) |
| **Automation** | Playwright, Python-Dotenv, Psycopg2 |
| **Frontend/UI** | Bootstrap 5 + Jinja2 |
| **Dashboard (Alt)** | Obsidian (Local-first Vault) |
| **Deployment** | Docker / Hugging Face Spaces |

---

## 🏗 System Architecture & Workflow 📂

### 1. File Lifecycle 🔄

Every document follows a strict state machine:

1. 📥 **Pending_Approval** → Entry point  
2. ⚙️ **Processing** → AI analysis stage  
3. ✅ **Approved / ❌ Rejected** → Final decision  
4. 🏁 **Completed / ⚠️ Failed** → Task execution status  

---

### 2. AI Brain Flow 🧠

- Documents are sent to LLM with a **strict system prompt**
- Output is enforced in **JSON format**
- Includes:
  - Decision  
  - Confidence Score  
  - Reasoning  

Ensures every action is **audit-defensible**

---

### 3. Watcher & Task Engine 📡

- Background process continuously polls directories  
- Prioritizes files (e.g., "urgent" tags)  
- Handles:
  - API lifecycle  
  - Retry mechanisms  
  - Task execution  

---

### 4. Database Sync 🐘

- Uses **PostgreSQL relational schema**  
- Stores:
  - Decisions  
  - Logs  
  - Task states  

Dashboard queries DB instead of filesystem → **fast + scalable**

---

### 5. Dashboard Interaction 🖥️

- Real-time UI with:
  - Auto-refresh  
  - File previews  
  - Search & filtering  
- Optimistic UX:
  - Client-side search  
  - Lazy-loaded previews  

---

### 6. External System Integrations 🔗

- **Odoo ERP:** Financial automation  
- **Neon DB:** Cloud audit logging  
- **Playwright:** Browser-based automation  
- **Obsidian Vault:** Human-in-the-loop visibility  

---

## 📂 Folder Structure 📂

```text
.
├── app.py                  # FastAPI Dashboard & API routes
├── main.py                 # AI Watcher & Task Engine
├── heartbeat.py            # System monitoring & orchestration
├── database.py             # PostgreSQL connection logic
├── templates/              # Jinja2 UI templates
├── Pending_Approval/       # Incoming documents 📥
├── Approved/               # Approved files ✅
├── Rejected/               # Rejected files ❌
├── Tasks/                  # JSON task workflows ⚙️
├── mcp_servers/            # Odoo & Social integrations
├── CEO_Reports/            # Generated business reports
├── Vault/                  # Human approval layer
└── requirements.txt        # Dependencies
```

---

## 🔧 Setup & Installation ⚙️

1. Clone the repository  
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure `.env`:
   - Odoo credentials  
   - Neon DB connection  
   - API keys (Gemini / Claude)  

4. Run the system:
   ```bash
   python heartbeat.py
   ```

---

## 📈 Future Scalability 🚀

- 🤝 **Multi-Agent AI System** (Finance, HR, Legal agents)  
- 🔔 **Slack / Email Webhooks** for real-time alerts  
- 🖼️ **OCR Support** for scanned documents & images  
- 🔐 **SAML / SSO Authentication**  
- ☁️ **Full Cloud-Native Microservices Architecture**  

---

## 🏁 Closing Note

The **AI Employee Vault** represents a shift from traditional automation to **Autonomous Enterprise Governance**.

It doesn’t just process data—it:
- Understands context  
- Makes decisions  
- Executes actions  
- Maintains accountability  

A true **AI-powered Digital Employee**.

---

## 🏆 Hackathon Context

**Built for:** *Hackathon 0 - Building Autonomous FTEs (2026)*  

This project demonstrates how AI can evolve from an assistant into a **fully autonomous operational unit** within modern enterprises.

---