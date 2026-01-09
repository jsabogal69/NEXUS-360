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
        Includes Reddit Insights and expanded keyword grid.
        """
        logger.info(f"[{self.role}] Generating Premium Detailed Report...")
        
        report_id = generate_id()
        h_data = full_data.get("harvester", {})
        s_data = full_data.get("scout", {})
        i_data = full_data.get("integrator", {})
        st_data = full_data.get("strategist", {})
        m_data = full_data.get("mathematician", {})
        p_data = full_data.get("senior_partner", {})
        
        raw_summary = p_data.get("executive_summary", "Sin resumen disponible.")
        summary = ""
        parts = raw_summary.split("**")
        for i, part in enumerate(parts):
            summary += f"<strong>{part}</strong>" if i % 2 == 1 else part

        scenarios = m_data.get("scenarios", {})
        
        sources = st_data.get("analyzed_sources", [])
        has_electronics = any(x in str(sources).upper() for x in ["65W", "GAN", "ADAPTADOR", "CHARGER"])
        has_lamp = any(x in str(sources).upper() for x in ["LAMP", "ILUMINACION", "LAMPARA"])
        has_baby = any(x in str(sources).upper() for x in ["BABY", "NIGHT LIGHT", "SLEEP AID", "BEBE", "NOCHE", "SUEÑO"])
        
        niche_title = "Dossier de Inteligencia: Iluminación & Ergonomía Premium" if has_lamp else \
                      ("Dossier de Inteligencia: Electrónica GaN" if has_electronics else \
                      ("Dossier de Inteligencia: Baby Sleep & Comfort Tech" if has_baby else "Dossier de Viabilidad Estratégica"))

        source_metadata = i_data.get("source_metadata", [])
        source_cards_html = ""
        for s in source_metadata:
            fname = s['name']
            summary_str = s.get("summary", "Metadatos, Estructura")
            
            # Icon and Color Logic
            ext = fname.split('.')[-1].upper() if '.' in fname else "INTEL"
            bg_color = "#eff6ff" # Default blue
            text_color = "#1e40af"
            icon = "📄"
            
            if ext == "PDF":
                bg_color = "#fef2f2"; text_color = "#991b1b"; icon = "📕"
            elif ext in ["CSV", "XLSX"]:
                bg_color = "#f0fdf4"; text_color = "#166534"; icon = "📊"
            elif ext in ["PNG", "JPG", "JPEG"]:
                bg_color = "#faf5ff"; text_color = "#6b21a8"; icon = "🖼️"
            elif s.get("type") == "scout_intelligence" or ext == "INTEL":
                bg_color = "#fff7ed"; text_color = "#9a3412"; icon = "🧠"

            source_cards_html += f"""
            <div class="source-card">
                <div class="source-header">
                    <span class="source-icon">{icon}</span>
                    <span class="source-badge" style="background:{bg_color}; color:{text_color};">{ext}</span>
                </div>
                <div class="source-name" title="{fname}">{fname}</div>
                <div class="source-summary">{summary_str}</div>
            </div>"""

        top_10_rows = ""
        top_10_list = s_data.get("top_10_products", [])
        for p in top_10_list:
            top_10_rows += f"""
            <tr>
                <td style="text-align:center; font-weight:bold; color:var(--accent);">#{p['rank']}</td>
                <td style="width:200px;"><strong>{p['name']}</strong><br><span style="color:#64748b; font-size:0.75rem;">MSRP: ${p['price']}</span></td>
                <td><span style="color:#f59e0b">{'★' * int(p['rating'])}{'☆' * (5-int(p['rating']))}</span></td>
                <td style="font-size:0.8rem; color:#166534; background: #f0fdf4;">{p.get('adv', 'N/A')}</td>
                <td style="font-size:0.8rem; color:#991b1b; background: #fef2f2;">{p.get('vuln', 'N/A')}</td>
                <td style="font-size:0.8rem; color:#1e40af; background: #eff6ff; font-weight:600;">{p.get('gap', 'N/A')}</td>
            </tr>"""

        sl = s_data.get("social_listening", {})
        pros_html = "".join([f'<li style="color:#166534; margin-bottom:4px;">✔ {p}</li>' for p in sl.get('pros', [])])
        cons_html = "".join([f'<li style="color:#991b1b; margin-bottom:4px;">✖ {c}</li>' for c in sl.get('cons', [])])
        
        sl_html = f"""
        <div style="display:grid; grid-template-columns: 1.25fr 1fr; gap:25px; margin-top:30px;">
            <!-- Column 1: Review Audit & Scholar -->
            <div style="display:flex; flex-direction:column; gap:25px;">
                <div style="background:#f8fafc; padding:30px; border-radius:16px; border:1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);">
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

                <div style="background:#f0f4ff; padding:30px; border-radius:16px; border:1px solid #c7d2fe; position:relative;">
                    <div style="position:absolute; top:20px; right:25px; opacity:0.1;"><svg width="40" height="40" fill="currentColor" viewBox="0 0 24 24"><path d="M12 3L1 9l11 6 9-4.91V17h2V9L12 3zM3.89 9L12 4.57 20.11 9 12 13.43 3.89 9zM12 15.33l-7 3.82V21h14v-1.85l-7-3.82z"/></svg></div>
                    <h4 style="margin-top:0; color:#3730a3; font-family:var(--serif); display:flex; align-items:center; gap:10px;">🎓 The Scholar Audit (Academic Intelligence)</h4>
                    <p style="font-size:0.95rem; color:#312e81; line-height:1.7; font-style:italic;">{sl.get('scholar_findings', 'Cargando hallazgos académicos...')}</p>
                    <div style="margin-top:15px; font-size:0.7rem; color:#4338ca; font-weight:700; text-transform:uppercase; letter-spacing:1px;">Fuentes: IEEE Xplore, Nature, Journal of Applied Physics</div>
                </div>
            </div>

            <!-- Column 2: Search, Reddit, TikTok -->
            <div style="display:flex; flex-direction:column; gap:25px;">
                <div style="background:#f0fdfa; padding:25px; border-radius:16px; border:1px solid #99f6e4;">
                    <h4 style="margin-top:0; color:#0d9488; font-family:var(--serif); display:flex; align-items:center; gap:10px;">📈 Google Search Intelligence</h4>
                    <p style="font-size:0.9rem; color:#134e4a; line-height:1.6;">{sl.get('google_search_insights', 'Analizando tendencias de búsqueda...')}</p>
                </div>

                <div style="background:#fdf4ff; padding:25px; border-radius:16px; border:1px solid #f5d0fe;">
                    <h4 style="margin-top:0; color:#86198f; font-family:var(--serif); display:flex; align-items:center; gap:10px;">🤖 Reddit & TikTok Community Pulse</h4>
                    <div style="margin-bottom:15px;">
                        <span style="font-size:0.7rem; font-weight:800; color:#701a75; text-transform:uppercase;">Reddit Experts:</span>
                        <div style="font-size:0.85rem; color:#4a044e; margin-top:5px; line-height:1.5;">{sl.get('reddit_insights', 'N/A')}</div>
                    </div>
                    <div>
                        <span style="font-size:0.7rem; font-weight:800; color:#701a75; text-transform:uppercase;">Social Momentum:</span>
                        <div style="font-size:0.85rem; color:#4a044e; margin-top:5px; line-height:1.5;">{sl.get('tiktok_trends', 'N/A')}</div>
                    </div>
                </div>

                <div style="background:#fffbeb; padding:25px; border-radius:16px; border:1px solid #fde68a;">
                    <h4 style="margin-top:0; color:#92400e; font-family:var(--serif); display:flex; align-items:center; gap:10px;">💡 Ultimate Consumer Desire</h4>
                    <p style="font-size:1rem; color:#78350f; line-height:1.6; font-weight:700; margin-bottom:0;">{sl.get('consumer_desire', 'N/A')}</p>
                </div>
            </div>
        </div>"""

        # SECTION IV: SALES INTELLIGENCE & SEASONALITY
        scout_full = i_data.get("scout_data", {})
        sales = scout_full.get("sales_intelligence", {})
        
        # Market Share Bars
        market_share_html = ""
        for brand in sales.get("market_share_by_brand", []):
            share = brand.get("share", 0)
            status = brand.get("status", "")
            color = "#2563eb" if "NEXUS" not in brand['brand'].upper() else "var(--accent)"
            market_share_html += f"""
            <div style="margin-bottom:15px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:5px; font-size:0.85rem; font-weight:700;">
                    <span style="color:var(--primary);">{brand['brand']} <span style="font-weight:400; color:#64748b; margin-left:8px;">{status}</span></span>
                    <span style="color:{color};">{share}%</span>
                </div>
                <div style="width:100%; height:10px; background:#f1f5f9; border-radius:99px; overflow:hidden;">
                    <div style="width:{share}%; height:100%; background:{color}; border-radius:99px;"></div>
                </div>
            </div>"""

        # Seasonality Tags
        season_peaks_html = ""
        for peak in sales.get("seasonality", {}).get("peaks", []):
            impact_color = "#b91c1c" if peak['impact'] == "Max" or peak['impact'] == "Extreme" else "#ea580c"
            season_peaks_html += f"""
            <div style="background:#fff; border:1px solid #e2e8f0; padding:12px; border-radius:8px; display:flex; align-items:center; gap:10px;">
                <div style="font-weight:900; color:{impact_color}; font-size:1.1rem; min-width:30px;">{peak['month'][:3].upper()}</div>
                <div>
                    <div style="font-size:0.8rem; font-weight:800; color:var(--primary);">{peak['event']}</div>
                    <div style="font-size:0.7rem; color:#64748b;">Impacto: {peak['impact']}</div>
                </div>
            </div>"""

        category_tags_html = "".join([f'<span class="tag-medium" style="margin-right:8px; margin-bottom:8px; display:inline-block; font-size:0.75rem; padding:4px 12px; border-radius:99px; background:#f8fafc; border:1px solid #e2e8f0; color:#475569;">{k}: {v}%</span>' for k,v in sales.get("sub_category_distribution", {}).items()])

        sales_section_html = f"""
        <h2 class="section-title">IV. Inteligencia de Ventas & Estacionalidad <span class="agent-badge">Matrix-Scout</span></h2>
        <div class="narrative">Correlación entre cuota de mercado, temporalidad anual y picos de oportunidad por categoría capturados mediante auditoría de imágenes y tablas de ventas.</div>
        
        <div style="display:grid; grid-template-columns: 1fr 1.2fr; gap:30px; margin-top:20px;">
            <div style="background:#ffffff; padding:30px; border-radius:16px; border:1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);">
                <h4 style="margin-top:0; color:var(--primary); font-family:var(--serif); border-bottom:1px solid #e2e8f0; padding-bottom:15px;">📊 Brand Market Share (Cuota de Mercado)</h4>
                <div style="margin-top:20px;">{market_share_html or '<p>Analizando datos de marcas...</p>'}</div>
                <div style="margin-top:25px; padding-top:20px; border-top:1px solid #f1f5f9;">
                    <div style="font-size:0.7rem; font-weight:900; color:#64748b; text-transform:uppercase; margin-bottom:10px; letter-spacing:1px;">Distribución por Sub-categoría</div>
                    <div style="display:flex; flex-wrap:wrap;">{category_tags_html or 'N/A'}</div>
                </div>
            </div>

            <div style="display:flex; flex-direction:column; gap:20px;">
                <div style="background:#fffcf0; padding:30px; border-radius:16px; border:1px solid #fde68a;">
                    <h4 style="margin-top:0; color:#92400e; font-family:var(--serif); display:flex; align-items:center; gap:8px;">🗓️ Seasonal Peaks (Ventanas de Oportunidad)</h4>
                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; margin-top:15px;">
                        {season_peaks_html or 'N/A'}
                    </div>
                </div>
                <div style="background:#f0fdf4; padding:25px; border-radius:16px; border:1px solid #86efac;">
                    <h4 style="margin-top:0; color:#166534; font-family:var(--serif); display:flex; align-items:center; gap:8px;">💡 Insight Estratégico de Ventas</h4>
                    <p style="font-size:0.95rem; color:#14532d; line-height:1.7; font-weight:600; margin-bottom:0;">{sales.get('seasonality', {}).get('strategy_insight', 'Correlacionando puntos de datos...')}</p>
                </div>
            </div>
        </div>"""

        trends_html = ""
        for trend in s_data.get("trends", []):
            if isinstance(trend, dict):
                title = trend.get("title", "Tendencia Emergente")
                desc = trend.get("description", "")
                trends_html += f"""
                <li style="margin-bottom:20px; list-style:none; border-left: 2px solid #e2e8f0; padding-left:20px; transition: border-color 0.2s ease;">
                    <div style="display:flex; align-items:center; gap:10px; font-weight:700; color:var(--primary); font-size:1.05rem; margin-bottom:6px;">
                        <span style="font-size:1.2rem;">🚀</span> {title}
                    </div>
                    <div style="font-size:0.85rem; color:#475569; line-height:1.7;">{desc}</div>
                </li>"""
            else:
                trends_html += f'<li style="margin-bottom:12px; display:flex; gap:10px; font-weight:600;"><span>🚀</span> <span>{trend}</span></li>'
            
        kw_grid = ""
        for kw in s_data.get("keywords", []):
            trend_color = "#10b981" if any(x in kw['trend'].upper() for x in ["UP", "HIGH", "VIRAL", "TRENDING"]) else "#3b82f6"
            kw_grid += f"""
            <div class="data-card" style="border-top:3px solid {trend_color}; background:#ffffff; padding:15px;">
                <div style="font-size:0.6rem; color:#64748b; text-transform:uppercase; letter-spacing:1px; font-weight:800;">SEO TERM</div>
                <div style="font-size:0.9rem; font-weight:bold; color:var(--primary); margin:4px 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="{kw['term']}">{kw['term']}</div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
                    <span style="font-size:0.7rem; background:#f1f5f9; padding:2px 8px; border-radius:99px; color:#475569;">VOL: {kw['volume']}</span>
                    <span style="font-size:0.7rem; color:{trend_color}; font-weight:800;">{kw['trend']}</span>
                </div>
            </div>"""

        strategist_grid_html = ""
        gaps = st_data.get('strategic_gaps', [])
        for gap in gaps:
            # New Structured Parsing
            lines = gap.split("\n")
            diagnosis = ""
            impact = ""
            strategy = ""
            
            for line in lines:
                if "DIAGNÓSTICO ESTRATÉGICO PROFUNDO" in line:
                    continue # Already in label
                elif "ANÁLISIS DE IMPACTO" in line:
                    impact = line.replace("ANÁLISIS DE IMPACTO:", "").strip()
                elif "💡 ESTRATEGIA NEXUS" in line:
                    strategy = line.replace("💡 ESTRATEGIA NEXUS:", "").strip()
                else:
                    if line.strip(): diagnosis += line + " "

            diagnosis = diagnosis.strip()
            
            strategist_grid_html += f"""
            <div class="data-card" style="grid-column: span 2; padding: 0; overflow: hidden; border: 1px solid #e2e8f0; background: #ffffff;">
                <div style="padding: 20px; border-bottom: 1px solid #f1f5f9;">
                    <div style="font-size: 0.65rem; color: #64748b; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 800; margin-bottom: 8px;">DIAGNÓSTICO ESTRATÉGICO PROFUNDO</div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #0f172a; line-height: 1.5;">{diagnosis}</div>
                </div>
                <div style="padding: 15px 20px; background: #fffaf5;">
                    <div style="font-size: 0.7rem; color: #9a3412; font-weight: 800; margin-bottom: 4px;">📈 ANÁLISIS DE IMPACTO</div>
                    <div style="font-size: 0.9rem; color: #7c2d12; line-height: 1.5;">{impact}</div>
                </div>
                <div style="padding: 20px; background: #f0f9ff; border-top: 1px solid #e0f2fe;">
                    <div style="font-size: 0.7rem; color: #0369a1; font-weight: 800; margin-bottom: 6px;">💡 ESTRATEGIA NEXUS</div>
                    <div style="font-size: 0.95rem; font-weight: 700; color: #0c4a6e; line-height: 1.5; border-left: 3px solid #0ea5e9; padding-left: 15px;">{strategy}</div>
                </div>
            </div>"""

        math_table_rows = ""
        amz_base = m_data.get("amazon_baseline", {})
        gen_ctx = m_data.get("general_market_context", {})

        for key, scn in scenarios.items():
            viability = scn.get('viability', 'Low')
            tag_class = "tag-risk" if "High" in viability or "Low" in viability else "tag-medium"
            if "Recommended" in viability: tag_class = "tag-recommended"
            
            # Sub-breakdown for Amazon Fees
            breakdown_html = '<div style="font-size:0.75rem; color:#64748b; margin-top:5px;">'
            for label, val in scn.get('breakdown', {}).items():
                breakdown_html += f"<div>• {label}: <strong>{val}</strong></div>"
            breakdown_html += '</div>'

            math_table_rows += f"""
            <tr>
                <td style="font-weight:700;">
                    {scn.get('name')}<br>
                    <span style="font-size:0.75rem; color:#64748b; font-weight:400; display:block; margin-top:4px;">📦 {scn.get('composition', 'Hardware Base')}</span>
                    {breakdown_html}
                </td>
                <td style="font-size:1.1rem; font-weight:700;">${scn.get('price')}</td>
                <td>${scn.get('landed')}</td>
                <td><strong style="color:var(--accent); font-size:1.1rem;">{scn.get('margin_pct')}%</strong></td>
                <td style="text-align:center;"><span style="font-weight:700; color:#1e293b;">{scn.get('break_even_qty', 'N/A')}</span> <span style="font-size:0.6rem; display:block; color:#94a3b8;">unidades</span></td>
                <td style="text-align:center;"><span style="font-weight:700; color:#1e293b;">{scn.get('payback_months', 'N/A')}</span> <span style="font-size:0.6rem; display:block; color:#94a3b8;">meses</span></td>
                <td><span class="tag {tag_class}">{viability}</span></td>
                <td style="font-size:0.85rem; color:#475569;">{scn.get('notes', '')}</td>
            </tr>"""

        # Market Benchmark Comparison (Forensic & FBA Sensitivity)
        fba_sense = m_data.get("fba_sensitivity_analysis", {})
        comps = fba_sense.get("competitors", [])
        nexus_target = fba_sense.get("nexus_target", {})
        
        bench_html = ""
        for p in comps[:6]: # Show top 6 for layout
            fba_b = p.get('fba_breakdown', {})
            bench_html += f"""
            <div class="data-card" style="background:#ffffff; border:1px solid #e2e8f0; padding:15px; border-left:4px solid {p.get('tier_color')};">
                <div style="font-size:0.6rem; color:#64748b; text-transform:uppercase; letter-spacing:1px; font-weight:800; margin-bottom:5px;">#{p.get('rank')} {p.get('efficiency_tier')}</div>
                <div style="font-size:0.95rem; font-weight:900; color:var(--primary); margin-bottom:8px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" title="{p.get('name')}">{p.get('name')}</div>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:3px; font-size:0.7rem; color:#475569; margin-bottom:8px; background:#f8fafc; padding:8px; border-radius:6px;">
                    <div>MSRP:</div><div style="text-align:right; font-weight:700;">${p.get('msrp')}</div>
                    <div>Pick & Pack:</div><div style="text-align:right;">${fba_b.get('pick_pack')}</div>
                    <div>Storage:</div><div style="text-align:right;">${fba_b.get('storage')}</div>
                    <div>Referral:</div><div style="text-align:right;">${fba_b.get('referral')}</div>
                    <div style="grid-column: span 2; border-top:1px solid #e2e8f0; margin-top:3px; padding-top:3px; font-weight:800; display:flex; justify-content:space-between;">
                        <span>TOTAL FBA:</span><span>${fba_b.get('total_logistics')}</span>
                    </div>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:700; font-size:0.6rem; color:#64748b;">IMPACTO:</span>
                    <span style="font-weight:900; color:{p.get('tier_color')};">{p.get('fba_impact_pct')}%</span>
                </div>
            </div>"""

        # NEXUS Highlight Card for FBA
        n_fba_b = nexus_target.get('fba_breakdown', {})
        nexus_fba_card = f"""
        <div class="data-card" style="background:#f0f9ff; border:2px solid #0ea5e9; padding:20px; grid-column: span 2;">
            <div style="display:flex; justify-content:space-between; align-items:start;">
                <div>
                    <div style="font-size:0.65rem; color:#0369a1; text-transform:uppercase; letter-spacing:1.5px; font-weight:800; margin-bottom:5px;">NEXUS EFFICIENCY TARGET</div>
                    <div style="font-size:1.3rem; font-weight:900; color:#0c4a6e;">{nexus_target.get('name')}</div>
                </div>
                <div style="background:#0ea5e9; color:white; padding:5px 12px; border-radius:99px; font-size:0.7rem; font-weight:800;">{nexus_target.get('efficiency_tier')}</div>
            </div>
            <div style="display:grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap:15px; margin-top:15px; border-top:1px solid #bae6fd; padding-top:15px;">
                <div>
                    <div style="font-size:0.6rem; color:#64748b; text-transform:uppercase;">MSRP</div>
                    <div style="font-size:1.1rem; font-weight:900; color:#0c4a6e;">${nexus_target.get('msrp')}</div>
                </div>
                <div>
                    <div style="font-size:0.6rem; color:#64748b; text-transform:uppercase;">Pick/Pack</div>
                    <div style="font-size:1.1rem; font-weight:900; color:#0c4a6e;">${n_fba_b.get('pick_pack')}</div>
                </div>
                <div>
                    <div style="font-size:0.6rem; color:#64748b; text-transform:uppercase;">Granular Fee</div>
                    <div style="font-size:1.1rem; font-weight:900; color:#0c4a6e;">${round(n_fba_b.get('storage') + n_fba_b.get('referral'), 2)}</div>
                </div>
                <div>
                    <div style="font-size:0.6rem; color:#64748b; text-transform:uppercase;">Eficiencia</div>
                    <div style="font-size:1.1rem; font-weight:900; color:#059669;">{nexus_target.get('fba_impact_pct')}%</div>
                </div>
            </div>
        </div>"""

        # Multivariate Analysis Section
        mra = m_data.get("multivariate_analysis", {})
        corr = mra.get("correlations", {})
        hotspots = mra.get("hotspots", [])
        
        hotspots_html = "".join([f'<div style="background:#f1f5f9; padding:10px; border-radius:8px; font-size:0.8rem; margin-bottom:8px; border-left:3px solid var(--accent);">🔥 {h}</div>' for h in hotspots])

        multivariate_panel = f"""
        <div style="grid-column: span 3; display:grid; grid-template-columns: 2fr 1fr; gap:20px; margin-top:20px; border-top:1px dashed #fdba74; padding-top:25px;">
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:20px;">
                <h5 style="margin:0 0 15px 0; color:var(--primary); font-size:0.9rem; text-transform:uppercase; letter-spacing:1px;">📊 Análisis Multivariable Relacional (MRA)</h5>
                <div style="display:flex; justify-content:space-around; align-items:center; height:100px; text-align:center;">
                    <div>
                        <div style="font-size:0.6rem; color:#64748b;">Mkt FBA Erosion</div>
                        <div style="font-size:1.4rem; font-weight:900; color:#dc2626;">{corr.get('avg_market_fba_impact')}%</div>
                    </div>
                    <div style="font-size:1.5rem; color:#e2e8f0;">→</div>
                    <div>
                        <div style="font-size:0.6rem; color:#64748b;">Mkt Net Margin</div>
                        <div style="font-size:1.4rem; font-weight:900; color:#2563eb;">{corr.get('avg_market_margin')}%</div>
                    </div>
                    <div style="font-size:1.5rem; color:#e2e8f0;">vs</div>
                    <div>
                        <div style="font-size:0.6rem; color:#64748b;">NEXUS Dominance Delta</div>
                        <div style="font-size:1.4rem; font-weight:900; color:#059669;">+{corr.get('nexus_dominance_delta')}%</div>
                    </div>
                </div>
                <p style="font-size:0.75rem; color:#64748b; margin-top:10px; font-style:italic;">* La correlación detectada es "{corr.get('fba_vs_margin')}". NEXUS rompe la tendencia de la categoría mediante el desequilibrio positivo de la curva de valor.</p>
            </div>
            <div>
                <h5 style="margin:0 0 10px 0; color:var(--primary); font-size:0.8rem; text-transform:uppercase;">Hotspots de Optimización</h5>
                {hotspots_html}
            </div>
        </div>"""

        # Amazon Unit Economics Panel Metrics
        msrp = amz_base.get('msrp', 0)
        cogs = amz_base.get('cogs_landed', 0)
        opex = amz_base.get('total_amz_opex', 0)
        net_profit = round(msrp - (cogs + opex), 2)
        net_margin_pct = round((net_profit / msrp) * 100, 1) if msrp > 0 else 0
        
        sku_props = gen_ctx.get("sku_proposals", {})

        verdict = st_data.get("dynamic_verdict", {})
        
        amz_context_html = f"""
        <div style="background:#fff7ed; border:1px solid #fdba74; padding:30px; border-radius:16px; margin-bottom:30px;">
             <h4 style="margin-top:0; color:#9a3412; font-family:var(--serif); display:flex; align-items:center; gap:10px;">⚖️ Análisis de Sensibilidad FBA & Tiers de Eficiencia</h4>
             <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:15px;">
                {nexus_fba_card}
                {bench_html}
             </div>
        </div>

        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:30px; margin-bottom:40px;">
            <div style="background:#f8fafc; border:1px solid #e2e8f0; padding:30px; border-radius:16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                <h4 style="margin-top:0; color:var(--primary); font-family:var(--serif); display:flex; align-items:center; gap:10px;">📦 Amazon Unit Economics (NEXUS Calibrado)</h4>
                <div style="display:flex; justify-content:space-between; margin-bottom:15px; padding-bottom:15px; border-bottom:1px solid #e2e8f0;">
                    <div>
                        <div style="font-size:0.7rem; color:#64748b; font-weight:800; text-transform:uppercase;">MSRP Sugerido</div>
                        <div style="font-size:1.5rem; font-weight:900; color:var(--primary);">${msrp}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:0.7rem; color:#64748b; font-weight:800; text-transform:uppercase;">Costo Landed (COGS)</div>
                        <div style="font-size:1.5rem; font-weight:900; color:var(--primary);">${cogs}</div>
                    </div>
                </div>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; font-size:0.95rem;">
                    <div style="color:#475569;">Comisión Referral (15%):</div><div style="text-align:right; font-weight:700; color:#1e293b;">-${amz_base.get('referral_fee')}</div>
                    <div style="color:#475569;">FBA Fulfillment & Shipping:</div><div style="text-align:right; font-weight:700; color:#1e293b;">-${amz_base.get('fba_fulfillment')}</div>
                    <div style="color:#475569;">Almacenamiento (Promedio):</div><div style="text-align:right; font-weight:700; color:#1e293b;">-${amz_base.get('monthly_storage')}</div>
                    <div style="color:#475569;">Inversión Ads/PPC (CAC):</div><div style="text-align:right; font-weight:700; color:#1e293b;">-${amz_base.get('ads_spend_cac')}</div>
                    <div style="grid-column: span 2; border-top: 2px solid #e2e8f0; margin: 10px 0; padding-top: 10px; display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:900; color:var(--primary); font-size:1.1rem;">Utilidad Neta por Unidad:</span>
                        <span style="font-weight:900; color:#065f46; font-size:1.3rem;">${net_profit} ({net_margin_pct}%)</span>
                    </div>
                </div>
                <div style="margin-top:15px; font-size:0.75rem; color:#64748b; font-style:italic;">* Modelo calibrado para un ACOS objetivo de {round(opex/msrp*100, 1) if msrp > 0 else 0}% en fase de escalado.</div>
            </div>
            <div style="display:flex; flex-direction:column; gap:20px;">
                <div style="background:#f0fdf4; border:1px solid #86efac; padding:25px; border-radius:16px; flex:1;">
                    <h4 style="margin-top:0; color:#166534; font-family:var(--serif); display:flex; align-items:center; gap:10px;">🌐 Análisis de Canal DTC</h4>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <div style="font-size:0.95rem; font-weight:700; color:#14532d;">Márgen Neto DTC:</div>
                        <div style="font-size:1.4rem; font-weight:900; color:#166534;">{gen_ctx.get('direct_to_consumer_margin')}%</div>
                    </div>
                    <div style="font-family:var(--mono); font-size:0.7rem; color:#166534; background:#dcfce7; padding:4px 8px; border-radius:4px; margin-bottom:10px; display:inline-block;">PROPOSED SKU: {sku_props.get('DTC_Exclusive', 'PENDING')}</div>
                    <p style="color:#166534; font-size:0.85rem; line-height:1.6; margin:0;">Eliminación total de comisiones de marketplace. El capital se reasigna a Equity de Marca.</p>
                </div>
                <div style="background:#eff6ff; border:1px solid #93c5fd; padding:25px; border-radius:16px; flex:1;">
                    <h4 style="margin-top:0; color:#1e40af; font-family:var(--serif); display:flex; align-items:center; gap:10px;">🏢 B2B & Wholesale Identity</h4>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <div style="font-size:0.95rem; font-weight:700; color:#1e3a8a;">Márgen Distribución:</div>
                        <div style="font-size:1.4rem; font-weight:900; color:#1e40af;">{gen_ctx.get('retail_distribution_margin')}%</div>
                    </div>
                    <div style="font-family:var(--mono); font-size:0.7rem; color:#1e40af; background:#dbeafe; padding:4px 8px; border-radius:4px; margin-bottom:10px; display:inline-block;">PROPOSED SKU: {sku_props.get('B2B_Bulk', 'PENDING')}</div>
                    <p style="color:#1e3a8a; font-size:0.85rem; line-height:1.6; margin:0;">Modelo de volumen masivo. Ideal para canales corporativos y canal mayorista.</p>
                </div>
            </div>
        </div>"""

        verdict = st_data.get("dynamic_verdict", {})
        roadmap_data = st_data.get("dynamic_roadmap", [])
        roadmap_html = ""
        for idx, step in enumerate(roadmap_data):
            roadmap_html += f"""
            <div style="display: flex; gap: 40px; margin-bottom: 50px; background: #fff; padding: 45px; border-radius: 16px; border: 1px solid #e2e8f0; position: relative; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.02);">
                <div style="font-family: var(--mono); font-size: 6rem; font-weight: 900; color: #f8fafc; position: absolute; top: -10px; right: 30px; z-index: 1; user-select: none;">{str(idx+1).zfill(2)}</div>
                <div style="position: relative; z-index: 2; width: 70px; height: 70px; background: linear-gradient(135deg, var(--primary) 0%, #1e293b 100%); color: white; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-family: var(--mono); font-size: 1.5rem; font-weight: bold; flex-shrink: 0; box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.2); transform: rotate(-3deg);">{str(idx+1).zfill(2)}</div>
                <div style="position: relative; z-index: 2; padding-top: 10px;">
                    <h3 style="margin: 0 0 15px 0; font-family: var(--serif); font-size: 1.5rem; color: var(--primary); letter-spacing: -1px; font-weight: 700;">{step[0]}</h3>
                    <div style="color: #475569; font-size: 1.15rem; line-height: 1.9; max-width: 900px; font-weight: 400;">{step[1]}</div>
                </div>
            </div>"""
        
        # Cleanup Section Title to have more weight

        # MCKINSEY-STYLE PARTNER SUMMARY FORMATTING
        partner_raw = st_data.get("partner_summary", summary)
        formatted_summary = ""
        if "### I." in partner_raw or "I. " in partner_raw:
             main_intro = partner_raw.split("### I.")[0] if "### I." in partner_raw else partner_raw.split("I. ")[0]
             formatted_summary += f'<div style="font-size:1.25rem; font-weight:600; color:var(--primary); margin-bottom:35px; line-height:1.6; border-left:4px solid var(--accent); padding-left:20px;">{main_intro.strip()}</div>'
             
             def get_block(text, start, end=None):
                 try:
                     parts = text.split(start)
                     if len(parts) > 1:
                         block = parts[1].split(end)[0] if end else parts[1]
                         return block.strip()
                 except: pass
                 return ""

             b1 = get_block(partner_raw, "I. ", "II. ") or get_block(partner_raw, "### I. ", "### II. ")
             b2 = get_block(partner_raw, "II. ", "III. ") or get_block(partner_raw, "### II. ", "### III. ")
             b3 = get_block(partner_raw, "III. ") or get_block(partner_raw, "### III. ")

             for idx, (title, content) in enumerate([("I. LA TRAMPA DE LA COMODITIZACIÓN", b1), ("II. EL FOSO ESTRATÉGICO", b2), ("III. VEREDICTO NEXUS", b3)]):
                 if content:
                     formatted_summary += f"""
                     <div style="margin-bottom:30px; background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:30px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);">
                         <div style="font-family:var(--mono); font-size:0.75rem; font-weight:800; color:var(--accent); letter-spacing:2px; margin-bottom:10px;">TESIS {idx+1}</div>
                         <h4 style="margin:0 0 15px 0; font-family:var(--serif); font-size:1.3rem; color:var(--primary);">{title}</h4>
                         <div style="font-size:1rem; color:#475569; line-height:1.8;">{content.replace("**", "<strong>").replace("</strong>", "</strong>")}</div>
                     </div>"""
             
             final_call = partner_raw.split("Es momento")[-1] if "Es momento" in partner_raw else ""
             if final_call:
                 formatted_summary += f'<div style="margin-top:40px; text-align:center; font-family:var(--serif); font-size:1.4rem; color:var(--primary); font-weight:700;">"Es momento{final_call.replace("**", "<strong>").replace("</strong>", "</strong>")}"</div>'
        else:
            formatted_summary = f'<div style="white-space: pre-wrap; font-size:1.1rem; line-height:1.8; color:#1e293b;">{partner_raw}</div>'

        html_report = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>NEXUS-360 // DOSSIER DE INTELIGENCIA DE ALTO NIVEL</title>
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
    <style>
        :root {{ --primary: #0f172a; --accent: #2563eb; --bg: #f8fafc; --card-bg: #ffffff; --border: #e2e8f0; --text: #334155; --serif: 'Merriweather', serif; --sans: 'Inter', sans-serif; --mono: 'JetBrains Mono', monospace; }}
        body {{ font-family: var(--sans); background: var(--bg); color: var(--text); padding: 40px; margin: 0; line-height: 1.6; }}
        .container {{ max-width: 1300px; margin: 0 auto; background: white; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.1); padding: 60px; border-radius: 12px; border-top: 10px solid var(--primary); }}
        header {{ text-align: left; margin-bottom: 50px; border-bottom: 2px solid #f1f5f9; padding-bottom: 30px; display: flex; justify-content: space-between; align-items: flex-end; }}
        .brand {{ font-family: var(--mono); font-size: 0.75rem; letter-spacing: 3px; color: var(--accent); text-transform: uppercase; font-weight: bold; }}
        h1 {{ font-family: var(--serif); font-size: 2.2rem; color: var(--primary); margin: 10px 0; }}
        .subtitle {{ font-size: 1.1rem; color: #64748b; font-weight: 300; border-left: 3px solid var(--accent); padding-left: 15px; }}
        .section-title {{ font-family: var(--serif); font-size: 1.4rem; color: var(--primary); margin-top: 60px; margin-bottom: 25px; display: flex; align-items: center; gap: 15px; background: #f1f5f9; padding: 15px 20px; border-radius: 6px; }}
        .agent-badge {{ background: var(--primary); color: white; border-radius: 3px; font-family: var(--mono); font-size: 0.65rem; padding: 4px 10px; text-transform: uppercase; }}
        .narrative {{ font-size: 0.95rem; color: #475569; margin-bottom: 20px; line-height: 1.7; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
        th {{ text-align: left; padding: 18px; font-size: 0.75rem; color: #64748b; text-transform: uppercase; border-bottom: 2px solid #f1f5f9; background: #f8fafc; }}
        td {{ padding: 18px; border-bottom: 1px solid #f1f5f9; font-size: 0.95rem; vertical-align: top; line-height: 1.5; }}
        .tag {{ padding: 5px 12px; border-radius: 4px; font-size: 0.7rem; font-weight: 800; }}
        .tag-risk {{ background: #fee2e2; color: #b91c1c; }}
        .tag-medium {{ background: #ffedd5; color: #c2410c; }}
        .tag-recommended {{ background: #dcfce7; color: #15803d; }}
        .verdict-banner {{ background: var(--primary); color: white; padding: 50px; border-radius: 12px; margin-top: 50px; position: relative; overflow: hidden; }}
        .verdict-banner::after {{ content: 'APPROVED'; position: absolute; top: 10px; right: -30px; transform: rotate(45deg); background: #10b981; color: white; padding: 10px 60px; font-weight: 900; font-size: 0.8rem; letter-spacing: 2px; }}
        .no-print {{ display: block; position: fixed; top: 20px; right: 20px; z-index: 1000; }}
        .print-btn {{ background: var(--accent); color: white; border: none; padding: 12px 25px; border-radius: 8px; font-family: var(--sans); font-weight: 600; cursor: pointer; box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3); display: flex; align-items: center; gap: 10px; font-size: 0.9rem; transition: all 0.2s ease; }}
        .source-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 15px; margin-bottom: 40px; }}
        .source-card {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; transition: all 0.2s ease; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
        .data-card {{ background: white; border: 1px solid var(--border); padding: 25px; border-radius: 10px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }}
        @media print {{ 
            @page {{ size: A4 portrait; margin: 20mm; }}
            .no-print {{ display: none !important; }} 
            body {{ padding: 0; background: white; -webkit-print-color-adjust: exact; print-color-adjust: exact; }} 
            .container {{ box-shadow: none; border-top: none; width: 100%; max-width: 100%; padding: 0; }}
            .section-title {{ break-after: avoid; page-break-after: avoid; margin-top: 40px !important; }}
            .data-card, tr, .verdict-banner, .source-card {{ break-inside: avoid; page-break-inside: avoid; }}
            h2.section-title:nth-of-type(n+6) {{ page-break-before: always; }} /* Force break for major final sections */
            .data-card {{ margin-bottom: 20px; }}
        }}
    </style>
</head>
<body>
    <div class="no-print"><button onclick="window.print()" class="print-btn">Exportar a PDF</button></div>
    <div class="container">
        <header>
            <div class="header-left">
                <span class="brand">NEXUS-360 ADVANCED STRATEGY UNIT // {report_id}</span>
                <h1>{niche_title}</h1>
                <div class="subtitle">Auditoría Transparente, Inteligencia de Mercado y Plan Maestro 2026</div>
            </div>
            <div style="text-align:right">
                <div style="font-weight:900; color:#b91c1c; font-size:0.9rem; letter-spacing:1px;">TOP SECRET // EYES ONLY</div>
                <div style="font-size:0.8rem; margin-top:5px; color:#64748b;">GÉNESIS: {timestamp_now().strftime('%d %B, %Y')}</div>
            </div>
        </header>

        <h2 class="section-title" style="margin-top:30px;">I. Auditoría de Fuentes & Trazabilidad <span class="agent-badge">Harvester</span></h2>
        <div class="source-grid">{source_cards_html}</div>

        <h2 class="section-title">II. Matriz de Inteligencia Competitiva (TOP 10) <span class="agent-badge">Scout</span></h2>
        <table>
            <thead><tr><th>Rank</th><th>Producto & Market Fit</th><th>Rating</th><th>Fortalezas</th><th>Vulnerabilidades</th><th>Brecha</th></tr></thead>
            <tbody>{top_10_rows}</tbody>
        </table>

        <h2 class="section-title">III. Social Listening & Review Audit <span class="agent-badge">Scout</span></h2>
        {sl_html}
        <div style="display:grid; grid-template-columns: 1fr 1.3fr; gap:30px; margin-top:30px;">
            <div style="background:#f1f5f9; padding:30px; border-radius:10px; border: 1px solid #cbd5e1;">
                <h4 style="margin-top:0; color:var(--primary); font-family:var(--serif);">Tendencias de Mercado 2026</h4>
                <ul style="padding:0; list-style:none;">{trends_html}</ul>
                <div style="margin-top:25px; padding-top:20px; border-top:1px solid #cbd5e1; font-style:italic;"><strong>Insight de Sentimiento:</strong> {s_data.get('sentiment_summary')}</div>
            </div>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px;">{kw_grid}</div>
        </div>

        <h2 class="section-title">IV. Inteligencia de Ventas & Estacionalidad <span class="agent-badge">Matrix-Scout</span></h2>
        {sales_section_html}

        <h2 class="section-title">V. Brechas & Propuestas de Valor Disruptivas <span class="agent-badge">Strategist</span></h2>
        <div class="card-grid" style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">{strategist_grid_html}</div>

        <h2 class="section-title">VI. Modelado Financiero & Unit Economics <span class="agent-badge">Mathematician</span></h2>
        {amz_context_html}
        <table>
            <thead><tr><th>Escenario</th><th>MSRP</th><th>Landed</th><th>Net %</th><th>Break-even</th><th>Payback</th><th>Viabilidad</th><th>Observaciones</th></tr></thead>
            <tbody>{math_table_rows}</tbody>
        </table>

        <h2 class="section-title">VII. Informe Final del Socio Director <span class="agent-badge">Senior Partner</span></h2>
        <div style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border:2px solid #e2e8f0; padding:50px; border-radius:16px; box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);">
            {formatted_summary}
        </div>

        <div class="verdict-banner">
            <span style="color:#60a5fa; font-family:var(--mono); font-weight:bold; font-size:0.8rem; letter-spacing:3px;">VEREDICTO MAESTRO</span>
            <div style="font-family:var(--serif); font-size:2.4rem; font-weight:700;">{verdict.get('title', '').upper()}</div>
            <div style="font-size:1.2rem; opacity:0.95; line-height:1.8;">{verdict.get('text', '')}</div>
        </div>

        <h2 class="section-title">VIII. Plan Maestro de Ejecución (Roadmap) <span class="agent-badge">Nexus-360</span></h2>
        <div style="margin-top:20px;">{roadmap_html}</div>

        <footer style="margin-top:80px; text-align:center; font-family:var(--mono); font-size:0.7rem; color:#94a3b8; border-top:1px solid #e2e8f0; padding-top:40px;">
            NEXUS-360 ADVANCED STRATEGY UNIT | PROTEGIDO POR PROTOCOLO AGENTIC-OS | {timestamp_now().strftime('%Y')}
        </footer>
    </div>
</body>
</html>
        """

        static_reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "reports")
        os.makedirs(static_reports_dir, exist_ok=True)
        filename = f"report_{report_id}.html"
        filepath = os.path.join(static_reports_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_report)
        
        # PERSISTENCE: Save full report intent to DB for future recursive ingestion
        report_record = {
            "id": report_id,
            "type": "nexus_final_report",
            "metadata": {
                "title": niche_title,
                "anchor": st_data.get("scout_anchor"),
                "report_url": f"/dashboard/reports/{filename}"
            },
            "intel_summary": {
                "verdict": verdict,
                "roadmap_phases": roadmap_data,
                "strategic_gaps": st_data.get('strategic_gaps', []),
                "financial_recommendation": scenarios.get("kit_premium", {})
            },
            "source_ssot_id": i_data.get("id"),
            "timestamp": timestamp_now()
        }
        self._save_report(report_record)

        return { "id": report_id, "type": "final_report", "pdf_url": report_record["metadata"]["report_url"], "generated_at": str(timestamp_now()), "html_content": html_report }

    def _save_report(self, data: dict):
        if not self.db: return
        try:
            self.db.collection("reports").document(data["id"]).set(data)
        except: pass
