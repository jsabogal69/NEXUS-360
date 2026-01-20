# ═══════════════════════════════════════════════════════════════════════════════
# NEXUS-360 MANDAMIENTO ARQUITECTÓNICO: NO DATA INVENTION
# ═══════════════════════════════════════════════════════════════════════════════
# 
# REGLA ABSOLUTA: Ningún agente puede INVENTAR datos cuantitativos.
# Todos los valores numéricos DEBEN provenir de:
#   1. Archivos POE reales (X-Ray, Cerebro, etc.)
#   2. APIs verificables (Amazon, Google Trends, etc.)
#   3. O marcarse explícitamente como "DATOS PENDIENTES"
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
    
    MANDAMIENTO: Este agente NO INVENTA datos cuantitativos.
    - Precios, ventas, market share: SOLO de archivos POE
    - LLM solo se usa para análisis CUALITATIVO (sentimiento, gaps, tendencias)
    - Si no hay datos POE, los campos cuantitativos = "PENDIENTE"
    """
    
    task_description = "Market Intelligence basada SOLO en datos POE verificables"
    
    def __init__(self):
        self.db = get_db()
        self.role = "NEXUS-2 (Scout)"

    @report_agent_activity
    async def perform_osint_scan(self, context_str: str, poe_data: dict = None) -> dict:
        """
        Ejecuta análisis de mercado.
        
        Args:
            context_str: Descripción del nicho/producto
            poe_data: Datos extraídos de archivos POE (X-Ray, Cerebro, etc.)
                      SI poe_data es None o vacío, los campos cuantitativos = PENDIENTE
        
        Returns:
            dict con findings - NUNCA con datos inventados
        """
        logger.info(f"[{self.role}] Analyzing Market: {context_str}")
        
        # ═══════════════════════════════════════════════════════════════════
        # PASO 1: Verificar si hay datos POE reales
        # ═══════════════════════════════════════════════════════════════════
        has_poe_data = poe_data is not None and poe_data.get("has_real_data", False)
        
        if has_poe_data:
            logger.info(f"[{self.role}] ✅ POE DATA DETECTED - Using real verified data")
            top_10 = poe_data.get("products", [])[:10]
            data_source = "POE_VERIFIED"
            data_source_file = poe_data.get("source_file", "Unknown")
        else:
            logger.warning(f"[{self.role}] ⚠️ NO POE DATA - Quantitative fields will be PENDIENTE")
            top_10 = []  # NO INVENTAMOS PRODUCTOS
            data_source = "PENDIENTE"
            data_source_file = None
        
        # ═══════════════════════════════════════════════════════════════════
        # PASO 2: LLM solo para análisis CUALITATIVO (no cuantitativo)
        # ═══════════════════════════════════════════════════════════════════
        logger.info(f"[{self.role}] Executing qualitative analysis via LLM...")
        
        try:
            llm_data = generate_market_intel(context_str)
            
            # SOLO extraemos datos CUALITATIVOS del LLM
            social = llm_data.get("social_listening", {})
            trends = llm_data.get("trends", [])
            keywords = llm_data.get("keywords", [])
            sentiment_summary = llm_data.get("sentiment_summary", "Análisis en progreso.")
            scholar_audit = llm_data.get("scholar_audit", [])
            content_opportunities = llm_data.get("content_opportunities", {})
            
            # IMPORTANTE: NO usamos top_10_products del LLM - son inventados
            # Solo usamos los datos POE reales
            
        except Exception as e:
            logger.error(f"[{self.role}] LLM analysis failed: {e}")
            social = {}
            trends = []
            keywords = []
            sentiment_summary = "Error en análisis LLM"
            scholar_audit = []
            content_opportunities = {}
        
        # ═══════════════════════════════════════════════════════════════════
        # PASO 3: Construir findings CON TRANSPARENCIA sobre fuente de datos
        # ═══════════════════════════════════════════════════════════════════
        
        findings = {
            "id": generate_id(),
            "product_anchor": context_str[:50],
            "scout_anchor": context_str[:50],
            
            # DATOS CUANTITATIVOS: Solo de POE o PENDIENTE
            "top_10_products": top_10,
            "data_source": data_source,
            "data_source_file": data_source_file,
            "has_poe_data": has_poe_data,
            
            # Si no hay POE, estos campos son explícitamente PENDIENTE
            "sales_intelligence": poe_data.get("sales_data", {}) if has_poe_data else {
                "status": "PENDIENTE",
                "message": "Subir archivo X-Ray de Helium10 para datos reales"
            },
            
            # DATOS CUALITATIVOS: Del LLM (análisis, no invención)
            "social_listening": social,
            "trends": trends,
            "keywords": keywords,
            "scholar_audit": scholar_audit,
            "sentiment_summary": sentiment_summary,
            "content_opportunities": content_opportunities,
            
            # Metadata
            "timestamp": timestamp_now(),
            "data_integrity": {
                "quantitative_source": data_source,
                "qualitative_source": "LLM_ANALYSIS",
                "warning": None if has_poe_data else "⚠️ DATOS CUANTITATIVOS PENDIENTES - Subir archivos POE"
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
    logger.info(f"{scout.role} Online - NO DATA INVENTION MODE")
