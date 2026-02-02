from agents.shared.utils import get_db
import json

def audit_reports():
    db = get_db()
    if not db:
        print("No DB connection")
        return
    
    reports_ref = db.collection("reports").order_by("timestamp", direction="DESCENDING").limit(10)
    docs = reports_ref.stream()
    
    print("Auditing latest 10 reports:")
    for doc in docs:
        data = doc.to_dict()
        report_id = doc.id
        title = data.get("metadata", {}).get("title")
        url = data.get("metadata", {}).get("report_url")
        print(f"ID: {report_id} | Title: {title} | URL: {url}")

if __name__ == "__main__":
    audit_reports()
