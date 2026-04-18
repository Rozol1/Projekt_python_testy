import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 11})

testy = [
    {"plik": "test_100", "label": "100 Użytkowników", "kolor": "#2ecc71"},
    {"plik": "test_1000", "label": "1000 Użytkowników", "kolor": "#f39c12"},
    {"plik": "test_5000", "label": "5000 Użytkowników", "kolor": "#e74c3c"}
]

# 1. Porównawczy wykres opóźnień (Latency)
plt.figure(figsize=(10, 5))
for test in testy:
    try:
        df = pd.read_csv(f"{test['plik']}_stats_history.csv", encoding_errors='replace')
        df = df[df['Name'] == 'Aggregated']
        sns.lineplot(x=range(len(df)), y=df['Total Average Response Time'], label=test['label'], color=test['kolor'], linewidth=2)
    except FileNotFoundError:
        pass

plt.title('Porównanie opóźnień Firebase Firestore pod obciążeniem', pad=15, fontweight='bold')
plt.xlabel('Czas trwania testu (próbki)')
plt.ylabel('Średni czas odpowiedzi (ms)')
plt.legend()
plt.tight_layout()
plt.savefig("wykres_porownawczy_opoznien.png", dpi=300)
print("[+] Wygenerowano wykres: wykres_porownawczy_opoznien.png")

# 2. Generowanie tabeli zbiorczej do LaTeXa
dane_tabeli = []
for test in testy:
    try:
        df_stats = pd.read_csv(f"{test['plik']}_stats.csv", encoding_errors='replace')
        podsumowanie = df_stats[df_stats['Name'] == 'Aggregated'].iloc[0]
        dane_tabeli.append({
            "Obciążenie": test['label'],
            "Zapytań": podsumowanie['Request Count'],
            "Błędy": podsumowanie['Failure Count'],
            "RPS": podsumowanie['Requests/s'],
            "Mediana (ms)": podsumowanie['Median Response Time'],
            "P95 (ms)": podsumowanie['95%']
        })
    except FileNotFoundError:
        pass

if dane_tabeli:
    df_tabela = pd.DataFrame(dane_tabeli)
    print("\n[+] Gotowy kod tabeli LaTeX:\n")
    print(df_tabela.to_latex(index=False, float_format="%.2f"))