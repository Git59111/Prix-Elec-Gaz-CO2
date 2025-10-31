import datetime
import os
import requests
import sys

def fetch_epex_prices():
    delivery_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    os.makedirs("archives/html", exist_ok=True)

    url = (
        f"https://www.epexspot.com/marketdata/auction-table"
        f"?modality=Auction&sub_modality=DayAhead"
        f"&auction=MRC&market_area=FR"
        f"&delivery_date={delivery_date}&product=60"
    )

    print(f"🔗 URL API utilisée : {url}")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/140.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.epexspot.com/en/market-results",
    }

    try:
        print("📡 Requête vers l’API EPEX…")
        r = requests.get(url, headers=headers, timeout=30)
        print(f"📶 Statut HTTP : {r.status_code}")

        if r.status_code != 200:
            print("❌ Erreur HTTP, accès refusé.")
            sys.exit(1)

        # Vérifie si le contenu est du JSON
        if "json" not in r.headers.get("Content-Type", ""):
            print("⚠️ Contenu inattendu :")
            print(r.text[:300])
            sys.exit(1)

        html_path = f"archives/html/epex_FR_{delivery_date}.json"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(r.text)

        print(f"✅ Données sauvegardées : {html_path}")

    except Exception as e:
        print(f"❌ Erreur : {e}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_epex_prices()

    
'''
V1

import datetime
import os
import requests
import sys  # pour signaler l'échec au workflow

def fetch_epex_prices():
    trading_date = datetime.date.today().strftime("%Y-%m-%d")
    delivery_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    os.makedirs("archives/html", exist_ok=True)
    os.makedirs("archives/csv", exist_ok=True)

    url = (
    f"https://www.epexspot.com/en/market-results?"
    f"market_area=XX&auction=MRC"   # XX n'existe pas
    f"&trading_date={trading_date}"
    f"&delivery_date={delivery_date}"
    f"&modality=Auction&sub_modality=DayAhead&data_mode=table&product=60"
    )


    html_path = f"archives/html/epex_FR_{delivery_date}.html"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Referer": "https://www.epexspot.com/en/market-results",
        "Upgrade-Insecure-Requests": "1",
    }

    try:
        print("📡 Requête principale (requests)...")
        response = requests.get(url, headers=headers, timeout=30)
        status = response.status_code
        print(f"📶 Statut HTTP : {status}")

        if status == 200 and "Forbidden" not in response.text:
            print("✅ Page HTML téléchargée avec succès.")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"📄 Page HTML archivée : {html_path}")
        else:
            print("❌ Accès refusé ou page vide.")
            sys.exit(1)  # <-- signal d'échec immédiat

    except Exception as e:
        print(f"❌ Erreur lors de la récupération : {e}")
        sys.exit(1)  # <-- signal d'échec immédiat

if __name__ == "__main__":
    fetch_epex_prices()
'''

