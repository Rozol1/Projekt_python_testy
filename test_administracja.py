import pytest
import requests
import random
import os
from config import BASE_URL, UPDATE_AUTH_URL, DB_PREFIX


def test_zmiana_hasla_personelu(headers):
    token = headers["Authorization"].split(" ")[1]

    # Zmiana hasła
    res = requests.post(UPDATE_AUTH_URL,
                        json={"idToken": token, "password": "BezpieczneHaslo123!", "returnSecureToken": True})
    assert res.status_code == 200

    # Natychmiastowy powrót do starego hasła!
    stare_haslo = os.getenv("TEST_USER_PASSWORD")
    res_revert = requests.post(UPDATE_AUTH_URL,
                               json={"idToken": token, "password": stare_haslo, "returnSecureToken": True})
    assert res_revert.status_code == 200


def test_zarzadzanie_menu(headers):
    id_dania = f"{DB_PREFIX}DANIE_{random.randint(100, 999)}"
    url = f"{BASE_URL}/menu"

    # Dodanie i Edycja
    requests.post(f"{url}?documentId={id_dania}",
                  json={"fields": {"nazwa": {"stringValue": "Test"}, "cena": {"integerValue": 20}}}, headers=headers)
    res_patch = requests.patch(f"{url}/{id_dania}?updateMask.fieldPaths=cena",
                               json={"fields": {"cena": {"integerValue": 35}}}, headers=headers)
    assert res_patch.status_code == 200

    # Usunięcie
    requests.delete(f"{url}/{id_dania}", headers=headers)


def test_edycja_liczby_stolikow(headers):
    stolik_id = f"{DB_PREFIX}DOSTAWKA_{random.randint(1, 99)}"
    requests.post(f"{BASE_URL}/tables?documentId={stolik_id}", json={"fields": {"status": {"stringValue": "Wolny"}}},
                  headers=headers)
    res_del = requests.delete(f"{BASE_URL}/tables/{stolik_id}", headers=headers)
    assert res_del.status_code == 200