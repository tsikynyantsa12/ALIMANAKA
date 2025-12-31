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
    
    # ========== 3-COLUMN LAYOUT: LEFT | CENTER | RIGHT ==========
    # LEFT: Date, Name, Badge, Moon Phase (no underline, stacked vertically)
    # CENTER: Text content (liturgical events, readings, programs)
    # RIGHT: Agricultural icons
    
    icon_size = 8  # Small consistent icons
    icon_spacing = 2
    
    # ===== LEFT COLUMN (Date, Name, Badge, Moon Phase) =====
    left_x = x + 2
    left_y = y + height - 8
    
    # Line 1: Day Number
    day_color = HexColor("#E8B4B8") if is_sunday else HexColor("#F5F5F0")  # Soft red or warm white
    canvas.setFillColor(day_color)
    canvas.setFont(FONT_BOLD, SIZE_DAY_NUM)
    canvas.drawString(left_x, left_y, str(day_num))
    
    # Line 2: Day Name (one line below)
    left_y -= 7
    canvas.setFillColor(HexColor("#F0E68C"))  # Softer light yellow
    canvas.setFont(FONT_REGULAR, SIZE_DAY_NAME)
    canvas.drawString(left_x, left_y, day_info["weekday"][:3].upper())
    
    # Line 3: Liturgical Color Badge
    left_y -= 6
    if specific_data is not None and liturgical_color_id != "vert":
        badge_width = 14
        badge_height = 5
        color_obj = liturgical_colors.get(liturgical_color_id, HexColor("#90EE90"))
        canvas.setFillColor(color_obj)
        canvas.setLineWidth(0.5)
        canvas.setStrokeColor(COLOR_TEXT_SECONDARY)
        canvas.rect(left_x, left_y, badge_width, badge_height, fill=1, stroke=1)
    
    # Line 4: Moon Phase Icon (if available)
    left_y -= 7
    moon_path = None
    if month_data and not month_data["lunes"].empty:
        lune_df = month_data["lunes"]
        lune_row = lune_df[lune_df['date'] == date_str]
        if not lune_row.empty:
            phase_id = lune_row.iloc[0].get('phase_id', '')
            moon_path = get_moon_icon(str(phase_id).strip().lower())
    
    if moon_path:
        try:
            canvas.drawImage(moon_path, left_x, left_y - icon_size, width=icon_size, height=icon_size, mask='auto')
        except:
            pass
    
    # ===== CENTER COLUMN (Text Content) =====
    center_x = x + 22  # Start after left column
    center_width = width - 50  # Space for left + right
    event_y = y + height - 12  # Start from top
    line_height = 7
    
    # Text Content (liturgical events, readings, programs)
    # 3a. Liturgical event name
    if specific_data is not None:
        name = specific_data.get('nom_dimanche', '')
        if pd.notna(name) and name:
            event_text = str(name)
            canvas.setFillColor(COLOR_TEXT)
            canvas.setFont(FONT_BOLD, SIZE_PROGRAM)
            canvas.drawString(center_x, event_y, event_text)
            event_y -= line_height
        
        # 3b. Readings (smaller, secondary)
        readings = []
        for col in ['lecture1', 'psaume', 'lecture2', 'evangile']:
            val = specific_data.get(col)
            if pd.notna(val) and str(val).strip():
                readings.append(str(val).strip())
        
        if readings:
            verse = " | ".join(readings)
            canvas.setFillColor(COLOR_TEXT_SECONDARY)
            canvas.setFont(FONT_ITALIC, SIZE_VERSE)
            # Truncate long readings to prevent overlap
            if len(verse) > 30:
                verse = verse[:27] + "…"
            canvas.drawString(center_x, event_y, f"« {verse} »")
            event_y -= line_height
    
    # 3c. Church programs
    if month_data and not month_data["eglise"].empty:
        prog_df = month_data["eglise"]
        prog_row = prog_df[prog_df['date'] == date_str]
        if not prog_row.empty:
            p = prog_row.iloc[0]
            text = f"{p.get('programme1', '')} {p.get('programme2', '')}".strip()
            if text:
                # Truncate to prevent overlap
                if len(text) > 30:
                    text = text[:27] + "…"
                canvas.setFillColor(COLOR_TEXT_SECONDARY)
                canvas.setFont(FONT_REGULAR, SIZE_PROGRAM - 1)
                canvas.drawString(center_x, event_y, text)
                event_y -= line_height
    
    # ===== RIGHT COLUMN (Agricultural Icons) =====
    if month_data and not month_data["agricole"].empty:
        agri_df = month_data["agricole"]
        agri_row = agri_df[agri_df['date'] == date_str]
        if not agri_row.empty:
            row = agri_row.iloc[0]
            
            # Get culture and action icons
            culture_path = get_culture_icon(row.get('culture_id', ''))
            action_path = get_agri_icon(row.get('action_id', ''))
            
            # Position icons at right side, top area
            agri_icon_x = x + width - icon_size - 2
            agri_icon_y = y + height - 8
            
            # Draw action icon (rightmost)
            if action_path:
                try:
                    canvas.drawImage(action_path, agri_icon_x, agri_icon_y - icon_size, width=icon_size, height=icon_size, mask='auto')
                    agri_icon_x -= icon_size + icon_spacing
                except:
                    pass
            
            # Draw culture icon (left of action icon)
            if culture_path:
                try:
                    canvas.drawImage(culture_path, agri_icon_x, agri_icon_y - icon_size, width=icon_size, height=icon_size, mask='auto')
                except:
                    pass
