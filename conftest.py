import pytest
import requests
import os
from config import AUTH_URL

@pytest.fixture(scope="session")
def headers():
    """Pobieranie tokenu."""
    payload = {
        "email": os.getenv("TEST_USER_EMAIL"),
        "password": os.getenv("TEST_USER_PASSWORD"),
        "returnSecureToken": True
    }
    resp = requests.post(AUTH_URL, json=payload)
    print("\n[DEBUG FIREBASE]:", resp.text)
    assert resp.status_code == 200, "Krytyczny błąd autoryzacji"
    return {"Authorization": f"Bearer {resp.json().get('idToken')}"}