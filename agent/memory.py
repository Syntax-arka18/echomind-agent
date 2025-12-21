from google.cloud import firestore
from config import PROJECT_ID

db = firestore.Client(
    project=PROJECT_ID,
    database="echomind-agent"
)

def load_messages(session_id: str):
    doc = db.collection("sessions").document(session_id).get()
    if doc.exists:
        return doc.to_dict().get("messages", [])
    return []

def save_messages(session_id: str, messages):
    db.collection("sessions").document(session_id).set({
        "messages": messages
    })
