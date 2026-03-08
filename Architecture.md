# AI Employee Vault Architecture

## Overview
The AI Employee Vault is designed as a modular, event-driven system built around a file-based vault structure. It leverages Python for its core logic, with AI functionalities encapsulated as "Agent Skills" and external integrations handled via "Multi-Channel Protocol (MCP) Servers".

## Key Components

### 1. Vault Structure
- **Purpose:** Centralized storage for documents, acting as the primary input and output mechanism.
- **Folders:**
    - `/Inbox`: Initial entry point for new documents.
    - `/Pending_Approval`: Documents awaiting AI-driven or human review.
    - `/Approved`: Documents that have passed AI approval.
    - `/Rejected`: Documents rejected by AI.
    - `/Done`: Documents for which all processing actions are completed.
    - `/Awaiting_Human_Review`: Sensitive documents flagged for human intervention.
    - `/Logs`: System logs and audit trails.
    - `/Plans`: AI-generated task plans.
    - `/Reports`: AI-generated briefings and reports (e.g., CEO Briefing).
    - `/agent_skills`: Container for all AI Agent Skills.
    - `/mcp_servers`: Container for all Multi-Channel Protocol servers.
    - `/utils`: Helper utilities.

### 2. Watcher Scripts
- **Purpose:** Monitor specific vault folders for new or modified documents and trigger processing.
- **Components:**
    - `watcher/watcher.py`: Primary watcher, monitors `/Pending_Approval` (or similar for entry).
    - `action_watcher.py`: Monitors `/Approved` and moves processed files to `/Done`.
    - **Mechanism:** Continuously polls folders using `os.listdir` and `time.sleep`.
    - **Scheduling:** Designed to be run by external schedulers (e.g., Windows Task Scheduler via `run_watchers.bat`).

### 3. AI Brain (`watcher/ai_brain.py`)
- **Purpose:** The central orchestrator for AI functionalities. It receives documents from watchers, determines their type, and dispatches them to appropriate "Agent Skills".
- **Design:** Acts as a dispatcher, not containing complex AI logic itself. It initializes instances of various Agent Skills.

### 4. Agent Skills (`agent_skills/`)
- **Purpose:** Modular, independent units of AI functionality. Each skill handles a specific task or type of document processing.
- **Examples:**
    - `evaluate_document.py`: AI logic for document approval/rejection and human review flagging.
    - `linkedin_poster.py`: Generates content and interfaces with LinkedIn via an MCP.
    - `plan_generator.py`: Creates `Plan.md` files for tasks.
    - `odoo_integrator.py`: Interfaces with Odoo via `OdooMCP` for accounting tasks.
    - `social_media_manager.py`: Manages posting and summary generation for various social platforms via `SocialMediaMCP`.
    - `ceo_briefing_generator.py`: Generates CEO Briefings.
    - `task_orchestrator.py`: (Placeholder for Ralph Wiggum loop) Manages multi-step autonomous tasks.
    - `personal_assistant.py`: (Placeholder for personal workflows) Handles personal-domain tasks.

### 5. Multi-Channel Protocol (MCP) Servers (`mcp_servers/`)
- **Purpose:** Abstraction layer for interacting with external services and APIs. Each MCP provides a standardized interface for a specific external platform.
- **Examples:**
    - `email_service.py`: Sends emails via SMTP.
    - `odoo_mcp.py`: Mock client for Odoo JSON-RPC APIs.
    - `social_media_mcp.py`: Mock client for Facebook, Instagram, Twitter/X APIs.

### 6. Utilities (`utils/`)
- **Purpose:** Shared helper functions and modules.
- **Examples:**
    - `audit_logger.py`: Centralized, comprehensive logging system.
    - `error_handler.py`: Decorators for robust error recovery and graceful degradation.

## Workflow Example: Document Processing

1.  A new document is placed in `/Inbox` (or directly in `/Pending_Approval`).
2.  `watcher.py` detects the document.
3.  `watcher.py` calls `AIBrain.evaluate(document_path)`.
4.  `AIBrain` first calls `evaluate_document` to get an initial decision (`approved`, `rejected`, `human_review`).
5.  Based on content, `AIBrain` might also trigger other skills:
    - If "sales" or "marketing" keywords: `linkedin_poster` is invoked.
    - If "invoice" or "expense" keywords: `odoo_integrator` is invoked.
    - If "social media post" keywords: `social_media_manager` is invoked.
    - If "goal:" or "complex task:" keywords: `task_orchestrator` is invoked.
6.  `watcher.py` then acts on the primary decision:
    - `approved`: Moves to `/Approved`, sends email. `action_watcher.py` moves it to `/Done`.
    - `rejected`: Moves to `/Rejected`, sends email.
    - `human_review`: Moves to `/Awaiting_Human_Review`, sends email notification.
7.  All critical actions and errors are logged via `AuditLogger`.
8.  Errors in skills or processing are handled gracefully by `error_handler` decorators.

## Gold Tier Specific Implementations

-   **Odoo Integration:** Mock Odoo MCP and `odoo_integrator` skill.
-   **Social Media Integration:** Mock Social Media MCP and `social_media_manager` skill.
-   **CEO Briefing:** `ceo_briefing_generator` skill (callable, not yet integrated into continuous workflow).
-   **Audit Logging:** `utils/audit_logger.py` and integration into `watcher.py`.
-   **Error Recovery:** `utils/error_handler.py` and decorators applied to skills and watchers.
-   **Ralph Wiggum Loop:** Mock `task_orchestrator` skill.
-   **Cross-Domain Integration:** Placeholder `personal_assistant.py` (to be created next).

## Future Enhancements
-   Implement real Odoo, Facebook, Instagram, Twitter APIs.
-   Develop more sophisticated AI reasoning for skills.
-   Integrate `ceo_briefing_generator` into a scheduled workflow.
-   Expand `task_orchestrator` with concrete planning and execution logic.
-   Add user interface for human review and task management.
-   Implement more personal workflows.
