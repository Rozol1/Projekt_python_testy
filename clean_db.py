import requests
import os
from dotenv import load_dotenv
from config import BASE_URL, DB_PREFIX, AUTH_URL

load_dotenv()


def get_token():
    payload = {
        "email": os.getenv("TEST_USER_EMAIL"),
        "password": os.getenv("TEST_USER_PASSWORD"),
        "returnSecureToken": True
    }
    resp = requests.post(AUTH_URL, json=payload)
    return resp.json().get("idToken")


def clean_collection(collection_name, headers):
    print(f"--- Czyszczenie kolekcji: {collection_name} ---")
    url = f"{BASE_URL}/{collection_name}"

    # 1. Pobranie listy dokumentów w kolekcji
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(f"Błąd lub pusta kolekcja {collection_name}")
        return 0

    documents = resp.json().get('documents', [])
    deleted_count = 0

    # 2. Iteracja i usuwanie pasujących dokumentów
    for doc in documents:
        # Wyciągamy samą nazwę dokumentu z pełnej ścieżki
        full_name = doc.get('name')
        doc_id = full_name.split('/')[-1]

        if doc_id.startswith(DB_PREFIX) or "locust" in doc_id.lower():
            delete_url = f"{BASE_URL}/{collection_name}/{doc_id}"
            del_resp = requests.delete(delete_url, headers=headers)
            if del_resp.status_code == 200:
                print(f" [OK] Usunięto: {doc_id}")
                deleted_count += 1
            else:
                print(f" [BŁĄD] Nie udało się usunąć: {doc_id}")

    return deleted_count


if __name__ == "__main__":
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Kolekcje do sprawdzenia
    collections = ["tables", "ordered_items", "menu"]
    total_deleted = 0

    print(f"Rozpoczynam sprzątanie bazy (Prefiks: {DB_PREFIX})...\n")

    for col in collections:
        total_deleted += clean_collection(col, headers)

    print(f"\n[ZAKOŃCZONO] Łącznie usunięto {total_deleted} rekordów testowych.")