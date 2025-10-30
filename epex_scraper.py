import datetime
import os
import pandas as pd
import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def fetch_epex_prices():
    trading_date = datetime.date.today().strftime("%Y-%m-%d")
    delivery_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    os.makedirs("archives/html", exist_ok=True)
    os.makedirs("archives/csv", exist_ok=True)

    # ⚙️ Options Chrome
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    )

    print("🌐 Lancement de Chrome via undetected-chromedriver (version 140)...")
    try:
        driver = uc.Chrome(version_main=140, options=options)
    except Exception as e:
        print(f"❌ Erreur au lancement de Chrome : {e}")
        return

    driver.get("https://www.epexspot.com/en/market-results")
    wait = WebDriverWait(driver, 25)

    # 1️⃣ Accepter le disclaimer s’il apparaît
    try:
        button = wait.until(EC.element_to_be_clickable((By.ID, "edit-acceptationbutton")))
        button.click()
        print("✅ Disclaimer accepté.")
    except Exception:
        print("⚠️ Aucun bouton d’acceptation détecté (peut-être déjà validé).")

    # 2️⃣ Attendre que les filtres soient disponibles
    try:
        wait.until(EC.presence_of_element_located((By.ID, "md_filters_wrapper")))
        print("✅ Bloc de filtres détecté.")
    except Exception:
        print("❌ Bloc de filtres introuvable, tentative de rechargement...")
        driver.refresh()
        time.sleep(8)

    # 3️⃣ Scroll pour déclencher les scripts JS
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
    time.sleep(4)

    # 4️⃣ Clic sur “See Results” pour charger les prix
    try:
        see_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".btn.btn-primary-outline.btn-full.btn-see-results")
            )
        )
        driver.execute_script("arguments[0].click();", see_button)
        print("🔎 Recherche des résultats lancée.")
    except Exception as e:
        print(f"❌ Impossible de cliquer sur See Results : {e}")
        driver.quit()
        return

    # 5️⃣ Attendre que le tableau apparaisse
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        print("✅ Tableau détecté.")
    except Exception:
        print("⚠️ Tableau non détecté après 20 secondes.")
        html_path = f"archives/html/epex_FR_{delivery_date}_empty.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"📄 Page enregistrée pour diagnostic : {html_path}")
        driver.quit()
        return

    # 6️⃣ Sauvegarder le HTML
    html = driver.page_source
    html_path = f"archives/html/epex_FR_{delivery_date}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"📄 Page enregistrée : {html_path}")

    # 7️⃣ Parser le tableau
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    rows = []
    for tr in table.find_all("tr"):
        cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
        if cells:
            rows.append(cells)

    if len(rows) < 2:
        print("⚠️ Aucun contenu exploitable trouvé dans le tableau.")
    else:
        df = pd.DataFrame(rows[1:], columns=rows[0])
        csv_path = f"archives/csv/epex_FR_{delivery_date}.csv"
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(f"📊 Fichier CSV enregistré : {csv_path} ({len(df)} lignes)")

    driver.quit()


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
