"""
═══════════════════════════════════════════════════════════════════════════════
NEXUS-360 REPORT OPTIMIZER v3.1
═══════════════════════════════════════════════════════════════════════════════
Módulo de optimización de estructura de reportes.
Reorganiza las secciones para un flujo ejecutivo más impactante.

ESTRUCTURA OPTIMIZADA:
I.   VEREDICTO EJECUTIVO - Lo más importante primero
II.  OPORTUNIDAD DE MERCADO - TAM/SAM + Buyer Personas + Pricing
III. ANÁLISIS COMPETITIVO - TOP 10 + Brechas
IV.  INSIGHTS DEL CONSUMIDOR - Reviews + Social + Pain Points
V.   UNIT ECONOMICS - Amazon Fees + Finanzas + Escenarios
VI.  ESTRATEGIA & ROADMAP - Estacionalidad + Plan
VII. COMPLIANCE & RIESGOS - Risk Matrix + Auditoría
VIII.APÉNDICE - Fuentes + Senior Partner
═══════════════════════════════════════════════════════════════════════════════
"""

import logging

logger = logging.getLogger(__name__)


def get_optimized_report_structure() -> dict:
    """
    Retorna la estructura optimizada de secciones del reporte.
    Cada sección incluye: orden, nombre, badge, contenido_keys.
    """
    return {
        "sections": [
            {
                "id": 1,
                "name": "I. Veredicto Ejecutivo",
                "badge": "NEXUS-360",
                "description": "Decisión estratégica y próximos pasos",
                "includes": ["verdict", "product_proposal", "differentiators", "actions"],
                "priority": "CRITICAL"
            },
            {
                "id": 2,
                "name": "II. Oportunidad de Mercado",
                "badge": "Market Intelligence",
                "description": "Dimensionamiento y segmentación",
                "includes": ["tam_sam_som", "buyer_personas", "price_tiers"],
                "priority": "HIGH"
            },
            {
                "id": 3,
                "name": "III. Análisis Competitivo",
                "badge": "Scout",
                "description": "TOP 10 y brechas estratégicas",
                "includes": ["top_10_matrix", "gaps", "opportunities"],
                "priority": "HIGH"
            },
            {
                "id": 4,
                "name": "IV. Insights del Consumidor",
                "badge": "Consumer Intelligence",
                "description": "Reviews, social listening, pain points",
                "includes": ["reviews_analysis", "social_listening", "pain_points", "usp"],
                "priority": "HIGH"
            },
            {
                "id": 5,
                "name": "V. Unit Economics & Viabilidad",
                "badge": "Mathematician",
                "description": "Fees, márgenes, escenarios",
                "includes": ["amazon_fees", "financial_scenarios", "stress_test", "three_scenarios"],
                "priority": "HIGH"
            },
            {
                "id": 6,
                "name": "VI. Estrategia Comercial & Roadmap",
                "badge": "Strategist",
                "description": "Estacionalidad y plan de ejecución",
                "includes": ["seasonality", "calendar", "roadmap"],
                "priority": "MEDIUM"
            },
            {
                "id": 7,
                "name": "VII. Compliance, Riesgos & Gobernanza",
                "badge": "Guardian",
                "description": "Risk matrix y auditoría de cumplimiento",
                "includes": ["risk_matrix", "compliance_audit", "veto_check"],
                "priority": "MEDIUM"
            },
            {
                "id": 8,
                "name": "VIII. Apéndice: Fuentes & Metodología",
                "badge": "Harvester",
                "description": "Trazabilidad de datos y resumen ejecutivo",
                "includes": ["source_cards", "senior_partner_summary"],
                "priority": "LOW"
            }
        ],
        "metadata": {
            "version": "3.1",
            "optimization_type": "executive_flow",
            "rationale": "Flujo ejecutivo que prioriza decisión > oportunidad > competencia > consumidor > finanzas > ejecución > riesgos > apéndice"
        }
    }


def generate_personas_summary_html(buyer_personas: list) -> str:
    """
    Genera HTML resumido de buyer personas para la sección de oportunidad de mercado.
    Solo muestra los nombres y un dato clave de cada uno.
    """
    if not buyer_personas:
        return '<span style="color:#64748b; font-style:italic;">Ejecutar análisis para generar personas</span>'
    
    colors = ["#6366f1", "#22c55e", "#f59e0b"]
    icons = ["👩‍💼", "🛒", "🚀"]
    
    html = ""
    for i, persona in enumerate(buyer_personas[:3]):
        color = colors[i % len(colors)]
        icon = icons[i % len(icons)]
        name = persona.get("name", f"Persona {i+1}")
        demographics = persona.get("demographics", {})
        age = demographics.get("age_range", "25-45")
        income = demographics.get("income_level", "Variable")
        
        html += f'''
        <div style="background:white; border:1px solid {color}33; border-radius:12px; padding:15px; flex:1; min-width:180px;">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                <span style="font-size:1.5rem;">{icon}</span>
                <div style="font-weight:700; color:{color}; font-size:0.9rem;">{name}</div>
            </div>
            <div style="font-size:0.75rem; color:#64748b;">📅 {age} | 💰 {income}</div>
        </div>
        '''
    
    return html


