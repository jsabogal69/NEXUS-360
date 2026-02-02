
import asyncio
import os
import sys
import logging

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.shared.llm_intel import generate_market_intel

logging.basicConfig(level=logging.INFO)

async def test_scholar_audit():
    # Test with a common product
    niche = "Suplementos de Creatina Monohidratada"
    print(f"\n--- Testing Niche: {niche} ---")
    data = generate_market_intel(niche)
    scholar = data.get("scholar_audit", [])
    print(f"Scholar Audit Items: {len(scholar)}")
    for i, s in enumerate(scholar):
        print(f"[{i+1}] {s.get('source')}: {s.get('finding')[:100]}...")

    # Test with a more generic/simple product
    niche = "Espátula de cocina de silicona"
    print(f"\n--- Testing Niche: {niche} ---")
    data = generate_market_intel(niche)
    scholar = data.get("scholar_audit", [])
    print(f"Scholar Audit Items: {len(scholar)}")
    for i, s in enumerate(scholar):
        print(f"[{i+1}] {s.get('source')}: {s.get('finding')[:100]}...")

if __name__ == "__main__":
    asyncio.run(test_scholar_audit())
