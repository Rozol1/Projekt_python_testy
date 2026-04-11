import requests, time, concurrent.futures, pandas as pd
from config import TABLES_URL, HEADERS, FILES, TIMEOUT

def test_read(req_id):
    start = time.time()
    rep = {"Req": req_id, "Latency_Sec": 0.0, "Status": "FAILED"}
    try:
        resp = requests.get(TABLES_URL, headers=HEADERS, timeout=TIMEOUT)
        rep["Latency_Sec"] = round(time.time() - start, 4)
        if resp.status_code == 200: rep["Status"] = "SUCCESS"
    except: rep["Latency_Sec"] = round(time.time() - start, 4)
    return rep

if __name__ == "__main__":
    print("Test 2: Odczyt danych (50 prób)")
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as ex:
        pd.DataFrame(list(ex.map(test_read, range(50)))).to_excel(FILES["read"], index=False)