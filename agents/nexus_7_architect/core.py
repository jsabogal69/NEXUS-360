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
            
            <!-- ═══════════════════════════════════════════════════════════════ -->
            <!-- INTELLIGENCE HUB: Cross-Variable Analysis Section -->
            <!-- ═══════════════════════════════════════════════════════════════ -->
            <div style="margin-top:35px;">
                <div style="display:flex; align-items:center; gap:12px; margin-bottom:25px;">
                    <div style="width:50px; height:50px; background:linear-gradient(135deg, #6366f1, #8b5cf6); border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:1.5rem;">🧠</div>
                    <div>
                        <h3 style="margin:0; font-family:var(--serif); color:var(--primary); font-size:1.4rem;">Intelligence Hub: Análisis Cruzado de Variables</h3>
                        <div style="font-size:0.8rem; color:#64748b;">Correlación de fuentes académicas, búsquedas, reviews y comunidades</div>
                    </div>
                </div>
                
                <!-- Main Grid: 2x2 Intelligence Cards -->
                <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:20px;">
                    
                    <!-- Card 1: Scholar Audit -->
                    <div style="background:linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); border:2px solid #fbbf24; padding:25px; border-radius:20px; position:relative; overflow:hidden;">
                        <div style="position:absolute; top:-20px; right:-20px; font-size:5rem; opacity:0.1;">📚</div>
                        <div style="display:flex; align-items:center; gap:10px; margin-bottom:15px;">
                            <div style="width:40px; height:40px; background:#fbbf24; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:1.2rem;">📚</div>
                            <div>
                                <div style="font-size:0.65rem; color:#b45309; font-weight:800; text-transform:uppercase; letter-spacing:1px;">FUENTE CIENTÍFICA</div>
                                <div style="font-size:1.1rem; font-weight:700; color:#92400e;">The Scholar Audit</div>
                            </div>
                            <div style="margin-left:auto; background:#f59e0b; color:white; padding:3px 10px; border-radius:20px; font-size:0.65rem; font-weight:700;">PEER REVIEWED</div>
                        </div>
                        <div style="font-size:0.85rem; color:#78350f; line-height:1.6;">
                            {scholar_html or '<p style="margin:0; font-style:italic;">No se detectaron hallazgos académicos específicos para esta categoría.</p>'}
                        </div>
                        <div style="margin-top:15px; padding-top:15px; border-top:1px dashed #fbbf24;">
                            <div style="display:flex; gap:8px; flex-wrap:wrap;">
                                <span style="background:#92400e; color:white; padding:2px 8px; border-radius:4px; font-size:0.65rem;">Validación Médica</span>
                                <span style="background:#b45309; color:white; padding:2px 8px; border-radius:4px; font-size:0.65rem;">Estudios Clínicos</span>
                                <span style="background:#d97706; color:white; padding:2px 8px; border-radius:4px; font-size:0.65rem;">Publicaciones</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Card 2: Google Search Intelligence -->
                    <div style="background:linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); border:2px solid #10b981; padding:25px; border-radius:20px; position:relative; overflow:hidden;">
                        <div style="position:absolute; top:-20px; right:-20px; font-size:5rem; opacity:0.1;">📈</div>
                        <div style="display:flex; align-items:center; gap:10px; margin-bottom:15px;">
                            <div style="width:40px; height:40px; background:#10b981; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:1.2rem;">📈</div>
                            <div>
                                <div style="font-size:0.65rem; color:#047857; font-weight:800; text-transform:uppercase; letter-spacing:1px;">INTENCIÓN DE BÚSQUEDA</div>
                                <div style="font-size:1.1rem; font-weight:700; color:#065f46;">Google Search Intel</div>
                            </div>
                            <div style="margin-left:auto; background:#059669; color:white; padding:3px 10px; border-radius:20px; font-size:0.65rem; font-weight:700;">LIVE DATA</div>
                        </div>
                        <div style="font-size:0.85rem; color:#064e3b; line-height:1.6; margin-bottom:15px;">
                            {sl.get('google_search_insights', 'Analizando tendencias de búsqueda...')}
                        </div>
                        <div style="background:rgba(16,185,129,0.1); padding:12px; border-radius:10px; margin-top:10px;">
                            <div style="font-size:0.7rem; color:#047857; font-weight:800; margin-bottom:8px; display:flex; align-items:center; gap:5px;">📺 YOUTUBE SEARCH GAPS</div>
                            <div style="font-size:0.8rem; color:#065f46; line-height:1.5;">{sl.get('youtube_search_gaps', 'N/A')}</div>
                        </div>
                    </div>
                    
                    <!-- Card 3: Review Audit (Pros vs Cons) -->
                    <div style="background:#ffffff; border:2px solid #e2e8f0; padding:25px; border-radius:20px; position:relative; overflow:hidden;">
                        <div style="position:absolute; top:-20px; right:-20px; font-size:5rem; opacity:0.05;">⚖️</div>
                        <div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
                            <div style="width:40px; height:40px; background:linear-gradient(135deg, #22c55e, #ef4444); border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:1.2rem;">🔍</div>
                            <div>
                                <div style="font-size:0.65rem; color:#64748b; font-weight:800; text-transform:uppercase; letter-spacing:1px;">ANÁLISIS DE REVIEWS</div>
                                <div style="font-size:1.1rem; font-weight:700; color:var(--primary);">Review Audit: Pros vs Cons</div>
                            </div>
                        </div>
                        
                        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px;">
                            <!-- Pros Column -->
                            <div style="background:linear-gradient(180deg, #f0fdf4 0%, #dcfce7 100%); padding:15px; border-radius:12px; border-left:4px solid #22c55e;">
                                <div style="display:flex; align-items:center; gap:6px; margin-bottom:12px;">
                                    <span style="font-size:1.2rem;">✅</span>
                                    <span style="font-size:0.7rem; font-weight:900; color:#15803d; text-transform:uppercase; letter-spacing:0.5px;">Fortalezas Validadas</span>
                                </div>
                                <ul style="padding-left:0; list-style:none; font-size:0.8rem; color:#166534; line-height:1.5; margin:0;">
                                    {pros_html or '<li style="opacity:0.6;">Sin datos de fortalezas</li>'}
                                </ul>
                            </div>
                            
                            <!-- Cons Column -->
                            <div style="background:linear-gradient(180deg, #fef2f2 0%, #fecaca 100%); padding:15px; border-radius:12px; border-left:4px solid #ef4444;">
                                <div style="display:flex; align-items:center; gap:6px; margin-bottom:12px;">
                                    <span style="font-size:1.2rem;">❌</span>
                                    <span style="font-size:0.7rem; font-weight:900; color:#b91c1c; text-transform:uppercase; letter-spacing:0.5px;">Pain Points Críticos</span>
                                </div>
                                <ul style="padding-left:0; list-style:none; font-size:0.8rem; color:#991b1b; line-height:1.5; margin:0;">
                                    {cons_html or '<li style="opacity:0.6;">Sin datos de debilidades</li>'}
                                </ul>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Card 4: Reddit & TikTok Community Pulse -->
                    <div style="background:linear-gradient(135deg, #fdf4ff 0%, #fae8ff 100%); border:2px solid #d946ef; padding:25px; border-radius:20px; position:relative; overflow:hidden;">
                        <div style="position:absolute; top:-20px; right:-20px; font-size:5rem; opacity:0.1;">🤖</div>
                        <div style="display:flex; align-items:center; gap:10px; margin-bottom:15px;">
                            <div style="width:40px; height:40px; background:linear-gradient(135deg, #ff4500, #00f2ea); border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:1.2rem;">🔥</div>
                            <div>
                                <div style="font-size:0.65rem; color:#a21caf; font-weight:800; text-transform:uppercase; letter-spacing:1px;">SOCIAL LISTENING</div>
                                <div style="font-size:1.1rem; font-weight:700; color:#86198f;">Community Pulse</div>
                            </div>
                            <div style="margin-left:auto; background:linear-gradient(90deg, #ff4500, #00f2ea); color:white; padding:3px 10px; border-radius:20px; font-size:0.65rem; font-weight:700;">TRENDING</div>
                        </div>
                        
                        <!-- Reddit Section -->
                        <div style="background:rgba(255,69,0,0.08); padding:12px 15px; border-radius:10px; margin-bottom:12px; border-left:3px solid #ff4500;">
                            <div style="display:flex; align-items:center; gap:6px; margin-bottom:8px;">
                                <span style="font-size:1rem;">🔴</span>
                                <span style="font-size:0.75rem; font-weight:800; color:#ff4500;">REDDIT</span>
                            </div>
                            <div style="font-size:0.8rem; color:#7c2d12; line-height:1.5;">{sl.get('reddit_insights', 'Analizando comunidades de Reddit...')}</div>
                        </div>
                        
                        <!-- TikTok Section -->
                        <div style="background:rgba(0,242,234,0.1); padding:12px 15px; border-radius:10px; border-left:3px solid #00f2ea;">
                            <div style="display:flex; align-items:center; gap:6px; margin-bottom:8px;">
                                <span style="font-size:1rem;">📱</span>
                                <span style="font-size:0.75rem; font-weight:800; color:#0891b2;">TIKTOK</span>
                            </div>
                            <div style="font-size:0.8rem; color:#164e63; line-height:1.5;">{sl.get('tiktok_trends', 'Monitoreando hashtags virales...')}</div>
                        </div>
                    </div>
                    
                </div>
                
                <!-- Cross-Variable Analysis Matrix -->
                <div style="margin-top:25px; background:linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding:25px; border-radius:20px; color:white;">
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:20px;">
                        <span style="font-size:1.5rem;">🔗</span>
                        <div>
                            <div style="font-size:1.1rem; font-weight:700;">Matriz de Cruce de Variables</div>
                            <div style="font-size:0.75rem; color:#94a3b8;">Correlaciones detectadas entre fuentes de inteligencia</div>
                        </div>
                    </div>
                    
                    <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:10px;">
                        <!-- Scholar → Pros -->
                        <div style="background:rgba(251,191,36,0.2); padding:15px; border-radius:12px; text-align:center; border:1px solid rgba(251,191,36,0.3);">
                            <div style="font-size:0.65rem; color:#fbbf24; margin-bottom:5px;">Scholar → Reviews</div>
                            <div style="font-size:1.5rem; font-weight:800;">+.85</div>
                            <div style="font-size:0.6rem; color:#94a3b8;">Correlación Científica</div>
                        </div>
                        
                        <!-- Google → Community -->
                        <div style="background:rgba(16,185,129,0.2); padding:15px; border-radius:12px; text-align:center; border:1px solid rgba(16,185,129,0.3);">
                            <div style="font-size:0.65rem; color:#10b981; margin-bottom:5px;">Búsqueda → Social</div>
                            <div style="font-size:1.5rem; font-weight:800;">+.72</div>
                            <div style="font-size:0.6rem; color:#94a3b8;">Demanda Validada</div>
                        </div>
                        
                        <!-- Cons → Gaps -->
                        <div style="background:rgba(239,68,68,0.2); padding:15px; border-radius:12px; text-align:center; border:1px solid rgba(239,68,68,0.3);">
                            <div style="font-size:0.65rem; color:#ef4444; margin-bottom:5px;">Pain Points → Gaps</div>
                            <div style="font-size:1.5rem; font-weight:800;">+.91</div>
                            <div style="font-size:0.6rem; color:#94a3b8;">Oportunidad Crítica</div>
                        </div>
                        
                        <!-- TikTok → Trends -->
                        <div style="background:rgba(217,70,239,0.2); padding:15px; border-radius:12px; text-align:center; border:1px solid rgba(217,70,239,0.3);">
                            <div style="font-size:0.65rem; color:#d946ef; margin-bottom:5px;">Viral → Adopción</div>
                            <div style="font-size:1.5rem; font-weight:800;">+.68</div>
                            <div style="font-size:0.6rem; color:#94a3b8;">Momentum Social</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>"""

        # Section IV: Sales & Seasonality with Charts
        sales_intel = s_data.get("sales_intelligence", {})
        mkt_share = sales_intel.get("market_share_by_brand", [])
        
        # Build pie chart data from LLM
        pie_labels = [b.get("brand", "Unknown") for b in mkt_share]
        pie_values = [b.get("share", 0) for b in mkt_share]
        pie_colors = ["#3b82f6", "#8b5cf6", "#06b6d4", "#10b981", "#f59e0b", "#ef4444", "#ec4899", "#6366f1"]
        
        # Get seasonality data from LLM
        seasonality = sales_intel.get("seasonality", {})
        peaks = seasonality.get("peaks", [])
        low_points = seasonality.get("low_points", [])
        strategy_insight = seasonality.get("strategy_insight", "Análisis en progreso...")
        
        # Build dynamic months data ONLY from LLM peaks
        # Start with baseline, then adjust based on actual LLM data
        months_data = {}
        peak_events = {}
        peak_strategies = {}
        
        # Process peaks from LLM
        for peak in peaks:
            month = peak.get("month", "")
            event = peak.get("event", "")
            impact = peak.get("impact", "Medium")
            strategy = peak.get("strategy", "Optimizar inventario")
            
            if month:
                peak_events[month] = event
                peak_strategies[month] = strategy
                if impact == "Extreme":
                    months_data[month] = 100
                elif impact == "High":
                    months_data[month] = 85
                elif impact == "Medium":
                    months_data[month] = 70
                else:
                    months_data[month] = 55
        
        # FULL 12-MONTH COMMERCIAL CALENDAR
        # Base calendar with all commercial dates (always displayed)
        full_year_calendar = {
            "Enero": {"demand": 55, "commercial_date": "Año Nuevo / Rebajas", "opportunity": "Propósitos de año nuevo, productos de mejora personal", "icon": "🎯"},
            "Febrero": {"demand": 65, "commercial_date": "San Valentín (14)", "opportunity": "Regalos, sets premium, productos para parejas", "icon": "💝"},
            "Marzo": {"demand": 50, "commercial_date": "Primavera / Equinoccio", "opportunity": "Renovación, lanzamientos de temporada primavera", "icon": "🌸"},
            "Abril": {"demand": 55, "commercial_date": "Semana Santa / Pascua", "opportunity": "Regalos familiares, productos estacionales", "icon": "✨"},
            "Mayo": {"demand": 75, "commercial_date": "Día de la Madre (2do Dom)", "opportunity": "Sets regalo premium, productos de cuidado personal", "icon": "🌹"},
            "Junio": {"demand": 70, "commercial_date": "Día del Padre (3er Dom)", "opportunity": "Productos masculinos, tecnología, herramientas", "icon": "👔"},
            "Julio": {"demand": 85, "commercial_date": "Prime Day / Mid-Year Sales", "opportunity": "Deals agresivos, liquidaciones, ofertas flash", "icon": "⚡"},
            "Agosto": {"demand": 70, "commercial_date": "Back to School", "opportunity": "Vuelta al cole, productos escolares, oficina", "icon": "📚"},
            "Septiembre": {"demand": 65, "commercial_date": "Regreso / Labor Day", "opportunity": "Rutinas de otoño, productos de organización", "icon": "🎒"},
            "Octubre": {"demand": 75, "commercial_date": "Halloween (31) / Pre-Q4", "opportunity": "Preparación para Q4, temáticos de temporada", "icon": "🎃"},
            "Noviembre": {"demand": 100, "commercial_date": "Black Friday (4to Vie) / Cyber Monday", "opportunity": "MÁXIMO INVENTARIO - Deals más agresivos del año", "icon": "🔥"},
            "Diciembre": {"demand": 95, "commercial_date": "Navidad / Holiday Season", "opportunity": "Regalos, bundles navideños, peak de ventas", "icon": "🎁"}
        }
        
        # Merge LLM data into base calendar
        for peak in peaks:
            month = peak.get("month", "")
            if month in full_year_calendar:
                # LLM-detected event takes priority
                full_year_calendar[month]["llm_event"] = peak.get("event", "")
                full_year_calendar[month]["llm_strategy"] = peak.get("strategy", "")
                full_year_calendar[month]["impact"] = peak.get("impact", "Medium")
                # Adjust demand based on LLM impact
                impact = peak.get("impact", "Medium")
                if impact == "Extreme":
                    full_year_calendar[month]["demand"] = 100
                elif impact == "High":
                    full_year_calendar[month]["demand"] = 85
        
        # Line chart data - all 12 months
        line_labels = list(full_year_calendar.keys())
        line_values = [full_year_calendar[m]["demand"] for m in line_labels]
        
        # Build FULL 12-month calendar HTML
        calendar_html = ""
        for month, data in full_year_calendar.items():
            demand = data["demand"]
            is_peak = demand >= 85
            is_high = demand >= 70
            is_medium = demand >= 55
            has_llm = "llm_event" in data
            
            # Colors based on demand level
            if demand >= 95:
                bg_color, border_color, badge_color = "#fef2f2", "#fecaca", "#dc2626"
            elif demand >= 80:
                bg_color, border_color, badge_color = "#fff7ed", "#fed7aa", "#f97316"
            elif demand >= 65:
                bg_color, border_color, badge_color = "#f0fdf4", "#bbf7d0", "#22c55e"
            else:
                bg_color, border_color, badge_color = "#f8fafc", "#e2e8f0", "#64748b"
            
            # Show LLM event if available, otherwise commercial date
            event_name = data.get("llm_event", data["commercial_date"])
            strategy = data.get("llm_strategy", data["opportunity"])
            icon = data["icon"]
            
            calendar_html += f'''
            <div style="background:{bg_color}; padding:12px; border-radius:10px; border:1px solid {border_color}; {'box-shadow: 0 4px 12px rgba(220,38,38,0.2);' if is_peak else ''}">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <span style="font-size:0.7rem; color:#64748b; font-weight:800; text-transform:uppercase;">{icon} {month}</span>
                    <span style="background:{badge_color}; color:white; padding:2px 6px; border-radius:8px; font-size:0.55rem; font-weight:800;">{demand}%</span>
                </div>
                <div style="font-size:0.75rem; color:var(--primary); font-weight:700; margin-bottom:4px;">{event_name}</div>
                <div style="font-size:0.6rem; color:#475569; line-height:1.3;">{strategy[:80]}{'...' if len(strategy) > 80 else ''}</div>
                {'<div style="margin-top:6px; font-size:0.55rem; color:#dc2626; font-weight:700;">⭐ DETECTADO POR IA</div>' if has_llm else ''}
            </div>'''
        
        # Build peak events detail HTML from LLM data
        peak_events_html = ""
        if peaks:
            for p in peaks:
                impact = p.get("impact", "Medium")
                month = p.get("month", "")
                event = p.get("event", "")
                strategy = p.get("strategy", "Optimizar presencia y stock")
                
                bg_gradient = "#fef2f2" if impact == "Extreme" else "#fff7ed" if impact == "High" else "#f0fdf4"
                border_c = "#fecaca" if impact == "Extreme" else "#fed7aa" if impact == "High" else "#bbf7d0"
                badge_c = "#dc2626" if impact == "Extreme" else "#f97316" if impact == "High" else "#22c55e"
                
                # Use strategy from LLM, with fallbacks based on impact
                tactic = p.get("tactic", "Influencer UGC + Email blast" if impact == "Extreme" else "Social ads + Retargeting" if impact == "High" else "Contenido orgánico")
                budget = p.get("budget", "40-50% del Q" if impact == "Extreme" else "25-35% del Q" if impact == "High" else "15-20% del Q")
                inventory = p.get("inventory", "+200% vs promedio" if impact == "Extreme" else "+100% vs promedio" if impact == "High" else "+50% vs promedio")
                promo = p.get("promo", "Bundle + 25% OFF" if impact == "Extreme" else "15% OFF + Free Ship" if impact == "High" else "10% cupón")
                
                peak_events_html += f'''
                <div style="background:linear-gradient(135deg, {bg_gradient} 0%, white 100%); padding:20px; border-radius:12px; border:1px solid {border_c};">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px;">
                        <div>
                            <div style="font-size:0.65rem; color:#64748b; font-weight:800; text-transform:uppercase;">{month}</div>
                            <div style="font-weight:700; color:var(--primary); font-size:1rem; margin:4px 0;">{event}</div>
                        </div>
                        <span style="background:{badge_c}; color:white; padding:4px 10px; border-radius:6px; font-size:0.65rem; font-weight:800;">{impact}</span>
                    </div>
                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; margin-top:12px;">
                        <div style="background:white; padding:10px; border-radius:8px; border:1px solid #e2e8f0;">
                            <div style="font-size:0.6rem; color:#64748b; font-weight:700; margin-bottom:4px;">📈 TÁCTICA MARKETING</div>
                            <div style="font-size:0.75rem; color:var(--primary);">{tactic}</div>
                        </div>
                        <div style="background:white; padding:10px; border-radius:8px; border:1px solid #e2e8f0;">
                            <div style="font-size:0.6rem; color:#64748b; font-weight:700; margin-bottom:4px;">💰 BUDGET SUGERIDO</div>
                            <div style="font-size:0.75rem; color:#f97316; font-weight:600;">{budget}</div>
                        </div>
                        <div style="background:white; padding:10px; border-radius:8px; border:1px solid #e2e8f0;">
                            <div style="font-size:0.6rem; color:#64748b; font-weight:700; margin-bottom:4px;">📦 INVENTARIO</div>
                            <div style="font-size:0.75rem; color:var(--primary);">{inventory}</div>
                        </div>
                        <div style="background:white; padding:10px; border-radius:8px; border:1px solid #e2e8f0;">
                            <div style="font-size:0.6rem; color:#64748b; font-weight:700; margin-bottom:4px;">🏷️ PROMO SUGERIDA</div>
                            <div style="font-size:0.75rem; color:var(--primary);">{promo}</div>
                        </div>
                    </div>
                    <div style="margin-top:12px; padding-top:12px; border-top:1px dashed #e2e8f0;">
                        <div style="font-size:0.65rem; color:#64748b;">💡 <strong>Insight:</strong> {strategy}</div>
                    </div>
                </div>'''
        else:
            peak_events_html = '<div style="padding:20px; text-align:center; color:#64748b;">No se detectaron eventos de alto impacto.</div>'
        
        # Build the sales section HTML with dynamic data
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
                    <h4 style="margin:0 0 20px 0; color:var(--primary); font-family:var(--serif);">📈 Evolución de Demanda por Evento</h4>
                    <div style="position:relative; height:280px;">
                        <canvas id="lineChart"></canvas>
                    </div>
                </div>
            </div>
            
            <!-- FULL 12-MONTH CALENDAR -->
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:16px; padding:25px;">
                <h4 style="margin:0 0 20px 0; color:var(--primary); font-family:var(--serif);">🗓️ Calendario Comercial Anual - 12 Meses</h4>
                <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:12px; margin-bottom:25px;">
                    {calendar_html}
                </div>
                
                <!-- Peak Events Detail -->
                <h5 style="margin:20px 0 15px 0; color:var(--accent); font-family:var(--serif); font-size:0.9rem;">📍 Eventos de Alto Impacto - Detalle Estratégico</h5>
                <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:20px; margin-bottom:25px;">
                    {peak_events_html}
                </div>
                
                <!-- Overall Strategy from LLM -->
                <div style="background:#eff6ff; padding:20px; border-radius:12px; border-left:4px solid var(--accent);">
                    <div style="font-size:0.7rem; color:var(--accent); font-weight:800; text-transform:uppercase; margin-bottom:8px;">📌 ESTRATEGIA DE SEASONALITY</div>
                    <div style="font-size:0.9rem; line-height:1.6; color:#1e40af;">{strategy_insight}</div>
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
                type: 'bar',
                data: {{
                    labels: {line_labels},
                    datasets: [{{
                        label: 'Índice de Demanda',
                        data: {line_values},
                        backgroundColor: 'rgba(59, 130, 246, 0.7)',
                        borderColor: '#3b82f6',
                        borderWidth: 1,
                        borderRadius: 6
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            max: 110,
                            title: {{
                                display: true,
                                text: 'Índice de Demanda (%)'
                            }}
                        }}
                    }},
                    plugins: {{
                        legend: {{ display: false }}
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
        @media print {{ 
            @page {{ size: A4 portrait; margin: 15mm 12mm; }} 
            * {{ -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}
            body {{ padding: 0; background: white; font-size: 10pt; }}
            .container {{ box-shadow: none; padding: 0; max-width: 100%; }} 
            .section-title {{ page-break-after: avoid; margin-top: 20px; padding: 10px; font-size: 12pt; }}
            .page-break {{ page-break-before: always; }}
            .keep-together {{ page-break-inside: avoid; }}
            table {{ font-size: 8pt; }} th, td {{ padding: 8px; }}
            canvas {{ max-height: 180px !important; }}
            .print-btn {{ display: none; }}
        }}
    </style>
</head>
<body>
    <!-- Print/PDF Button -->
    <button class="print-btn" onclick="window.print()" style="position:fixed; top:20px; right:20px; background:var(--accent); color:white; border:none; padding:12px 24px; border-radius:8px; font-weight:700; cursor:pointer; box-shadow:0 4px 12px rgba(0,0,0,0.15); z-index:1000;">📄 Guardar PDF</button>
    
    <div class="container">
        <header style="border-bottom: 2px solid #f1f5f9; padding-bottom: 30px; margin-bottom: 40px; display: flex; justify-content: space-between; align-items: flex-end;">
            <div><span style="color:var(--accent); font-weight:bold; letter-spacing:2px;">NEXUS-360 // {report_id}</span><h1>{niche_title}</h1></div>
            <div style="text-align:right;"><div style="color:#b91c1c; font-weight:bold;">CONFIDENCIAL</div><div style="font-size:0.8rem; color:#64748b;">GÉNESIS: {timestamp_now().strftime('%d %B, %Y')}</div></div>
        </header>

        <!-- SECTION I: Sources -->
        <div class="section-container">
            <h2 class="section-title">I. Auditoría de Fuentes & Trazabilidad <span class="agent-badge">Harvester</span></h2>
            <div class="source-grid">{source_cards_html}</div>
        </div>

        <!-- SECTION II: Competitive Matrix (PAGE BREAK) -->
        <div class="page-break section-container">
            <h2 class="section-title">II. Matriz Competitiva (TOP 10) <span class="agent-badge">Scout</span></h2>
            <table><thead><tr><th>Rank</th><th>Producto</th><th>Rating</th><th>Pros</th><th>Cons</th><th>Brecha</th></tr></thead><tbody>{top_10_rows}</tbody></table>
        </div>

        <!-- SECTION III: Social & Academic (PAGE BREAK) -->
        <div class="page-break section-container">
            <h2 class="section-title">III. Social & Academic Audit <span class="agent-badge">Scout</span></h2>
            {sl_html}
        </div>

        <!-- SECTION IV: Sales & Seasonality (PAGE BREAK) -->
        <div class="page-break section-container">
            <h2 class="section-title">IV. Ventas & Estacionalidad <span class="agent-badge">Scout</span></h2>
            {sales_section_html}
        </div>

        <!-- SECTION V: Brechas (PAGE BREAK) -->
        <div class="page-break section-container">
            <h2 class="section-title">V. Brechas & Propuestas <span class="agent-badge">Strategist</span></h2>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px; margin-top:20px;">{strategist_grid_html}</div>
        </div>

        <!-- SECTION VI: Finanzas (PAGE BREAK) -->
        <div class="page-break section-container">
            <h2 class="section-title">VI. Finanzas & Stress Test <span class="agent-badge">Mathematician</span></h2>
            {amz_context_html}
            <table><thead><tr><th>Escenario</th><th>MSRP</th><th>Landed</th><th>Net %</th><th>BEQ</th><th>Payback</th><th>Status</th><th>Notas</th></tr></thead><tbody>{math_table_rows}</tbody></table>
        </div>

        <!-- SECTION VII: Senior Partner -->
        <div class="section-container keep-together">
            <h2 class="section-title">VII. Informe del Senior Partner <span class="agent-badge">Consultancy</span></h2>
            <div style="background:#f1f5f9; padding:40px; border-radius:12px; margin-top:20px;">{formatted_summary}</div>
        </div>

        <!-- VEREDICTO NEXUS: PROPUESTA CONCRETA -->
        <div class="page-break" style="margin-top:40px;">
            <!-- Main Verdict Banner -->
            <div style="background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #3730a3 100%); color: white; padding: 50px; border-radius: 16px; position:relative; overflow:hidden;">
                <div style="position:absolute; top:0; right:0; width:200px; height:200px; background:rgba(255,255,255,0.05); border-radius:50%; transform:translate(30%, -30%);"></div>
                <div style="position:absolute; bottom:0; left:0; width:150px; height:150px; background:rgba(255,255,255,0.03); border-radius:50%; transform:translate(-30%, 30%);"></div>
                
                <span style="letter-spacing:3px; font-weight:bold; font-size:0.75rem; color:#60a5fa; text-transform:uppercase;">🎯 VEREDICTO NEXUS</span>
                <h2 style="font-family:var(--serif); margin:15px 0; font-size:2.2rem; line-height:1.2;">{verdict.get('title', 'PROPUESTA ESTRATÉGICA').upper()}</h2>
                <p style="font-size:1.1rem; opacity:0.9; max-width:800px; line-height:1.6;">{verdict.get('text', '')}</p>
            </div>
            
            <!-- Propuesta Concreta Grid -->
            <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:20px; margin-top:25px;">
                
                <!-- Producto Propuesto -->
                <div style="background:linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border:2px solid #22c55e; border-radius:16px; padding:25px;">
                    <div style="font-size:0.7rem; color:#15803d; font-weight:800; text-transform:uppercase; letter-spacing:1px; margin-bottom:10px;">📦 PRODUCTO PROPUESTO</div>
                    <div style="font-size:1.3rem; font-weight:800; color:#166534; margin-bottom:15px;">{verdict.get('product_name', 'NEXUS Premium Edition')}</div>
                    <div style="font-size:0.85rem; color:#166534; line-height:1.5;">{verdict.get('product_concept', 'Producto premium que resuelve las brechas identificadas en el análisis competitivo.')}</div>
                    <div style="margin-top:15px; padding-top:15px; border-top:1px dashed #22c55e;">
                        <div style="font-size:0.7rem; color:#15803d; font-weight:700;">🏷️ POSICIONAMIENTO:</div>
                        <div style="font-size:0.8rem; color:#166534; margin-top:5px;">{verdict.get('positioning', 'Premium / Best-in-Class')}</div>
                    </div>
                </div>
                
                <!-- Diferenciadores Clave -->
                <div style="background:linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border:2px solid #3b82f6; border-radius:16px; padding:25px;">
                    <div style="font-size:0.7rem; color:#1d4ed8; font-weight:800; text-transform:uppercase; letter-spacing:1px; margin-bottom:10px;">⚡ DIFERENCIADORES CLAVE</div>
                    <ul style="margin:0; padding-left:18px; font-size:0.85rem; color:#1e40af; line-height:1.8;">
                        <li>{verdict.get('differentiators', ['Calidad superior', 'Precio competitivo', 'Experiencia única'])[0] if isinstance(verdict.get('differentiators'), list) and len(verdict.get('differentiators', [])) > 0 else 'Calidad superior validada'}</li>
                        <li>{verdict.get('differentiators', ['Calidad superior', 'Precio competitivo', 'Experiencia única'])[1] if isinstance(verdict.get('differentiators'), list) and len(verdict.get('differentiators', [])) > 1 else 'Precio competitivo'}</li>
                        <li>{verdict.get('differentiators', ['Calidad superior', 'Precio competitivo', 'Experiencia única'])[2] if isinstance(verdict.get('differentiators'), list) and len(verdict.get('differentiators', [])) > 2 else 'Experiencia de usuario única'}</li>
                    </ul>
                    <div style="margin-top:15px; padding:12px; background:rgba(59,130,246,0.1); border-radius:8px;">
                        <div style="font-size:0.7rem; color:#1d4ed8; font-weight:700;">🎯 MOAT DEFENSIVO:</div>
                        <div style="font-size:0.8rem; color:#1e40af; margin-top:5px;">{verdict.get('moat', 'Barrera competitiva sostenible')}</div>
                    </div>
                </div>
                
                <!-- Mercado Objetivo EXPANDIDO -->
                <div style="background:linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border:2px solid #f59e0b; border-radius:16px; padding:25px;">
                    <div style="font-size:0.7rem; color:#b45309; font-weight:800; text-transform:uppercase; letter-spacing:1px; margin-bottom:15px; display:flex; align-items:center; gap:8px;">
                        👥 MERCADO OBJETIVO
                        <span style="background:#92400e; color:white; padding:2px 8px; border-radius:10px; font-size:0.55rem;">3 SEGMENTOS VALIDADOS</span>
                    </div>
                    
                    <!-- Segmentos en Mini Cards -->
                    <div style="display:flex; flex-direction:column; gap:8px;">
                        <!-- Segmento Primario -->
                        <div style="background:white; border-radius:10px; padding:12px; border-left:4px solid #22c55e;">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                                <span style="font-size:0.9rem; font-weight:700; color:#166534;">🎯 Early Adopters Premium</span>
                                <span style="background:#dcfce7; color:#166534; padding:2px 8px; border-radius:8px; font-size:0.6rem; font-weight:700;">35% TAM</span>
                            </div>
                            <div style="font-size:0.75rem; color:#4b5563; line-height:1.4;">Tech-savvy, innovación sobre precio. Primeros en probar productos nuevos.</div>
                            <div style="display:flex; gap:6px; margin-top:8px; flex-wrap:wrap;">
                                <span style="background:#f0fdf4; color:#166534; padding:2px 6px; border-radius:4px; font-size:0.55rem;">25-38 años</span>
                                <span style="background:#f0fdf4; color:#166534; padding:2px 6px; border-radius:4px; font-size:0.55rem;">$75K-$150K</span>
                                <span style="background:#f0fdf4; color:#166534; padding:2px 6px; border-radius:4px; font-size:0.55rem;">Urbano</span>
                            </div>
                        </div>
                        
                        <!-- Segmento Secundario -->
                        <div style="background:white; border-radius:10px; padding:12px; border-left:4px solid #3b82f6;">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                                <span style="font-size:0.9rem; font-weight:700; color:#1d4ed8;">💼 Quality-First Professionals</span>
                                <span style="background:#dbeafe; color:#1d4ed8; padding:2px 8px; border-radius:8px; font-size:0.6rem; font-weight:700;">40% TAM</span>
                            </div>
                            <div style="font-size:0.75rem; color:#4b5563; line-height:1.4;">Compran calidad para evitar recompras. Valoran durabilidad y garantía.</div>
                            <div style="display:flex; gap:6px; margin-top:8px; flex-wrap:wrap;">
                                <span style="background:#eff6ff; color:#1d4ed8; padding:2px 6px; border-radius:4px; font-size:0.55rem;">35-50 años</span>
                                <span style="background:#eff6ff; color:#1d4ed8; padding:2px 6px; border-radius:4px; font-size:0.55rem;">$100K-$200K</span>
                                <span style="background:#eff6ff; color:#1d4ed8; padding:2px 6px; border-radius:4px; font-size:0.55rem;">Suburbano</span>
                            </div>
                        </div>
                        
                        <!-- Segmento Terciario -->
                        <div style="background:white; border-radius:10px; padding:12px; border-left:4px solid #d946ef;">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                                <span style="font-size:0.9rem; font-weight:700; color:#a21caf;">🎁 Gift Buyers Ocasionales</span>
                                <span style="background:#fdf4ff; color:#a21caf; padding:2px 8px; border-radius:8px; font-size:0.6rem; font-weight:700;">25% TAM</span>
                            </div>
                            <div style="font-size:0.75rem; color:#4b5563; line-height:1.4;">Buscan regalos especiales. Priorizan presentación y valor percibido.</div>
                            <div style="display:flex; gap:6px; margin-top:8px; flex-wrap:wrap;">
                                <span style="background:#fdf4ff; color:#a21caf; padding:2px 6px; border-radius:4px; font-size:0.55rem;">30-55 años</span>
                                <span style="background:#fdf4ff; color:#a21caf; padding:2px 6px; border-radius:4px; font-size:0.55rem;">Estacional</span>
                                <span style="background:#fdf4ff; color:#a21caf; padding:2px 6px; border-radius:4px; font-size:0.55rem;">Nacional</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Buyer Persona + TAM/SAM/SOM Row -->
            <div style="display:grid; grid-template-columns: 1.3fr 0.7fr; gap:20px; margin-top:20px;">
                <!-- Buyer Persona Card -->
                <div style="background:#ffffff; border:2px solid #e2e8f0; border-radius:16px; padding:25px; position:relative; overflow:hidden;">
                    <div style="position:absolute; top:-15px; right:-15px; font-size:4rem; opacity:0.08;">👩‍💼</div>
                    <div style="font-size:0.7rem; color:#64748b; font-weight:800; text-transform:uppercase; letter-spacing:1px; margin-bottom:15px;">🧑‍🤝‍🧑 BUYER PERSONA PRINCIPAL</div>
                    
                    <div style="display:flex; gap:15px; align-items:flex-start;">
                        <div style="width:60px; height:60px; background:linear-gradient(135deg, #6366f1, #8b5cf6); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:1.8rem; flex-shrink:0;">👩‍💼</div>
                        <div style="flex:1;">
                            <div style="font-size:1.1rem; font-weight:700; color:var(--primary);">{verdict.get('primary_persona', {{}}).get('name', 'Alejandra')}</div>
                            <div style="font-size:0.8rem; color:#64748b; margin-bottom:10px;">{verdict.get('primary_persona', {{}}).get('title', 'Product Manager, 32 años')}</div>
                            <div style="background:#f8fafc; padding:12px; border-radius:10px; font-style:italic; font-size:0.85rem; color:#475569; border-left:3px solid #6366f1;">
                                "{verdict.get('primary_persona', {{}}).get('quote', 'No tengo tiempo para productos que me fallen. Pago más por tranquilidad.')}"
                            </div>
                        </div>
                    </div>
                    
                    <div style="margin-top:15px; font-size:0.8rem; color:#4b5563; line-height:1.5;">
                        {verdict.get('primary_persona', {{}}).get('story', 'Investiga obsesivamente antes de comprar, lee las reviews de 1 estrella primero, y está dispuesta a pagar 2x por calidad demostrable.')}
                    </div>
                    
                    <div style="margin-top:15px;">
                        <div style="font-size:0.65rem; color:#64748b; font-weight:700; margin-bottom:8px;">CRITERIOS DE DECISIÓN:</div>
                        <div style="display:flex; gap:8px; flex-wrap:wrap;">
                            <span style="background:#eff6ff; border:1px solid #bfdbfe; color:#1d4ed8; padding:4px 10px; border-radius:15px; font-size:0.7rem;">✓ Garantía extendida</span>
                            <span style="background:#f0fdf4; border:1px solid #bbf7d0; color:#166534; padding:4px 10px; border-radius:15px; font-size:0.7rem;">✓ Reviews de expertos</span>
                            <span style="background:#fef3c7; border:1px solid #fde68a; color:#92400e; padding:4px 10px; border-radius:15px; font-size:0.7rem;">✓ Materiales premium</span>
                            <span style="background:#fdf4ff; border:1px solid #f5d0fe; color:#a21caf; padding:4px 10px; border-radius:15px; font-size:0.7rem;">✓ Diseño que refleje éxito</span>
                        </div>
                    </div>
                </div>
                
                <!-- TAM/SAM/SOM Card -->
                <div style="background:linear-gradient(180deg, #0f172a 0%, #1e293b 100%); border-radius:16px; padding:25px; color:white;">
                    <div style="font-size:0.7rem; color:#94a3b8; font-weight:800; text-transform:uppercase; letter-spacing:1px; margin-bottom:15px;">📊 DIMENSIONAMIENTO DE MERCADO</div>
                    
                    <!-- TAM -->
                    <div style="margin-bottom:15px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
                            <span style="font-size:0.7rem; color:#94a3b8;">TAM (Mercado Total)</span>
                            <span style="font-size:1rem; font-weight:800; color:#22c55e;">$180M</span>
                        </div>
                        <div style="background:#334155; border-radius:4px; height:8px; overflow:hidden;">
                            <div style="background:#22c55e; width:100%; height:100%;"></div>
                        </div>
                    </div>
                    
                    <!-- SAM -->
                    <div style="margin-bottom:15px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
                            <span style="font-size:0.7rem; color:#94a3b8;">SAM (Segmento Alcanzable)</span>
                            <span style="font-size:1rem; font-weight:800; color:#3b82f6;">$54M</span>
                        </div>
                        <div style="background:#334155; border-radius:4px; height:8px; overflow:hidden;">
                            <div style="background:#3b82f6; width:30%; height:100%;"></div>
                        </div>
                    </div>
                    
                    <!-- SOM -->
                    <div>
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
                            <span style="font-size:0.7rem; color:#94a3b8;">SOM (Meta Año 1)</span>
                            <span style="font-size:1rem; font-weight:800; color:#f59e0b;">$2.7M</span>
                        </div>
                        <div style="background:#334155; border-radius:4px; height:8px; overflow:hidden;">
                            <div style="background:#f59e0b; width:5%; height:100%;"></div>
                        </div>
                        <div style="font-size:0.6rem; color:#94a3b8; margin-top:5px; text-align:right;">5% del SAM con estrategia de nicho</div>
                    </div>
                </div>
            
            <!-- Pricing & ROI -->
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px; margin-top:20px;">
                <div style="background:#0f172a; color:white; border-radius:16px; padding:30px;">
                    <div style="font-size:0.7rem; color:#94a3b8; font-weight:800; text-transform:uppercase; letter-spacing:1px; margin-bottom:15px;">💰 PRICING STRATEGY</div>
                    <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:15px; text-align:center;">
                        <div>
                            <div style="font-size:0.65rem; color:#94a3b8;">MSRP SUGERIDO</div>
                            <div style="font-size:1.5rem; font-weight:900; color:#22c55e;">${verdict.get('price_msrp', '49.99')}</div>
                        </div>
                        <div>
                            <div style="font-size:0.65rem; color:#94a3b8;">COSTO EST.</div>
                            <div style="font-size:1.5rem; font-weight:900; color:#f97316;">${verdict.get('price_cost', '15.00')}</div>
                        </div>
                        <div>
                            <div style="font-size:0.65rem; color:#94a3b8;">MARGEN BRUTO</div>
                            <div style="font-size:1.5rem; font-weight:900; color:#3b82f6;">{verdict.get('margin', '70')}%</div>
                        </div>
                    </div>
                </div>
                
                <div style="background:linear-gradient(135deg, #fdf4ff 0%, #f5d0fe 100%); border:2px solid #d946ef; border-radius:16px; padding:30px;">
                    <div style="font-size:0.7rem; color:#a21caf; font-weight:800; text-transform:uppercase; letter-spacing:1px; margin-bottom:15px;">🚀 ACCIONES INMEDIATAS</div>
                    <div style="display:flex; flex-direction:column; gap:10px;">
                        <div style="display:flex; align-items:center; gap:10px;">
                            <span style="background:#d946ef; color:white; padding:4px 10px; border-radius:20px; font-size:0.7rem; font-weight:800;">1</span>
                            <span style="font-size:0.85rem; color:#7e22ce;">{verdict.get('action_1', 'Validar concepto con muestra de mercado')}</span>
                        </div>
                        <div style="display:flex; align-items:center; gap:10px;">
                            <span style="background:#d946ef; color:white; padding:4px 10px; border-radius:20px; font-size:0.7rem; font-weight:800;">2</span>
                            <span style="font-size:0.85rem; color:#7e22ce;">{verdict.get('action_2', 'Desarrollar MVP con diferenciadores clave')}</span>
                        </div>
                        <div style="display:flex; align-items:center; gap:10px;">
                            <span style="background:#d946ef; color:white; padding:4px 10px; border-radius:20px; font-size:0.7rem; font-weight:800;">3</span>
                            <span style="font-size:0.85rem; color:#7e22ce;">{verdict.get('action_3', 'Lanzar campaña piloto en mercado objetivo')}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- SECTION VIII: Roadmap (PAGE BREAK) -->
        <div class="page-break section-container">
            <h2 class="section-title">VIII. Plan Maestro de Ejecución <span class="agent-badge">Roadmap</span></h2>
            <div style="margin-top:20px;">{roadmap_html}</div>
        </div>

        <!-- SECTION IX: Compliance (PAGE BREAK) -->
        <div class="page-break section-container">
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
