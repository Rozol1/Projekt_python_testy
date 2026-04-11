import os

# --- DANE Z FIREBASE ---
PROJECT_ID = "ID_PROJEKTU_FIREBASE"
API_KEY = "API_KEY_FIREBASE"
TOKEN = "TOKEN_FIREBASE"

# --- ADRESY API ---
AUTH_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
BASE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents"
TABLES_URL = f"{BASE_URL}/tables"
ORDERS_URL = f"{BASE_URL}/ordered_items"

# --- ZAKRES IZOLACJI DANYCH  ---
TEST_TABLE_PREFIX = "TESTOWY_STOLIK_"
TEST_TABLE_MIN = 40
TEST_TABLE_MAX = 100

# --- USTAWIENIA SKRYPTÓW ---
TIMEOUT = 10
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

FILES = {
    "auth": "wyniki_test_1_auth.xlsx",
    "read": "wyniki_test_2_odczyt.xlsx"
}
