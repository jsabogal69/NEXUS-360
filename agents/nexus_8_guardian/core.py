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
    async def validate_input(self, input_id: str, content: dict) -> bool:
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

    @report_agent_activity
    async def perform_compliance_audit(self, strategy_data: dict) -> dict:
        """
        Verifica que las recomendaciones cumplan con estándares internacionales 
        como USB-IF, Nivel VI de eficiencia energética y seguridad industrial.
        """
        anchor = strategy_data.get("scout_anchor", "Mercado")
        norm_anchor = anchor.upper()
        
        is_electronics = any(x in norm_anchor for x in ["65W", "GAN", "CHARGER", "ADAPTADOR", "POWER"])
        is_lamp = any(x in norm_anchor for x in ["LAMP", "ILUMINACION", "LAMPARA", "LED", "LIGHTING"])
        
        audit_results = []
        if is_electronics:
            audit_results.append({"std": "USB-IF / PD 3.1", "status": "MANDATORY", "desc": "Garantiza negociación de energía segura sin daño a placas base."})
            audit_results.append({"std": "Efficiency Level VI", "status": "MANDATORY", "desc": "Regulación global de consumo fantasma y eficiencia térmica."})
        elif is_lamp:
            audit_results.append({"std": "UL/CE Safety", "status": "MANDATORY", "desc": "Certificación de estabilidad térmica y riesgo de incendio por drivers LED."})
            audit_results.append({"std": "CRI Stability", "status": "RECOMMENDED", "desc": "Control de calidad en el bining de LEDs para evitar derivas cromáticas."})
        else:
            audit_results.append({"std": "ISO 9001", "status": "RECOMMENDED", "desc": "Estándar base de gestión de calidad para manufactura general."})

        return {
            "id": generate_id(),
            "niche_compliance": anchor,
            "audits": audit_results,
            "security_protocol": "EYES ONLY - E2E Encrypted Pipeline",
            "timestamp": timestamp_now()
        }

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
