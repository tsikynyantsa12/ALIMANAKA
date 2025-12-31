import pandas as pd
from reportlab.lib.colors import HexColor
from config.colors import COLOR_TEXT, COLOR_TEXT_SECONDARY, COLOR_DIMANCHE, COLOR_GRID, COLOR_HEADER, COLORS
from config.fonts import FONT_BOLD, FONT_REGULAR, FONT_ITALIC, SIZE_DAY_NUM, SIZE_DAY_NAME, SIZE_PROGRAM, SIZE_VERSE
from utils.icon_mapper import get_moon_icon, get_agri_icon, get_culture_icon
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT

styles = getSampleStyleSheet()
# Style des paragraphes pour le programme et les versets
style_program = ParagraphStyle('Program', parent=styles['Normal'], fontSize=SIZE_PROGRAM, leading=SIZE_PROGRAM+3, alignment=TA_LEFT, textColor=COLOR_TEXT, fontName=FONT_BOLD)
style_verse = ParagraphStyle('Verse', parent=styles['Normal'], fontSize=SIZE_VERSE-1, leading=SIZE_VERSE+2, alignment=TA_LEFT, textColor=COLOR_TEXT_SECONDARY, fontName=FONT_ITALIC)

def calculate_day_height(day_info, month_data):
    """Calcule la hauteur nécessaire pour une ligne de jour en fonction du contenu."""
    base_height = 18 # Hauteur de base réduite pour plus de compacité
    date_str = day_info["date"].isoformat()
    extra_height = 0
    if month_data and not month_data["dimanches"].empty:
        df = month_data["dimanches"]
        row = df[df['date'] == date_str]
        if not row.empty:
            extra_height += 15 # Moins d'espace pour les dimanches
    if month_data and not month_data["eglise"].empty:
        prog_df = month_data["eglise"]
        prog_row = prog_df[prog_df['date'] == date_str]
        if not prog_row.empty:
            extra_height += 8
    return base_height + extra_height

