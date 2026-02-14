import logging
import asyncio
from ..shared.utils import get_db, generate_id, timestamp_now, report_agent_activity, sanitize_text_field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NEXUS-6")

class Nexus6SeniorPartner:
    task_description = "Draft a professional executive summary and final verdict"
    def __init__(self):
        self.db = get_db()
        self.role = "NEXUS-6 (Senior Partner)"

    @report_agent_activity
    async def synthesize_executive_summary(self, math_data: dict, strategy_data: dict) -> dict:
        """
        Synthesizes all findings into a high-level executive summary.
        Now compatible with structured strategic_gaps.
        """
        logger.info(f"[{self.role}] Drafting Executive Summary...")
        
        # Extract specific data for synthesis
        scenarios = math_data.get("scenarios", {})
        kit_margin = scenarios.get("kit_premium", {}).get("net_margin_pct", 0)
        indiv_margin = scenarios.get("individual_amz", {}).get("net_margin_pct", 0)
        gaps = strategy_data.get("strategic_gaps", [])
        verdict = strategy_data.get("dynamic_verdict", {})
        
        # Clean gaps - handle both dict and string for robustness
        clean_gaps = []
        for g in gaps:
            if isinstance(g, dict):
                clean_gaps.append(g.get("gap", "Oportunidad de Mercado"))
            else:
                clean_gaps.append(str(g).split(":")[0].replace("**", "").strip())
        
        # Professional Synthesis Narrative
        anchor = strategy_data.get("scout_anchor", "la categoría analizada")
        
        # Grounding with dynamic strategic insights from Strategist
        thesis = verdict.get("strategic_thesis", "Dominancia por Ecosistema y Diferenciación")
        insight = verdict.get("key_insight", f"Déficit de calidad en el segmento {anchor}")
        angle = verdict.get("competitive_angle", "Excelencia técnica y diseño emocional")
        market_logic = verdict.get("market_sizing", {}).get("logic", "Cálculo basado en volumen promedio de mercado")
        
        summary = (
            f"Socio, tras una inmersión forense en los {len(strategy_data.get('analyzed_sources', []))} archivos de inteligencia y un escaneo OSINT, "
            f"mi síntesis es definitiva: **{thesis}**.\n\n"
            
            f"**I. La Trampa de la Comoditización:** El análisis transversal confirma que el modelo de 'Unidad Base' es financieramente insostenible. "
            f"Con un margen neto proyectado de apenas el {indiv_margin}%, cualquier fricción en el ACOS o FBA absorbería el beneficio. "
            f"Vender solo hardware es una 'carrera hacia el fondo'.\n\n"
            
            f"**II. El Insight Maestro:** El mercado sufre de un **{insight}**. "
            f"Nuestra ventaja reside en el **{angle}**. Al escalar hacia el Digital Kit / Ecosistema, proyectamos un margen del **{kit_margin}%**, "
            f"creando un foso defensivo emocional e industrial inalcanzable para clones genéricos.\n\n"
            
            f"**III. Dimensionamiento Económico:** {market_logic}\n\n"
            
            f"**IV. Veredicto NEXUS:** Recomiendo ignorar el retail masivo tradicional para posicionarnos como el nuevo referente de {anchor}. "
            f"El Roadmap de 90 días está calibrado para ganar autoridad técnica antes de escalar la demanda masiva.\n\n"
            f"**Es momento de dejar de ser un vendedor para convertirnos en el dueño de la categoría.**"
        )

        # ═══════════════════════════════════════════════════════════════════
        # PASO 5: Psicológia de Consumo (Bullet Points & Educación)
        # ═══════════════════════════════════════════════════════════════════
        creative_copy = self._generate_creative_copy(strategy_data)
        
        final_summary = {
            "id": generate_id(),
            "parent_math_id": math_data.get("id"),
            "executive_summary": sanitize_text_field(summary),
            "verdict": verdict,
            "creative_copy": creative_copy,
            "timestamp": timestamp_now()
        }
        
        self._save_summary(final_summary)
        return final_summary

    def _generate_creative_copy(self, strategy_data: dict) -> dict:
        """
        Genera Bullet Points basados en la frustración #1 y estrategia de educación.
        """
        avatars = strategy_data.get("avatars", [])
        primary_avatar = avatars[0] if avatars else {"name": "Usuario", "pain_point": "Falta de calidad"}
        pain_point = primary_avatar.get("pain_point", "La inconsistencia en el mercado.")
        
        # Bullet Point #1: Resolución de Frustración #1 (Psicología de Consumo)
        bp1 = f"✅ ADIÓS A {pain_point.upper()}: Diseñado específicamente para resolver la frustración #1 detectada en el nicho."
        
        # Bullet Point #2: Benefit from JTBD (dynamic from strategy)
        anchor = strategy_data.get("scout_anchor", "el mercado")
        bp2 = f"🚀 EL TRABAJO HECHO: Resuelve el problema real que los compradores de {anchor} enfrentan día a día."
        
        # Bullet Point #3: Authority from competitive analysis
        num_competitors = len(strategy_data.get("scout_data", {}).get("top_10_products", []))
        bp3 = f"💎 CALIDAD NEXUS: Calibrado con análisis de {num_competitors} competidores para exceder los estándares del mercado."
        
        return {
            "bullet_points": [bp1, bp2, bp3],
            "education_strategy": f"Enfocar el contenido en el 'Job-to-be-done': Cómo {primary_avatar.get('name')} logra su objetivo final usando el producto.",
            "hook": primary_avatar.get("trigger", "La solución definitiva.")
        }

    def _save_summary(self, data: dict):
        if not self.db: return
        try:
            self.db.collection("validated_intelligence").document(data["id"]).set(data)
        except: pass
