import pandas as pd
import os

def load_csv(file_path):
    if not os.path.exists(file_path):
        return pd.DataFrame()
    try:
        return pd.read_csv(file_path)
    except Exception:
        return pd.DataFrame()

def get_month_data(month_idx):
    month_folder = f"data/mois/{month_idx:02d}"
    data = {
        "dimanches": load_csv(f"{month_folder}/dimanches.csv"),
        "eglise": load_csv(f"{month_folder}/programme_eglise.csv"),
        "agricole": load_csv(f"{month_folder}/programme_agricole.csv"),
        "feries": load_csv(f"{month_folder}/jours_feries.csv"),
        "lunes": load_csv(f"{month_folder}/phases_lunaires.csv")
    }
    return data

def get_global_data():
    return {
        "couleurs": load_csv("data/global/couleurs_liturgiques.csv"),
        "cultures": load_csv("data/global/cultures.csv"),
        "actions": load_csv("data/global/actions_agricoles.csv"),
        "phases": load_csv("data/global/phases_lunaires.csv"),
        "logos": load_csv("data/global/logos.csv"),
        "entetes": load_csv("data/global/entetes.csv")
    }
