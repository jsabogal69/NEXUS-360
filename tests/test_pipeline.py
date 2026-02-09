import asyncio
import logging
from agents.nexus_1_harvester.core import Nexus1Harvester
from agents.nexus_8_guardian.core import Nexus8Guardian
from agents.nexus_2_scout.core import Nexus2Scout
from agents.nexus_3_integrator.core import Nexus3Integrator
from agents.nexus_4_strategist.core import Nexus4Strategist
from agents.nexus_5_mathematician.core import Nexus5Mathematician
from agents.nexus_6_senior_partner.core import Nexus6SeniorPartner
from agents.nexus_7_architect.core import Nexus7Architect

# Disable excessive logging for test
logging.getLogger("NEXUS-GATEWAY").setLevel(logging.WARNING)

async def run_full_validation():
    print("🚀 INICIANDO VALIDACIÓN DEL MOTOR NEXUS-360...")
    
    try:
        # 1. HARVESTER
        harvester = Nexus1Harvester()
        print("✔ Cargando Harvester...")
        
        # 2. SCOUT (Market Intel)
        print("✔ Ejecutando Scout (Inteligencia de Mercado)...")
        scout = Nexus2Scout()
        findings = await scout.perform_osint_scan("Cargador GaN 65W")
        
        # 3. INTEGRATOR
        print("✔ Consolidando Datos (Integrator)...")
        integrator = Nexus3Integrator()
        ssot = await integrator.consolidate_data(["doc_mock_1"], ["ADAPTADOR_65W_TEST.pdf"], {"folder_name": "Test Niche"})
        
        # 4. STRATEGIST
        print("✔ Generando Estrategia (Strategist)...")
        strategist = Nexus4Strategist()
        strategy = await strategist.analyze_gaps(ssot)
        
        # 5. MATHEMATICIAN
        print("✔ Calculando ROI (Mathematician)...")
        math_agent = Nexus5Mathematician()
        models = await math_agent.calculate_roi_models(strategy)
        
        # 6. SENIOR PARTNER
        print("✔ Redactando Síntesis (Senior Partner)...")
        partner = Nexus6SeniorPartner()
        summary = await partner.synthesize_executive_summary(models, strategy)
        
        # 7. ARCHITECT
        print("✔ Construyendo Dossier Final (Architect)...")
        architect = Nexus7Architect()
        full_data = {
            "harvester": {"files": 1},
            "scout": findings,
            "integrator": ssot,
            "strategist": strategy,
            "mathematician": models,
            "senior_partner": summary
        }
        report = await architect.generate_report_artifacts(full_data)
        
        print("\n✅ VALIDACIÓN EXITOSA")
        print(f"📊 Reporte Generado en: {report['pdf_url']}")
        print("---")
        print(f"Veredicto: {strategy['dynamic_verdict']['title']}")
        print(f"Propuesta: {models['scenarios']['kit_premium']['name']}")
        
    except Exception as e:
        print(f"\n❌ ERROR EN LA CADENA: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_full_validation())
