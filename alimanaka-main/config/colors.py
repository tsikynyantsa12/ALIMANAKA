from reportlab.lib.colors import HexColor, Color

def get_liturgical_colors(global_data=None):
    mapping = {}
    if global_data is not None and not global_data["couleurs"].empty:
        for _, row in global_data["couleurs"].iterrows():
            cid = str(row['id']).lower()
            hex_code = str(row['code_hex'])
            c = HexColor(hex_code)
            mapping[cid] = c # No alpha, just the color for the border
    
    defaults = {
        "vert": HexColor("#a8d5ba"),
        "rouge": HexColor("#f1948a"),
        "violet": HexColor("#c39bd3"),
        "blanc": HexColor("#fefefe")
    }
    for k, v in defaults.items():
        if k not in mapping:
            mapping[k] = v
    return mapping

# 5 Core colors as requested (Low saturation)
COLOR_TEXT = HexColor("#1A1A1A") # Near black
COLOR_TEXT_SECONDARY = HexColor("#444444")
COLOR_GRID = Color(0, 0, 0, alpha=0.15) # Thin low opacity grid

COLOR_MESSE = HexColor("#5D7B93") # Muted Blue
COLOR_REUNION = HexColor("#7BAE7F") # Muted Green
COLOR_FETE = HexColor("#D4A373") # Muted Orange
COLOR_DIMANCHE = HexColor("#B56565") # Muted Red
COLOR_HOLIDAY = HexColor("#990000")

LITURGICAL_COLORS = get_liturgical_colors()
