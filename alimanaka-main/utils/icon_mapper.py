import os

ICONS = {
    "recolte": "assets/icons/recolte.jpg",
    "semis": "assets/icons/semis.jpg",
    "entretien": "assets/icons/entretien.jpg",
    "plantation": "assets/icons/plantation.jpg",
    "pleine_lune": "assets/icons/pleine_lune.jpg",
    "nouvelle_lune": "assets/icons/pleine_lune.jpg", # Fallback if specific icon missing
    "premier_quartier": "assets/icons/quartier.jpg",
    "dernier_quartier": "assets/icons/quartier.jpg",
    "nouvelle": "assets/icons/pleine_lune.jpg",
    "premier": "assets/icons/quartier.jpg",
    "pleine": "assets/icons/pleine_lune.jpg",
    "dernier": "assets/icons/quartier.jpg",
    # Cultures
    "riz": "assets/icons/cultures/riz.jpg",
    "manioc": "assets/icons/cultures/manioc.jpg",
    "haricot": "assets/icons/cultures/haricot.jpg",
    "mais": "assets/icons/cultures/mais.jpg",
}

def get_icon_path(key):
    if not key: return None
    path = ICONS.get(str(key).lower())
    if path and os.path.exists(path):
        return path
    return None

def get_moon_icon(phase_id):
    """Maps the phase_id from monthly data to the correct icon path using global IDs."""
    if not phase_id: return None
    # Ensure phase_id matches the 'id' in our ICONS dictionary
    # which is derived from the global/phases_lunaires.csv IDs
    return get_icon_path(phase_id)

def get_agri_icon(action):
    return get_icon_path(action)

def get_culture_icon(culture):
    return get_icon_path(culture)
