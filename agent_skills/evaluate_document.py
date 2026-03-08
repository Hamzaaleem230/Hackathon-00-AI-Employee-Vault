import os
from utils.error_handler import robust_skill_execution

@robust_skill_execution(fallback_return_value="rejected", skill_name="EvaluateDocument")
def evaluate_document(file_path: str) -> str:
    """
    Evaluates a document and returns 'approved', 'rejected', or 'human_review'.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().lower()

    # Human Review Logic
    if "sensitive" in content or "confidential" in content:
        return "human_review"

    # Simple Rule Logic
    if "urgent" in content:
        return "approved"

    if "approved" in content:
        return "approved"

    if "reject" in content:
        return "rejected"

    # Default fallback
    return "rejected"
