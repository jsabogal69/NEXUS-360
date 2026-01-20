# ═══════════════════════════════════════════════════════════════════════════════
# NEXUS-360 SCOUT AGENT
# ═══════════════════════════════════════════════════════════════════════════════
# 
# POLÍTICA DE DATOS:
# - TOP 10 Competidores: Del LLM (análisis cualitativo: nombres, pros, cons, gaps)
# - PRECIOS en TOP 10: Marcados como "ESTIMADO IA" si no hay POE
# - PRECIOS MSRP/TAM/SAM: SOLO de archivos POE (o PENDIENTE)
#
# ═══════════════════════════════════════════════════════════════════════════════

import logging
from ..shared.utils import get_db, generate_id, timestamp_now, report_agent_activity
from ..shared.llm_intel import generate_market_intel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NEXUS-2")

class Nexus2Scout:
    """
    NEXUS-2 Scout Agent - Market Intelligence
    
    Genera TOP 10 competidores vía LLM (análisis cualitativo).
    Los PRECIOS del LLM se marcan claramente como "ESTIMADO IA".
    Para precios consistentes, se requieren archivos POE (X-Ray).
    """
    
    task_description = "Market Intelligence con transparencia de fuentes de datos"
    
    def __init__(self):
        self.db = get_db()
        self.role = "NEXUS-2 (Scout)"

    @report_agent_activity
    async def perform_osint_scan(self, context_str: str, poe_data: dict = None) -> dict:
        """
        Ejecuta análisis de mercado.
        
        Args:
            context_str: Descripción del nicho/producto
            poe_data: Datos extraídos de archivos POE (X-Ray, Helium10)
        
        Returns:
            dict con findings incluyendo TOP 10 y source tracking
        """
        logger.info(f"[{self.role}] Analyzing Market: {context_str}")
        
        # ═══════════════════════════════════════════════════════════════════
        # PASO 1: Verificar si hay datos POE reales para PRECIOS
        # ═══════════════════════════════════════════════════════════════════
        has_poe_data = poe_data is not None and poe_data.get("has_real_data", False)
        
        if has_poe_data:
            logger.info(f"[{self.role}] ✅ POE DATA DETECTED - Using real verified pricing")
            poe_products = poe_data.get("products", [])[:10]
            pricing_source = "POE_VERIFIED"
            data_source_file = poe_data.get("source_file", "Unknown")
        else:
            logger.info(f"[{self.role}] ℹ️ No POE data - LLM prices marked as estimates")
            poe_products = []
            pricing_source = "LLM_ESTIMATE"
            data_source_file = None
        
        # ═══════════════════════════════════════════════════════════════════
        # PASO 2: LLM para análisis de mercado y TOP 10
        # El TOP 10 es válido para: nombres, pros, cons, gaps, brechas
        # Los PRECIOS se marcan según la fuente (POE vs LLM)
        # ═══════════════════════════════════════════════════════════════════
        logger.info(f"[{self.role}] Executing market analysis via LLM...")
        
        llm_top_10 = []
        social = {}
        trends = []
        keywords = []
        sentiment_summary = "Análisis en progreso."
        scholar_audit = []
        content_opportunities = {}
        sales_intelligence = {}
        
        try:
            llm_data = generate_market_intel(context_str)
            
            # TOP 10 del LLM - válido para análisis cualitativo
            llm_top_10 = llm_data.get("top_10_products", [])
            
            # Marcar los precios del LLM como estimados
            for product in llm_top_10:
                if not has_poe_data:
                    product["price_source"] = "LLM_ESTIMATE"
                    product["price_disclaimer"] = "⚡ Estimado"
                else:
                    product["price_source"] = "POE_VERIFIED"
                    product["price_disclaimer"] = "📁 POE"
            
            # Datos cualitativos (siempre del LLM - esto es análisis, no invención)
            social = llm_data.get("social_listening", {})
            trends = llm_data.get("trends", [])
            keywords = llm_data.get("keywords", [])
            sentiment_summary = llm_data.get("sentiment_summary", "Análisis en progreso.")
            scholar_audit = llm_data.get("scholar_audit", [])
            content_opportunities = llm_data.get("content_opportunities", {})
            sales_intelligence = llm_data.get("sales_intelligence", {})
            
        except Exception as e:
            logger.error(f"[{self.role}] LLM analysis failed: {e}")
        
        # ═══════════════════════════════════════════════════════════════════
        # PASO 3: Decidir qué TOP 10 usar
        # Si hay POE: merge con datos reales de precio
        # Si no hay POE: usar LLM pero marcar precios como estimados
        # ═══════════════════════════════════════════════════════════════════
        
        if has_poe_data and poe_products:
            # Usar productos POE (tienen precios reales)
            final_top_10 = poe_products
            for p in final_top_10:
                p["price_source"] = "POE_VERIFIED"
        else:
            # Usar TOP 10 del LLM (análisis cualitativo válido, precios estimados)
            final_top_10 = llm_top_10
        
        # ═══════════════════════════════════════════════════════════════════
        # PASO 4: Construir findings CON TRANSPARENCIA
        # ═══════════════════════════════════════════════════════════════════
        
        findings = {
            "id": generate_id(),
            "product_anchor": context_str[:50],
            "scout_anchor": context_str[:50],
            
            # TOP 10 con source tracking
            "top_10_products": final_top_10,
            "pricing_source": pricing_source,
            "data_source_file": data_source_file,
            "has_poe_data": has_poe_data,
            
            # Datos cualitativos del LLM (análisis, no invención)
            "social_listening": social,
            "trends": trends,
            "keywords": keywords,
            "sales_intelligence": sales_intelligence,
            "scholar_audit": scholar_audit,
            "sentiment_summary": sentiment_summary,
            "content_opportunities": content_opportunities,
            
            # Metadata
            "timestamp": timestamp_now(),
            "data_integrity": {
                "top_10_source": pricing_source,
                "qualitative_source": "LLM_ANALYSIS",
                "price_disclaimer": "⚡ Precios estimados por IA" if not has_poe_data else "📁 Precios de archivos POE"
            }
        }
        
        self._save_findings(findings)
        return findings

    def _save_findings(self, data: dict):
        if not self.db: return
        try: 
            self.db.collection("validated_intelligence").document(data["id"]).set(data)
        except: 
            pass


# Entry point for testing
if __name__ == "__main__":
    scout = Nexus2Scout()
    logger.info(f"{scout.role} Online")
