import uuid
from firebase_admin import firestore
from typing import Dict, Any

def create_session(user_id: str, initial_data: Dict[str, Any]) -> Dict[str, Any]:
    db = firestore.client()
    session_id = str(uuid.uuid4())
    
    session_data = {
        "user_uid": user_id,
        "created_at": firestore.SERVER_TIMESTAMP,
        "status": "planning_started",
        **initial_data  
    }
    
    db.collection("sessions").document(session_id).set(session_data)
    session_data["session_id"] = session_id
    return session_data

def get_session(session_id: str) -> Dict[str, Any] | None:
    db = firestore.client()
    doc_ref = db.collection("sessions").document(session_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None

def update_session(session_id: str, data_to_update: Dict[str, Any]):
    db = firestore.client()
    doc_ref = db.collection("sessions").document(session_id)
    data_to_update["last_updated"] = firestore.SERVER_TIMESTAMP
    
    doc_ref.update(data_to_update)