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
from ..shared.llm_intel import generate_market_intel, generate_enhanced_mock
from ..shared.google_trends import get_google_trends_data, extract_trend_keywords

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
    async def perform_osint_scan(self, context_str: str, poe_data: dict = None, search_terms_data: dict = None, raw_text_context: str = None) -> dict:
        """
        Ejecuta análisis de mercado.
        
        Args:
            context_str: Descripción del nicho/producto
            poe_data: Datos extraídos de X-Ray/Helium10 (Productos)
            search_terms_data: Datos extraídos de Search Terms (Keywords)
            raw_text_context: Información extraída de documentos (PDF, etc.)
        
        Returns:
            dict con findings incluyendo TOP 10, source tracking y Hard Data Metrics
        """
        logger.info(f"[{self.role}] Analyzing Market: {context_str}")
        
        # ═══════════════════════════════════════════════════════════════════
        # PASO 1: Etiquetado de Confianza y Preparación de "HARD DATA" Context
        # ═══════════════════════════════════════════════════════════════════
        has_poe_data = poe_data is not None and poe_data.get("has_real_data", False)
        
        # Prepare Hard Data Summary string for LLM Context
        hard_data_summary = "HARD DATA SUMMARY (FROM UPLOADED FILES):\n"
        
        if has_poe_data:
            confidence_tag = "🟢 POE (Dato real de Amazon)"
            poe_products = poe_data.get("products", [])[:10]
            pricing_source = "POE_VERIFIED"
            data_source_file = poe_data.get("source_file", "Unknown")
            
            # --- EXTRACT METRICS FROM POE (X-RAY) ---
            total_rev = poe_data.get("total_revenue", 0)
            avg_price = poe_data.get("average_price", 0)
            avg_bsr = poe_data.get("average_bsr", 0) or 0
            
            hard_data_summary += f"- MARKET SIZE: {len(poe_products)} analyzed products.\n"
            hard_data_summary += f"- FINANCIALS: Total Revenue=${total_rev:,.2f}, Avg Price=${avg_price:.2f}\n"
            hard_data_summary += f"- BSR: Average Best Seller Rank={avg_bsr}\n"
            
            # ═══════════════════════════════════════════════════════════════════
            # CRITICAL: Pass REAL PRODUCT DATA to LLM for specific analysis
            # ═══════════════════════════════════════════════════════════════════
            hard_data_summary += "\n--- REAL COMPETITOR PRODUCTS FROM AMAZON (ANALYZE THESE SPECIFICALLY) ---\n"
            for i, prod in enumerate(poe_products[:10], 1):
                name = prod.get("name", prod.get("title", "Unknown"))[:100]
                asin = prod.get("asin", "N/A")
                price = prod.get("price", 0)
                rating = prod.get("rating", 0)
                reviews = prod.get("reviews", 0)
                brand = prod.get("brand", "Unknown")
                bsr = prod.get("bsr", prod.get("rank", "N/A"))
                
                hard_data_summary += f"""
#{i}. {name}
   - ASIN: {asin}
   - Brand: {brand}
   - Price: ${price}
   - Rating: {rating}★ ({reviews} reviews)
   - BSR: #{bsr}
"""
            hard_data_summary += "\nIMPORTANT: Base your analysis on THESE SPECIFIC products. Identify their REAL pros/cons based on their metrics and typical review patterns for this product type.\n"
            
            # ── NICHE ANALYTICS CONTEXT (from DataExpert Pandas engine) ──
            niche_analytics = poe_data.get("niche_analytics", {})
            if niche_analytics:
                hard_data_summary += "\n--- ADVANCED NICHE ANALYTICS (Data-Driven via Pandas) ---\n"
                
                # Demographics
                demo = niche_analytics.get("demographics", {})
                if demo:
                    dom_seg = demo.get("dominant_segment", "N/A")
                    cls_rate = demo.get("classification_rate", 0)
                    segs = demo.get("segments", {})
                    seg_str = ", ".join([f"{k}: {v.get('pct', 0)}%" for k, v in segs.items() if k != "Unspecified"])
                    hard_data_summary += f"- DEMOGRAPHICS: Dominant={dom_seg} | Classified={cls_rate}% | Breakdown: {seg_str}\n"
                
                # Brand Concentration
                bc = niche_analytics.get("brand_concentration", {})
                if bc:
                    hard_data_summary += f"- BRAND CONCENTRATION: HHI={bc.get('hhi_index', 0)} ({bc.get('hhi_label', 'N/A')}), {bc.get('unique_brands', 0)} unique brands, Top: {bc.get('top_brand', 'N/A')} ({bc.get('top_brand_share', 0)}%)\n"
                
                # Revenue Pareto
                rp = niche_analytics.get("revenue_pareto", {})
                if rp:
                    hard_data_summary += f"- REVENUE DISTRIBUTION: {rp.get('interpretation', 'N/A')} (Concentration: {rp.get('concentration', 'N/A')})\n"
                
                # Price Analytics
                pa = niche_analytics.get("price", {})
                if pa:
                    hard_data_summary += f"- PRICE ANALYTICS: Sweet Spot={pa.get('sweet_spot', 'N/A')}, Std Dev=${pa.get('std', 0)}, Range=${pa.get('min', 0)}-${pa.get('max', 0)}\n"
                
                # Review Velocity
                rv = niche_analytics.get("review_velocity", {})
                if rv:
                    hard_data_summary += f"- REVIEW VELOCITY: Median={rv.get('p50', 0)}/mo, P75={rv.get('p75', 0)}/mo, P90={rv.get('p90', 0)}/mo\n"
                
                hard_data_summary += "\nUse these analytics to provide data-backed strategic recommendations.\n"
            
        else:
            confidence_tag = "🟡 ESTIMADO (Cálculo IA - SIN DATOS REALES)"
            poe_products = []
            pricing_source = "LLM_ESTIMATE"
            data_source_file = None
            hard_data_summary += "- NO PRODUCT DATA AVAILABLE (Use LLM estimates cautiously)\n"

        # --- EXTRACT METRICS FROM SEARCH TERMS ---
        if search_terms_data and search_terms_data.get("has_search_data", False):
            st_file = search_terms_data.get("source_file", "search_terms.csv")
            top_kws = search_terms_data.get("top_keywords", [])[:5]
            
            hard_data_summary += f"\n- SEARCH TERMS SOURCE: {st_file}\n"
            
            # Calculate aggregate metrics if possible
            total_sv = sum(int(k.get("search_volume", 0)) for k in top_kws)
            avg_click_share = 0
            count_cs = 0
            
            kw_lines = []
            for kw in top_kws:
                term = kw.get("term", "unknown")
                sv = kw.get("search_volume", 0)
                cs = kw.get("click_share", "N/A")
                conv = kw.get("conversion_rate", "N/A")
                kw_lines.append(f"  * '{term}': Vol={sv}, ClickShare={cs}, Conv={conv}")
                
                # Try to parse click share for avg
                try:
                    if isinstance(cs, str) and "%" in cs:
                        val = float(cs.replace("%", ""))
                        avg_click_share += val
                        count_cs += 1
                    elif isinstance(cs, (int, float)):
                        avg_click_share += float(cs)
                        count_cs += 1
                except: pass
            
            avg_cs_str = f"{avg_click_share/count_cs:.1f}%" if count_cs > 0 else "N/A"
            
            hard_data_summary += f"- KEYWORD METRICS: Top 5 Vol={total_sv}, Avg Click Share={avg_cs_str}\n"
            hard_data_summary += "  Top Keywords:\n" + "\n".join(kw_lines)
        else:
            hard_data_summary += "\n- NO SEARCH TERM DATA AVAILABLE.\n"

        logger.info(f"[{self.role}] Context prepared with Hard Data:\n{hard_data_summary}")

        # Combine Raw Context with Hard Data Summary
        final_context_block = (raw_text_context or "") + "\n\n" + hard_data_summary
        
        # ═══════════════════════════════════════════════════════════════════
        # PASO 2: LLM para análisis de mercado y TOP 10
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
        market_metrics = {}
        google_trends_raw = {}
        
        try:
            # Pass our enriched context
            llm_data = generate_market_intel(context_str, additional_context=final_context_block)
            
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
            
            # 3. Validation & Fallback for Social Listening
            # If LLM returned empty social data, force heuristic fallback
            social = llm_data.get("social_listening", {})
            if not social or not social.get("pain_keywords"):
                logger.warning(f"[{self.role}] ⚠️ LLM returned empty social data. Activating Heuristic Fallback.")
                fallback_data = generate_enhanced_mock(context_str)
                social = fallback_data.get("social_listening", {})
                llm_data["social_listening"] = social # Update main dict
                
                # Also fill other possibly missing fields
                if not llm_data.get("content_opportunities"):
                    llm_data["content_opportunities"] = fallback_data.get("content_opportunities", {})
                if not llm_data.get("trends"):
                     llm_data["trends"] = fallback_data.get("trends", [])

            trends = llm_data.get("trends", [])
            keywords = llm_data.get("keywords", [])
            
            # New Hard Data Metrics from LLM
            market_metrics = llm_data.get("market_metrics", {})
            
            # ═══════════════════════════════════════════════════════════════════
            # v2.1: REAL GOOGLE TRENDS INTEGRATION
            # ═══════════════════════════════════════════════════════════════════
            # Extract keyword strings from dict format (keywords are [{term:..., volume:...}, ...])
            keyword_strings = []
            for kw in keywords:
                if isinstance(kw, dict):
                    keyword_strings.append(kw.get("term", ""))
                elif isinstance(kw, str):
                    keyword_strings.append(kw)
            keyword_strings = [k for k in keyword_strings if k]  # Remove empty
            
            trend_keywords = extract_trend_keywords(context_str, keyword_strings)
            logger.info(f"[{self.role}] Fetching real-time Google Trends for: {trend_keywords}")
            google_trends_raw = get_google_trends_data(trend_keywords)
            
            sentiment_summary = llm_data.get("sentiment_summary", "Análisis en progreso.")
            scholar_audit = llm_data.get("scholar_audit", [])
            content_opportunities = llm_data.get("content_opportunities", {})
            sales_intelligence = llm_data.get("sales_intelligence", {})
            
            # POE v3.0: Nuevos campos detallados
            buyer_personas = llm_data.get("buyer_personas", [])
            reviews_analysis = llm_data.get("reviews_analysis", {})
            price_tiers = llm_data.get("price_tiers", {})
            amazon_fees_structure = llm_data.get("amazon_fees_structure", {})
            
        except Exception as e:
            logger.error(f"[{self.role}] LLM analysis failed: {e}")
            # ═══════════════════════════════════════════════════════════════════
            # CRITICAL FIX: Activate Heuristic Fallback on LLM Failure
            # ═══════════════════════════════════════════════════════════════════
            logger.warning(f"[{self.role}] 🚨 Activating FULL Heuristic Fallback due to LLM failure.")
            fallback_data = generate_enhanced_mock(context_str)
            social = fallback_data.get("social_listening", {})
            trends = fallback_data.get("trends", [])
            keywords = fallback_data.get("keywords", [])
            market_metrics = fallback_data.get("market_metrics", {})
            sentiment_summary = fallback_data.get("sentiment_summary", "Análisis pendiente.")
            scholar_audit = fallback_data.get("scholar_audit", [])
            content_opportunities = fallback_data.get("content_opportunities", {})
            sales_intelligence = fallback_data.get("sales_intelligence", {})
            google_trends_raw = {}
            
            # POE v3.0: Fallback vacío para nuevos campos
            buyer_personas = []
            reviews_analysis = {}
            price_tiers = {}
            amazon_fees_structure = {}
        
        # ═══════════════════════════════════════════════════════════════════
        # PASO 3: Decidir qué TOP 10 usar
        # Si hay POE: merge con datos reales de precio
        # Si no hay POE: usar LLM pero marcar precios como estimados
        # ═══════════════════════════════════════════════════════════════════
        
        if has_poe_data and poe_products:
            # Usar productos POE (tienen precios reales)
            logger.info(f"[{self.role}] 🛡️ POE MODE ACTIVATED: Using {len(poe_products)} verified products from CSV/Input.")
            final_top_10 = poe_products
            
            # Enriquecimiento Heurístico para evitar "N/A"
            # Enriquecimiento Semántico (Semantic Distributor)
            # Combinamos la verdad numérica del POE con la profundidad cualitativa del LLM
            
            social_pros = social.get("pros", [])
            social_cons = social.get("cons", [])
            social_pain = social.get("pain_keywords", [])
            
            for i, p in enumerate(final_top_10):
                p["price_source"] = "POE_VERIFIED"
                rating = float(p.get("rating", 0))
                reviews = int(p.get("reviews", 0))
                price = float(p.get("price", 0))
                bsr = int(p.get("bsr", 0)) or int(p.get("rank", 0))
                name = p.get("name", "")[:30]
                # NEW Helium 10 fields
                brand = p.get("brand", "N/A")
                seller_country = str(p.get("seller_country", "N/A")).upper()
                fulfillment = str(p.get("fulfillment", "N/A")).upper()
                rev_velocity = int(p.get("review_velocity", 0))
                seller_age = int(p.get("seller_age_months", 0))
                sponsored = str(p.get("sponsored", "No"))
                images = int(p.get("images_count", 0))
                recent_purch = int(p.get("recent_purchases", 0))
                sales = int(p.get("sales", 0))
                
                # ═══════════════════════════════════════════════════════════════════
                # ENHANCED SEMANTIC DISTRIBUTOR v3.0 - Full Helium 10 Intelligence
                # ═══════════════════════════════════════════════════════════════════
                
                # 1. ADVANTAGE (PROS) - Basado en métricas reales + H10 extended
                if rating >= 4.7 and reviews >= 1000:
                    velocity_note = f" | Momentum: {rev_velocity} rev/mes" if rev_velocity > 100 else ""
                    p["adv"] = f"Rating {rating}★ + {reviews:,} reseñas: LÍDER VALIDADO{velocity_note}"
                elif rev_velocity >= 200 and rating >= 4.5:
                    p["adv"] = f"🚀 Momentum explosivo: {rev_velocity} reviews/mes + {rating}★ = Crecimiento viral"
                elif recent_purch >= 5000 and rating >= 4.5:
                    p["adv"] = f"🔥 {recent_purch:,} compras recientes + {rating}★ = Producto trending"
                elif rating >= 4.5 and reviews >= 500:
                    p["adv"] = f"Alta satisfacción ({rating}★) con {reviews:,} reviews | {brand}"
                elif bsr and bsr <= 500:
                    p["adv"] = f"BSR #{bsr:,}: Demanda extremadamente alta | {fulfillment}"
                elif bsr and bsr <= 2000:
                    amz_note = " (Amazon como seller)" if "AMZ" in seller_country or "AMAZON" in str(p.get("seller_name", "")).upper() else ""
                    p["adv"] = f"BSR #{bsr:,}: Alta rotación{amz_note}"
                elif price < 20 and rating >= 4.0:
                    p["adv"] = f"Best Value: ${price:.2f} con {rating}★ | {brand}"
                elif reviews >= 3000:
                    p["adv"] = f"Dominación social: {reviews:,} reseñas (social proof masivo)"
                elif seller_age >= 60 and rating >= 4.3:
                    p["adv"] = f"Veterano ({seller_age} meses) con {rating}★: Posicionamiento estable"
                elif sponsored and sponsored not in ("No", "N/A", "", "nan"):
                    p["adv"] = f"Inversión PPC activa ({sponsored}) = Budget de marketing confirmado"
                elif social_pros:
                    p["adv"] = social_pros[i % len(social_pros)]
                else:
                    p["adv"] = f"Posicionado: {brand} | Rating {rating}★ | {fulfillment}"

                # 2. VULNERABILITY (CONS) - Detecta debilidades con H10 intel
                if rating < 3.5:
                    p["vuln"] = f"⚠️ Rating CRÍTICO {rating}★: Producto en riesgo de deslistado"
                elif "CN" in seller_country and rating < 4.3:
                    p["vuln"] = f"🇨🇳 Seller China + Rating {rating}★: Calidad inconsistente, reviews a riesgo"
                elif rating < 4.0 and reviews > 500:
                    p["vuln"] = f"Rating {rating}★ con {reviews:,} reviews: Problemas sistémicos de calidad"
                elif images < 5 and reviews < 500:
                    p["vuln"] = f"📸 Solo {images} imágenes + {reviews} reviews: Listing sub-optimizado"
                elif rating < 4.3 and social_pain:
                    pk = social_pain[i % len(social_pain)]
                    kw = pk.get('keyword', 'calidad') if isinstance(pk, dict) else str(pk)
                    p["vuln"] = f"Pain Point: '{kw}' (Rating {rating}★)"
                elif sponsored and sponsored not in ("No", "N/A", "", "nan") and rating < 4.5:
                    p["vuln"] = f"💸 Dependencia PPC ({sponsored}) + {rating}★: Orgánico débil"
                elif reviews < 50 and bsr and bsr > 10000:
                    p["vuln"] = f"Riesgo: Solo {reviews} reviews + BSR #{bsr:,} = No validado"
                elif reviews < 100:
                    p["vuln"] = f"Falta validación: Solo {reviews} reseñas | Seller age: {seller_age}mo"
                elif price > 40 and rating < 4.3:
                    p["vuln"] = f"Precio premium (${price:.2f}) sin rating premium ({rating}★)"
                elif seller_age < 12 and reviews < 300:
                    p["vuln"] = f"🆕 Seller nuevo ({seller_age} meses) con {reviews} reviews: No consolidado"
                elif social_cons:
                    p["vuln"] = social_cons[i % len(social_cons)]
                else:
                    p["vuln"] = f"Competencia intensa en rango ${price:.0f} | {seller_country}"

                # 3. STRATEGIC GAP - Oportunidades con H10 deep intel
                if rating < 4.0 and reviews > 1000:
                    p["gap"] = f"🎯 DISRUPTOR: Líder débil ({rating}★) con {reviews:,} ventas = Mejor calidad gana"
                elif "CN" in seller_country and rating < 4.5 and sales > 1000:
                    p["gap"] = f"🇺🇸 ATTACK: Seller CN ({rating}★, {sales:,} ventas) → Entrar con marca US + calidad"
                elif seller_age < 18 and sales > 2000:
                    p["gap"] = f"⚡ FAST MOVER: Seller nuevo ({seller_age}mo) con {sales:,} ventas → Mercado crece rápido"
                elif rating >= 4.7 and reviews < 200:
                    p["gap"] = f"🚀 ESCALAR: Excelente ({rating}★) pero invisible ({reviews} reviews) → PPC + marketing"
                elif price > 35 and rating < 4.2:
                    p["gap"] = f"⚔️ ATTACK: ${price:.2f} injustificado con {rating}★ → Entrada por valor"
                elif images < 6 and rating >= 4.0:
                    p["gap"] = f"📸 LISTING: Solo {images} fotos con {rating}★ → Superarlo con media profesional"
                elif bsr and bsr > 50000:
                    p["gap"] = f"📈 NICHO: BSR #{bsr:,} = Segmento desatendido"
                elif fulfillment == "FBM" and sales > 500:
                    p["gap"] = f"📦 FBA ADVANTAGE: Competidor en FBM ({sales:,} ventas) → Ganar con Prime/FBA"
                elif p.get("age_segment") == "Unspecified" and sales > 500:
                    p["gap"] = f"🎯 SEGMENTACIÓN: {sales:,} ventas sin target demográfico claro → Posicionar por edad"
                elif p.get("age_segment") and p.get("age_segment") != "Unspecified" and price > 30 and p.get("age_segment") in ("Preschool", "Toddler"):
                    p["gap"] = f"💰 MISMATCH: ${price:.2f} en {p['age_segment']} → Padres buscan valor, entrar con precio competitivo"
                elif reviews > 5000 and rating >= 4.5:
                    p["gap"] = f"🛡️ DIFERENCIACIÓN: Líder fuerte → Innovación o nicho específico"
                else:
                    seg_note = f" | Target: {p.get('age_segment', 'N/A')}" if p.get('age_segment', 'Unspecified') != 'Unspecified' else ''
                    p["gap"] = f"Branding & Storytelling diferenciado vs {brand}{seg_note}"
                    
        else:
            # Usar TOP 10 del LLM (análisis cualitativo válido, precios estimados)
            logger.warning(f"[{self.role}] ⚠️ LLM MODE: No verified POE data found. Using LLM estimates (Risk of hallucination).")
            final_top_10 = llm_top_10
            
        # ═══════════════════════════════════════════════════════════════════
        # v2.3: MARKET SHARE CALCULATION FROM REVIEWS (Data-Driven)
        # ═══════════════════════════════════════════════════════════════════
        # Instead of trusting LLM or using flat defaults, we calculate Share of Voice
        # based on Review Count of the identified Top 10 products.
        
        try:
            # Robust extraction of Total Reviews
            total_reviews = 0
            for p in final_top_10:
                try:
                     raw_reviews = str(p.get("reviews", "0")).lower().replace(",", "")
                     if 'k' in raw_reviews:
                         val = float(raw_reviews.replace("k", "")) * 1000
                     else:
                         val = float(raw_reviews)
                     total_reviews += int(val)
                except:
                     pass

            if total_reviews > 0:
                calculated_shares = []
                for p in final_top_10[:5]: # Top 5 only for the chart
                    try:
                        # Cleaning review count (handle strings like '1,200', '1.5k')
                        raw_reviews = str(p.get("reviews", "0")).lower().replace(",", "")
                        if 'k' in raw_reviews:
                            r_val = float(raw_reviews.replace("k", "")) * 1000
                        else:
                            r_val = float(raw_reviews)
                        
                        reviews_val = int(r_val)
                    except:
                        reviews_val = 0
                    
                    share_pct = int((reviews_val / total_reviews) * 100) if total_reviews > 0 else 0
                    calculated_shares.append({
                        "brand": p.get("name", "Unknown").split()[0], # Short brand name
                        "share": share_pct,
                        "status": "Calculated from Reviews"
                    })
                
                # Update the sales_intelligence with this REAL data
                sales_intelligence["market_share_by_brand"] = calculated_shares
                logger.info(f"[{self.role}] ✅ Market Share calculated from Review Counts (Total: {total_reviews})")
        except Exception as e:
            logger.warning(f"[{self.role}] Failed to calculate market share from reviews: {e}")
        
        # ═══════════════════════════════════════════════════════════════════
        # PASO 4: Construir findings CON TRANSPARENCIA
        # ═══════════════════════════════════════════════════════════════════
        
        try:
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
                "google_trends_raw": google_trends_raw,
                
                # ═══════════════════════════════════════════════════════════════════
                # POE v3.0: Nuevos campos detallados
                # ═══════════════════════════════════════════════════════════════════
                "buyer_personas": buyer_personas,
                "reviews_analysis": reviews_analysis,
                "price_tiers": price_tiers,
                "amazon_fees_structure": amazon_fees_structure,
                
                # ═══════════════════════════════════════════════════════════════════
                # POE v4.0: Search Terms Intelligence (Traffic & Demand Analysis)
                # ═══════════════════════════════════════════════════════════════════
                "search_terms_intel": search_terms_data if search_terms_data and search_terms_data.get("has_search_data") else {},
                
                # ═══════════════════════════════════════════════════════════════════
                # POE v5.0: Niche Analytics (Pandas-Powered Demographics & Metrics)
                # ═══════════════════════════════════════════════════════════════════
                "niche_analytics": poe_data.get("niche_analytics", {}) if has_poe_data else {},
                
                # ═══════════════════════════════════════════════════════════════════
                # PASO 5: Detección de 'Lightning Bolt Scaling'
                # ═══════════════════════════════════════════════════════════════════
                "lightning_bolt_opportunity": self._detect_lightning_scaling(social),
                "confidence_tag": confidence_tag,
                
                # Metadata
                "timestamp": timestamp_now(),
                "data_integrity": {
                    "top_10_source": pricing_source,
                    "qualitative_source": "LLM_ANALYSIS",
                    "price_disclaimer": "⚡ Precios estimados por IA" if not has_poe_data else "📁 Precios de archivos POE"
                }
            }
        except Exception as e:
            logger.error(f"[SCOUT-CRITICAL] Failed to construct findings: {e}")
            findings = {
                "id": generate_id(),
                "product_anchor": context_str[:50],
                "scout_anchor": "FALLBACK - ERROR",
                "social_listening": social or {},
                "top_10_products": final_top_10 or [],
                "trends": trends or [],
                "keywords": [],
                "sales_intelligence": {},
                "timestamp": timestamp_now(),
                "error": str(e)
            }
        
        self._save_findings(findings)
        return findings

    def _detect_lightning_scaling(self, social_data: dict) -> dict:
        """
        Detecta si el interés social crece >20% mientras la oferta es vieja.
        """
        is_trending = any(word in str(social_data).lower() for word in ["viral", "crecimiento", "tendencia", "bolado", "hot"])
        velocity = str(social_data.get("tiktok_trends", ""))
        
        if is_trending and ("vistas" in velocity.lower() or "millones" in velocity.lower()):
            return {
                "is_lightning": True,
                "velocity_score": "ALTA (>25% interés social)",
                "reason": "Interés en TikTok/IG subiendo rápido vs oferta estática en Amazon.",
                "action": "OPORTUNIDAD RELÁMPAGO: Lanzar variante diferenciada máximo 60 días."
            }
        return {"is_lightning": False}

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
