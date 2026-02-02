import requests
import json

def check_api():
    try:
        r = requests.get("http://localhost:8000/api/reports")
        data = r.json()
        print(f"Status: {r.status_code}")
        print(f"Source: {data.get('source')}")
        print(f"Count: {data.get('count')}")
        
        reports = data.get("reports", [])
        if reports:
            print("\nFirst 3 reports in JSON:")
            print(json.dumps(reports[:3], indent=2))
        else:
            print("No reports found in JSON response")
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    check_api()
