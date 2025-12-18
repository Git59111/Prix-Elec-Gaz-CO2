import datetime
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def fetch_epex_prices():
    # 📅 Dates
    trading_date = datetime.date.today().strftime("%Y-%m-%d")
    delivery_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    # 📁 Dossier d’archive
    archive_dir = "archives/html"
    os.makedirs(archive_dir, exist_ok=True)

    html_path = f"{archive_dir}/epex_FR_{delivery_date}.html"

    print("🌐 Lancement de Chrome headless (Selenium only)…")

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=en-US")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 30)

    try:
        # 🧭 Accès direct à la page des résultats Day-Ahead FR
        url = (
            "https://www.epexspot.com/en/market-results?"
            "market_area=FR&auction=MRC&"
            f"delivery_date={delivery_date}&"
            "modality=Auction&sub_modality=DayAhead"
        )

        print(f"🔗 URL visitée : {url}")
        driver.get(url)

        # ✅ Accepter le disclaimer si présent
        try:
            button = wait.until(
                EC.element_to_be_clickable((By.ID, "edit-acceptationbutton"))
            )
            button.click()
            print("✅ Disclaimer accepté.")
            time.sleep(3)
        except Exception:
            print("ℹ️ Disclaimer déjà accepté ou absent.")

        # ⏳ Attente explicite du tableau de résultats
        print("⏳ Attente du tableau des prix…")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        time.sleep(2)  # sécurité JS

        # 📄 Sauvegarde du HTML complet rendu
        html = driver.page_source

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"✅ HTML EPEX sauvegardé : {html_path}")

    except Exception as e:
        print("❌ Erreur lors du scraping EPEX :", e)

    finally:
        driver.quit()
        print("🏁 Fin du scraper EPEX (Selenium).")


if __name__ == "__main__":
    fetch_epex_prices()


