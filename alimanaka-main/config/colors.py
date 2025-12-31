from reportlab.lib.colors import HexColor, Color

def get_liturgical_colors(global_data=None):
    """Load liturgical colors from CSV with fallback defaults"""
    mapping = {}
    if global_data is not None and not global_data["couleurs"].empty:
        for _, row in global_data["couleurs"].iterrows():
            cid = str(row['id']).strip().lower()
            hex_code = str(row['code_hex']).strip()
            try:
                mapping[cid] = HexColor(hex_code)
            except:
                pass
    
    defaults = {
        "vert": HexColor("#6ba886"),      # Darker green for visibility
        "rouge": HexColor("#c94c4c"),     # Richer red
        "violet": HexColor("#9b6ba8"),    # Richer purple
        "blanc": HexColor("#e8e8e8")      # Off-white for better contrast
    }
    
    for k, v in defaults.items():
        if k not in mapping:
            mapping[k] = v
    return mapping

# Système de couleurs pour le design (Cohérent et Accessible)
COLOR_TEXT = HexColor("#1A1A1A")                # Anthracite pour une meilleure lisibilité sur fond clair
COLOR_TEXT_SECONDARY = HexColor("#4A4A4A")     # Gris foncé pour le texte secondaire
COLOR_HEADER = HexColor("#003366")             # Bleu marine profond
COLOR_HEADER_ACCENT = HexColor("#8B0000")      # Rouge brique pour les accents
COLOR_DARK_BLUE = HexColor("#001F3F")          # Bleu nuit
COLOR_HEADER_BG = Color(0, 51, 102, alpha=0.08) # Bleu très pâle
COLOR_GRID = Color(0, 0, 0, alpha=0.12)         # Gris très léger pour la grille
COLOR_BACKGROUND = HexColor("#FFFFFF")        # Fond blanc
COLOR_SUNDAY_BG = Color(139, 0, 0, alpha=0.05)  # Fond rouge très léger pour les dimanches

# Semantic Colors
COLOR_MESSE = HexColor("#4A6FA5")              # Service blue
COLOR_REUNION = HexColor("#6BA86F")            # Meeting green
COLOR_FETE = HexColor("#C89D4A")               # Celebration gold
COLOR_DIMANCHE = HexColor("#C44E52")           # Sunday red
COLOR_HOLIDAY = HexColor("#8B0000")            # Holiday dark red

LITURGICAL_COLORS = get_liturgical_colors()
