from ..shared.utils import get_db, ValidationStatus, timestamp_now, report_agent_activity, generate_id
from ..shared.llm_intel import GEMINI_AVAILABLE, generate_compliance_audit
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
    async def perform_compliance_audit(self, strategy_data: dict, mathematician_data: dict = None) -> dict:
        """
        Auditoría exhaustiva de cumplimiento regulatorio internacional.
        Genera estándares específicos según la categoría del producto.
        
        Args:
            strategy_data: Data from Strategist agent
            mathematician_data: Optional data from Mathematician for margin validation
        """
        anchor = strategy_data.get("scout_anchor", "Mercado")
        norm_anchor = anchor.upper()
        
        # ═══════════════════════════════════════════════════════════════════
        # CATEGORY DETECTION (REQUIRED for compliance rules)
        # ═══════════════════════════════════════════════════════════════════
        # Initialize variables to avoid potential NameError in complex flows
        is_beauty_personal_care = False
        is_baby = False
        is_food = False
        is_fitness = False

        is_beauty_personal_care = any(kw in norm_anchor for kw in [
            "SKINCARE", "COSMETIC", "LOTION", "CREAM", "SERUM", "TOPICAL",
            "SHAMPOO", "CONDITIONER", "MOISTURIZER", "CLEANSER", "SOAP",
            "DEODORANT", "SUNSCREEN", "MAKEUP", "FOUNDATION", "MASCARA",
            "BEAUTY", "PERSONAL CARE", "BODY WASH", "HAIRCARE"
        ])
        is_baby = any(kw in norm_anchor for kw in [
            "BABY", "INFANT", "CHILD", "KIDS", "NIÑO", "BEBE", "BEBÉ",
            "TODDLER", "NEWBORN", "NURSERY", "PEDIATRIC"
        ])
        is_food = any(kw in norm_anchor for kw in [
            "SUPPLEMENT", "VITAMIN", "FOOD", "DIETARY", "EDIBLE",
            "NUTRITION", "PROTEIN", "HERBAL", "ORGANIC FOOD"
        ])
        is_fitness = any(kw in norm_anchor for kw in [
            "FITNESS", "GYM", "EXERCISE", "WORKOUT", "SPORT",
            "YOGA", "TRAINING", "ATHLETIC"
        ])
        
        logger.info(f"[{self.role}] Category Detection: beauty={is_beauty_personal_care}, baby={is_baby}, food={is_food}, fitness={is_fitness}")
        
        # EXPERT DYNAMIC AUDIT (LLM V2)
        # We try to use the dynamic LLM audit first if available
        dynamic_audit = {}
        if GEMINI_AVAILABLE:
            dynamic_audit = generate_compliance_audit(anchor)
            if dynamic_audit and "audits" in dynamic_audit:
                risk_level = dynamic_audit.get("risk_level", "MEDIUM")
                compliance_score = dynamic_audit.get("compliance_score", 75)
                audit_results = dynamic_audit.get("audits", [])
            else:
                # Fallback if LLM output is malformed
                risk_level = "MEDIUM"
                compliance_score = 65
                audit_results = []

        # LEGACY/FALLBACK KEYWORD-BASED AUDIT (If dynamic_audit is empty or lacks fields)
        if not audit_results:
            risk_level = "LOW"
            compliance_score = 70
            audit_results = [
                {"std": "CE Marking (EU)", "status": "MANDATORY", "desc": f"Declaración de conformidad con directivas europeas aplicables para '{anchor}'. Obligatorio para venta en Espacio Económico Europeo.", "source": "FALLBACK_GENERIC"},
                {"std": "REACH Compliance (EU)", "status": "MANDATORY", "desc": "Regulación de químicos en productos vendidos en UE. Declaración de ausencia de sustancias de muy alta preocupación (SVHC).", "source": "FALLBACK_GENERIC"},
                {"std": "California Prop 65", "status": "MANDATORY", "desc": f"Advertencias para productos de '{anchor}' que contienen químicos de la lista de California.", "source": "FALLBACK_GENERIC"},
                {"std": "Amazon Product Compliance", "status": "MANDATORY", "desc": f"Requisitos específicos de Amazon Seller Central para la categoría '{anchor}'. Documentación de seguridad requerida.", "source": "FALLBACK_GENERIC"},
                {"std": "Country of Origin Labeling", "status": "MANDATORY", "desc": "Marcado obligatorio de 'Made in [Country]' en todos los productos importados. Regulado por CBP.", "source": "FALLBACK_GENERIC"},
                {"std": "Product Liability Insurance", "status": "RECOMMENDED", "desc": f"Seguro de responsabilidad del producto para '{anchor}'. Protección legal contra claims de consumidores.", "source": "FALLBACK_GENERIC"},
                {"std": "FBA Compliance (Amazon)", "status": "MANDATORY", "desc": "Requisitos de empaque, etiquetado y códigos de barras para Fulfillment by Amazon. Pasos de prep específicos por categoría.", "source": "FALLBACK_GENERIC"}
            ]

        # ═══════════════════════════════════════════════════════════════════
        # RISK MATRIX CONSTRUCTION
        # ═══════════════════════════════════════════════════════════════════
        risk_matrix = []
        veto_triggered = False
        veto_reasons = []
        
        # ═══════════════════════════════════════════════════════════════════
        # v3.0: FINANCIAL MARGIN VALIDATION (From Mathematician)
        # ═══════════════════════════════════════════════════════════════════
        if mathematician_data:
            margin_validation = mathematician_data.get("margin_validation", {})
            conservative_margin = margin_validation.get("conservative_margin", 100)
            passes_threshold = margin_validation.get("passes_threshold", True)
            
            if not passes_threshold:
                veto_triggered = True
                veto_reasons.append(f"⚠️ VETO FINANCIERO: Margen proyectado ({conservative_margin:.1f}%) por debajo del límite de seguridad (15%)")
                risk_matrix.append({
                    "risk": "Viabilidad Financiera Crítica",
                    "description": f"El margen neto proyectado ({conservative_margin:.1f}%) no absorbe fluctuaciones de CAC/PPC.",
                    "impact": "CRÍTICO",
                    "mitigation": "Rediseñar Unit Economics (reducir COGS o aumentar MSRP)",
                    "status": "VETO ACTIVO"
                })
                logger.warning(f"[{self.role}] ⛔ VETO: Financial margin {conservative_margin:.1f}% below 15% threshold")
        
        
        # Gating Categories that require Amazon approval
        gating_categories = {
            "topical": ["TOPICAL", "SKIN", "CREAM", "LOTION", "SERUM", "COSMETIC"],
            "hazmat": ["BATTERY", "LITHIUM", "FLAMMABLE", "AEROSOL", "CHEMICAL"],
            "pesticide": ["PESTICIDE", "INSECTICIDE", "REPELLENT", "HERBICIDE"],
            "medical": ["MEDICAL", "HEALTH", "THERAPEUTIC", "CURE", "TREAT"],
            "supplement": ["SUPPLEMENT", "VITAMIN", "DIETARY", "HERBAL"]
        }
        
        # Check for gating requirements
        for gate_type, keywords in gating_categories.items():
            if any(kw in norm_anchor for kw in keywords):
                risk_matrix.append({
                    "risk": f"Amazon Gating - {gate_type.title()}",
                    "description": f"Categoría '{gate_type}' requiere aprobación previa de Amazon",
                    "impact": "ALTO",
                    "mitigation": "Solicitar ungating en Seller Central antes de listado",
                    "status": "PENDIENTE"
                })
        
        # AUTOMATIC VETO CONDITIONS
        # Topical products without COA
        if is_beauty_personal_care:
            risk_matrix.append({
                "risk": "Certificate of Analysis (COA)",
                "description": "Productos tópicos requieren COA de laboratorio independiente",
                "impact": "CRÍTICO",
                "mitigation": "Obtener COA de proveedor o laboratorio tercero",
                "status": "REQUERIDO"
            })
            # Check if user declared having COA (future: from input data)
            has_coa = False  # TODO: Check from input files
            if not has_coa:
                veto_triggered = True
                veto_reasons.append("⚠️ VETO: Producto Topical sin Certificate of Analysis (COA)")
        
        # Baby products - strictest requirements
        if is_baby:
            risk_matrix.append({
                "risk": "CPSIA Testing Certificate",
                "description": "Productos infantiles requieren CPC (Children's Product Certificate)",
                "impact": "CRÍTICO",
                "mitigation": "Testing en laboratorio CPSC-accepted antes de importación",
                "status": "OBLIGATORIO"
            })
            has_cpc = False  # TODO: Check from input files
            if not has_cpc:
                veto_triggered = True
                veto_reasons.append("⚠️ VETO: Producto para bebé sin Children's Product Certificate (CPC)")
        
        # Food/Supplements - FDA requirements
        if is_food:
            risk_matrix.append({
                "risk": "FDA Facility Registration",
                "description": "Instalaciones de manufactura deben estar registradas con FDA",
                "impact": "CRÍTICO",
                "mitigation": "Verificar FDA Registration Number del fabricante",
                "status": "OBLIGATORIO"
            })
            has_fda_reg = False  # TODO: Check from input files
            if not has_fda_reg:
                veto_triggered = True
                veto_reasons.append("⚠️ VETO: Suplemento/Alimento sin FDA Facility Registration")
        
        # Patent risk (basic keyword detection)
        patent_red_flags = ["PATENTED", "PATENT PENDING", "®", "™", "PROPRIETARY"]
        if any(flag in norm_anchor for flag in patent_red_flags):
            risk_matrix.append({
                "risk": "Posible Infracción de Patente",
                "description": "Producto o descripción contiene indicadores de patente activa",
                "impact": "ALTO",
                "mitigation": "Consulta legal antes de producción",
                "status": "INVESTIGAR"
            })
        
        # Liability risk for personal use products
        if is_beauty_personal_care or is_baby or is_food or is_fitness:
            risk_matrix.append({
                "risk": "Product Liability Insurance",
                "description": "Productos de uso personal requieren seguro de responsabilidad",
                "impact": "MEDIO",
                "mitigation": "Obtener póliza de $1M+ antes de ventas",
                "status": "RECOMENDADO"
            })
        
        # Add default risks
        risk_matrix.append({
            "risk": "Cambios Regulatorios",
            "description": "Regulaciones pueden cambiar post-lanzamiento",
            "impact": "MEDIO",
            "mitigation": "Monitoreo continuo de CPSC, FDA, FTC",
            "status": "ONGOING"
        })
        
        # Determine final risk level based on veto
        if veto_triggered:
            risk_level = "CRITICAL - VETO ACTIVO"
            compliance_score = max(compliance_score - 30, 0)
        
        return {
            "id": generate_id(),
            "niche_compliance": anchor,
            "risk_level": risk_level,
            "compliance_score": compliance_score,
            "audits": audit_results,
            "total_standards": len(audit_results),
            "mandatory_count": len([a for a in audit_results if a["status"] == "MANDATORY"]),
            
            # NEW v2.0: Risk Matrix and Veto System
            "risk_matrix": risk_matrix,
            "veto_triggered": veto_triggered,
            "veto_reasons": veto_reasons,
            "veto_message": veto_reasons[0] if veto_reasons else None,
            
            "security_protocol": "EYES ONLY - E2E Encrypted Pipeline",
            "audit_note": f"Auditoría de {len(audit_results)} estándares. Matriz de riesgo: {len(risk_matrix)} factores identificados." + (" ⛔ VETO AUTOMÁTICO ACTIVADO" if veto_triggered else ""),
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
