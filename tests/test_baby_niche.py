import asyncio
import logging
import os
from agents.nexus_1_harvester.core import Nexus1Harvester
from agents.nexus_10_guardian.core import Nexus10Guardian
from agents.nexus_2_scout.core import Nexus2Scout
from agents.nexus_3_integrator.core import Nexus3Integrator
from agents.nexus_4_strategist.core import Nexus4Strategist
from agents.nexus_5_mathematician.core import Nexus5Mathematician
from agents.nexus_6_senior_partner.core import Nexus6SeniorPartner
from agents.nexus_7_architect.core import Nexus7Architect

# Disable excessive logging for test
logging.getLogger("NEXUS-GATEWAY").setLevel(logging.WARNING)

async def run_full_validation():
    print("\n" + "="*50)
    print("🚀 INICIANDO TEST FORENSE: NICHO BABY SLEEP TECH")
    print("="*50 + "\n")
    
    try:
        # TEST CONTEXT (Parámetro Rector)
        product_context = "Lámpara de noche para bebé con espectro rojo, silicona médica y sensor de llanto IA."
        
        # 1. SCOUT (Market Intel) - Testing new niche detection
        print("✔ [SCOUT] Investigando mercado para: " + product_context)
        scout = Nexus2Scout()
        findings = await scout.perform_osint_scan(product_context)
        print(f"   ∟ Nicho Detectado: {findings['product_anchor']}")
        print(f"   ∟ Competidores: {len(findings['top_10_products'])} líderes identificados.")
        
        # 2. INTEGRATOR - Testing new descriptive summaries
        print("✔ [INTEGRATOR] Consolidando fuentes y trazabilidad...")
        integrator = Nexus3Integrator()
        # Mocking file list from the user's latest request for summary testing
        mock_files = [
            "NicheDetailsSearchTermsTab_1_9_2026.csv",
            "ESTUDIO DE OPORTUNIDAD - BABY LAMP",
            "NicheDetailsProductsTab_1_9_2026",
            "NicheDetailsProductsTab_1_9_2026.csv",
            "Lampara baby HiQ",
            "Xray_Keyword2026-01-09.csv",
            "serpTable2026-01-09.csv",
            "Screenshot 2026-01-09 at 7.25.21 AM.png",
            "Screenshot 2026-01-09 at 7.25.10 AM.png",
            "NichesProductAppears_1_9_2026.csv",
            "AsinExplorerSearchResults_1_9_2026.csv"
        ]
        ssot = await integrator.consolidate_data([f"mock_id_{i}" for i in range(len(mock_files))], mock_files, {"scout_anchor": findings['product_anchor']})
        
        # 3. STRATEGIST - Testing Baby Niche logic
        print("✔ [STRATEGIST] Extrayendo brechas tácticas...")
        strategist = Nexus4Strategist()
        strategy = await strategist.analyze_gaps(ssot)
        print(f"   ∟ Veredicto: {strategy['dynamic_verdict']['title']}")
        
        # 4. MATHEMATICIAN - Testing Baby Tech financial model
        print("✔ [MATHEMATICIAN] Modelando escenarios ROI...")
        math_agent = Nexus5Mathematician()
        models = await math_agent.calculate_roi_models(strategy)
        print(f"   ∟ Margen Kit Recomendado: {models['scenarios']['kit_premium']['margin_pct']}%")
        
        # 5. SENIOR PARTNER
        print("✔ [PARTNER] Generando síntesis ejecutiva...")
        partner = Nexus6SeniorPartner()
        summary = await partner.synthesize_executive_summary(models, strategy)
        
        # 6. ARCHITECT - Generating the final masterpiece
        print("✔ [ARCHITECT] Renderizando Dossier Final Premium...")
        architect = Nexus7Architect()
        full_data = {
            "harvester": {"files": len(mock_files)},
            "scout": findings,
            "integrator": ssot,
            "strategist": strategy,
            "mathematician": models,
            "senior_partner": summary
        }
        report = await architect.generate_report_artifacts(full_data)
        
        print("\n" + "="*50)
        print("✅ TEST COMPLETADO CON ÉXITO")
        print(f"📊 REPORTE GENERADO: {report['pdf_url']}")
        print("   (Verifica en agents/static/reports/...)")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"\n❌ FALLA EN LA TUBERÍA: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_full_validation())