def draw_day_row(canvas, x, y, width, height, day_info, month_data=None, global_data=None):
    """Dessine une ligne de jour avec les informations liturgiques et agricoles."""
    from config.colors import get_liturgical_colors, COLORS
    liturgical_colors = get_liturgical_colors(global_data)
    
    liturgical_color_id = "vert"
    day_num = day_info["day"]
    date_str = day_info["date"].isoformat()
    is_sunday = day_info["weekday"].lower().startswith('dim')
    
    specific_data = None
    if month_data and not month_data["dimanches"].empty:
        df = month_data["dimanches"]
        row = df[df['date'] == date_str]
        if not row.empty:
            specific_data = row.iloc[0]
            liturgical_color_id = str(specific_data.get('couleur_id', 'vert')).lower()

    # Ligne de séparation fine
    canvas.saveState()
    if is_sunday:
        canvas.setFillColor(COLORS['light_gray'])
        canvas.rect(x, y, width, height, fill=1, stroke=0)
    
    canvas.setStrokeColor(COLOR_GRID)
    canvas.setLineWidth(0.2)
    canvas.line(x, y, x + width, y)
    canvas.restoreState()
    
    # MISE EN PAGE : GAUCHE (Date) | CENTRE (Texte) | DROITE (Icônes)
    icon_size = 7
    icon_spacing = 1
    
    # COLONNE GAUCHE (Date)
    left_x = x + 2
    left_y = y + height - 7
    
    # Numéro du jour
    day_color = COLORS['red_carmin'] if is_sunday else COLORS['black']
    canvas.setFillColor(day_color)
    canvas.setFont(FONT_BOLD, SIZE_DAY_NUM)
    canvas.drawString(left_x, left_y - 4, str(day_num))
    
    # Nom du jour
    left_y -= 5
    canvas.setFillColor(COLORS['dark_blue'])
    canvas.setFont(FONT_REGULAR, SIZE_DAY_NAME)
    canvas.drawString(left_x, left_y - 4, day_info["weekday"][:3].upper())
    
    # Badge de couleur liturgique
    left_y -= 5
    if specific_data is not None and liturgical_color_id != "vert":
        badge_width = 10
        badge_height = 3
        color_obj = liturgical_colors.get(liturgical_color_id, COLORS['green'])
        canvas.setFillColor(color_obj)
        canvas.setLineWidth(0.3)
        canvas.setStrokeColor(COLORS['dark_blue'])
        canvas.rect(left_x, left_y - 4, badge_width, badge_height, fill=1, stroke=1)
    
    # Icône de phase lunaire
    moon_path = None
    if month_data and not month_data["lunes"].empty:
        lune_df = month_data["lunes"]
        lune_row = lune_df[lune_df['date'] == date_str]
        if not lune_row.empty:
            phase_id = lune_row.iloc[0].get('phase_id', '')
            moon_path = get_moon_icon(str(phase_id).strip().lower())
    
    # COLONNE CENTRALE (Texte)
    center_x = x + 18
    center_width = width - 40
    event_y = y + height - 9
    line_height = 6
    
    # Événement liturgique
    if specific_data is not None:
        name = specific_data.get('nom_dimanche', '')
        if pd.notna(name) and name:
            event_text = str(name)
            canvas.setFillColor(COLOR_HEADER)
            canvas.setFont(FONT_BOLD, SIZE_PROGRAM - 0.5)
            canvas.drawString(center_x, event_y, event_text)
            event_y -= line_height
        
        # Lectures
        readings = []
        for col in ['lecture1', 'psaume', 'lecture2', 'evangile']:
            val = specific_data.get(col)
            if pd.notna(val) and str(val).strip():
                readings.append(str(val).strip())
        
        if readings:
            verse = " | ".join(readings)
            canvas.setFillColor(COLOR_TEXT_SECONDARY)
            canvas.setFont(FONT_ITALIC, SIZE_VERSE - 0.5)
            if len(verse) > 25:
                verse = verse[:22] + "…"
            canvas.drawString(center_x, event_y, f"« {verse} »")
            event_y -= line_height
    
    # Programmes de l'église
    if month_data and not month_data["eglise"].empty:
        prog_df = month_data["eglise"]
        prog_row = prog_df[prog_df['date'] == date_str]
        if not prog_row.empty:
            p = prog_row.iloc[0]
            text = f"{p.get('programme1', '')} {p.get('programme2', '')}".strip()
            if text:
                if len(text) > 25:
                    text = text[:22] + "…"
                canvas.setFillColor(COLOR_TEXT_SECONDARY)
                canvas.setFont(FONT_REGULAR, SIZE_PROGRAM - 1.5)
                canvas.drawString(center_x, event_y, text)
                event_y -= line_height
    
    # COLONNE DE DROITE (Icônes agricoles et Lune)
    if moon_path:
        moon_x = x + width - 25
        moon_y = y + height - 7
        try:
            canvas.drawImage(moon_path, moon_x, moon_y - icon_size, width=icon_size, height=icon_size, mask='auto')
        except: pass
    
    if month_data and not month_data["agricole"].empty:
        agri_df = month_data["agricole"]
        agri_row = agri_df[agri_df['date'] == date_str]
        if not agri_row.empty:
            row = agri_row.iloc[0]
            culture_path = get_culture_icon(row.get('culture_id', ''))
            action_path = get_agri_icon(row.get('action_id', ''))
            agri_icon_x = x + width - icon_size - 1
            agri_icon_y = y + height - 7
            
            if action_path:
                try:
                    canvas.drawImage(action_path, agri_icon_x, agri_icon_y - icon_size, width=icon_size, height=icon_size, mask='auto')
                    agri_icon_x -= icon_size + icon_spacing
                except: pass
            
            if culture_path:
                try:
                    canvas.drawImage(culture_path, agri_icon_x, agri_icon_y - icon_size, width=icon_size, height=icon_size, mask='auto')
                except: pass
