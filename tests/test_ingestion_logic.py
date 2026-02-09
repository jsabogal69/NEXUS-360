import pandas as pd
import io
from agents.shared.data_expert import DataExpert
import logging

# Setup basic logging to console
logging.basicConfig(level=logging.INFO)

def test_header_hunter():
    print("🧪 Testing DataExpert 'Header Hunter'...")
    
    # Simulating a helium10-style export with metadata at top
    csv_content = """Report Generated: 2026-02-03
Exported by: Nexus User
Filter: None

ASIN,Product Name,Price,Sales,Revenue,BSR,Reviews
B08XYZ123,"Real Product A",25.99,1000,25990,500,120
B09ABC456,"Real Product B",15.50,2000,31000,200,500
"""
    
    encoded_content = csv_content.encode('utf-8')
    
    # Process
    df = DataExpert.process_csv(encoded_content)
    
    print(f"📊 Columns Found: {df.columns.tolist()}")
    print(f"📄 Row Count: {len(df)}")
    
    # Check if it found the right headers
    if "price" in df.columns and "asin" in df.columns:
        print("✅ SUCCESS: Header Hunter found the correct columns.")
        
        # Test Extraction
        result = DataExpert.extract_xray_pricing(df, "test.csv")
        print(f"💰 Extraction Result: {result['total_products']} products found.")
        print(f"   First Product: {result['products'][0]['title']}")
        if result['products'][0]['title'] == "Real Product A":
            print("✅ SUCCESS: Data matched.")
        else:
            print("❌ FAILURE: Product title mismatch.")
            
    else:
        print("❌ FAILURE: Did not find expected headers.")

if __name__ == "__main__":
    test_header_hunter()
