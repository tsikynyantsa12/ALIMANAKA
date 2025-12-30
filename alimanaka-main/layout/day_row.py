import pandas as pd
from config.colors import COLOR_TEXT, COLOR_TEXT_SECONDARY, COLOR_DIMANCHE, COLOR_GRID
from config.fonts import FONT_BOLD, FONT_REGULAR, FONT_ITALIC, SIZE_DAY_NUM, SIZE_DAY_NAME, SIZE_PROGRAM, SIZE_VERSE
from utils.icon_mapper import get_moon_icon, get_agri_icon, get_culture_icon
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT

styles = getSampleStyleSheet()
# Adding subtle text shadow simulation via leading/styling isn't direct in Paragraph, 
# but we focus on weight contrast and clarity.
style_program = ParagraphStyle('Program', parent=styles['Normal'], fontSize=SIZE_PROGRAM, leading=SIZE_PROGRAM+3, alignment=TA_LEFT, textColor=COLOR_TEXT, fontName=FONT_BOLD)
style_verse = ParagraphStyle('Verse', parent=styles['Normal'], fontSize=SIZE_VERSE-1, leading=SIZE_VERSE+2, alignment=TA_LEFT, textColor=COLOR_TEXT_SECONDARY, fontName=FONT_ITALIC)

def calculate_day_height(day_info, month_data):
    base_height = 24 # Whitespace as main structure
    date_str = day_info["date"].isoformat()
    extra_height = 0
    if month_data and not month_data["dimanches"].empty:
        df = month_data["dimanches"]
        row = df[df['date'] == date_str]
        if not row.empty:
            extra_height += 20
    if month_data and not month_data["eglise"].empty:
        prog_df = month_data["eglise"]
        prog_row = prog_df[prog_df['date'] == date_str]
        if not prog_row.empty:
            extra_height += 10
    return base_height + extra_height

def draw_day_row(canvas, x, y, width, height, day_info, month_data=None, global_data=None):
    from config.colors import get_liturgical_colors
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

    # Separation by horizontal line (1px, low opacity)
    canvas.saveState()
    canvas.setStrokeColor(COLOR_GRID)
    canvas.setLineWidth(0.5)
    canvas.line(x, y, x + width, y)
    
    # Larger color indicator (left bar - 5px for better visibility)
    bg_color = COLOR_DIMANCHE if is_sunday else liturgical_colors.get(liturgical_color_id, liturgical_colors.get("vert"))
    canvas.setFillColor(bg_color)
    canvas.rect(x, y + 1, 4, height - 2, fill=1, stroke=0)
    
    # Subtle background tint (10% opacity)
    canvas.setFillColor(bg_color)
    canvas.setFillAlpha(0.08)
    canvas.rect(x + 4, y + 1, width - 4, height - 2, fill=1, stroke=0)
    canvas.setFillAlpha(1.0)
    canvas.restoreState()
    
    # Day Typography
    canvas.setFillColor(COLOR_DIMANCHE if is_sunday else COLOR_TEXT)
    canvas.setFont(FONT_BOLD, SIZE_DAY_NUM)
    canvas.drawString(x + 6, y + height - 14, str(day_num))
    
    canvas.setFillColor(COLOR_TEXT_SECONDARY)
    canvas.setFont(FONT_REGULAR, SIZE_DAY_NAME - 3)
    canvas.drawString(x + 6, y + 6, day_info["weekday"][:3].upper())
    
    content_x = x + 26
    content_width = width - 42
    
    story = []
    if specific_data is not None:
        name = specific_data.get('nom_dimanche', '')
        if pd.notna(name) and name:
            story.append(Paragraph(str(name), style_program))
        
        readings = []
        for col in ['lecture1', 'psaume', 'lecture2', 'evangile']:
            val = specific_data.get(col)
            if pd.notna(val) and str(val).strip():
                readings.append(str(val).strip())
        
        verse = " | ".join(readings)
        if verse:
            story.append(Paragraph(f"« {verse} »", style_verse))

    if month_data and not month_data["eglise"].empty:
        prog_df = month_data["eglise"]
        prog_row = prog_df[prog_df['date'] == date_str]
        if not prog_row.empty:
            p = prog_row.iloc[0]
            text = f"{p.get('programme1', '')} {p.get('programme2', '')}".strip()
            if text:
                story.append(Paragraph(text, ParagraphStyle('Small', parent=styles['Normal'], fontSize=SIZE_PROGRAM-1, leading=SIZE_PROGRAM+1, textColor=COLOR_TEXT_SECONDARY)))

    if story:
        f = Frame(content_x, y, content_width, height, leftPadding=1, bottomPadding=2, rightPadding=1, topPadding=1, showBoundary=0)
        f.addFromList(story, canvas)

    icon_size = 10  # Larger icons for better visibility
    icon_spacing = 11  # Space between icons
    
    # Icons layout: top-right for moon, bottom-right for agriculture
    icons_drawn = 0
    
    # Moon icon (top-right)
    if month_data and not month_data["lunes"].empty:
        lune_df = month_data["lunes"]
        lune_row = lune_df[lune_df['date'] == date_str]
        if not lune_row.empty:
            phase_id = lune_row.iloc[0].get('phase_id', '')
            moon_path = get_moon_icon(str(phase_id).strip().lower())
            if moon_path:
                canvas.drawImage(moon_path, x + width - 12, y + height - 12, width=icon_size, height=icon_size, mask='auto')

    # Agricultural icons (bottom-right, stacked horizontally)
    if month_data and not month_data["agricole"].empty:
        agri_df = month_data["agricole"]
        agri_row = agri_df[agri_df['date'] == date_str]
        if not agri_row.empty:
            row = agri_row.iloc[0]
            icon_x = x + width - (icon_size + 2)
            
            # Action icon (first, rightmost)
            action_path = get_agri_icon(row.get('action_id', ''))
            if action_path:
                canvas.drawImage(action_path, icon_x, y + 2, width=icon_size, height=icon_size, mask='auto')
                icon_x -= (icon_size + 1)
                icons_drawn += 1
            
            # Culture icon (second, to the left)
            culture_path = get_culture_icon(row.get('culture_id', ''))
            if culture_path:
                canvas.drawImage(culture_path, icon_x, y + 2, width=icon_size, height=icon_size, mask='auto')
                icons_drawn += 1
