import logging
import re
import random
from ..shared.utils import get_db, generate_id, timestamp_now, report_agent_activity
from ..shared.llm_intel import generate_market_intel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NEXUS-2")

class Nexus2Scout:
    task_description = "Reactive Market Intelligence with Patel-Vee Protocol (MANDATORY DEEP SOCIAL LISTENING)"
    def __init__(self):
        self.db = get_db()
        self.role = "NEXUS-2 (Scout)"

    @report_agent_activity
    async def perform_osint_scan(self, context_str: str) -> dict:
        """
        Hyper-Detailed Market Scout with Patel-Vee Protocol.
        ALWAYS uses LLM (Gemini AI) for deep social listening and real competitive intelligence.
        No hardcoded data - all insights are generated dynamically by AI.
        """
        logger.info(f"[{self.role}] Analyzing Market Landscape for: {context_str}")
        
        # ═══════════════════════════════════════════════════════════════════
        # PATEL-VEE SOCIAL LISTENING PROTOCOL
        # ═══════════════════════════════════════════════════════════════════
        logger.info(f"[{self.role}] Executing Patel-Vee Social Listening Protocol via Gemini AI...")
        
        # Call the LLM to generate real market intelligence
        llm_data = generate_market_intel(context_str)
        
        # Extract all data from LLM response
        niche_name = llm_data.get("niche_name", context_str[:50])
        top_10 = llm_data.get("top_10_products", [])
        social = llm_data.get("social_listening", {})
        trends = llm_data.get("trends", [])
        keywords = llm_data.get("keywords", [])
        sales_intelligence = llm_data.get("sales_intelligence", {})
        sentiment_summary = llm_data.get("sentiment_summary", "Análisis en progreso.")
        scholar_audit = llm_data.get("scholar_audit", [])
        content_opportunities = llm_data.get("content_opportunities", {})
        
        # Log success metrics
        emotional_analysis = social.get("emotional_analysis", {})
        pain_keywords = social.get("pain_keywords", [])
        competitor_gaps = social.get("competitor_gaps", [])
        
        logger.info(f"[{self.role}] LLM Response Summary:")
        logger.info(f"  - Niche: {niche_name}")
        logger.info(f"  - Products: {len(top_10)}")
        logger.info(f"  - Emotional Analysis: {'YES' if emotional_analysis else 'NO'}")
        logger.info(f"  - Pain Keywords: {len(pain_keywords)}")
        logger.info(f"  - Competitor Gaps: {len(competitor_gaps)}")
        
        # Build findings object with all Patel-Vee data
        findings = {
            "id": generate_id(),
            "product_anchor": niche_name,
            "scout_anchor": niche_name,
            "top_10_products": top_10,
            "social_listening": social,
            "trends": trends,
            "keywords": keywords,
            "sales_intelligence": sales_intelligence,
            "scholar_audit": scholar_audit,
            "sentiment_summary": sentiment_summary,
            "content_opportunities": content_opportunities,
            "timestamp": timestamp_now()
        }
        
        self._save_findings(findings)
        return findings

    def _save_findings(self, data: dict):
        if not self.db: return
        try: self.db.collection("validated_intelligence").document(data["id"]).set(data)
        except: pass

# Entry point for testing
if __name__ == "__main__":
    scout = Nexus2Scout()
    logger.info(f"{scout.role} Online.")