def optimize_section_order(sections_data: dict) -> list:
    """
    Dado un diccionario con datos de secciones, retorna una lista ordenada
    según la estructura optimizada.
    """
    structure = get_optimized_report_structure()
    ordered = []
    
    for section in structure["sections"]:
        section_content = {
            "id": section["id"],
            "name": section["name"],
            "badge": section["badge"],
            "priority": section["priority"],
            "content_keys": section["includes"],
            "has_data": False
        }
        
        # Verificar si hay datos para esta sección
        for key in section["includes"]:
            if key in sections_data and sections_data[key]:
                section_content["has_data"] = True
                break
        
        ordered.append(section_content)
    
    return ordered


def get_section_css_class(priority: str) -> str:
    """
    Retorna la clase CSS según la prioridad de la sección.
    """
    priority_classes = {
        "CRITICAL": "section-critical",
        "HIGH": "section-high",
        "MEDIUM": "section-medium",
        "LOW": "section-low"
    }
    return priority_classes.get(priority, "section-medium")


def generate_optimized_header_html(report_id: str, niche_title: str, timestamp: str) -> str:
    """
    Genera el header optimizado del reporte.
    """
    return f'''
    <header style="border-bottom: 3px solid #0f172a; padding-bottom: 30px; margin-bottom: 40px; display: flex; justify-content: space-between; align-items: flex-end;">
        <div>
            <span style="color:#6366f1; font-weight:bold; letter-spacing:3px; font-size:0.8rem;">NEXUS-360 EXECUTIVE DOSSIER</span>
            <span style="color:#94a3b8; font-size:0.7rem; margin-left:10px;">// {report_id}</span>
            <h1 style="margin:10px 0 0 0; font-size:2.2rem; color:#0f172a; font-family:Georgia, serif;">{niche_title}</h1>
        </div>
        <div style="text-align:right;">
            <div style="background:#dc2626; color:white; padding:5px 12px; border-radius:6px; font-weight:bold; font-size:0.7rem; display:inline-block; margin-bottom:5px;">CONFIDENCIAL</div>
            <div style="font-size:0.75rem; color:#64748b;">{timestamp}</div>
        </div>
    </header>
    '''


def generate_optimized_footer_html(year: str) -> str:
    """
    Genera el footer optimizado del reporte.
    """
    return f'''
    <footer style="margin-top:60px; text-align:center; padding:30px 0; border-top:2px solid #e2e8f0;">
        <div style="display:flex; justify-content:center; align-items:center; gap:30px; margin-bottom:15px;">
            <div style="font-size:0.7rem; color:#94a3b8;">
                <span style="font-weight:800; color:#6366f1;">NEXUS-360</span> EXECUTIVE DOSSIER v3.1
            </div>
            <div style="width:1px; height:15px; background:#e2e8f0;"></div>
            <div style="font-size:0.65rem; color:#94a3b8;">
                ESTRUCTURA OPTIMIZADA PARA DECISIONES EJECUTIVAS
            </div>
        </div>
        <div style="font-size:0.6rem; color:#cbd5e1;">
            © {year} NEXUS-360 Advanced Strategy Unit | Documento generado automáticamente
        </div>
    </footer>
    '''


def validate_data_completeness(data: dict) -> dict:
    """
    Valida la completitud de los datos y retorna un reporte de validación.
    """
    required_fields = {
        "verdict": ["title", "text"],
        "tam_sam_som": ["tam", "sam", "som"],
        "top_10": ["products"],
        "buyer_personas": [],
        "reviews_analysis": ["rating_distribution"],
        "amazon_fees": ["referral_fee_pct"],
        "financial_scenarios": ["scenarios"]
    }
    
    validation = {
        "is_complete": True,
        "missing_fields": [],
        "completeness_score": 0
    }
    
    total_fields = 0
    complete_fields = 0
    
    for section, fields in required_fields.items():
        section_data = data.get(section, {})
        
        if not section_data:
            validation["missing_fields"].append(section)
            validation["is_complete"] = False
        else:
            complete_fields += 1
            
            for field in fields:
                total_fields += 1
                if field in section_data:
                    complete_fields += 1
                else:
                    validation["missing_fields"].append(f"{section}.{field}")
        
        total_fields += 1
    
    validation["completeness_score"] = int((complete_fields / total_fields) * 100) if total_fields > 0 else 0
    
    return validation


# Constantes de estilo para consistencia
SECTION_STYLES = {
    "container": "background:white; border-radius:16px; padding:30px; margin-bottom:30px; box-shadow:0 4px 6px -1px rgba(0,0,0,0.07);",
    "title": "font-size:1.4rem; font-weight:800; color:#0f172a; margin:0 0 20px 0; padding-bottom:15px; border-bottom:2px solid #e2e8f0;",
    "badge": "background:#6366f1; color:white; padding:3px 10px; border-radius:20px; font-size:0.65rem; font-weight:700; margin-left:10px;",
    "grid_2col": "display:grid; grid-template-columns: 1fr 1fr; gap:25px;",
    "grid_3col": "display:grid; grid-template-columns: repeat(3, 1fr); gap:20px;",
    "card": "background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:20px;",
    "card_accent": "background:linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border:2px solid #3b82f6; border-radius:16px; padding:25px;",
}


logger.info("[ReportOptimizer] Module loaded - v3.1 Executive Flow Structure")
