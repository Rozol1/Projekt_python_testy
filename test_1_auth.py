import requests, time, concurrent.futures, pandas as pd
from config import AUTH_URL, FILES, TIMEOUT

def test_auth(user_id):
    start = time.time()
    payload = {"email": f"fake_{user_id}@umami.pl", "password": "Password123!", "returnSecureToken": True}
    rep = {"Req": user_id, "Latency_Sec": 0.0, "Status": "FAILED"}
    try:
        resp = requests.post(AUTH_URL, json=payload, timeout=TIMEOUT)
        rep["Latency_Sec"] = round(time.time() - start, 4)
        if resp.status_code in [200, 400]: rep["Status"] = "SUCCESS"
    except: rep["Latency_Sec"] = round(time.time() - start, 4)
    return rep

if __name__ == "__main__":
    print("Test 1: Masowe logowanie (30 prób)")
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
        pd.DataFrame(list(ex.map(test_auth, range(30)))).to_excel(FILES["auth"], index=False)