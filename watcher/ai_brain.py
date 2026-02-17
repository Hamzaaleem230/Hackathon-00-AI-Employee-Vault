import os


class AIBrain:

    @staticmethod
    def evaluate(file_path: str) -> str:
        """
        Returns: 'approved' or 'rejected'
        """

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().lower()

            # Simple Rule Logic
            if "urgent" in content:
                return "approved"

            if "approved" in content:
                return "approved"

            if "reject" in content:
                return "rejected"

            # Default fallback
            return "rejected"

        except Exception as e:
            print("AI Brain Error:", e)
            return "rejected"
