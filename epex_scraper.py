import datetime
import os
import sys
import requests
import pandas as pd

def fetch_epex_prices():
    # 📅 Dates : trading = aujourd’hui, delivery = demain
    trading_date = datetime.date.today().strftime("%Y-%m-%d")
    delivery_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    # 📂 Dossiers d’archives
    os.makedirs("archives/html", exist_ok=True)
    os.makedirs("archives/csv", exist_ok=True)
    os.makedirs("archives/json", exist_ok=True)

    # 🌐 API JSON interne d’EPEX SPOT
    # ⚠️ Cette URL fonctionne pour les prix Day-Ahead France
    api_url = (
        "https://www.epexspot.com/marketdata/auction-table?"
        f"modality=Auction&sub_modality=DayAhead&auction=MRC"
        f"&market_area=FR&delivery_date={delivery_date}&product=60"
    )

    print(f"🔗 URL API utilisée : {api_url}")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/128.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": "https://www.epexspot.com/en/market-results",
        "X-Requested-With": "XMLHttpRequest",
    }

    try:
        print("📡 Requête vers l’API EPEX…")
        r = requests.get(api_url, headers=headers, timeout=30)
        print(f"📶 Statut HTTP : {r.status_code}")

        if r.status_code != 200:
            print("❌ Échec de la récupération des données.")
            sys.exit(1)

        data = r.json()

        # 💾 Sauvegarde JSON brute
        json_path = f"archives/json/epex_FR_{delivery_date}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            import json
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"📄 Données JSON archivées : {json_path}")

        # 🧩 Extraction du tableau de prix
        if "data" not in data or not data["data"]:
            print("⚠️ Aucun prix trouvé dans la réponse JSON.")
            sys.exit(1)

        # EPEX renvoie souvent une structure sous forme de liste de dicts
        df = pd.DataFrame(data["data"])
        print(f"✅ {len(df)} lignes récupérées.")

        # 💾 Sauvegarde CSV
        csv_path = f"archives/csv/epex_FR_{delivery_date}.csv"
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(f"📊 Fichier CSV enregistré : {csv_path}")

    except Exception as e:
        print(f"❌ Erreur : {e}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_epex_prices()


'''
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


import datetime
import os
import requests

def fetch_epex_prices():
    # 📅 Dates
    trading_date = datetime.date.today().strftime("%Y-%m-%d")
    delivery_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    # 📂 Dossiers
    os.makedirs("archives/html", exist_ok=True)
    os.makedirs("archives/csv", exist_ok=True)

    # 🌐 URL cible
    url = (
        f"https://www.epexspot.com/en/market-results?"
        f"market_area=FR&auction=MRC"
        f"&trading_date={trading_date}"
        f"&delivery_date={delivery_date}"
        f"&modality=Auction&sub_modality=DayAhead&data_mode=table&product=60"
    )

    print(f"🔗 URL utilisée : {url}")

    # 🧠 Headers complets (simulation navigateur Chrome)
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/128.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Referer": "https://www.epexspot.com/en/market-results",
        "Upgrade-Insecure-Requests": "1",
    }

    html_path = f"archives/html/epex_FR_{delivery_date}.html"

    try:
        print("📡 Requête principale (requests)...")
        response = requests.get(url, headers=headers, timeout=30)
        status = response.status_code
        print(f"📶 Statut HTTP : {status}")

        # ⚠️ Vérification simple du contenu
        if status == 200 and "Forbidden" not in response.text:
            print("✅ Page HTML téléchargée avec succès.")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"📄 Page HTML archivée : {html_path}")
        else:
            print("❌ Accès refusé ou page vide, page sauvegardée pour diagnostic.")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"📄 Page archivée pour analyse : {html_path}")

    except Exception as e:
        print(f"❌ Erreur lors de la récupération : {e}")

if __name__ == "__main__":
    fetch_epex_prices()



import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def fetch_epex_prices():
    # 📅 Aujourd’hui = jour d’exécution ; Demain = livraison
    trading_date = datetime.date.today().strftime("%Y-%m-%d")
    delivery_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    # 📂 Créer les dossiers d’archives
    os.makedirs("archives/html", exist_ok=True)
    os.makedirs("archives/csv", exist_ok=True)

    # 🌐 URL cible
    url = (
        f"https://www.epexspot.com/en/market-results?"
        f"market_area=FR&auction=MRC"
        f"&trading_date={trading_date}"
        f"&delivery_date={delivery_date}"
        f"&modality=Auction&sub_modality=DayAhead&data_mode=table&product=60"
    )
    print(f"🔗 URL utilisée : {url}")

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    # 💾 Archive HTML
    html_path = f"archives/html/epex_FR_{delivery_date}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(response.text)
    print(f"📄 Page HTML archivée : {html_path}")


if __name__ == "__main__":
    fetch_epex_prices()
'''
