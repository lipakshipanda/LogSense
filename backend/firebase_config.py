import os
import firebase_admin
from firebase_admin import credentials, firestore

CRED_PATH = os.getenv("FIREBASE_CRED_PATH", "serviceAccountKey.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(CRED_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()