import requests
from config import API_KEY, AUTH_URL

EMAIL = "MAIL_ZAREJESTROWANEGO_UZYTKOWNIKA"
HASLO = "HASLO_TEGO_UZYTKOWNIKA"

print("Loguję się do Firebase po token...")
response = requests.post(AUTH_URL, json={"email": EMAIL, "password": HASLO, "returnSecureToken": True})

if response.status_code == 200:
    print(f"\n[SUKCES] Twój TOKEN to:\n{response.json().get('idToken')}")
else:
    print(f"\n[BŁĄD] {response.text}")
