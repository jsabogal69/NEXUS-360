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
            top_10_rows += f"""
            <tr>
                <td style="text-align:center; font-weight:bold; color:var(--accent);">#{p['rank']}</td>
                <td><strong>{p['name']}</strong><br><span style="color:#64748b; font-size:0.75rem;">MSRP: ${p.get('price', 'N/A')}</span></td>
                <td><span style="color:#f59e0b">{'★' * int(min(5, p.get('rating', 0)))}{'☆' * (5-int(min(5, p.get('rating', 0))))}</span></td>
                <td style="font-size:0.8rem; color:#166534; background: #f0fdf4;">{p.get('adv', 'N/A')}</td>
                <td style="font-size:0.8rem; color:#991b1b; background: #fef2f2;">{p.get('vuln', 'N/A')}</td>
                <td style="font-size:0.8rem; color:#1e40af; background: #eff6ff; font-weight:600;">{p.get('gap', 'N/A')}</td>
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

        sl_html = f"""
        <div style="display:grid; grid-template-columns: 1.25fr 1fr; gap:25px; margin-top:30px;">
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
                </div>
                <div style="background:#fdf4ff; padding:25px; border-radius:16px; border:1px solid #f5d0fe;">
                    <h4 style="margin-top:0; color:#86198f; font-family:var(--serif);">🤖 Reddit & TikTok Community Pulse</h4>
                    <div style="font-size:0.85rem; color:#4a044e; line-height:1.5;">{sl.get('reddit_insights', 'N/A')}</div>
                </div>
            </div>
        </div>"""

        # Section IV: Sales & Seasonality
        sales_intel = s_data.get("sales_intelligence", {})
        mkt_share = sales_intel.get("market_share_by_brand", [])
        mkt_share_html = "".join([f'<div style="margin-bottom:12px;"><div style="display:flex; justify-content:space-between; font-size:0.8rem; margin-bottom:4px;"><span>{b["brand"]}</span><span style="font-weight:bold;">{b["share"]}%</span></div><div style="width:100%; height:8px; background:#e2e8f0; border-radius:4px; overflow:hidden;"><div style="width:{b["share"]}%; height:100%; background:var(--accent);"></div></div></div>' for b in mkt_share])

        peaks = sales_intel.get("seasonality", {}).get("peaks", [])
        peaks_html = "".join([f'<div style="background:#ffffff; padding:12px; border-radius:8px; border:1px solid #e2e8f0; text-align:center;"><div style="font-size:0.65rem; color:#64748b; font-weight:800; text-transform:uppercase;">{p["month"]}</div><div style="font-weight:700; color:var(--primary); font-size:0.9rem; margin:4px 0;">{p["event"]}</div><div style="font-size:0.7rem; color:var(--accent); font-weight:800;">IMPACT: {p["impact"]}</div></div>' for p in peaks])

        sales_section_html = f"""
        <div style="display:grid; grid-template-columns: 1fr 1.5fr; gap:30px; margin-top:20px;">
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:16px; padding:30px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);">
                <h4 style="margin:0 0 20px 0; color:var(--primary); font-family:var(--serif);">Market Share Distribution</h4>
                {mkt_share_html}
            </div>
            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:16px; padding:30px;">
                <h4 style="margin:0 0 20px 0; color:var(--primary); font-family:var(--serif);">Calendario Estratégico de Ventas</h4>
                <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:12px;">{peaks_html}</div>
                <div style="margin-top:20px; background:#eff6ff; padding:15px; border-radius:8px; border-left:4px solid var(--accent);">
                    <div style="font-size:0.7rem; color:var(--accent); font-weight:800; text-transform:uppercase; margin-bottom:5px;">Seasonality Strategy</div>
                    <div style="font-size:0.85rem; line-height:1.5; color:#1e40af;">{sales_intel.get('seasonality', {}).get('strategy_insight', 'N/A')}</div>
                </div>
            </div>
        </div>"""

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
                <td>${s['msrp']}</td>
                <td>${s['landed_cost']}</td>
                <td style="font-weight:bold; color:#059669;">{s['net_margin_pct']}%</td>
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
        :root {{ --primary: #0f172a; --accent: #2563eb; --serif: 'Merriweather', serif; --sans: 'Inter', sans-serif; }}
        body {{ font-family: var(--sans); background: #f8fafc; color: #334155; padding: 40px; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 60px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }}
        .section-title {{ font-family: var(--serif); font-size: 1.5rem; color: var(--primary); margin-top: 50px; background: #f1f5f9; padding: 15px; border-radius: 6px; display: flex; justify-content: space-between; }}
        .agent-badge {{ background: var(--primary); color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th {{ text-align: left; background: #f8fafc; padding: 15px; border-bottom: 2px solid #e2e8f0; font-size: 0.75rem; text-transform: uppercase; }}
        td {{ padding: 15px; border-bottom: 1px solid #f1f5f9; }}
        .source-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; margin-top: 20px; }}
        .source-card {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 15px; }}
        .verdict-banner {{ background: var(--primary); color: white; padding: 40px; border-radius: 12px; margin-top: 40px; }}
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
        <div style="display:grid; grid-template-columns: 2fr 1.2fr; gap:30px; margin-top:20px;">
            <table><thead><tr><th>Estándar</th><th>Estatus</th><th>Descripción</th></tr></thead><tbody>{compliance_rows}</tbody></table>
            <div style="background:var(--primary); color:white; padding:25px; border-radius:12px;">
                <div style="font-size:0.6rem; color:#60a5fa; letter-spacing:2px; margin-bottom:10px;">SECURITY PROTOCOL</div>
                <h4 style="margin:0 0 10px 0;">{g_data.get('security_protocol')}</h4>
                <p style="font-size:0.8rem; color:#94a3b8;">Cifrado de extremo a extremo activo. Auditoría de estándares internacionales aprobada.</p>
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
            "timestamp": timestamp_now()
        }
        self._save_report(report_record)

        return { "id": report_id, "pdf_url": report_record["metadata"]["report_url"], "html_content": html_report }

    def _save_report(self, data: dict):
        if not self.db: return
        try: self.db.collection("reports").document(data["id"]).set(data)
        except: pass
