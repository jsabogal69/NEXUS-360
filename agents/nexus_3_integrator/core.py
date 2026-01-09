import logging
from ..shared.utils import get_db, generate_id, timestamp_now, report_agent_activity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NEXUS-3")

class Nexus3Integrator:
    task_description = "Consolidate harvested & scout data into a Single Source of Truth (SSOT)"
    def __init__(self):
        self.db = get_db()
        self.role = "NEXUS-3 (Integrator)"

    @report_agent_activity
    async def consolidate_data(self, input_ids: list, filenames_override: list = None, data_stats: dict = None, pre_fetched_docs: dict = None) -> dict:
        """
        Consolidates all inputs into an SSOT. 
        Crucial: It fetches the SCOUT data to define the 'Anchor Niche' for the rest of the pipeline.
        """
        logger.info(f"[{self.role}] Consolidating inputs: {input_ids}")
        
        pre_fetched_docs = pre_fetched_docs or {}
        data_stats = data_stats or {}
        lineage = data_stats.get("lineage", {})
        input_details = []
        scout_context = {}
        
        for i_id in input_ids:
            try:
                # 0. Check pre-fetched first (Resilience for tests/offline)
                if i_id in pre_fetched_docs:
                    s_data = pre_fetched_docs[i_id]
                    if s_data.get("product_anchor"):
                        scout_context = s_data
                        input_details.append({
                            "id": i_id, 
                            "name": s_data["product_anchor"], 
                            "type": "scout_intelligence",
                            "summary": "Inteligencia OSINT: Reddit, TikTok y Benchmarking de Mercado."
                        })
                        continue

                # 1. Try to fetch from validated_intelligence (where Scout saves)
                if self.db:
                    scout_doc = self.db.collection("validated_intelligence").document(i_id).get()
                    if scout_doc.exists:
                        s_data = scout_doc.to_dict()
                        if s_data.get("product_anchor"):
                            scout_context = s_data
                            input_details.append({
                                "id": i_id, 
                                "name": s_data["product_anchor"], 
                                "type": "scout_intelligence",
                                "summary": "Inteligencia OSINT: Reddit, TikTok y Benchmarking de Mercado."
                            })
                            continue

                    # 2. Try to fetch from reports (NEXUS Dossiers)
                    report_doc = self.db.collection("reports").document(i_id).get() if self.db else None
                    if report_doc and report_doc.exists:
                        r_data = report_doc.to_dict()
                        input_details.append({
                            "id": i_id, 
                            "name": r_data["metadata"]["title"], 
                            "type": "nexus_report",
                            "summary": "Pre-Analytic Intelligence: Veredictos Históricos y Roadmaps NEXUS."
                        })
                        # Merge previous report context into SSOT stats for Strategist
                        data_stats["previous_intel"] = r_data.get("intel_summary", {})
                        continue

                    # 3. Try to fetch from raw_inputs (Harvester)
                    doc = self.db.collection("raw_inputs").document(i_id).get() if self.db else None
                    if doc and doc.exists:
                        d = doc.to_dict()
                        name = d.get("file_name", "Archivo")
                        input_details.append({
                            "id": i_id, 
                            "name": name, 
                            "type": "harvester_file",
                            "summary": self._infer_summary(name, lineage.get(name, {}))
                        })
            except Exception as e:
                logger.warning(f"Error consolidating input {i_id}: {str(e)}")

        # Priority override with names from payload
        if filenames_override and not input_details:
             for name in filenames_override:
                 input_details.append({
                     "id": generate_id(), 
                     "name": name, 
                     "type": "file", 
                     "summary": self._infer_summary(name, lineage.get(name, {}))
                 })

        # Robust anchor recovery
        scout_anchor = scout_context.get("product_anchor")
        if not scout_anchor:
            scout_anchor = data_stats.get("scout_anchor")
        if not scout_anchor:
            scout_anchor = "Mercado Detectado"

        consolidated_record = {
            "id": generate_id(),
            "type": "ssot_record",
            "source_metadata": input_details, 
            "data_stats": data_stats,
            "scout_anchor": scout_anchor,
            "scout_data": scout_context, # Preserve full scout detail (including sales_intelligence)
            "timestamp": timestamp_now()
        }
        
        self._save_ssot(consolidated_record)
        return consolidated_record

    def _infer_summary(self, filename: str, file_lineage: dict = None) -> str:
        if file_lineage and file_lineage.get("accessed_data"):
             return ", ".join(file_lineage["accessed_data"])
        
        fname = filename.upper()
        if "XRAY" in fname:
            return "Volumen de búsquedas Helium10, Ingresos estimados por ASIN, Benchmark de precios y BSR."
        elif "KEYWORD" in fname or "SERP" in fname:
            return "Tendencias de búsqueda, Rankings orgánicos, Dificultad de Keyword (KD) y PPC Bids."
        elif "SEARCHTERMS" in fname:
            return "Palabras clave de conversión, Cuota de mercado por término y Análisis de competencia SEO."
        elif "PRODUCTS" in fname or "ASIN" in fname or "SEARCHRESULTS" in fname:
            return "Matriz técnica de competidores, Ratings promedio y Análisis de variantes (Top Sellers)."
        elif "NICHES" in fname:
            return "Categorización de mercado, Segmentación de sub-nichos y Visibilidad de marca."
        elif ".PNG" in fname or ".JPG" in fname or "SCREENSHOT" in fname:
            return "Auditoría visual: Infografías, Diseño de empaque y Calidad fotográfica en Amazon."
        elif "OPORTUNIDAD" in fname or "ESTUDIO" in fname:
            return "Análisis de viabilidad, Roadmap de lanzamiento y Análisis de brechas de satisfacción."
        elif "LAMP" in fname or "PROD" in fname or "HIQ" in fname:
            return "Especificaciones de ingeniería, Materiales (Grade), y Propuesta de Valor única."
        
        return "Estructura de Datos: Identificación de patrones analizada por el motor de IA."

    def _save_ssot(self, data: dict):
        if not self.db: return
        try:
            self.db.collection("validated_intelligence").document(data["id"]).set(data)
        except: pass
