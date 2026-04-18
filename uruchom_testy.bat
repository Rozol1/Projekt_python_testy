@echo off
echo =======================================================
echo     ROZPOCZYNAM ZAUTOMATYZOWANY POTOK TESTOWY UMAMI    
echo =======================================================
echo.

echo [KROK 0/5] Sprawdzanie i instalacja zaleznosci (requirements.txt)...
pip install -r requirements.txt
echo.

echo [KROK 1/5] Uruchamianie testow funkcjonalnych (Pytest)...
pytest -s --html=raport_QA.html --self-contained-html
echo.

echo [KROK 2/5] Testy obciazeniowe Locust (100 uzytkownikow)...
locust -f locustfile.py --headless -u 100 -r 10 --run-time 1m --csv=test_100
echo.

echo [KROK 3/5] Testy obciazeniowe Locust (1000 uzytkownikow)...
locust -f locustfile.py --headless -u 1000 -r 50 --run-time 1m --csv=test_1000
echo.

echo [KROK 4/5] Generowanie wykresow i tabel (Pandas/Matplotlib)...
python analiza_wynikow.py
echo.

echo [KROK 5/5] Sprzatanie bazy danych po testach...
python clean_db.py
echo.

echo =======================================================
echo     POTOK ZAKONCZONY SUKCESEM! SPRAWDZ PLIKI RAPORTOW   
echo =======================================================
pause
