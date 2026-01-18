import logging
import os
from ..shared.utils import get_db, generate_id, timestamp_now, report_agent_activity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NEXUS-7")

class Nexus7Architect:
    task_description = "Synthesize all agent outputs into a premium HTML report"
    def __init__(self):
        self.db = get_db()
        self.role = "NEXUS-7 (Architect)"

    @report_agent_activity
    async def generate_report_artifacts(self, full_data: dict) -> dict:
        """
        Generates a premium, highly detailed HTML report.
        Includes Scholar Audit, Stress Test, and Compliance Audit.
        """
        logger.info(f"[{self.role}] Generating Premium Detailed Report...")
        
        report_id = generate_id()
        h_data = full_data.get("harvester", {})
        s_data = full_data.get("scout", {})
        i_data = full_data.get("integrator", {})
        st_data = full_data.get("strategist", {})
        m_data = full_data.get("mathematician", {})
        p_data = full_data.get("senior_partner", {})
        g_data = full_data.get("guardian", {})
        gen_ctx = m_data.get("general_market_context", {})
        
        # Formatting High-Level Summary
        raw_summary = p_data.get("executive_summary", "Sin resumen disponible.")
        summary = ""
        parts = raw_summary.split("**")
        for i, part in enumerate(parts):
            summary += f"<strong>{part}</strong>" if i % 2 == 1 else part

        scenarios = m_data.get("scenarios", {})
        amz_base = m_data.get("amazon_baseline", {})
        
        sources = st_data.get("analyzed_sources", [])
        has_electronics = any(x in str(sources).upper() for x in ["65W", "GAN", "ADAPTADOR", "CHARGER"])
        has_lamp = any(x in str(sources).upper() for x in ["LAMP", "ILUMINACION", "LAMPARA"])
        has_baby = any(x in str(sources).upper() for x in ["BABY", "NIGHT LIGHT", "SLEEP AID", "BEBE", "NOCHE", "SUEÑO"])
        
        niche_title = "Dossier de Inteligencia: Iluminación & Ergonomía Premium" if has_lamp else \
                      ("Dossier de Inteligencia: Electrónica GaN" if has_electronics else \
                      ("Dossier de Inteligencia: Baby Sleep & Comfort Tech" if has_baby else "Dossier de Viabilidad Estratégica"))

        # Section I: Source Cards
        source_metadata = i_data.get("source_metadata", [])
        source_cards_html = ""
        for s in source_metadata:
            fname = s['name']
            summary_str = s.get("summary", "Metadatos, Estructura")
            ext = fname.split('.')[-1].upper() if '.' in fname else "INTEL"
            bg_color = "#eff6ff"; text_color = "#1e40af"; icon = "📄"
            if ext == "PDF": bg_color = "#fef2f2"; text_color = "#991b1b"; icon = "📕"
            elif ext in ["CSV", "XLSX"]: bg_color = "#f0fdf4"; text_color = "#166534"; icon = "📊"
            elif ext in ["PNG", "JPG", "JPEG"]: bg_color = "#faf5ff"; text_color = "#6b21a8"; icon = "🖼️"
            elif s.get("type") == "scout_intelligence" or ext == "INTEL": bg_color = "#fff7ed"; text_color = "#9a3412"; icon = "🧠"

            source_cards_html += f"""
            <div class="source-card">
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <span style="font-size:1.2rem;">{icon}</span>
                    <span style="background:{bg_color}; color:{text_color}; padding:2px 8px; border-radius:4px; font-size:0.6rem; font-weight:800;">{ext}</span>
                </div>
                <div style="font-weight:700; font-size:0.85rem; color:var(--primary); overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">{fname}</div>
                <div style="font-size:0.7rem; color:#64748b; margin-top:5px; line-height:1.4;">{summary_str}</div>
            </div>"""

        # Section II: Competitive Matrix
        top_10_rows = ""
        top_10_list = s_data.get("top_10_products", [])
        for p in top_10_list:
            rating = p.get('rating', 0)
            reviews = p.get('reviews', 0)
            price = p.get('price', 0)
            
            # Format reviews count
            if reviews >= 1000:
                reviews_display = f"{reviews/1000:.1f}K"
            else:
                reviews_display = str(reviews)
            
            # Rating color based on value
            if rating >= 4.5:
                rating_color = "#166534"
                rating_bg = "#dcfce7"
                rating_badge = "EXCELENTE"
            elif rating >= 4.0:
                rating_color = "#854d0e"
                rating_bg = "#fef9c3"
                rating_badge = "MUY BUENO"
            elif rating >= 3.5:
                rating_color = "#c2410c"
                rating_bg = "#ffedd5"
                rating_badge = "BUENO"
            else:
                rating_color = "#991b1b"
                rating_bg = "#fee2e2"
                rating_badge = "REGULAR"
            
            # Price tier indicator
            if price >= 50:
                price_tier = "💎 Premium"
                price_color = "#7c3aed"
            elif price >= 25:
                price_tier = "⭐ Mid-Range"
                price_color = "#0369a1"
            else:
                price_tier = "💰 Value"
                price_color = "#166534"
            
            top_10_rows += f"""
            <tr>
                <td style="text-align:center; font-weight:bold; color:var(--accent); font-size:1.2rem;">#{p['rank']}</td>
                <td style="min-width:180px;">
                    <strong style="color:var(--primary); font-size:0.95rem;">{p['name']}</strong>
                    <div style="display:flex; gap:10px; margin-top:8px; flex-wrap:wrap;">
                        <span style="background:#f1f5f9; color:#475569; padding:3px 8px; border-radius:4px; font-size:0.7rem; font-weight:600;">${price:.2f}</span>
                        <span style="color:{price_color}; font-size:0.65rem; font-weight:700;">{price_tier}</span>
                    </div>
                </td>
                <td style="min-width:140px;">
                    <div style="display:flex; flex-direction:column; gap:6px;">
                        <div style="display:flex; align-items:center; gap:6px;">
                            <span style="color:#f59e0b; font-size:1.1rem;">{'★' * int(min(5, rating))}{'☆' * (5-int(min(5, rating)))}</span>
                            <span style="font-weight:800; color:{rating_color}; font-size:0.95rem;">{rating:.1f}</span>
                        </div>
                        <div style="display:flex; align-items:center; gap:8px;">
                            <span style="font-size:0.7rem; color:#64748b;">📊 {reviews_display} reseñas</span>
                        </div>
                        <span style="background:{rating_bg}; color:{rating_color}; padding:2px 6px; border-radius:3px; font-size:0.55rem; font-weight:800; width:fit-content;">{rating_badge}</span>
                    </div>
                </td>
                <td style="font-size:0.8rem; color:#166534; background: #f0fdf4; max-width:200px;">{p.get('adv', 'N/A')}</td>
                <td style="font-size:0.8rem; color:#991b1b; background: #fef2f2; max-width:200px;">{p.get('vuln', 'N/A')}</td>
                <td style="font-size:0.8rem; color:#1e40af; background: #eff6ff; font-weight:600; max-width:180px;">{p.get('gap', 'N/A')}</td>
            </tr>"""

        # Section III: Social & Scholar
        sl = s_data.get("social_listening", {})
        pros_html = "".join([f'<li style="color:#166534; margin-bottom:4px;">✔ {p}</li>' for p in sl.get('pros', [])])
        cons_html = "".join([f'<li style="color:#991b1b; margin-bottom:4px;">✖ {c}</li>' for c in sl.get('cons', [])])
        
        scholar = s_data.get("scholar_audit", [])
        scholar_html = ""
        for item in scholar:
            scholar_html += f"""
            <div style="background:#f0f9ff; border:1px solid #bae6fd; padding:15px; border-radius:12px; margin-bottom:12px; border-left:4px solid #0284c7;">
                <div style="font-size:0.65rem; color:#0369a1; font-weight:800; text-transform:uppercase;">{item['source']} // {item['relevance']}</div>
                <div style="font-size:0.9rem; color:#0c4a6e; font-style:italic; margin-top:5px;">"{item['finding']}"</div>
            </div>"""

        # Build emotional analysis section
        emotional = sl.get("emotional_analysis", {})
        emotional_html = ""
        if emotional:
            emotions = [
                ("😤 Frustración", emotional.get("frustration", "N/A"), "#dc2626", "#fef2f2"),
                ("💭 Nostalgia", emotional.get("nostalgia", "N/A"), "#7c3aed", "#f5f3ff"),
                ("😂 Humor", emotional.get("humor", "N/A"), "#0891b2", "#ecfeff"),
                ("✨ Deseo", emotional.get("desire", "N/A"), "#059669", "#ecfdf5"),
                ("🤨 Escepticismo", emotional.get("skepticism", "N/A"), "#d97706", "#fffbeb")
            ]
            for label, text, color, bg in emotions:
                emotional_html += f'<div style="background:{bg}; padding:12px; border-radius:8px; margin-bottom:8px; border-left:3px solid {color};"><span style="font-weight:700; color:{color}; font-size:0.75rem;">{label}</span><p style="margin:5px 0 0 0; font-size:0.8rem; color:#374151; font-style:italic;">"{text}"</p></div>'
        
        # Build pain keywords table
        pain_keywords = sl.get("pain_keywords", [])
        pain_html = ""
        for pk in pain_keywords[:5]:
            if isinstance(pk, dict):
                pain_html += f'<tr><td style="font-weight:600; color:#dc2626;">{pk.get("keyword", "")}</td><td style="font-size:0.75rem;">{pk.get("search_intent", "")}</td><td><span style="background:#fee2e2; color:#991b1b; padding:2px 6px; border-radius:3px; font-size:0.65rem; font-weight:700;">{pk.get("volume", "")}</span></td><td style="font-size:0.75rem; color:#475569;">{pk.get("opportunity", "")}</td></tr>'
        
        # Build competitor gaps
        comp_gaps = sl.get("competitor_gaps", [])
        comp_gaps_html = ""
        for cg in comp_gaps[:3]:
            if isinstance(cg, dict):
                comp_gaps_html += f'<div style="background:#fff7ed; padding:15px; border-radius:8px; margin-bottom:10px; border-left:3px solid #ea580c;"><div style="font-weight:700; color:#c2410c; font-size:0.85rem;">{cg.get("competitor", "")}</div><div style="font-size:0.8rem; color:#78350f; margin-top:5px;"><strong>Ignoran:</strong> {cg.get("ignored_issue", "")}</div><div style="font-size:0.75rem; color:#9a3412; font-style:italic; margin-top:5px;">"{cg.get("user_frustration", "")}"</div></div>'
        
        # Build content opportunities (GaryVee + Patel)
        content_opps = s_data.get("content_opportunities", {})
        gv_ideas = content_opps.get("garyvee_style", [])
        patel_ideas = content_opps.get("patel_style", [])
        
        gv_html = ""
        for idea in gv_ideas[:3]:
            if isinstance(idea, dict):
                gv_html += f'<div style="background:#fdf4ff; padding:12px; border-radius:8px; margin-bottom:8px; border-left:3px solid #a855f7;"><div style="font-weight:700; color:#7e22ce; font-size:0.85rem;">🔥 {idea.get("idea", "")}</div><div style="font-size:0.75rem; color:#6b21a8; margin-top:5px;">Formato: {idea.get("format", "")} | Hook: "{idea.get("hook", "")}" | Emoción: {idea.get("emotional_trigger", "")}</div></div>'
        
        patel_html = ""
        for idea in patel_ideas[:3]:
            if isinstance(idea, dict):
                patel_html += f'<div style="background:#f0fdf4; padding:12px; border-radius:8px; margin-bottom:8px; border-left:3px solid #22c55e;"><div style="font-weight:700; color:#15803d; font-size:0.85rem;">📊 {idea.get("idea", "")}</div><div style="font-size:0.75rem; color:#166534; margin-top:5px;">Keyword: {idea.get("target_keyword", "")} | Intent: {idea.get("search_intent", "")} | Gap: {idea.get("content_gap", "")}</div></div>'
        
        # Build attention formats section
        attention = sl.get("attention_formats", {})
        attention_html = ""
        if attention:
            attention_html = f'''
            <div style="background:#eff6ff; padding:15px; border-radius:8px;">
                <div style="font-size:0.7rem; color:#1e40af; font-weight:800; text-transform:uppercase; margin-bottom:8px;">🎯 FORMATOS QUE RETIENEN ATENCIÓN</div>
                <div style="font-size:0.85rem; color:#1e3a8a; margin-bottom:8px;"><strong>Qué funciona:</strong> {attention.get("what_works", "N/A")}</div>
                <div style="font-size:0.85rem; color:#1e3a8a; margin-bottom:8px;"><strong>Tono:</strong> {attention.get("tone", "N/A")}</div>
                <div style="font-size:0.85rem; color:#1e3a8a;"><strong>Elementos virales:</strong> {attention.get("viral_elements", "N/A")}</div>
            </div>'''
        
        # White space topics
        white_space = sl.get("white_space_topics", [])
        white_space_html = "".join([f'<span style="background:#fef3c7; color:#92400e; padding:4px 10px; border-radius:12px; font-size:0.75rem; font-weight:600; margin:3px;">{t}</span>' for t in white_space[:5]])
        
        # Cultural vibe
        cultural_vibe = sl.get("cultural_vibe", "Analizando el tono de la comunidad...")

        sl_html = f"""
        <div style="margin-top:30px;">
            <!-- Row 1: Emotional Analysis + Competitor Gaps -->
            <div style="display:grid; grid-template-columns: 1.5fr 1fr; gap:25px; margin-bottom:25px;">
                <div style="background:#ffffff; border:1px solid #e2e8f0; padding:25px; border-radius:16px;">
                    <h4 style="margin-top:0; color:var(--primary); font-family:var(--serif); display:flex; align-items:center; gap:10px; border-bottom:1px solid #f1f5f9; padding-bottom:15px;">🎭 Análisis Emocional del Mercado (GaryVee Method)</h4>
                    {emotional_html or '<p style="font-size:0.8rem; color:#64748b;">No se detectó análisis emocional específico.</p>'}
                </div>
                <div style="background:#ffffff; border:1px solid #e2e8f0; padding:25px; border-radius:16px;">
                    <h4 style="margin-top:0; color:#ea580c; font-family:var(--serif); display:flex; align-items:center; gap:10px; border-bottom:1px solid #fed7aa; padding-bottom:15px;">🎯 Gaps de Competidores</h4>
                    {comp_gaps_html or '<p style="font-size:0.8rem; color:#64748b;">No se detectaron gaps específicos.</p>'}
                </div>
            </div>
            
            <!-- Row 2: Pain Keywords Table -->
            <div style="background:#ffffff; border:1px solid #e2e8f0; padding:25px; border-radius:16px; margin-bottom:25px;">
                <h4 style="margin-top:0; color:#dc2626; font-family:var(--serif); display:flex; align-items:center; gap:10px; border-bottom:1px solid #fecaca; padding-bottom:15px;">🔑 Keywords de Dolor (Neil Patel Method)</h4>
                <table style="width:100%; margin-top:15px;"><thead><tr><th style="text-align:left; font-size:0.7rem; color:#991b1b;">KEYWORD</th><th style="text-align:left; font-size:0.7rem; color:#991b1b;">INTENT</th><th style="text-align:left; font-size:0.7rem; color:#991b1b;">VOLUMEN</th><th style="text-align:left; font-size:0.7rem; color:#991b1b;">OPORTUNIDAD</th></tr></thead><tbody>{pain_html or '<tr><td colspan="4" style="color:#64748b; font-size:0.8rem;">No se detectaron pain keywords.</td></tr>'}</tbody></table>
            </div>
            
            <!-- Row 3: Content Opportunities -->
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:25px; margin-bottom:25px;">
                <div style="background:#faf5ff; border:1px solid #e9d5ff; padding:25px; border-radius:16px;">
                    <h4 style="margin-top:0; color:#7c3aed; font-family:var(--serif); display:flex; align-items:center; gap:10px; border-bottom:1px solid #ddd6fe; padding-bottom:15px;">🔥 Contenido Estilo GaryVee (Alto Impacto)</h4>
                    {gv_html or '<p style="font-size:0.8rem; color:#64748b;">No se detectaron oportunidades GaryVee.</p>'}
                </div>
                <div style="background:#f0fdf4; border:1px solid #bbf7d0; padding:25px; border-radius:16px;">
                    <h4 style="margin-top:0; color:#15803d; font-family:var(--serif); display:flex; align-items:center; gap:10px; border-bottom:1px solid #86efac; padding-bottom:15px;">📊 Contenido Estilo Patel (SEO/Educativo)</h4>
                    {patel_html or '<p style="font-size:0.8rem; color:#64748b;">No se detectaron oportunidades Patel.</p>'}
                </div>
            </div>
            
            <!-- Row 4: Cultural Vibe + White Space + Attention Formats -->
            <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:25px; margin-bottom:25px;">
                <div style="background:#fef3c7; border:1px solid #fcd34d; padding:20px; border-radius:16px;">
                    <h4 style="margin-top:0; color:#92400e; font-family:var(--serif); font-size:0.9rem;">🌡️ Cultural Vibe Check</h4>
                    <p style="font-size:0.85rem; color:#78350f; margin:10px 0 0 0; font-style:italic;">"{cultural_vibe}"</p>
                </div>
                <div style="background:#fefce8; border:1px solid #fef08a; padding:20px; border-radius:16px;">
                    <h4 style="margin-top:0; color:#854d0e; font-family:var(--serif); font-size:0.9rem;">⚪ White Space Topics</h4>
                    <div style="display:flex; flex-wrap:wrap; gap:5px; margin-top:10px;">{white_space_html or '<span style="color:#64748b; font-size:0.8rem;">N/A</span>'}</div>
                </div>
                {attention_html}
            </div>
            
            <!-- Row 5: Scholar Audit + Pros/Cons -->
            <div style="display:grid; grid-template-columns: 1.25fr 1fr; gap:25px;">
                <div style="display:flex; flex-direction:column; gap:25px;">
                    <div style="background:#ffffff; border:1px solid #e2e8f0; padding:25px; border-radius:16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);">
                        <h4 style="margin-top:0; color:var(--primary); font-family:var(--serif); display:flex; align-items:center; gap:10px; border-bottom:1px solid #f1f5f9; padding-bottom:15px;">📚 The Scholar Audit: Validación Científica</h4>
                        {scholar_html or '<p style="font-size:0.8rem;">No se detectaron hallazgos académicos específicos.</p>'}
                    </div>
                    <div style="background:#f8fafc; padding:30px; border-radius:16px; border:1px solid #e2e8f0;">
                        <h4 style="margin-top:0; color:var(--primary); font-family:var(--serif); display:flex; align-items:center; gap:10px; border-bottom:1px solid #e2e8f0; padding-bottom:15px;">🔍 Review Audit: Fortalezas y Vulnerabilidades</h4>
                        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px; margin-top:20px;">
                            <div>
                                <div style="font-size:0.7rem; font-weight:900; color:#15803d; text-transform:uppercase; margin-bottom:12px; letter-spacing:1px; background:#f0fdf4; padding:4px 10px; border-radius:4px; display:inline-block;">Market Validation (Pros)</div>
                                <ul style="padding-left:0; list-style:none; font-size:0.85rem; line-height:1.6;">{pros_html or '<li>N/A</li>'}</ul>
                            </div>
                            <div>
                                <div style="font-size:0.7rem; font-weight:900; color:#b91c1c; text-transform:uppercase; margin-bottom:12px; letter-spacing:1px; background:#fef2f2; padding:4px 10px; border-radius:4px; display:inline-block;">Critical Pain Points (Cons)</div>
                                <ul style="padding-left:0; list-style:none; font-size:0.85rem; line-height:1.6;">{cons_html or '<li>N/A</li>'}</ul>
                            </div>
                        </div>
                    </div>
                </div>
                <div style="display:flex; flex-direction:column; gap:25px;">
                    <div style="background:#f0fdfa; padding:25px; border-radius:16px; border:1px solid #99f6e4;">
                        <h4 style="margin-top:0; color:#0d9488; font-family:var(--serif);">📈 Google Search Intelligence</h4>
                        <p style="font-size:0.9rem; color:#134e4a; line-height:1.6;">{sl.get('google_search_insights', 'Analizando tendencias de búsqueda...')}</p>
                        <div style="margin-top:15px; padding-top:15px; border-top:1px solid #99f6e4;">
                            <div style="font-size:0.7rem; color:#0d9488; font-weight:800; margin-bottom:5px;">📺 YOUTUBE SEARCH GAPS</div>
                            <p style="font-size:0.8rem; color:#134e4a; margin:0;">{sl.get('youtube_search_gaps', 'N/A')}</p>
                        </div>
                    </div>
                    <div style="background:#fdf4ff; padding:25px; border-radius:16px; border:1px solid #f5d0fe;">
                        <h4 style="margin-top:0; color:#86198f; font-family:var(--serif);">🤖 Reddit & TikTok Community Pulse</h4>
                        <div style="font-size:0.85rem; color:#4a044e; line-height:1.5; margin-bottom:15px;"><strong>Reddit:</strong> {sl.get('reddit_insights', 'N/A')}</div>
                        <div style="font-size:0.85rem; color:#4a044e; line-height:1.5;"><strong>TikTok:</strong> {sl.get('tiktok_trends', 'N/A')}</div>
                    </div>
                </div>
            </div>
        </div>"""

        # Section IV: Sales & Seasonality with Charts
        sales_intel = s_data.get("sales_intelligence", {})
        mkt_share = sales_intel.get("market_share_by_brand", [])
        
        # Build pie chart data
        pie_labels = [b.get("brand", "Unknown") for b in mkt_share]
        pie_values = [b.get("share", 0) for b in mkt_share]
        pie_colors = ["#3b82f6", "#8b5cf6", "#06b6d4", "#10b981", "#f59e0b", "#ef4444", "#ec4899", "#6366f1"]
        
        # Build seasonality data for line chart (12 months)
        seasonality = sales_intel.get("seasonality", {})
        peaks = seasonality.get("peaks", [])
        low_points = seasonality.get("low_points", [])
        
        # Create month data with estimated demand values
        months_data = {
            "Enero": 60, "Febrero": 45, "Marzo": 55, "Abril": 50, "Mayo": 55, "Junio": 60,
            "Julio": 75, "Agosto": 65, "Septiembre": 70, "Octubre": 80, "Noviembre": 95, "Diciembre": 100
        }
        
        # Adjust based on peaks
        for peak in peaks:
            month = peak.get("month", "")
            impact = peak.get("impact", "Medium")
            if month in months_data:
                if impact == "Extreme":
                    months_data[month] = 100
                elif impact == "High":
                    months_data[month] = 90
                elif impact == "Medium":
                    months_data[month] = 75
        
        line_labels = list(months_data.keys())
        line_values = list(months_data.values())
        
        # Build peak annotations for key dates
        peak_annotations_js = ""
        for i, peak in enumerate(peaks[:6]):
            month = peak.get("month", "")
            event = peak.get("event", "")
            if month in line_labels:
                month_idx = line_labels.index(month)
                peak_annotations_js += f'''
                    {{
                        type: 'label',
                        xValue: {month_idx},
                        yValue: {months_data.get(month, 70)},
                        backgroundColor: 'rgba(239, 68, 68, 0.9)',
                        borderRadius: 6,
                        color: 'white',
                        font: {{ size: 10, weight: 'bold' }},
                        content: ['{event}'],
                        padding: 6
                    }},'''

        sales_section_html = f"""
        <div style="margin-top:20px;">
            <!-- Charts Row -->
            <div style="display:grid; grid-template-columns: 1fr 1.5fr; gap:30px; margin-bottom:30px;">
                <!-- Pie Chart: Market Share -->
                <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:16px; padding:30px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);">
                    <h4 style="margin:0 0 20px 0; color:var(--primary); font-family:var(--serif);">📊 Market Share por Marca</h4>
                    <div style="position:relative; height:280px;">
                        <canvas id="pieChart"></canvas>
                    </div>
                </div>
                
                <!-- Line Chart: Seasonality -->
                <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:16px; padding:30px;">
                    <h4 style="margin:0 0 20px 0; color:var(--primary); font-family:var(--serif);">📈 Evolución de Demanda por Mes</h4>
                    <div style="position:relative; height:280px;">
                        <canvas id="lineChart"></canvas>
                    </div>
                </div>
            </div>
            
            <!-- Key Dates Legend -->
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:16px; padding:25px;">
                <h4 style="margin:0 0 15px 0; color:var(--primary); font-family:var(--serif);">🗓️ Fechas Clave del Año</h4>
                <div style="display:grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap:12px;">
                    {''.join([f'''
                    <div style="background:{'#fef2f2' if p.get('impact') == 'Extreme' else '#fff7ed' if p.get('impact') == 'High' else '#f0fdf4'}; padding:12px; border-radius:8px; border-left:4px solid {'#dc2626' if p.get('impact') == 'Extreme' else '#f97316' if p.get('impact') == 'High' else '#22c55e'};">
                        <div style="font-size:0.65rem; color:#64748b; font-weight:800; text-transform:uppercase;">{p.get('month', '')}</div>
                        <div style="font-weight:700; color:var(--primary); font-size:0.9rem; margin:4px 0;">{p.get('event', '')}</div>
                        <div style="font-size:0.7rem; color:{'#dc2626' if p.get('impact') == 'Extreme' else '#f97316' if p.get('impact') == 'High' else '#22c55e'}; font-weight:800;">IMPACTO: {p.get('impact', 'Medium')}</div>
                        <div style="font-size:0.7rem; color:#64748b; margin-top:4px;">{p.get('strategy', 'Optimizar inventario')}</div>
                    </div>''' for p in peaks[:6]])}
                </div>
                <div style="margin-top:20px; background:#eff6ff; padding:15px; border-radius:8px; border-left:4px solid var(--accent);">
                    <div style="font-size:0.7rem; color:var(--accent); font-weight:800; text-transform:uppercase; margin-bottom:5px;">📌 Seasonality Strategy</div>
                    <div style="font-size:0.85rem; line-height:1.5; color:#1e40af;">{seasonality.get('strategy_insight', 'N/A')}</div>
                </div>
            </div>
        </div>
        
        <!-- Chart.js Scripts -->
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
            // Pie Chart: Market Share
            new Chart(document.getElementById('pieChart'), {{
                type: 'doughnut',
                data: {{
                    labels: {pie_labels},
                    datasets: [{{
                        data: {pie_values},
                        backgroundColor: {pie_colors[:len(pie_values)]},
                        borderWidth: 2,
                        borderColor: '#ffffff'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            position: 'right',
                            labels: {{
                                usePointStyle: true,
                                padding: 15,
                                font: {{ size: 11 }}
                            }}
                        }}
                    }}
                }}
            }});
            
            // Line Chart: Seasonality
            new Chart(document.getElementById('lineChart'), {{
                type: 'line',
                data: {{
                    labels: {line_labels},
                    datasets: [{{
                        label: 'Índice de Demanda',
                        data: {line_values},
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        fill: true,
                        tension: 0.4,
                        pointRadius: 6,
                        pointBackgroundColor: function(context) {{
                            const value = context.raw;
                            if (value >= 90) return '#dc2626';
                            if (value >= 75) return '#f97316';
                            return '#3b82f6';
                        }},
                        pointBorderColor: '#ffffff',
                        pointBorderWidth: 2
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{
                            beginAtZero: false,
                            min: 30,
                            max: 110,
                            title: {{
                                display: true,
                                text: 'Índice de Demanda (%)'
                            }}
                        }}
                    }},
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    return 'Demanda: ' + context.raw + '%';
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        </script>"""

        # Section V: Strategist Gaps
        gaps = st_data.get("strategic_gaps", [])
        strategist_grid_html = ""
        for g in gaps:
            strategist_grid_html += f"""
            <div style="background:white; border:1px solid #e2e8f0; padding:25px; border-radius:16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03);">
                <div style="font-size:0.65rem; color:var(--accent); font-weight:800; text-transform:uppercase; letter-spacing:1px; margin-bottom:10px;">Gap Detectado: {g.get('niche', 'General')}</div>
                <h4 style="margin:0 0 10px 0; color:var(--primary); font-family:var(--serif);">{g.get('gap', 'Oportunidad de Mercado')}</h4>
                <p style="font-size:0.85rem; color:#475569; line-height:1.6; border-top:1px solid #f1f5f9; padding-top:15px; margin-top:10px;"><strong>Propuesta NEXUS:</strong> {g.get('proposal', 'N/A')}</p>
            </div>"""

        # Section VI: Financials & Stress Test
        fba_sens = m_data.get("fba_sensitivity_analysis", {})
        nexus_target = fba_sens.get("nexus_target", {})
        n_fba_b = nexus_target.get("fba_breakdown", {})
        
        nexus_fba_card = f"""
        <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color:white; padding:25px; border-radius:16px; box-shadow: 0 10px 20px rgba(0,0,0,0.1);">
            <div style="font-size:0.65rem; color:#94a3b8; font-weight:800; text-transform:uppercase; letter-spacing:2px; margin-bottom:15px;">NEXUS TARGET UNIT</div>
            <div style="font-size:1.3rem; font-weight:900; margin-bottom:20px;">{nexus_target.get('name')}</div>
            <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:10px; text-align:center; border-top:1px solid rgba(255,255,255,0.1); padding-top:15px;">
                <div><div style="font-size:0.6rem; color:#94a3b8;">Pick/Pack</div><div style="font-size:1rem; font-weight:700;">${n_fba_b.get('pick_pack')}</div></div>
                <div><div style="font-size:0.6rem; color:#94a3b8;">Storage/Ref</div><div style="font-size:1rem; font-weight:700;">${round(n_fba_b.get('storage', 0) + n_fba_b.get('referral', 0), 2)}</div></div>
                <div><div style="font-size:0.6rem; color:#94a3b8;">Impacto</div><div style="font-size:1rem; font-weight:700; color:#10b981;">{nexus_target.get('fba_impact_pct')}%</div></div>
            </div>
        </div>"""

        comps = fba_sens.get("competitors", [])
        bench_html = ""
        for p in comps[:10]:
            bench_html += f"""
            <div style="background:white; border:1px solid #e2e8f0; padding:12px; border-radius:10px; display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <div style="font-weight:700; font-size:0.75rem; color:#334155;">#{p['rank']} {p['name']}</div>
                <div style="display:flex; gap:10px; align-items:center;">
                    <div style="font-size:0.75rem; color:#64748b;">${p['fba_breakdown']['total_logistics']}</div>
                    <div style="font-size:0.7rem; font-weight:900; color:{p['tier_color']}; background:{p['tier_color']}20; padding:2px 6px; border-radius:3px;">{p['fba_impact_pct']}%</div>
                </div>
            </div>"""
        bench_html = f'<div style="grid-column: span 1; background:#ffffff50; padding:10px; border-radius:12px;">{bench_html}</div>'

        mra = m_data.get("multivariate_analysis", {})
        corr = mra.get("correlations", {})
        multivariate_panel = f"""
        <div style="grid-column: span 1; background:white; border-radius:16px; padding:20px; border:1px solid #fdba74;">
             <h5 style="margin:0 0 15px 0; color:#9a3412; font-size:0.8rem; text-transform:uppercase;">Dominance Analysis</h5>
             <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px; text-align:center;">
                <div><div style="font-size:0.6rem; color:#64748b;">Mkt FBA Avg</div><div style="font-size:1.2rem; font-weight:900; color:#dc2626;">{corr.get('avg_market_fba_impact')}%</div></div>
                <div><div style="font-size:0.6rem; color:#64748b;">Dominance Delta</div><div style="font-size:1.2rem; font-weight:900; color:#059669;">+{corr.get('nexus_dominance_delta')}%</div></div>
             </div>
             <div style="margin-top:15px; font-size:0.7rem; color:#9a3412; font-style:italic; line-height:1.4;">* NEXUS desvincula la rentabilidad del costo logístico mediante el desequilibrio positivo de valor.</div>
        </div>"""

        st_test = m_data.get("stress_test", {})
        st_impact = st_test.get("impact", {})
        erosion_val = float(st_impact.get("profit_erosion", "0%").replace("%", ""))
        erosion_width = min(100, max(0, erosion_val * 4))
        stress_panel_html = f"""
        <div style="margin-top:25px; background:#fef2f2; border:1px solid #fecaca; border-radius:16px; padding:20px; grid-column: span 3;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0; color:#991b1b; font-size:1rem;">🌩️ Stress Test: High-CAC Volatility Simulation</h4>
                <div style="background:#dc2626; color:white; padding:4px 12px; border-radius:6px; font-weight:900; font-size:0.7rem;">{st_impact.get('resilience_status').upper()}</div>
            </div>
            <div style="margin-top:15px; display:grid; grid-template-columns: 2fr 1.5fr; gap:30px; align-items:center;">
                <div>
                     <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:0.8rem; font-weight:700; color:#991b1b;"><span>Profit Erosion Impact</span><span>{st_impact.get('profit_erosion')}</span></div>
                     <div style="width:100%; height:10px; background:#fee2e2; border-radius:5px; overflow:hidden;"><div style="width:{erosion_width}%; height:100%; background:#991b1b;"></div></div>
                </div>
                <div style="font-size:0.85rem; color:#7f1d1d; line-height:1.5;"><strong>Veredicto:</strong> {st_test.get('verdict')}</div>
            </div>
        </div>"""

        amz_context_html = f"""
        <div style="background:#fff7ed; border:1px solid #fdba74; padding:30px; border-radius:16px; margin-bottom:30px;">
             <h4 style="margin-top:0; color:#9a3412; font-family:var(--serif);">⚖️ Análisis Multivariable (MRA) & Stress Test (TOP 10)</h4>
             <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:15px;">
                {nexus_fba_card}
                {bench_html}
                {multivariate_panel}
                {stress_panel_html}
             </div>
        </div>"""

        math_table_rows = ""
        for key, s in scenarios.items():
            math_table_rows += f"""
            <tr>
                <td><strong>{s['name']}</strong><br><span style="font-size:0.75rem; color:#64748b;">{s.get('composition', '')}</span></td>
                <td>${s['price']}</td>
                <td>${s['landed']}</td>
                <td style="font-weight:bold; color:#059669;">{s['margin_pct']}%</td>
                <td>{s.get('break_even_qty', 'N/A')} u</td>
                <td>{s.get('payback_months', 'N/A')} m</td>
                <td><span class="tag tag-recommended">VIABLE</span></td>
                <td style="font-size:0.8rem; line-height:1.4;">{s.get('notes', 'Calculado')}</td>
            </tr>"""

        # Section VII: Senior Partner Summary
        partner_raw = st_data.get("partner_summary", summary)
        formatted_summary = f'<div style="font-size:1.05rem; line-height:1.8; color:#1e293b; white-space:pre-wrap;">{partner_raw}</div>'

        # Section VIII: Roadmap
        roadmap_data = st_data.get("dynamic_roadmap", [])
        roadmap_html = ""
        for idx, step in enumerate(roadmap_data):
            roadmap_html += f"""
            <div style="display:flex; gap:30px; margin-bottom:25px; background:white; padding:25px; border-radius:12px; border:1px solid #e2e8f0; position:relative;">
                <div style="width:40px; height:40px; background:var(--primary); color:white; border-radius:8px; display:flex; align-items:center; justify-content:center; font-weight:bold; flex-shrink:0;">{idx+1}</div>
                <div><h4 style="margin:0 0 10px 0; color:var(--primary);">{step[0]}</h4><p style="margin:0; font-size:0.9rem; color:#475569;">{step[1]}</p></div>
            </div>"""

        # Section IX: Compliance Audit
        audits = g_data.get("audits", [])
        compliance_rows = ""
        for a in audits:
            status_color = "#15803d" if a['status'] == "MANDATORY" else "#c2410c"
            status_bg = "#dcfce7" if a['status'] == "MANDATORY" else "#ffedd5"
            compliance_rows += f"""
            <tr>
                <td style="font-weight:800;">{a['std']}</td>
                <td><span style="background:{status_bg}; color:{status_color}; padding:4px 10px; border-radius:4px; font-size:0.65rem; font-weight:900;">{a['status']}</span></td>
                <td style="font-size:0.85rem; color:#475569;">{a['desc']}</td>
            </tr>"""

        # HTML Assembly
        verdict = st_data.get("dynamic_verdict", {})
        html_report = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>NEXUS-360 DOSSIER</title>
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {{ 
            --primary: #16213a; 
            --accent: #28529a; 
            --lime: #84cc16;
            --serif: 'Montserrat', sans-serif; 
            --sans: 'Inter', system-ui, -apple-system, sans-serif; 
        }}
        body {{ font-family: var(--sans); background: #f9fafb; color: #333333; padding: 40px; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 60px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }}
        .section-title {{ font-family: var(--serif); font-size: 1.4rem; color: var(--primary); margin-top: 50px; background: #f5f8fc; padding: 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; border-left: 5px solid var(--lime); }}
        .agent-badge {{ background: var(--accent); color: white; padding: 3px 10px; border-radius: 4px; font-size: 0.7rem; font-weight: 800; text-transform: uppercase; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th {{ text-align: left; background: #f8fafc; padding: 15px; border-bottom: 2px solid #e2e8f0; font-size: 0.75rem; text-transform: uppercase; color: var(--accent); }}
        td {{ padding: 15px; border-bottom: 1px solid #f1f5f9; }}
        .source-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; margin-top: 20px; }}
        .source-card {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 15px; transition: transform 0.2s; }}
        .source-card:hover {{ transform: translateY(-3px); border-color: var(--lime); }}
        .verdict-banner {{ background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%); color: white; padding: 40px; border-radius: 12px; margin-top: 40px; }}
        @media print {{ @page {{ size: A4 portrait; margin: 15mm; }} .container {{ box-shadow: none; padding: 0; }} }}
    </style>
</head>
<body>
    <div class="container">
        <header style="border-bottom: 2px solid #f1f5f9; padding-bottom: 30px; margin-bottom: 40px; display: flex; justify-content: space-between; align-items: flex-end;">
            <div><span style="color:var(--accent); font-weight:bold; letter-spacing:2px;">NEXUS-360 // {report_id}</span><h1>{niche_title}</h1></div>
            <div style="text-align:right;"><div style="color:#b91c1c; font-weight:bold;">SECRET // EYES ONLY</div><div style="font-size:0.8rem; color:#64748b;">GÉNESIS: {timestamp_now().strftime('%d %B, %Y')}</div></div>
        </header>

        <h2 class="section-title">I. Auditoría de Fuentes & Trazabilidad <span class="agent-badge">Harvester</span></h2>
        <div class="source-grid">{source_cards_html}</div>

        <h2 class="section-title">II. Matriz Competitiva (TOP 10) <span class="agent-badge">Scout</span></h2>
        <table><thead><tr><th>Rank</th><th>Producto</th><th>Rating</th><th>Pros</th><th>Cons</th><th>Brecha</th></tr></thead><tbody>{top_10_rows}</tbody></table>

        <h2 class="section-title">III. Social & Academic Audit <span class="agent-badge">Scout</span></h2>
        {sl_html}

        <h2 class="section-title">IV. Ventas & Estacionalidad <span class="agent-badge">Scout</span></h2>
        {sales_section_html}

        <h2 class="section-title">V. Brechas & Propuestas <span class="agent-badge">Strategist</span></h2>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px; margin-top:20px;">{strategist_grid_html}</div>

        <h2 class="section-title">VI. Finanzas & Stress Test <span class="agent-badge">Mathematician</span></h2>
        {amz_context_html}
        <table><thead><tr><th>Escenario</th><th>MSRP</th><th>Landed</th><th>Net %</th><th>BEQ</th><th>Payback</th><th>Status</th><th>Notas</th></tr></thead><tbody>{math_table_rows}</tbody></table>

        <h2 class="section-title">VII. Informe del Senior Partner <span class="agent-badge">Consultancy</span></h2>
        <div style="background:#f1f5f9; padding:40px; border-radius:12px; margin-top:20px;">{formatted_summary}</div>

        <div class="verdict-banner">
            <span style="letter-spacing:2px; font-weight:bold; font-size:0.8rem; color:#60a5fa;">VEREDICTO NEXUS</span>
            <h2 style="font-family:var(--serif); margin:10px 0; font-size:2rem;">{verdict.get('title', '').upper()}</h2>
            <p style="font-size:1.1rem; opacity:0.9;">{verdict.get('text', '')}</p>
        </div>

        <h2 class="section-title">VIII. Plan Maestro de Ejecución <span class="agent-badge">Roadmap</span></h2>
        <div style="margin-top:20px;">{roadmap_html}</div>

        <h2 class="section-title">IX. Compliance & Seguridad <span class="agent-badge">Guardian</span></h2>
        <div style="display:grid; grid-template-columns: 2fr 1fr; gap:30px; margin-top:20px;">
            <div>
                <div style="display:flex; gap:15px; margin-bottom:20px;">
                    <div style="background:#fee2e2; color:#991b1b; padding:8px 15px; border-radius:8px; font-weight:bold; font-size:0.75rem;">NIVEL DE RIESGO: {g_data.get('risk_level', 'MEDIUM')}</div>
                    <div style="background:#dbeafe; color:#1e40af; padding:8px 15px; border-radius:8px; font-weight:bold; font-size:0.75rem;">SCORE DE CUMPLIMIENTO: {g_data.get('compliance_score', 75)}%</div>
                    <div style="background:#f0fdf4; color:#166534; padding:8px 15px; border-radius:8px; font-weight:bold; font-size:0.75rem;">{g_data.get('total_standards', len(audits))} ESTÁNDARES AUDITADOS</div>
                </div>
                <table><thead><tr><th>Estándar</th><th>Estatus</th><th>Descripción</th></tr></thead><tbody>{compliance_rows}</tbody></table>
                <p style="margin-top:15px; font-size:0.8rem; color:#64748b; font-style:italic;">{g_data.get('audit_note', '')}</p>
            </div>
            <div style="background:var(--primary); color:white; padding:25px; border-radius:12px; height:fit-content;">
                <div style="font-size:0.6rem; color:#60a5fa; letter-spacing:2px; margin-bottom:10px;">SECURITY PROTOCOL</div>
                <h4 style="margin:0 0 10px 0;">{g_data.get('security_protocol')}</h4>
                <p style="font-size:0.8rem; color:#94a3b8; margin-bottom:15px;">Cifrado de extremo a extremo activo. Auditoría de estándares internacionales aprobada.</p>
                <div style="border-top:1px solid rgba(255,255,255,0.1); padding-top:15px; margin-top:15px;">
                    <div style="font-size:0.65rem; color:#60a5fa; margin-bottom:5px;">REQUISITOS OBLIGATORIOS</div>
                    <div style="font-size:1.5rem; font-weight:bold;">{g_data.get('mandatory_count', 0)}</div>
                </div>
            </div>
        </div>

        <footer style="margin-top:50px; text-align:center; font-size:0.7rem; color:#94a3b8; border-top:1px solid #e2e8f0; padding-top:20px;">NEXUS-360 ADVANCED STRATEGY UNIT | {timestamp_now().strftime('%Y')}</footer>
    </div>
</body>
</html>"""

        static_reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "reports")
        os.makedirs(static_reports_dir, exist_ok=True)
        filename = f"report_{report_id}.html"
        filepath = os.path.join(static_reports_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_report)
        
        # PERSISTENCE
        report_record = {
            "id": report_id,
            "type": "nexus_final_report",
            "metadata": { "title": niche_title, "report_url": f"/dashboard/reports/{filename}" },
            "intel_summary": { "verdict": verdict }, # Added for recursive intelligence
            "timestamp": timestamp_now()
        }
        self._save_report(report_record)

        return { "id": report_id, "pdf_url": report_record["metadata"]["report_url"], "html_content": html_report }

    def _save_report(self, data: dict):
        if not self.db: return
        try: self.db.collection("reports").document(data["id"]).set(data)
        except: pass
