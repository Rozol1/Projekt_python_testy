import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
API_KEY = os.getenv("FIREBASE_API_KEY")

# Działanie na testowych danych
DB_PREFIX = "TEST_QA_"

# Łączenie z projektem firebase
AUTH_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
UPDATE_AUTH_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={API_KEY}"
BASE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents"