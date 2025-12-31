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

# Design System Colors (Cohesive & Accessible - Light for photo background)
# Updated with harmonized palette per design spec
COLOR_TEXT = HexColor("#FFFFFF")                # White for maximum contrast with photo
COLOR_TEXT_SECONDARY = HexColor("#F0F0F0")     # Light gray for secondary text
COLOR_HEADER = HexColor("#FFFFFF")             # White for main header (primary text)
COLOR_HEADER_ACCENT = HexColor("#F4C430")      # Gold for accent text (Batalo, keywords)
COLOR_DARK_BLUE = HexColor("#000032")          # Dark blue for background/accents
COLOR_HEADER_BG = Color(0, 0, 50, alpha=0.15) # Semi-transparent dark blue background (15% opacity)
COLOR_GRID = Color(255, 255, 255, alpha=0.25) # White grid lines
COLOR_BACKGROUND = HexColor("#FAFAFA")        # Very light gray background

# Semantic Colors
COLOR_MESSE = HexColor("#4A6FA5")              # Service blue
COLOR_REUNION = HexColor("#6BA86F")            # Meeting green
COLOR_FETE = HexColor("#C89D4A")               # Celebration gold
COLOR_DIMANCHE = HexColor("#C44E52")           # Sunday red
COLOR_HOLIDAY = HexColor("#8B0000")            # Holiday dark red

LITURGICAL_COLORS = get_liturgical_colors()
