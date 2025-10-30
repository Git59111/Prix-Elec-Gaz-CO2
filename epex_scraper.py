import datetime
import os
import sys
import requests
import pandas as pd
import json

def fetch_epex_prices():
    trading_date = datetime.date.today().strftime("%Y-%m-%d")
    delivery_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    os.makedirs("archives/html", exist_ok=True)
    os.makedirs("archives/csv", exist_ok=True)
    os.makedirs("archives/json", exist_ok=True)

    session = requests.Session()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/128.0.0.0 Safari/537.36"
        ),
        "Referer": "https://www.epexspot.com/en/market-results",
    }

    # Étape 1️⃣ : accéder à la page principale pour obtenir les cookies
    print("🌐 Initialisation de la session EPEX...")
    r1 = session.get("https://www.epexspot.com/en/market-results", headers=headers)
    if r1.status_code != 200:
        print("❌ Impossible d’accéder à la page d’accueil.")
        sys.exit(1)

    # Étape 2️⃣ : simuler le clic sur le bouton “Accept conditions”
    payload = {
        "form_id": "data_disclaimer_acceptation_form",
        "op": "Access to EPEX Spot website "
    }

    r2 = session.post("https://www.epexspot.com/en/market-results", data=payload, headers=headers)
    if r2.status_code != 200:
        print("❌ Échec de la validation du disclaimer.")
        sys.exit(1)

    print("✅ Disclaimer accepté, session authentifiée.")

    # Étape 3️⃣ : requête vers l’API JSON (avec cookies de session)
    api_url = (
        "https://www.epexspot.com/marketdata/auction-table?"
        f"modality=Auction&sub_modality=DayAhead&auction=MRC"
        f"&market_area=FR&delivery_date={delivery_date}&product=60"
    )

    print(f"🔗 URL API utilisée : {api_url}")

    r3 = session.get(api_url, headers=headers)
    print(f"📶 Statut HTTP : {r3.status_code}")

    # Vérification du contenu
    if not r3.text.strip().startswith("{"):
        print("⚠️ La réponse n’est pas du JSON, voici l’aperçu :")
        print(r3.text[:300])
        sys.exit(1)

    data = r3.json()

    # 💾 Sauvegarde JSON
    json_path = f"archives/json/epex_FR_{delivery_date}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"📄 Données JSON archivées : {json_path}")

    if "data" not in data or not data["data"]:
        print("⚠️ Aucune donnée dans la réponse JSON.")
        sys.exit(1)

    df = pd.DataFrame(data["data"])
    csv_path = f"archives/csv/epex_FR_{delivery_date}.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"📊 CSV enregistré : {csv_path}")

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
