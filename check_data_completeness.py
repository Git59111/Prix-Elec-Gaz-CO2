import os
import pandas as pd

EXCEL_PATH = "data/epexspot_prices.xlsx"

def check_last_day_electricity():
    """Vérifie si la dernière journée dans le fichier Excel contient des données valides."""
    
    if not os.path.exists(EXCEL_PATH):
        print(f"❌ Fichier introuvable : {EXCEL_PATH}")
        return 1

    # Lecture du fichier Excel
    sheets = pd.read_excel(EXCEL_PATH, sheet_name=None)
    if "Prix Spot" not in sheets:
        print("❌ Feuille 'Prix Spot' introuvable dans le fichier Excel.")
        return 1

    df = sheets["Prix Spot"]

    # Identifier la dernière colonne de données (dernier jour)
    data_columns = [c for c in df.columns if c.lower() not in ["heure", "index"]]
    if not data_columns:
        print("❌ Aucune colonne de données trouvée dans 'Prix Spot'.")
        return 1

    last_col = data_columns[-1]
    col_values = df[last_col].astype(str).str.strip()

    # Compter les valeurs manquantes ou '-'
    missing_count = (col_values.isin(["-", "", "nan"])).sum()

    print(f"🗓️ Vérification de la colonne '{last_col}' : {missing_count}/24 manquantes")

    # Échec si toutes les valeurs du dernier jour sont vides
    if missing_count == 24:
        print("❌ Échec : toutes les valeurs du dernier jour sont vides ou '-'")
        return 1

    print("✅ Données présentes pour le dernier jour, tout est OK.")
    return 0


if __name__ == "__main__":
    exit(check_last_day_electricity())

'''

import os
import pandas as pd
from datetime import datetime

EXCEL_PATH = "data/epexspot_prices.xlsx"

def check_last_day_electricity():
    if not os.path.exists(EXCEL_PATH):
        print(f"❌ Fichier introuvable : {EXCEL_PATH}")
        return 1

    # Lecture du fichier Excel
    sheets = pd.read_excel(EXCEL_PATH, sheet_name=None)
    if "Prix Spot" not in sheets:
        print("❌ Feuille 'Prix Spot' introuvable dans le fichier Excel.")
        return 1

    df = sheets["Prix Spot"]

    # Identifier la dernière colonne (dernier jour)
    data_columns = [c for c in df.columns if c.lower() not in ["heure", "index"]]
    if not data_columns:
        print("❌ Aucune colonne de données trouvée dans 'Prix Spot'.")
        return 1

    last_col = data_columns[-1]
    col_values = df[last_col].astype(str).str.strip()

    # Compter les valeurs manquantes ou '-'
    missing_count = (col_values.isin(["-", "", "nan"])).sum()

    print(f"🗓️ Vérification de la colonne '{last_col}' : {missing_count}/24 manquantes")

    if missing_count == 24:
        print("❌ Échec : toutes les valeurs du dernier jour sont vides ou '-'")
        return 1

    print("✅ Données présentes pour le dernier jour, tout est OK.")
    return 0

if __name__ == "__main__":
    exit(check_last_day_electricity())
'''
