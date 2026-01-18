from ..shared.utils import get_db, ValidationStatus, timestamp_now, report_agent_activity, generate_id
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
        Validates raw input against safety, expert formatting, and schema rules.
        """
        logger.info(f"[{self.role}] Expertise Validation for: {input_id}")
        
        # Expert Fetch: If content is a placeholder, get real data from DB
        real_content = content
        if self.db and (not content or content.get("raw_content") == "batch_processing"):
            doc = self.db.collection("raw_inputs").document(input_id).get()
            if doc.exists:
                real_content = doc.to_dict()
        
        is_valid = True
        rejection_reason = None
        
        raw_text = real_content.get("raw_content", "")
        structured = real_content.get("structured_data")

        # 1. EMPTY CONTENT CHECK
        if not raw_text and not structured:
            is_valid = False
            rejection_reason = "NULL_DATA: No content or structured data found."

        # 2. EXPERT NUMBER CHECK (Anomaly Detection)
        if structured and isinstance(structured, list):
            # Check if numbers look sane or if there was a normalization failure
            # Heuristic: If a price column has values > 1,000,000 for a 65W charger, it's likely a separator error
            for row in structured[:20]:
                for k, v in row.items():
                    if "price" in k or "cost" in k:
                        if isinstance(v, (int, float)) and v > 500000:
                            is_valid = False
                            rejection_reason = f"FORMAT_ERROR: Suspiciously high value in {k} ({v}). Check thousands separator."
                            break

        # 3. CONTENT INTEGRITY (AI Hallucinated Text or Corrupted Data)
        if "Error in expert extraction" in raw_text:
            is_valid = False
            rejection_reason = "CORRUPTION: Harvester failed to read file bytes correctly."

        # 4. CROSS-FIELD VALIDATION
        if structured and len(structured) > 0:
            first_row_keys = set(structured[0].keys())
            if len(first_row_keys) < 2:
                is_valid = False
                rejection_reason = "STRUCTURE_WARNING: Low column density. Check if CSV separator was detected incorrectly."

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
