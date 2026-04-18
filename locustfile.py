from locust import HttpUser, task, between, events
import random
import os
import requests
from dotenv import load_dotenv

# Wczytanie bezpiecznych zmiennych z pliku .env
load_dotenv()

# Zmienna globalna przechowująca token. Zostanie ustawiona tylko raz!
GLOBAL_TOKEN = None


# =====================================================================
# ZDARZENIE INICJALIZACYJNE (Uruchamia się 1 raz przed startem kelnerów)
# =====================================================================
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    global GLOBAL_TOKEN
    print("\n[INIT] Rozpoczynam pobieranie globalnego tokenu autoryzacji...")

    api_key = os.getenv("FIREBASE_API_KEY")
    email = os.getenv("TEST_USER_EMAIL")
    password = os.getenv("TEST_USER_PASSWORD")

    auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    resp = requests.post(auth_url, json=payload)

    if resp.status_code == 200:
        GLOBAL_TOKEN = resp.json().get('idToken')
        print("[SUKCES] Token pobrany! Baza jest gotowa na przyjęcie ruchu.\n")
    else:
        print(f"[BŁĄD KRYTYCZNY LOGOWANIA]: Serwer zwrócił błąd:\n{resp.text}")
        # Zatrzymanie testu, jeśli nie udało się pobrać tokenu
        environment.runner.quit()


# =====================================================================
# ZACHOWANIE UŻYTKOWNIKA (To robi każdy z wirtualnych kelnerów)
# =====================================================================
class PersonelUmami(HttpUser):
    # Czas namysłu pracownika (od 2 do 6 sekund)
    wait_time = between(2, 6)
    host = "https://firestore.googleapis.com"

    def on_start(self):
        # Każdy użytkownik wpina do swoich nagłówków pobrany wcześniej GLOBAL_TOKEN.
        # Dzięki temu generujemy 0 zapytań do Google Auth podczas startu kelnerów!
        self.headers = {"Authorization": f"Bearer {GLOBAL_TOKEN}"}

        project_id = os.getenv("FIREBASE_PROJECT_ID")
        self.base_path = f"/v1/projects/{project_id}/databases/(default)/documents"
        self.db_prefix = "TEST_QA_"

    # --- WAGA 100 (Codzienna Praca Sali) ---
    @task(100)
    def operacje_sali(self):
        # Odczyt sali
        self.client.get(f"{self.base_path}/tables", headers=self.headers, name="1. Odczyt Sali")

        # Zmiana statusu obsługiwanego stolika
        t_id = f"{self.db_prefix}STOLIK_{random.randint(1, 50)}"
        payload = {"fields": {"status": {"stringValue": "Zajęty"}}}
        self.client.patch(f"{self.base_path}/tables/{t_id}?updateMask.fieldPaths=status",
                          json=payload, headers=self.headers, name="2. Zmiana statusu stolika")

    # --- WAGA 5 (Zarządzanie Menu) ---
    @task(5)
    def edycja_menu(self):
        # Symulacja drobnej edycji (np. ceny)
        d_id = f"{self.db_prefix}MENU_{random.randint(1, 10)}"
        payload = {"fields": {"cena": {"integerValue": random.randint(30, 60)}}}
        self.client.post(f"{self.base_path}/menu?documentId={d_id}",
                         json=payload, headers=self.headers, name="3. Dodanie/Edycja Menu")

    # --- WAGA 1 (Incydenty) ---
    @task(1)
    def incydenty_administracyjne(self):
        # Szybkie dostawienie i usunięcie stolika awaryjnego (np. dla dużego zgrupowania gości)
        s_id = f"{self.db_prefix}INC_STOLIK"
        payload = {"fields": {"status": {"stringValue": "Wolny"}}}

        self.client.post(f"{self.base_path}/tables?documentId={s_id}",
                         json=payload, headers=self.headers, name="4. Dostawienie stolika")
        self.client.delete(f"{self.base_path}/tables/{s_id}",
                           headers=self.headers, name="4. Usunięcie stolika")