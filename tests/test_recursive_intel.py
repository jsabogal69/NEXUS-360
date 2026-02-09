import asyncio
import logging
from agents.nexus_2_scout.core import Nexus2Scout
from agents.nexus_3_integrator.core import Nexus3Integrator
from agents.nexus_4_strategist.core import Nexus4Strategist
from agents.nexus_5_mathematician.core import Nexus5Mathematician
from agents.nexus_6_senior_partner.core import Nexus6SeniorPartner
from agents.nexus_7_architect.core import Nexus7Architect

async def test_recursive_intelligence():
    print("\n" + "="*50)
    print("🚀 INICIANDO TEST DE INTELIGENCIA RECURSIVA")
    print("="*50 + "\n")

    # --- PASO 1: GENERAR REPORTE ORIGINAL (BABY LAMP) ---
    print("📋 [FASE 1] Generando Análisis Original...")
    scout = Nexus2Scout()
    scout_data = await scout.perform_osint_scan("Baby Lamp Red Spectrum")
    
    integrator = Nexus3Integrator()
    ssot = await integrator.consolidate_data([scout_data["id"]], pre_fetched_docs={scout_data["id"]: scout_data})
    
    strategist = Nexus4Strategist()
    strategy = await strategist.analyze_gaps(ssot)
    
    math_agent = Nexus5Mathematician()
    math_results = await math_agent.calculate_roi_models(strategy)
    
    partner = Nexus6SeniorPartner()
    summary = await partner.synthesize_executive_summary(math_results, strategy)
    
    architect = Nexus7Architect()
    full_data = {
        "scout": scout_data,
        "integrator": ssot,
        "strategist": strategy,
        "mathematician": math_results,
        "senior_partner": summary
    }
    first_report = await architect.generate_report_artifacts(full_data)
    first_id = first_report["id"]
    print(f"✅ Reporte Original Guardado con ID: {first_id}")

    # --- PASO 2: USAR EL REPORTE COMO ENTRADA PARA UN SEGUNDO ANÁLISIS ---
    print("\n📋 [FASE 2] Iniciando Análisis Recursivo (Usando Reporte previo)...")
    
    # Simulating the second session where the user "uploads" the previous report
    new_scout_data = await scout.perform_osint_scan("Baby Lamp Q2 2026 Expansion")
    
    # The Integrator should now find the 'first_id' in the 'reports' collection
    # (In this mock environment, we might need to simulate the database find or ensure the Architect saved it)
    # Since we use Mock DB in shared/utils, it should be in memory.
    
    input_ids = [new_scout_data["id"], first_id]
    
    # In practice, we might not have 'first_report' in pre_fetched_docs if it's from DB,
    # but for local test we can pass it or rely on the Mock DB.
    # Let's rely on the Mock DB since Architect.generate_report_artifacts saves it.
    
    new_ssot = await integrator.consolidate_data(input_ids, pre_fetched_docs={new_scout_data["id"]: new_scout_data})
    
    new_strategy = await strategist.analyze_gaps(new_ssot)
    
    print("\n--- Verificando Continuidad Estratégica ---")
    gaps = new_strategy["strategic_gaps"]
    gaps_text = " ".join([g.get('gap', '') for g in gaps])
    
    if "Continuidad Estratégica" in gaps_text:
        print("✔ [RECURSIVIDAD] El sistema reconoció el informe previo y activó la continuidad estratégica.")
        print(f"   Insight detectado: {gaps[0]['gap'][:150]}...")
    else:
        print("✖ [ERROR] El sistema no reconoció el informe previo como dato de entrada.")
        print(f"   Gaps encontrados: {new_strategy['strategic_gaps']}")

    print("\n" + "="*50)
    print("✅ TEST COMPLETADO")
    print("="*50 + "\n")

if __name__ == "__main__":
    asyncio.run(test_recursive_intelligence())
