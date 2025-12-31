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

# Palette de couleurs du logo Luther Rose
COLORS = {
    'blue_royal': HexColor('#0066CC'),      # Bordure extérieure du logo
    'red_carmin': HexColor('#DC143C'),      # Cœur central
    'black': HexColor('#000000'),           # Croix
    'white': HexColor('#FFFFFF'),           # Rose/fond
    'green': HexColor('#2E8B57'),           # Feuilles
    'gold': HexColor('#FFD700'),            # Cercle doré
    'light_blue': HexColor('#E6F2FF'),      # Fond clair alternatif
    'dark_blue': HexColor('#003D82'),       # Texte foncé
    'light_gray': HexColor('#F5F5F5'),      # Dimanches
    'orange': HexColor('#FF8C00'),          # Variante orange
}

# Couleurs alternées par mois
MONTH_COLORS = {
    1: 'blue_royal',      # Janvier
    2: 'red_carmin',      # Février
    3: 'orange',          # Mars
    4: 'blue_royal',      # Avril
    5: 'green',           # Mai
    6: 'red_carmin',      # Juin
    7: 'orange',          # Juillet
    8: 'blue_royal',      # Août
    9: 'green',           # Septembre
    10: 'red_carmin',     # Octobre
    11: 'orange',         # Novembre
    12: 'green',          # Décembre
}

# Système de couleurs pour le design (Cohérent et Accessible)
COLOR_TEXT = COLORS['black']
COLOR_TEXT_SECONDARY = COLORS['dark_blue']
COLOR_HEADER = COLORS['dark_blue']
COLOR_HEADER_ACCENT = COLORS['red_carmin']
COLOR_DARK_BLUE = COLORS['dark_blue']
COLOR_HEADER_BG = Color(0, 51, 102, alpha=0.08)
COLOR_GRID = Color(0, 0, 0, alpha=0.12)
COLOR_BACKGROUND = COLORS['white']
COLOR_SUNDAY_BG = Color(245/255, 245/255, 245/255, alpha=0.1) # light_gray approximation

# Semantic Colors
COLOR_MESSE = COLORS['blue_royal']
COLOR_REUNION = COLORS['green']
COLOR_FETE = COLORS['gold']
COLOR_DIMANCHE = COLORS['red_carmin']
COLOR_HOLIDAY = COLORS['red_carmin']

LITURGICAL_COLORS = get_liturgical_colors()
