import asyncio
import os
import sys
from agents.nexus_10_guardian.core import Nexus10Guardian

# Ensure agents package is importable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_dynamic_audit():
    guardian = Nexus10Guardian()
    
    # Test case 1: 65W GaN Charger (Electronics)
    print("\n--- Testing 65W GaN Charger ---")
    strategy_data_electronics = {"scout_anchor": "Cargador GaN 65W USB-C de pared"}
    audit_electronics = await guardian.perform_compliance_audit(strategy_data_electronics)
    
    print(f"Risk Level: {audit_electronics['risk_level']}")
    print(f"Compliance Score: {audit_electronics['compliance_score']}%")
    print(f"Standards ({audit_electronics['total_standards']}):")
    for std in audit_electronics['audits']:
        print(f"- {std['std']} ({std['status']})")
    
    # Test case 2: Something that definitely isn't fitness, e.g. a book or generic gift
    print("\n--- Testing Generic Gift (Lámpara Luna) ---")
    strategy_data_generic = {"scout_anchor": "Lámpara Luna Personalizada con Foto"}
    audit_generic = await guardian.perform_compliance_audit(strategy_data_generic)
    
    print(f"Risk Level: {audit_generic['risk_level']}")
    print(f"Compliance Score: {audit_generic['compliance_score']}%")
    print(f"Standards ({audit_generic['total_standards']}):")
    for std in audit_generic['audits']:
        print(f"- {std['std']} ({std['status']})")

if __name__ == "__main__":
    asyncio.run(test_dynamic_audit())
