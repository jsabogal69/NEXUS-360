import sys
import os
import logging
from agents.shared.data_expert import DataExpert

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_extraction():
    print("--- TESTING DATA EXPERT EXTRACTION ---")
    
    # 1. Simulate CSV content (Raw text that user might paste)
    csv_text = """
ASIN,Product Name,Price,Monthly Sales,Brand,Revenue
B08XYZ1234,"Lego Architecture New York City, Build It Yourself Skyline Model Kit",49.99,1200,LEGO,59988
B07ABC9876,"Ravensburger 1000 Piece Puzzle - Harry Potter",19.95,850,Ravensburger,16957
B09DEF5432,"Buffalo Games - Darrell Bush - Canoe Lake - 1000 Piece Jigsaw Puzzle",14.99,2100,Buffalo Games,31479
    """.strip()
    
    print(f"Input Length: {len(csv_text)}")
    print("Input Preview:", csv_text[:100])
    
    # 2. Extract
    try:
        content_bytes = csv_text.encode('utf-8')
        result = DataExpert.extract_pricing_from_bytes(content_bytes, "manual_paste.csv")
        
        print("\n--- EXTRACTION RESULT ---")
        print(f"Has Real Data: {result.get('has_real_data')}")
        print(f"Total Products: {result.get('total_products')}")
        
        products = result.get('products', [])
        if products:
            print(f"\nTop 3 Products Found:")
            for i, p in enumerate(products[:3]):
                print(f"{i+1}. {p.get('title')[:50]}...")
                print(f"   ASIN: {p.get('asin')}")
                print(f"   Price: {p.get('price')}")
        else:
            print("❌ NO PRODUCTS EXTRACTED")
            
        return result
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_extraction()
