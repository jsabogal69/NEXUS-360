import asyncio
import json
import os
import sys

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from agents.nexus_4_strategist.core import Nexus4Strategist
from agents.nexus_2_scout.core import Nexus2Scout

async def test_transparency():
    print("\n--- Testing Market Transparency & Grounding ---")
    
    # 1. Scout Scan (Mock context for speed, but grounded)
    scout = Nexus2Scout()
    product_desc = "Cargador Gan 65W ultra-compacto"
    context = "El usuario busca un cargador de viaje que no se caliente y sea compatible con MacBook Pro."
    
    print(f"Scouting: {product_desc}...")
    scout_data = await scout.perform_osint_scan(product_desc, raw_text_context=context)
    
    # 2. Strategist Analysis
    strategist = Nexus4Strategist()
    ssot_mock = {
        "id": "mock-ssot",
        "scout_anchor": product_desc,
        "scout_data": scout_data,
        "analyzed_sources": ["test_doc.pdf"],
        "harvester_data": {"xray_data": {"has_real_data": False}}
    }
    
    print("Analyzing strategy...")
    strategy = await strategist.analyze_gaps(ssot_mock)
    
    # 3. Verify TAM Calculation Logic
    market_sizing = strategy.get("dynamic_verdict", {}).get("market_sizing", {})
    logic = market_sizing.get("logic", "MISSING")
    tam = market_sizing.get("tam", "MISSING")
    
    print(f"\nTAM: {tam}")
    print(f"Logic: {logic}")
    
    if "ASP" in logic and "*" in logic:
        print("✅ TAM logic is transparent and contains calculation formula.")
    else:
        print("❌ TAM logic is generic or missing formula.")
        
    # 4. Verify Grounding (Avatars)
    avatars = strategy.get("dynamic_verdict", {}).get("target_segments", [])
    print(f"\nAvatars Detected: {len(avatars)}")
    for av in avatars:
        print(f" - {av['name']}: {av['pain_points'][0]}")
        # Check for generic names
        if av['name'] in ["Early Adopters", "Quality Seekers"]:
            print(f" ⚠️ Avatar name '{av['name']}' might still be generic.")
            
    # 5. Verify Sanitization
    summary = strategy.get("partner_summary", "")
    if "fall primaril" in summary or "lead to" in summary.split('.')[-1]:
         print("❌ Sanitization failed, stutter detected.")
    else:
         print("✅ Sanitization check passed (no common stutters in summary).")

if __name__ == "__main__":
    asyncio.run(test_transparency())
