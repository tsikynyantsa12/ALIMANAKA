import os

ICONS = {
    # Agricultural actions - new emoji-style icons
    "recolte": "assets/icons/recolte_new.png",
    "semis": "assets/icons/semis_new.png",
    "entretien": "assets/icons/entretien_new.png",
    "plantation": "assets/icons/plantation_new.png",
    
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
    
    # Cultures - new emoji-style icons
    "riz": "assets/icons/mais_new.png",
    "manioc": "assets/icons/manioc_new.png",
    "haricot": "assets/icons/haricot_new.png",
    "mais": "assets/icons/mais_new.png",
    "arachide": "assets/icons/arachide.png",
    
    # Legacy fallback
    "riz_legacy": "assets/icons/cultures/riz.jpg",
    "manioc_legacy": "assets/icons/cultures/manioc.jpg",
    "haricot_legacy": "assets/icons/cultures/haricot.jpg",
    "mais_legacy": "assets/icons/cultures/mais.jpg",
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
