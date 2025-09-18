import os
import firebase_admin
from firebase_admin import credentials, firestore
from passlib.context import CryptContext
from src.core.config import settings

from firebase_admin import firestore
from passlib.context import CryptContext
from typing import Dict, Any

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db: firestore.Client, username: str) -> Dict[str, Any] | None:
    user_ref = db.collection("users").document(username)
    user = user_ref.get()
    if user.exists:
        return user.to_dict()
    return None

COLLECTION_NAME = "users"

try:
    project_id = settings.GCP_PROJECT_ID
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': project_id,
    })
    db = firestore.client()
except KeyError:
    print("Error: The GCP_PROJECT_ID environment variable is not set.")
    print("Please set it before running the script: export GCP_PROJECT_ID='your-project-id'")
    exit()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: firestore.Client, username: str, plain_password: str):
    hashed_password = pwd_context.hash(plain_password)

    user_data = {
        "username": username,
        "hashed_password": hashed_password,
        "created_at": firestore.SERVER_TIMESTAMP
    }
    
    db.collection("users").document(username).set(user_data)




