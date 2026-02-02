from agents.shared.utils import get_db
import json

def thorough_audit():
    db = get_db()
    if not db:
        print("No DB connection")
        return
    
    collections = ["reports", "nexus_archive"]
    for coll in collections:
        print(f"\n--- Auditing collection: {coll} ---")
        ref = db.collection(coll).order_by("timestamp" if coll == "reports" else "created_at", direction="DESCENDING").limit(20)
        docs = ref.stream()
        
        for doc in docs:
            data = doc.to_dict()
            metadata = data.get("metadata", {})
            if isinstance(metadata, list):
                 print(f"ID: {doc.id} | WARNING: metadata is a LIST: {metadata}")
                 continue
            
            url = metadata.get("report_url")
            id_field = data.get("id") or data.get("case_id")
            
            if not url:
                print(f"ID: {doc.id} | MISSING URL | Keys: {list(data.keys())} | Metadata Keys: {list(metadata.keys()) if metadata else 'None'}")
            else:
                print(f"ID: {doc.id} | URL: {url}")

if __name__ == "__main__":
    thorough_audit()
