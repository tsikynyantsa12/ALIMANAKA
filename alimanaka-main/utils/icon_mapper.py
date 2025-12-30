import os

ICONS = {
    # Agricultural icons
    "recolte": "assets/icons/recolte.jpg",
    "semis": "assets/icons/semis.jpg",
    "entretien": "assets/icons/entretien.jpg",
    "plantation": "assets/icons/plantation.jpg",
    
    # Lunar phases - new emoji-style icons
    "nouvelle_lune": "assets/icons/nouvelle_lune.png",
    "pleine_lune": "assets/icons/pleine_lune_new.png",
    "premier_quartier": "assets/icons/premiere_quartier.png",
    "dernier_quartier": "assets/icons/dernier_quartier.png",
    
    # Aliases for lunar phases
    "nouvelle": "assets/icons/nouvelle_lune.png",
    "pleine": "assets/icons/pleine_lune_new.png",
    "premier": "assets/icons/premiere_quartier.png",
    "dernier": "assets/icons/dernier_quartier.png",
    "premier_croissant": "assets/icons/premier_croissant.png",
    "dernier_croissant": "assets/icons/dernier_croissant.png",
    
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
