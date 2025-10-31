import os
import datetime
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EXCEL_PATH = "data/epexspot_prices.xlsx"
EMAIL_TO = "GitHub59111@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(missing_info):
    """Envoie un email récapitulatif avec les anomalies détectées."""
    sender = "GitHub Actions <action@github.com>"
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = EMAIL_TO
    msg["Subject"] = "[ALERTE] Données manquantes EPEX / Gaz / CO2"

    body = (
        "Bonjour,\n\n"
        "Des données sont manquantes dans le fichier epexspot_prices.xlsx :\n\n"
        + "\n".join(missing_info)
        + "\n\nCordialement,\nVotre bot GitHub 🤖"
    )
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
        server.send_message(msg)

    print("📧 Email d'alerte envoyé avec succès.")


def check_data():
    """Analyse les feuilles Excel pour détecter les données manquantes."""
    if not os.path.exists(EXCEL_PATH):
        print(f"❌ Fichier introuvable : {EXCEL_PATH}")
        return

    sheets = pd.read_excel(EXCEL_PATH, sheet_name=None)
    missing_info = []

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)

    # Helper pour comparer formats de dates ("30-oct.", "31-oct.")
    def fmt_date(date):
        return date.strftime("%d-%b").lower().replace("may", "mai").replace("oct", "oct.")

    tomorrow_label = fmt_date(tomorrow)
    yesterday_label = fmt_date(yesterday)

    print(f"🗓️ Vérification des colonnes : {yesterday_label} (Gaz/CO2), {tomorrow_label} (Elec)")

    # === 1️⃣ Électricité ===
    if "Prix Spot" in sheets:
        df_elec = sheets["Prix Spot"]
        if tomorrow_label in df_elec.columns:
            missing_cells = df_elec[df_elec[tomorrow_label].isin(["-", None, ""])]
            if not missing_cells.empty:
                hours = ", ".join(missing_cells["Heure"].astype(str))
                missing_info.append(f"⚡ Électricité ({tomorrow_label}) : {len(missing_cells)} cases vides ({hours})")
        else:
            missing_info.append(f"⚡ Aucune colonne '{tomorrow_label}' trouvée dans 'Prix Spot'.")

    # === 2️⃣ Gaz ===
    if "Gaz" in sheets:
        df_gaz = sheets["Gaz"]
        df_gaz["Date"] = df_gaz["Date"].astype(str)
        if yesterday.strftime("%Y-%m-%d") in df_gaz["Date"].values:
            val = df_gaz.loc[df_gaz["Date"] == yesterday.strftime("%Y-%m-%d"), "Last Price"].values[0]
            if str(val).strip() in ["-", "nan", ""]:
                missing_info.append(f"🔥 Gaz ({yesterday}) : valeur vide.")
        else:
            missing_info.append(f"🔥 Aucune donnée Gaz pour {yesterday}.")
    
    # === 3️⃣ CO2 ===
    if "CO2" in sheets:
        df_co2 = sheets["CO2"]
        df_co2["Date"] = df_co2["Date"].astype(str)
        if yesterday.strftime("%Y-%m-%d") in df_co2["Date"].values:
            val = df_co2.loc[df_co2["Date"] == yesterday.strftime("%Y-%m-%d"), "Last Price"].values[0]
            if str(val).strip() in ["-", "nan", ""]:
                missing_info.append(f"🌍 CO2 ({yesterday}) : valeur vide.")
        else:
            missing_info.append(f"🌍 Aucune donnée CO2 pour {yesterday}.")

    # === Rapport ===
    if missing_info:
        print("⚠️ Données manquantes détectées :")
        for m in missing_info:
            print("   -", m)
        send_email(missing_info)
    else:
        print("✅ Toutes les données sont présentes et complètes.")


if __name__ == "__main__":
    check_data()
