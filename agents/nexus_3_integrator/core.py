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
        logger.info(f"[{self.role}] 🔒 Processing ONLY these {len(input_ids)} IDs — no external data")
        
        pre_fetched_docs = pre_fetched_docs or {}
        data_stats = data_stats or {}
        lineage = data_stats.get("lineage", {})
        input_details = []
        scout_context = {}
        harvester_context = {
            "xray_data": {"has_real_data": False, "source_files": []},
            "data_stats": data_stats
        }
        search_context = {
            "total_volume": 0,
            "avg_conversion_rate": 0.0,
            "weighted_conversion_sum": 0,
            "total_volume_for_conversion": 0,
            "top_keywords": []
        }
        
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
                        
                        # SEARCH TERMS AGGREGATION
                        st_data = d.get("search_terms_data", {})
                        if st_data and st_data.get("has_search_data"):
                            search_context["total_volume"] += st_data.get("total_search_volume", 0)
                            search_context["top_keywords"].extend(st_data.get("top_keywords", []))
                            if st_data.get("avg_conversion_rate", 0) > 0:
                                vol = st_data.get("total_search_volume", 0)
                                conv = st_data.get("avg_conversion_rate", 0)
                                search_context["weighted_conversion_sum"] += (vol * conv)
                                search_context["total_volume_for_conversion"] += vol
                        
                        # X-RAY AGGREGATION (POE Pricing)
                        xr_data = d.get("xray_data", {})
                        if xr_data and xr_data.get("has_real_data"):
                            harvester_context["xray_data"]["has_real_data"] = True
                            harvester_context["xray_data"]["source_files"].append(name)
                                
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

        # Calculate final weighted conversion rate
        final_conversion_rate = 12.0 # Default if no data
        if search_context["total_volume_for_conversion"] > 0:
            final_conversion_rate = round(search_context["weighted_conversion_sum"] / search_context["total_volume_for_conversion"], 2)
            
        search_data_summary = {
            "has_real_data": search_context["total_volume"] > 0,
            "total_search_volume": search_context["total_volume"],
            "avg_conversion_rate": final_conversion_rate,
            "top_keywords": list(set(search_context["top_keywords"]))[:10]
        }

        # Robust anchor recovery
        scout_anchor = scout_context.get("product_anchor")
        if not scout_anchor:
            scout_anchor = data_stats.get("scout_anchor")
        if not scout_anchor:
            scout_anchor = "Mercado Detectado"

        # ═══════════════════════════════════════════════════════════════════
        # PASO 5: Cuadro de las 4 Acciones (ERRC Grid - Océano Azul)
        # ═══════════════════════════════════════════════════════════════════
        errc_grid = self._calculate_errc_grid(scout_context)

        # ═══════════════════════════════════════════════════════════════════
        # PASO 6: Consolidación de Financial Data & Métricas Duras
        # ═══════════════════════════════════════════════════════════════════
        # Recuperar métricas del LLM (market_metrics) y datos crudos si existen
        market_metrics = scout_context.get("market_metrics", {})
        
        # Parseo robusto de datos financieros
        avg_price = market_metrics.get("average_price", 0.0)
        # Fees estimados (30-40% aprox si no hay dato real)
        estimated_fees = round(avg_price * 0.35, 2) 
        
        # Conversion Rate & Click Share
        avg_cvr = market_metrics.get("avg_conversion_rate", search_context.get("avg_conversion_rate", 0))
        # Click Share: Try to get from metrics, else generic estimation based on monopoly
        monopoly = market_metrics.get("monopoly_status", "Competitivo")
        estimated_click_share = 12.0 # Default
        if "Monopolio" in monopoly: estimated_click_share = 65.0
        elif "Fragmentado" in monopoly: estimated_click_share = 8.0
        
        # Top Keywords click share aggregation
        if market_metrics.get("top_keywords_data"):
             try:
                 shares = [float(str(k.get("click_share", "0")).replace("%","")) for k in market_metrics.get("top_keywords_data", [])]
                 if shares: estimated_click_share = sum(shares) / len(shares)
             except: pass

        financial_data = {
            "has_financial_data": avg_price > 0,
            "avg_price": avg_price,
            "avg_fees": estimated_fees,
            "net_margin_percent": round(((avg_price - estimated_fees - (avg_price*0.25))/avg_price)*100, 1) if avg_price > 0 else 0, # Rough margin calc
            "avg_active_sellers": len(scout_context.get("top_10_products", [])) or 10,
            "common_dimensions": "Standard Size", # Placeholder as we don't have dims yet
            "avg_click_share": round(estimated_click_share, 1),
            "avg_conversion_rate": avg_cvr,
            "market_size_revenue": market_metrics.get("tam_monthly_revenue", 0)
        }
        
        consolidated_record = {
            "id": generate_id(),
            "type": "ssot_record",
            "source_metadata": input_details, 
            "data_stats": data_stats,
            "scout_anchor": scout_anchor,
            "scout_data": scout_context, # Preserve full scout detail
            "harvester_data": harvester_context, # NEW: Raw validated data for Strategist
            "search_data": search_data_summary, 
            "financial_data": financial_data, # Nueva sección crítica para Architect
            "errc_grid": errc_grid,
            "timestamp": timestamp_now()
        }
        
        self._save_ssot(consolidated_record)
        return consolidated_record

    def _calculate_errc_grid(self, scout_data: dict) -> dict:
        """
        Calcula el Cuadro de las 4 Acciones (Eliminar, Reducir, Incrementar, Crear)
        basándose en el análisis de mercado del Scout.
        """
        cons = scout_data.get("social_listening", {}).get("cons", [])
        pros = scout_data.get("social_listening", {}).get("pros", [])
        trends = scout_data.get("trends", [])
        
        # Lógica de Análisis para el Océano Azul
        eliminate = []
        reduce = []
        raise_actions = []
        create = []
        
        # 1. ELIMINAR: Características costosas que el cliente ya no valora o que causan fricción
        for c in cons:
            c_str = c.get("text", str(c)) if isinstance(c, dict) else str(c)
            if any(word in c_str.lower() for word in ["costoso", "caro", "complejo", "difícil", "innecesario"]):
                eliminate.append(f"Eliminar {c_str.split(':')[0] if ':' in c_str else c_str}")
        
        # 2. REDUCIR: Características sobre-diseñadas que exceden la necesidad del cliente
        for p in pros:
            p_str = p.get("text", str(p)) if isinstance(p, dict) else str(p)
            if any(word in p_str.lower() for word in ["estándar", "común", "genérico", "promedio"]):
                reduce.append(f"Reducir dependencia en {p_str}")
        
        # 3. INCREMENTAR: Elementos que deben estar muy por encima del estándar de la industria
        for c in cons:
            c_str = c.get("text", str(c)) if isinstance(c, dict) else str(c)
            if any(word in c_str.lower() for word in ["falta", "pobre", "malo", "débil", "lento"]):
                raise_actions.append(f"Incrementar {c_str.replace('Falta de ', '').replace('Pobre ', '')}")
        
        # 4. CREAR: Elementos que la industria nunca ha ofrecido (basado en White Space / Trends)
        white_space = scout_data.get("social_listening", {}).get("white_space_topics", [])
        for topic in white_space:
            create.append(f"Crear solución de {topic}")
        
        for t in trends:
            create.append(f"Innovar en {t.get('title')}")

        return {
            "eliminate": eliminate[:3] or ["Redundancias técnicas", "Embalaje excesivo"],
            "reduce": reduce[:3] or ["Marketing genérico", "Complejidad de uso"],
            "raise": raise_actions[:3] or ["Durabilidad percibida", "Velocidad de respuesta"],
            "create": create[:3] or ["Ecosistema digital", "Experiencia de unboxing premium"]
        }

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
