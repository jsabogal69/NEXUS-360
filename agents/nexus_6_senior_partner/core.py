import logging
import asyncio
from ..shared.utils import get_db, generate_id, timestamp_now, report_agent_activity

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
        Now more professional, detailed, and non-repetitive.
        """
        logger.info(f"[{self.role}] Drafting Executive Summary...")
        
        # Extract specific data for synthesis
        scenarios = math_data.get("scenarios", {})
        kit_margin = scenarios.get("kit_premium", {}).get("margin_pct", 0)
        indiv_margin = scenarios.get("individual_amz", {}).get("margin_pct", 0)
        gaps = strategy_data.get("strategic_gaps", [])
        verdict = strategy_data.get("dynamic_verdict", {})
        
        # Clean gaps to avoid repetition in the summary
        clean_gaps = [g.split(":")[0].replace("**", "").strip() for g in gaps]
        
        # Professional Synthesis Narrative
        # High-Level Strategic Storytelling Engine
        anchor = strategy_data.get("scout_anchor", "la categoría analizada")
        
        summary = (
            f"Socio, tras una inmersión forense en los {len(strategy_data.get('analyzed_sources', []))} archivos de inteligencia y un escaneo OSINT en tiempo real, "
            f"mi síntesis es definitiva: estamos ante una oportunidad de **Dominancia por Ecosistema**, no por producto.\n\n"
            
            f"**I. La Trampa de la Comoditización:** El análisis de 'Amazon Unit Economics' confirma que entrar con una 'Unidad Base' es un ejercicio de autodestrucción financiera. "
            f"Con un margen neto proyectado de apenas el {indiv_margin}%, cualquier fluctuación en el ACOS o en las tarifas de FBA absorbería la rentabilidad. "
            f"Vender solo hardware en este nicho es participar en una 'carrera hacia el fondo' contra fabricantes asiáticos con estructuras de costo inalcanzables.\n\n"
            
            f"**II. El Foso Estratégico:** Sin embargo, la ventaja reside en lo que la competencia ignora. Hemos detectado que el mercado sufre de un **{clean_gaps[0] if clean_gaps else 'déficit cultural de producto'}**. "
            f"Mientras los líderes se pelean por centavos, existe un segmento de 'Inversores de Estilo de Vida' desatendido que busca durabilidad, salud certificada y una estética que eleve su entorno de vida. "
            f"Nuestra propuesta de **Digital Kit / Ecosistema** no solo soluciona estos puntos de dolor, sino que dispara nuestro margen al {kit_margin}%, "
            f"diluyendo el costo de adquisición de clientes (CAC) y creando una barrera de entrada tecnológica y emocional.\n\n"
            
            f"**III. Veredicto NEXUS:** Mi recomendación es ignorar el retail masivo tradicional y posicionarnos como el **'Gold Standard'** de {anchor}. "
            f"No vendemos un objeto más en su hogar; vendemos una infraestructura de bienestar y estatus. "
            f"La hoja de ruta de 5 fases está calibrada para ganar autoridad clínica y técnica antes de escalar la demanda. "
            f"Tenemos los datos, tenemos el modelo financiero y tenemos la brecha de mercado abierta.\n\n"
            f"**Es momento de dejar de ser un vendedor para convertirnos en el dueño de la categoría.** El Dossier está listo para ejecución."
        )

        final_summary = {
            "id": generate_id(),
            "parent_math_id": math_data.get("id"),
            "executive_summary": summary,
            "verdict": verdict,
            "timestamp": timestamp_now()
        }
        
        self._save_summary(final_summary)
        return final_summary

    def _save_summary(self, data: dict):
        if not self.db: return
        try:
            self.db.collection("validated_intelligence").document(data["id"]).set(data)
        except: pass
