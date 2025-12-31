import pandas as pd
from reportlab.lib.colors import HexColor
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

    # Thin separator line (transparent layout, no backgrounds)
    canvas.saveState()
    canvas.setStrokeColor(COLOR_GRID)
    canvas.setLineWidth(0.5)
    canvas.line(x, y, x + width, y)
    canvas.restoreState()
    
    # Day Typography (top-left aligned for clear reading order)
    # Day number - Sundays in soft red, weekdays in warm white
    day_color = HexColor("#E8B4B8") if is_sunday else HexColor("#F5F5F0")  # Soft red or warm white
    canvas.setFillColor(day_color)
    canvas.setFont(FONT_BOLD, SIZE_DAY_NUM)
    canvas.drawString(x + 5, y + height - 13, str(day_num))  # Reduced from 6/14 to 5/13
    
    # Day name - soft light tone for secondary hierarchy
    canvas.setFillColor(HexColor("#F0E68C"))  # Softer light yellow
    canvas.setFont(FONT_REGULAR, SIZE_DAY_NAME)
    canvas.drawString(x + 5, y + 4, day_info["weekday"][:3].upper())  # Reduced from 6 to 5, y from 6 to 4
    
    icon_size = 8  # Small consistent icons
    icon_spacing = 2  # Space between icon and text
    
    # Content area for events (with space for icons on left)
    content_x = x + 24  # Reduced from 26 (compact day column)
    content_width = width - 40  # Adjusted width
    event_y = y + height - 16  # Reduced from 18 (saves 2pt per day)
    line_height = 7  # Reduced from 8 (tighter event spacing)
    
    # Render events with icons inline (left-aligned)
    rendered_events = 0
    
    # 1. Liturgical events (with optional moon icon)
    if specific_data is not None:
        name = specific_data.get('nom_dimanche', '')
        if pd.notna(name) and name:
            event_text = str(name)
            
            # Try to get moon phase icon for this day
            moon_path = None
            if month_data and not month_data["lunes"].empty:
                lune_df = month_data["lunes"]
                lune_row = lune_df[lune_df['date'] == date_str]
                if not lune_row.empty:
                    phase_id = lune_row.iloc[0].get('phase_id', '')
                    moon_path = get_moon_icon(str(phase_id).strip().lower())
            
            # Draw moon icon if available (left of text)
            icon_x = content_x
            text_x = content_x + icon_spacing + 2
            if moon_path:
                try:
                    canvas.drawImage(moon_path, icon_x, event_y - icon_size, width=icon_size, height=icon_size, mask='auto')
                    text_x += icon_size + icon_spacing
                except:
                    pass
            
            # Draw event text
            canvas.setFillColor(COLOR_TEXT)
            canvas.setFont(FONT_BOLD, SIZE_PROGRAM)
            canvas.drawString(text_x, event_y, event_text)
            rendered_events += 1
            event_y -= line_height
        
        # Readings (smaller, no icon)
        readings = []
        for col in ['lecture1', 'psaume', 'lecture2', 'evangile']:
            val = specific_data.get(col)
            if pd.notna(val) and str(val).strip():
                readings.append(str(val).strip())
        
        if readings:
            verse = " | ".join(readings)
            canvas.setFillColor(COLOR_TEXT_SECONDARY)
            canvas.setFont(FONT_ITALIC, SIZE_VERSE)
            canvas.drawString(content_x, event_y, f"« {verse} »")
            event_y -= line_height
    
    # 2. Church programs (with action icon)
    if month_data and not month_data["eglise"].empty:
        prog_df = month_data["eglise"]
        prog_row = prog_df[prog_df['date'] == date_str]
        if not prog_row.empty:
            p = prog_row.iloc[0]
            text = f"{p.get('programme1', '')} {p.get('programme2', '')}".strip()
            if text:
                # Programs don't have semantic icons, render as simple text
                canvas.setFillColor(COLOR_TEXT_SECONDARY)
                canvas.setFont(FONT_REGULAR, SIZE_PROGRAM - 1)
                canvas.drawString(content_x, event_y, text)
                rendered_events += 1
                event_y -= line_height
    
    # 3. Agricultural events (with culture + action icons)
    if month_data and not month_data["agricole"].empty:
        agri_df = month_data["agricole"]
        agri_row = agri_df[agri_df['date'] == date_str]
        if not agri_row.empty:
            row = agri_row.iloc[0]
            
            # Get culture and action icons
            culture_path = get_culture_icon(row.get('culture_id', ''))
            action_path = get_agri_icon(row.get('action_id', ''))
            
            # Icons positioned left of text
            icon_x = content_x
            text_x = content_x + icon_spacing + 2
            
            # Draw culture icon (first icon, leftmost)
            if culture_path:
                try:
                    canvas.drawImage(culture_path, icon_x, event_y - icon_size, width=icon_size, height=icon_size, mask='auto')
                    text_x = content_x + icon_size + icon_spacing + 2
                except:
                    pass
            
            # Draw action icon (second icon, next to culture)
            if action_path:
                try:
                    canvas.drawImage(action_path, icon_x + icon_size + icon_spacing, event_y - icon_size, width=icon_size, height=icon_size, mask='auto')
                    text_x = content_x + (icon_size + icon_spacing) * 2 + 2
                except:
                    pass
            
            # Agricultural event label (if any)
            if culture_path or action_path:
                canvas.setFillColor(COLOR_TEXT_SECONDARY)
                canvas.setFont(FONT_REGULAR, SIZE_PROGRAM - 1)
                canvas.drawString(text_x, event_y, "Agriculture")
