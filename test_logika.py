import pytest
import requests
import random
from config import BASE_URL, DB_PREFIX


def test_odczyt_mapy_sali(headers):
    resp = requests.get(f"{BASE_URL}/tables", headers=headers)
    assert resp.status_code == 200


def test_pelny_cykl_zamowienia(headers):
    zam_id = f"{DB_PREFIX}ZAMOWIENIE_{random.randint(1000, 9999)}"
    url = f"{BASE_URL}/ordered_items"

    # Krok 1: Dodanie (CREATE)
    res_post = requests.post(f"{url}?documentId={zam_id}", json={"fields": {"status": {"stringValue": "W kuchni"}}},
                             headers=headers)
    assert res_post.status_code == 200

    # Krok 2: Aktualizacja (UPDATE)
    res_patch = requests.patch(f"{url}/{zam_id}?updateMask.fieldPaths=status",
                               json={"fields": {"status": {"stringValue": "Wydane"}}}, headers=headers)
    assert res_patch.status_code == 200

    # Krok 3: Zwolnienie stolika (DELETE)
    res_del = requests.delete(f"{url}/{zam_id}", headers=headers)
    assert res_del.status_code == 200