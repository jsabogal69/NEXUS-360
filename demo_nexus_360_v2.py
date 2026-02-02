import asyncio
import logging
import sys
import os
import json

# Ensure agents package is importable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.nexus_4_strategist.core import Nexus4Strategist
from agents.nexus_5_mathematician.core import Nexus5Mathematician
from agents.nexus_8_guardian.core import Nexus8Guardian
from agents.nexus_6_senior_partner.core import Nexus6SeniorPartner
from agents.nexus_7_architect.core import Nexus7Architect

# Disable excessive logging for cleaner demo
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("DEMO")

async def run_demo():
    print("="*60)
    print("🚀 NEXUS-360 V2.1: DEMO FULL SCOPE (CERO SIMPLIFICACIÓN)")
    print("="*60)

    strategist = Nexus4Strategist()
    mathematician = Nexus5Mathematician()
    guardian = Nexus8Guardian()
    partner = Nexus6SeniorPartner()
    architect = Nexus7Architect()

    # 1. ESCENARIO VIABLE: "Niche Baby Monitor with AI"
    print("\n🔹 CASO 1: PRODUCTO VIABLE (Monitor de Bebé con IA)")
    
    # Mock data simulate SSOT from Integrator
    ssot_viable = {
        "id": "ssot_viable_001",
        "product_description": "Smart AI Baby Monitor with Breathing Detection and Night Vision",
        "market_stats": {"avg_price": 149.99, "category": "Baby Care"},
        "scout_anchor": "baby monitor ai",
        "top_features": ["4K Resolution", "Local AI processing", "No monthly fees"],
        "pain_points": [
            {"pain": "Poor battery life", "importance": 9.5, "satisfaction": 3.2},
            {"pain": "Delayed notifications", "importance": 9.8, "satisfaction": 4.1},
            {"pain": "Privacy concerns/Cloud hacking", "importance": 9.2, "satisfaction": 2.5}
        ]
    }

    print("Step 1: Strategist analyzing gaps...")
    strategy_viable = await strategist.analyze_gaps(ssot_viable)
    
    print("Step 2: Mathematician calculating ROI & Opportunity Scores...")
    strategy_viable['pain_points'] = ssot_viable['pain_points'] 
    math_data_viable = await mathematician.calculate_roi_models(strategy_viable)
    
    print("Step 3: Guardian performing Compliance & Veto check...")
    audit_viable = await guardian.perform_compliance_audit(strategy_viable, mathematician_data=math_data_viable)

    print("\nStep 4: Architect generating FULL SCOPE report...")
    full_data_viable = {
        "harvester": {"source": "Demo Full Scope 2026"},
        "scout": {
            "product_anchor": "baby monitor ai",
            "lightning_bolt_opportunity": {
                "is_lightning": True,
                "velocity_score": "ALTA (9.2/10)",
                "reason": "Gap de privacidad masivo en competidores actuales. Demanda por soluciones No-Cloud subiendo 45% trimestral."
            },
            "top_10_products": [
                {"rank": 1, "name": "Nanit Pro 4K", "rating": 4.8, "reviews": 12500, "price": 299, "adv": "Best Tracking", "vuln": "Suscripción obligatoria", "gap": "Hardware alto costo"},
                {"rank": 2, "name": "Owlet Cam 2", "rating": 4.6, "reviews": 8200, "price": 159, "adv": "Pulse-Ox integration", "vuln": "Dependencia del Cloud", "gap": "Privacidad"},
                {"rank": 3, "name": "Eufy SpaceView", "rating": 4.5, "reviews": 15000, "price": 129, "adv": "Local viewing", "vuln": "Baja resolución", "gap": "Calidad Imagen"},
                {"rank": 4, "name": "Lollipop Baby", "rating": 4.2, "reviews": 3400, "price": 149, "adv": "Flexible design", "vuln": "Montaje frágil", "gap": "Durabilidad"},
                {"rank": 5, "name": "Arlo Baby", "rating": 4.0, "reviews": 5600, "price": 199, "adv": "Smart Home integration", "vuln": "Software lento", "gap": "UX"}
            ],
            "scholar_audit": [
                {"source": "Academy of Pediatrics", "finding": "Digital noise reduction in baby monitors reduces parental stress alerts by 40%.", "relevance": "High Impact"},
                {"source": "Cybersecurity Institute", "finding": "Local processing is the 2026 gold standard for 'Smart Home' privacy.", "relevance": "Critical Security"}
            ],
            "social_listening": {
                "emotional_analysis": {
                    "frustration": "Hartos de falsas alarmas que despiertan a toda la casa.",
                    "desire": "Queremos tecnología que no envíe videos a servidores externos.",
                    "humor": "Cuando el sensor de llanto se activa con el ronquido del padre.",
                    "nostalgia": "Extrañamos la simplicidad de los monitores analógicos.",
                    "skepticism": "No creen las promesas de 'IA avanzada' sin evidencia."
                },
                "pain_keywords": [
                    {"keyword": "baby monitor no wifi", "volume": "High", "search_intent": "Transactional", "opportunity": "Niche Gap"},
                    {"keyword": "best baby monitor 2026", "volume": "Rising", "search_intent": "Informational", "opportunity": "SEO Target"},
                    {"keyword": "baby monitor privacy", "volume": "Medium", "search_intent": "Investigational", "opportunity": "Content Gap"},
                    {"keyword": "monitor bebe sin suscripcion", "volume": "High", "search_intent": "Transactional", "opportunity": "Latam Market"},
                    {"keyword": "baby monitor false alarms fix", "volume": "High", "search_intent": "Problem-Solving", "opportunity": "Tutorial Content"}
                ],
                "competitor_gaps": [
                    {"competitor": "Nanit Pro", "ignored_issue": "Obligación de suscripción mensual", "user_frustration": "Pagué $300 y aún quieren $10/mes extra"},
                    {"competitor": "Owlet Cam", "ignored_issue": "Dependencia total del servidor cloud", "user_frustration": "Si se cae su servidor, perdemos el video"},
                    {"competitor": "Eufy SpaceView", "ignored_issue": "Resolución baja en modo nocturno", "user_frustration": "A las 3am no veo nada claramente"}
                ],
                "white_space_topics": [
                    "Monitores para gemelos (doble cuna)",
                    "Integración con sistemas de domótica local",
                    "Alertas personalizables por tipo de ruido",
                    "Modo viaje con batería extendida",
                    "Privacidad HIPAA para datos de bebé"
                ],
                "cultural_vibe": "Comunidad escéptica hacia las marcas 'tech-first' pero entusiasta por soluciones que priorizan privacidad. Tono protector y cauteloso típico de padres primerizos.",
                "tiktok_trends": "#BabyMonitorHacks 15M vistas, @TechDadReviews 500K seguidores, formato 'unboxing + test nocturno' domina",
                "reddit_insights": "r/beyondthebump muy activo con quejas de suscripciones. r/homeassistant busca monitores integrables. Opinión dominante: local > cloud.",
                "youtube_search_gaps": "'Cómo eliminar suscripción de monitor Nanit' sin respuestas de calidad. 'Monitor local sin internet' < 5 videos relevantes.",
                "consumer_desire": "Un monitor 4K con IA local, sin suscripciones, que funcione offline y respete la privacidad absoluta del bebé."
            },
            "content_opportunities": {
                "garyvee_style": [
                    {"idea": "El SCAM de las suscripciones en monitores de bebé", "format": "Rant Video 60s", "hook": "Te vendieron un monitor de $300 y TODAVÍA quieren $10/mes", "emotional_trigger": "Indignación"},
                    {"idea": "Por qué tu monitor envía videos de tu bebé a China", "format": "Storytelling/Exposé", "hook": "Tu bebé está en un servidor en Shanghai ahora mismo", "emotional_trigger": "Miedo/Protección"},
                    {"idea": "Padres Tech vs Padres Privacidad: Quién gana?", "format": "Debate POV", "hook": "Tu suegra tiene razón sobre los gadgets", "emotional_trigger": "Conflicto familiar"}
                ],
                "patel_style": [
                    {"idea": "Guía completa: Mejores monitores de bebé 2026 sin suscripción", "target_keyword": "baby monitor without subscription", "search_intent": "Comparison", "content_gap": "No existe guía actualizada sin afiliados obvios"},
                    {"idea": "Cómo configurar un monitor de bebé offline en 10 minutos", "target_keyword": "offline baby monitor setup", "search_intent": "Tutorial", "content_gap": "Videos existentes son de 2022"},
                    {"idea": "Baby Monitor Security: Lo que las marcas no te dicen", "target_keyword": "baby monitor security risks", "search_intent": "Educational", "content_gap": "Contenido técnico pero accesible para padres"}
                ]
            },

            "confidence_tag": "🟢 POE VALIDATED",
            "sales_intelligence": {
                "market_share_by_brand": [
                    {"brand": "Nanit", "share": 35},
                    {"brand": "Owlet", "share": 25},
                    {"brand": "Eufy", "share": 20},
                    {"brand": "Others", "share": 20}
                ],
                "seasonality": {
                    "peaks": [{"month": "Noviembre", "event": "Black Friday", "impact": "Extreme", "strategy": "Max inventory boost"}],
                    "strategy_insight": "El mercado de Baby Monitors pica en Q4 por regalos de fin de año y baby showers estacionales."
                }
            }
        },
        "integrator": {
            "source_metadata": [
                {"name": "Intel_Global_Baby_2026.pdf", "type": "pdf", "summary": "Tendencias de natalidad y tech"},
                {"name": "Competitor_Matrix_Raw.csv", "type": "csv", "summary": "Pricing y Ratings Amazon"},
                {"name": "Sentiment_Deep_Dive.json", "type": "intel", "summary": "2,000 reseñas analizadas"}
            ],
            "errc_grid": {
                "eliminate": ["Monthly Subscriptions", "Cloud Storage Fees"],
                "reduce": ["Lag", "False Positives", "Price"],
                "raise": ["Resolution (4K)", "Local AI Accuracy"],
                "create": ["Edge-AI Breathing Sensor", "Privacy-First Branding"]
            }
        },
        "strategist": strategy_viable,
        "mathematician": math_data_viable,
        "senior_partner": {
            "executive_summary": "Oportunidad quirúrgica en el nicho de monitores de bebé mediante la eliminación del 'Cloud-Tax' y la implementación de IA local. Los márgenes son robustos y el gap de privacidad es el mayor pain-point sin resolver.",
            "creative_copy": {
                "bullet_points": [
                    "Tu Video, Tu Casa: Procesamiento 100% Local sin Nube.",
                    "Precisión Quirúrgica: Identifica humanos vs mascotas al instante.",
                    "Libertad Total: Cero cuotas mensuales de por vida."
                ]
            }
        },
        "guardian": audit_viable,
        "inspector": {
            "logistics_viability": {
                "bopis": {"status": "Válido", "reason": "Apto para recogida en tienda"},
                "mcf": {"status": "Aprobado", "reason": "Cumple estándares de Amazon FBA"}
            }
        }
    }
    
    report = await architect.generate_report_artifacts(full_data_viable)
    print(f"   - Report Generated: {report.get('pdf_url')}")
    
    # Generate Executive Brief (1-Page Summary)
    print("Step 5: Generating Executive Brief (1-Page Decision Canvas)...")
    report_id = report.get('pdf_url', '').split('/')[-1].replace('.html', '').replace('report_', '')
    brief = await architect.generate_executive_brief(full_data_viable, full_report_id=report_id)
    print(f"   - Executive Brief: /dashboard/reports/brief_{brief.get('brief_id')}.html")
    print(f"   - Verdict: {brief.get('verdict')} | Confidence: {brief.get('confidence')}%")


    # 2. ESCENARIO VETO: "Generic iPhone Charger"
    print("\n" + "="*60)
    print("\n🔹 CASO 2: PRODUCTO DE RIESGO (Escenario de Veto)")
    
    # Mock data to trigger veto
    math_data_risk = {
        "scenarios": {},
        "margin_validation": {"conservative_margin": 12.5, "passes_threshold": False}
    }
    strategy_risk = {
        "id": "strat_risk_002",
        "scout_anchor": "baby generic charger (dummy)", 
        "dynamic_verdict": {"target_price": 9.99},
    }

    print("Step 1: Guardian validation...")
    audit_risk = await guardian.perform_compliance_audit(strategy_risk, mathematician_data=math_data_risk)

    print("\n🚫 RESULTADOS CASO 2:")
    if audit_risk.get("veto_triggered"):
        print(f"   - Guardian Veto: ❌ VETOED")
        print(f"   - Reasoning: {audit_risk.get('veto_message')}")
    else:
        print(f"   - Guardian Veto: ✔ APPROVED (Unexpected)")

    print("\n" + "="*60)
    print("🏁 FIN DE LA DEMOSTRACIÓN V2.1")

if __name__ == "__main__":
    asyncio.run(run_demo())
