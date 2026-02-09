import asyncio
import logging
from agents.nexus_2_scout.core import Nexus2Scout
from agents.nexus_3_integrator.core import Nexus3Integrator
from agents.nexus_4_strategist.core import Nexus4Strategist
from agents.nexus_5_mathematician.core import Nexus5Mathematician
from agents.nexus_6_senior_partner.core import Nexus6SeniorPartner
from agents.nexus_7_architect.core import Nexus7Architect

async def test_charger_niche():
    print("\n" + "="*50)
    print("🚀 INICIANDO TEST FORENSE: NICHO CHARGER 65W")
    print("="*50 + "\n")

    # 1. SCOUT
    scout = Nexus2Scout()
    context = "cargador 65W GaN adapter power"
    print(f"✔ [SCOUT] Investigando mercado para: {context}")
    scout_data = await scout.perform_osint_scan(context)
    
    # 2. INTEGRATOR (Simulating a session with "old" lamp files but NEW charger scout)
    integrator = Nexus3Integrator()
    input_ids = [scout_data["id"], "mock_old_lamp_file_id"]
    
    # Passing pre_fetched_docs to ensure Integrator picks the NEW scout_data
    pre_fetched = {
        scout_data["id"]: scout_data
    }
    
    filenames = ["ESTUDIO DE OPORTUNIDAD - BABY LAMP.pdf", "Lampara baby HiQ.xlsx"]
    print(f"✔ [INTEGRATOR] Consolidando fuentes (Mezcla controlada con pre-fetch)...")
    ssot = await integrator.consolidate_data(input_ids, filenames_override=filenames, pre_fetched_docs=pre_fetched)
    
    # 3. STRATEGIST
    strategist = Nexus4Strategist()
    print(f"✔ [STRATEGIST] Extrayendo brechas tácticas...")
    strategy = await strategist.analyze_gaps(ssot)
    
    # 4. MATHEMATICIAN
    math_agent = Nexus5Mathematician()
    print(f"✔ [MATHEMATICIAN] Modelando escenarios ROI...")
    math_results = await math_agent.calculate_roi_models(strategy)
    
    # 5. SENIOR PARTNER
    partner = Nexus6SeniorPartner()
    print(f"✔ [PARTNER] Generando síntesis ejecutiva...")
    summary = await partner.synthesize_executive_summary(math_results, strategy)
    
    # 6. ARCHITECT
    architect = Nexus7Architect()
    print(f"✔ [ARCHITECT] Renderizando Dossier Final Premium...")
    full_data = {
        "scout": scout_data,
        "integrator": ssot,
        "strategy": strategy,
        "mathematician": math_results,
        "partner": summary
    }
    # Fix: Architect.generate_report_artifacts is an async method decorated with report_agent_activity
    report = await architect.generate_report_artifacts(full_data)
    
    print("\n" + "="*50)
    print("✅ TEST COMPLETADO CON ÉXITO")
    print(f"📊 REPORTE GENERADO: {report.get('pdf_url', 'N/A')}")
    
    html = report['html_content']
    print("\n--- Verificando Coherencia ---")
    if "Cargadores GaN" in html or "Charger" in html:
         print("✔ [COHERENCIA] El reporte se enfoca en CARGADORES GAN.")
    else:
         print("✖ [ERROR] El reporte conserva datos de LÁMPARAS.")
         
    if "Baby Sleep Tech" in html or "Lámpara LED" in html:
         print("✖ [ERROR] Se detectaron Unit Economics contaminados.")
    else:
         print("✔ [COHERENCIA] Unit Economics limpios de casos anteriores.")
         
    if "Mercado Detectado" in html:
         print("✖ [ADVERTENCIA] Se encontró placeholder 'Mercado Detectado'.")
    else:
         print("✔ [COHERENCIA] Placeholders erradicados.")
    print("="*50 + "\n")

if __name__ == "__main__":
    asyncio.run(test_charger_niche())
