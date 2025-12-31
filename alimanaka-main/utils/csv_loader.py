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
        "entetes": load_csv("data/global/entetes.csv"),
        "mois": load_csv("data/global/mois.csv"),
        "photos": load_csv("data/global/photos.csv"),
        "configuration": load_csv("data/global/configuration.csv")
    }

def get_config_value(key, default=None, global_data=None):
    """Récupère une valeur de configuration."""
    if global_data is None:
        global_data = get_global_data()
    if not global_data.get("configuration", pd.DataFrame()).empty:
        config_df = global_data["configuration"]
        row = config_df[config_df['cle'] == key]
        if not row.empty:
            return row.iloc[0]['valeur']
    return default

def get_month_name(month_num, global_data=None):
    """Récupère le nom d'un mois."""
    if global_data is None:
        global_data = get_global_data()
    if not global_data.get("mois", pd.DataFrame()).empty:
        mois_df = global_data["mois"]
        row = mois_df[mois_df['numero'] == month_num]
        if not row.empty:
            return row.iloc[0]['nom_complet']
    return f"Mois {month_num}"

def get_photos_for_page(page_num, global_data=None):
    """Récupère les photos pour une page donnée."""
    if global_data is None:
        global_data = get_global_data()
    if not global_data.get("photos", pd.DataFrame()).empty:
        photos_df = global_data["photos"]
        rows = photos_df[photos_df['numero_page'] == page_num]
        return rows.to_dict('records')
    return []
