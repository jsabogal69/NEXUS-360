import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum
import uuid

# --- CONFIGURATION ---
PROJECT_ID = "nexus-360-suite" 
CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "serviceAccountKey.json")

# --- FIREBASE INIT ---
# --- MOCK FIRESTORE FOR DEV ---
class MockDocument:
    def __init__(self, data): self.data = data; self.exists = True
    def to_dict(self): return self.data

class MockCollection:
    def __init__(self, storage, name): self.storage = storage; self.name = name
    def document(self, doc_id):
        class DocRef:
            def __init__(self, s, n, i): self.s = s; self.n = n; self.i = i
            def set(self, data): 
                if self.n not in self.s: self.s[self.n] = {}
                self.s[self.n][self.i] = data
            def get(self):
                data = self.s.get(self.n, {}).get(self.i)
                return MockDocument(data) if data else type('EmptyDoc', (), {'exists': False})()
        return DocRef(self.storage, self.name, doc_id)

class MockFirestore:
    _storage = {}
    def collection(self, name): return MockCollection(self._storage, name)

def get_db():
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        print(f"[ERROR] Firebase Init Failed: {e}. Falling back to In-Memory MockDB.")
        return MockFirestore()

# --- SHARED TYPES ---
class AgentRole(Enum):
    HARVESTER = "NEXUS-1"
    GUARDIAN = "NEXUS-8"

class ValidationStatus(Enum):
    PENDING = "pending"
    VALIDATED = "validated"
    REJECTED = "rejected"

def generate_id() -> str:
    return str(uuid.uuid4())

def timestamp_now():
    return datetime.utcnow()
# --- AGENT ACTIVITY REPORTING ---
import json
from datetime import datetime

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)
LOG_PATH = os.path.join(REPORTS_DIR, "agent_activity.log")

import inspect

def report_agent_activity(func):
    """Decorator to log human input and agent task description. Makes the function async."""
    async def wrapper(self, *args, **kwargs):
        input_data = args[0] if args else kwargs.get("payload")
        task_desc = getattr(self, "task_description", func.__name__)
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent": self.__class__.__name__,
            "task": task_desc,
            "input": input_data,
        }
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")
            
        if inspect.iscoroutinefunction(func):
            return await func(self, *args, **kwargs)
        else:
            return func(self, *args, **kwargs)
    return wrapper

# --- GOOGLE DRIVE INIT ---
# --- GOOGLE DRIVE INIT ---
from googleapiclient.discovery import build
from google.oauth2 import service_account

def get_drive_service():
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    if not os.path.exists(CREDENTIALS_PATH):
        print(f"[WARNING] Google Drive Credentials not found at {CREDENTIALS_PATH}")
        return None
    
    try:
        cred = service_account.Credentials.from_service_account_file(
            CREDENTIALS_PATH, scopes=SCOPES)
        return build('drive', 'v3', credentials=cred)
    except Exception as e:
        print(f"[ERROR] Google Drive Init Failed: {e}")
        return None
