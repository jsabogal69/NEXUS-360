from ..shared.utils import get_db, ValidationStatus, timestamp_now, report_agent_activity
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NEXUS-8")

class Nexus8Guardian:
    task_description = "Validate input data schema and compliance"
    def __init__(self):
        self.db = get_db()
        self.role = "NEXUS-8 (The Guardian)"

    @report_agent_activity
    def validate_input(self, input_id: str, content: dict) -> bool:
        """
        Validates raw input against safety and schema rules.
        """
        logger.info(f"[{self.role}] Validating Input: {input_id}")
        
        is_valid = True
        rejection_reason = None
        
        # 1. Schema Check (Basic existence of required keys)
        if not content.get("raw_content"):
            is_valid = False
            rejection_reason = "Missing 'raw_content'"

        # 2. Content Safety (Placeholder for more complex logic)
        # e.g., check for banned keywords or malicious patterns
        
        status = ValidationStatus.VALIDATED.value if is_valid else ValidationStatus.REJECTED.value
        
        self._update_status(input_id, status, rejection_reason)
        return is_valid

    def _update_status(self, input_id: str, status: str, reason: str = None):
        if not self.db:
            logger.warning("DB not connected, skipping update.")
            return

        try:
            ref = self.db.collection("raw_inputs").document(input_id)
            update_data = {
                "validation_status": status,
                "validated_at": timestamp_now(),
                "validator": self.role
            }
            if reason:
                update_data["rejection_reason"] = reason
            
            ref.update(update_data)
            logger.info(f"[{self.role}] Updated {input_id} to {status}")
        except Exception as e:
            logger.error(f"Failed to update Firestore: {e}")

# Entry point for testing
if __name__ == "__main__":
    guardian = Nexus8Guardian()
    logger.info(f"{guardian.role} Online.")
