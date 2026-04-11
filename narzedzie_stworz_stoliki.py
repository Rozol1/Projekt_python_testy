import requests
import concurrent.futures
from config import TABLES_URL, HEADERS, TEST_TABLE_PREFIX, TEST_TABLE_MIN, TEST_TABLE_MAX

def stworz_stolik(numer):
    url = f"{TABLES_URL}?documentId={TEST_TABLE_PREFIX}{numer}"
    payload = {"fields": {"numer": {"integerValue": numer}, "status": {"stringValue": "Wolny"}, "guests_count": {"integerValue": 0}}}
    resp = requests.post(url, json=payload, headers=HEADERS)
    return resp.status_code == 200

if __name__ == "__main__":
    print(f"Generowanie sztucznych stolików ({TEST_TABLE_MIN}-{TEST_TABLE_MAX})...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        wyniki = list(ex.map(stworz_stolik, range(TEST_TABLE_MIN, TEST_TABLE_MAX + 1)))
    print(f"Utworzono {wyniki.count(True)} stolików testowych.")