'''

import datetime
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_epex_prices():
    trading_date = datetime.date.today().strftime("%Y-%m-%d")
    delivery_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    os.makedirs("archives/html", exist_ok=True)

    print("🌐 Lancement de Chrome headless…")
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    # 🧭 Aller directement sur la page du marché FR
    driver.get(f"https://www.epexspot.com/en/market-results?market_area=FR")

    # ✅ Accepter le disclaimer (s’il apparaît)
    try:
        button = wait.until(EC.element_to_be_clickable((By.ID, "edit-acceptationbutton")))
        button.click()
        print("✅ Disclaimer accepté.")
        time.sleep(3)
    except Exception:
        print("⚠️ Aucun bouton d’acceptation trouvé (probablement déjà validé).")

    # ⚙️ Charger la page de résultats du jour (pour s'assurer que les cookies sont actifs)
    driver.get(f"https://www.epexspot.com/en/market-data?market_area=FR&delivery_date={delivery_date}")
    time.sleep(5)

    # 🔑 Récupérer les cookies valides
    cookies = driver.get_cookies()
    driver.quit()

    session = requests.Session()
    for c in cookies:
        session.cookies.set(c["name"], c["value"])

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://www.epexspot.com/en/market-results",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    api_url = (
        f"https://www.epexspot.com/marketdata/auction-table?"
        f"modality=Auction&sub_modality=DayAhead&auction=MRC&"
        f"market_area=FR&delivery_date={delivery_date}&product=60"
    )
    print(f"🔗 URL API utilisée : {api_url}")

    response = session.get(api_url, headers=headers, timeout=30)
    print(f"📶 Statut HTTP : {response.status_code}")

    html_path = f"archives/html/epex_FR_{delivery_date}.html"

    # ✅ Vérifie la présence du tableau
    if response.status_code == 200 and "<table" in response.text:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"✅ Tableau sauvegardé : {html_path}")
    else:
        # Fallback : sauvegarder directement le rendu Selenium
        print("⚠️ Pas de tableau trouvé, tentative de sauvegarde via Selenium…")
        driver = webdriver.Chrome(options=options)
        driver.get(f"https://www.epexspot.com/en/market-data?market_area=FR&delivery_date={delivery_date}")
        time.sleep(5)
        html = driver.page_source
        driver.quit()

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"⚠️ Contenu Selenium sauvegardé : {html_path}")

    print("🏁 Fin du script sans erreur.")

if __name__ == "__main__":
    fetch_epex_prices()


import datetime
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_epex_prices():
    # 📅 Dates (trading = aujourd’hui, livraison = demain)
    trading_date = datetime.date.today().strftime("%Y-%m-%d")
    delivery_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    os.makedirs("archives/html", exist_ok=True)

    # 🚀 Lancer Chrome headless pour accepter le disclaimer
    print("🌐 Lancement de Chrome headless…")
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)
    driver.get("https://www.epexspot.com/en/market-results")

    # ✅ Accepter le disclaimer si présent
    try:
        button = wait.until(EC.element_to_be_clickable((By.ID, "edit-acceptationbutton")))
        button.click()
        print("✅ Disclaimer accepté.")
        time.sleep(2)
    except Exception:
        print("⚠️ Aucun bouton d’acceptation trouvé (probablement déjà validé).")

    # 🔑 Récupérer les cookies de session
    cookies = driver.get_cookies()
    driver.quit()

    session = requests.Session()
    for c in cookies:
        session.cookies.set(c["name"], c["value"])

    # 🔗 URL API EPEX
    api_url = (
        f"https://www.epexspot.com/marketdata/auction-table?"
        f"modality=Auction&sub_modality=DayAhead&auction=MRC&"
        f"market_area=FR&delivery_date={delivery_date}&product=60"
    )
    print(f"🔗 URL API utilisée : {api_url}")

    # ⚙️ En-têtes réalistes
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/140.0.0.0 Safari/537.36",
        "Referer": "https://www.epexspot.com/en/market-results",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    # 📡 Requête API avec cookie
    print("📡 Requête vers l’API EPEX…")
    response = session.get(api_url, headers=headers, timeout=30)
    print(f"📶 Statut HTTP : {response.status_code}")

    html_path = f"archives/html/epex_FR_{delivery_date}.html"

    if response.status_code == 200 and "<table" in response.text:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"✅ Tableau sauvegardé : {html_path}")
    else:
        # Sauvegarder pour diagnostic
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"⚠️ Contenu inattendu sauvegardé pour analyse : {html_path}")
        raise SystemExit(1)

    print("🏁 Fin du script sans erreur.")

if __name__ == "__main__":
    fetch_epex_prices()

JSP A TESTER 
import datetime
import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_epex_prices():
    # 📅 Date de livraison = demain
    delivery_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    # 📂 Dossier de sortie
    os.makedirs("archives/html", exist_ok=True)
    html_path = f"archives/html/epex_FR_{delivery_date}.html"

    # ⚙️ Configuration de Chrome headless
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0.0.0 Safari/537.36"
    )

    print("🌐 Lancement de Chrome (headless)...")
    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(f"❌ Erreur au lancement de Chrome : {e}")
        sys.exit(1)

    driver.get("https://www.epexspot.com/en/market-results")
    wait = WebDriverWait(driver, 30)

    # Étape 1️⃣ : Accepter le disclaimer si présent
    try:
        btn = wait.until(EC.element_to_be_clickable((By.ID, "edit-acceptationbutton")))
        btn.click()
        print("✅ Disclaimer accepté.")
    except Exception:
        print("⚠️ Bouton d’acceptation non trouvé (probablement déjà validé).")

    # Étape 2️⃣ : Attendre que les filtres soient chargés
    try:
        wait.until(EC.presence_of_element_located((By.ID, "md_filters_wrapper")))
        print("✅ Filtres détectés.")
    except Exception:
        print("❌ Les filtres n’ont pas pu être chargés.")
        driver.quit()
        sys.exit(1)

    # Étape 3️⃣ : Clic sur “See results” (robuste)
    try:
        see_buttons = driver.find_elements(
            By.XPATH,
            "//button[contains(., 'See results') or contains(., 'Voir les résultats')]"
        )
        if see_buttons:
            driver.execute_script("arguments[0].click();", see_buttons[0])
            print("🔎 Clic sur 'See results' effectué (via XPath).")
        else:
            print("⚠️ Aucun bouton 'See results' trouvé, tentative JS...")
            driver.execute_script("""
                const btn = [...document.querySelectorAll('button')].find(b =>
                    b.textContent.includes('See results') || b.textContent.includes('Voir les résultats')
                );
                if (btn) btn.click();
            """)
        time.sleep(4)
    except Exception as e:
        print(f"❌ Erreur lors du clic sur 'See results' : {e}")

    # Étape 4️⃣ : Attendre le tableau
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        print("✅ Tableau détecté.")
    except Exception:
        print("⚠️ Tableau non détecté après 20s, sauvegarde du HTML actuel.")
        time.sleep(5)

    # Étape 5️⃣ : Sauvegarde du HTML complet
    try:
        html = driver.page_source
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"📄 Page sauvegardée : {html_path}")
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde : {e}")
        driver.quit()
        sys.exit(1)

    driver.quit()
    print("✅ Fin du script sans erreur.")

if __name__ == "__main__":
    fetch_epex_prices()


FOCNTIONNE, ESQIVE LE BLOQUEUR MAIS NE TROUVE PAS LES DONNEES
import datetime
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_epex_prices():
    delivery_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    os.makedirs("archives/html", exist_ok=True)
    html_path = f"archives/html/epex_FR_{delivery_date}.html"

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0.0.0 Safari/537.36"
    )

    print("🌐 Lancement de Chrome (headless)...")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.epexspot.com/en/market-results")

    wait = WebDriverWait(driver, 30)

    # Étape 1 : accepter le disclaimer
    try:
        btn = wait.until(EC.element_to_be_clickable((By.ID, "edit-acceptationbutton")))
        btn.click()
        print("✅ Disclaimer accepté.")
    except Exception:
        print("⚠️ Bouton d’acceptation non trouvé (probablement déjà validé).")

    # Étape 2 : attendre le bloc de filtres
    try:
        wait.until(EC.presence_of_element_located((By.ID, "md_filters_wrapper")))
        print("✅ Filtres chargés.")
    except Exception:
        print("❌ Les filtres n’ont pas pu être chargés, tentative de rechargement...")
        driver.refresh()
        time.sleep(8)

    # Étape 3 : cliquer sur “See results”
    try:
        see_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-see-results")))
        driver.execute_script("arguments[0].click();", see_btn)
        print("🔎 Clic sur 'See results' effectué.")
    except Exception:
        print("⚠️ Bouton 'See results' introuvable, on continue quand même...")

    # Étape 4 : attendre que le tableau apparaisse
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        print("✅ Tableau détecté.")
    except Exception:
        print("⚠️ Tableau non détecté après 20s. Sauvegarde du HTML actuel pour diagnostic.")

    # Étape 5 : sauvegarde du HTML complet
    html = driver.page_source
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"📄 Page sauvegardée : {html_path}")

    driver.quit()


if __name__ == "__main__":
    fetch_epex_prices()

    

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

