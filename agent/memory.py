from google.cloud import firestore
from config import PROJECT_ID

db = firestore.Client(
    project=PROJECT_ID,
    database="echomind-agent"
)

def load_session(session_id: str):
    doc = db.collection("sessions").document(session_id).get()
    if doc.exists:
        return doc.to_dict()
    return {
        "messages": [],
        "persona": None
    }

def save_session(session_id: str, session_data: dict):
    db.collection("sessions").document(session_id).set(session_data)
