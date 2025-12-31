import os
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from config.page import PAGE_SIZE, PAGE_SIZE_A4
from layout.day_row import draw_day_row, calculate_day_height
from utils.date_utils import get_days_in_month
from utils.csv_loader import get_month_data, get_global_data
from config.fonts import SIZE_HEADER_MAIN
from config.colors import COLORS, MONTH_COLORS, COLOR_TEXT_SECONDARY, COLOR_HEADER, COLOR_BACKGROUND, COLOR_GRID, COLOR_HEADER_BG
import math

def draw_wave_decoration(c, width, height, color, position='top'):
    """Dessine une vague décorative moderne"""
    wave_height = 80
    wave_amplitude = 20
    c.saveState()
    c.setFillColor(color)
    if position == 'top':
        y_base = height - wave_height
    else:
        y_base = wave_height
    p = c.beginPath()
    if position == 'top':
        p.moveTo(0, height)
        for x in range(0, int(width) + 1, 5):
            y = y_base + wave_amplitude * math.sin(x * 0.02)
            p.lineTo(x, y)
        p.lineTo(width, height)
    else:
        p.moveTo(0, 0)
        for x in range(0, int(width) + 1, 5):
            y = y_base + wave_amplitude * math.sin(x * 0.02)
            p.lineTo(x, y)
        p.lineTo(width, 0)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()

def draw_header(c, width, height, page_num, global_data):
    """Dessine l'en-tête avec les logos et les titres."""
    logo_eglise = "assets/images/logo_eglise.png"
    logo_agri = "assets/images/logo_agri.png"
    # Augmentation de 8% par rapport à l'original (0.20 * 1.08 = 0.216)
    header_height = height * 0.216
    logo_size = header_height * 0.5
    
    c.saveState()
    c.setFillColor(COLORS['blue_royal'])
    # On remplit le rectangle bleu pour couvrir la hauteur
    c.rect(0, height - header_height, width, header_height, fill=1, stroke=0)
    c.restoreState()
    
    draw_wave_decoration(c, width, height, COLORS['blue_royal'], 'top')
    
    # Logos positionnés plus haut (center_y augmenté)
    center_y = height - header_height / 2 + 15
    if os.path.exists(logo_eglise):
        c.drawImage(logo_eglise, 40, center_y - logo_size/2, width=logo_size, height=logo_size, mask='auto')
    if os.path.exists(logo_agri):
        c.drawImage(logo_agri, width - 40 - logo_size, center_y - logo_size/2, width=logo_size, height=logo_size, mask='auto')
    
    if not global_data["entetes"].empty:
        entetes_df = global_data["entetes"].sort_values('ligne')
        # Texte repositionné pour l'en-tête réduit
        curr_y = height - 20
        for idx, (_, row) in enumerate(entetes_df.iterrows()):
            text_content = str(row['texte']).strip()
            if idx == 0:
                size = SIZE_HEADER_MAIN * 0.9 # Légère réduction pour l'espace
                c.setFont("Helvetica-Bold", size)
                c.setFillColor(COLORS['white'])
                c.drawCentredString(width/2, curr_y, text_content)
            else:
                size = SIZE_HEADER_MAIN * 0.55
                c.setFont("Helvetica-Bold", size)
                c.setFillColor(COLORS['white'])
                c.drawCentredString(width/2, curr_y, text_content)
            curr_y -= size + 6

def draw_technical_legend(c, x, y, width, height):
    """Dessine une légende technique stylisée avec icônes."""
    from utils.icon_mapper import get_moon_icon, get_agri_icon, get_culture_icon
    c.saveState()
    c.setStrokeColor(COLOR_GRID)
    c.setLineWidth(0.8)
    c.roundRect(x, y, width, height, 8, stroke=1, fill=0)
    c.setFillColor(COLORS['blue_royal'])
    c.roundRect(x, y + height - 15, width, 15, 5, fill=1, stroke=0)
    c.setFillColor(COLORS['white'])
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(x + width/2, y + height - 10, "LÉGENDE")
    
    curr_y = y + height - 30
    c.setFont("Helvetica", 7)
    c.setFillColor(COLORS['black'])
    
    items = [
        ("pleine", "Phase Lunaire"),
        ("riz", "Culture / Travail"),
        ("semis", "Action Agricole"),
    ]
    
    icon_size = 10
    for icon_id, label in items:
        icon_path = None
        if label == "Phase Lunaire":
            icon_path = get_moon_icon(icon_id)
        elif label == "Culture / Travail":
            icon_path = get_culture_icon(icon_id)
        else:
            icon_path = get_agri_icon(icon_id)
            
        if icon_path and os.path.exists(icon_path):
            try:
                c.drawImage(icon_path, x + 8, curr_y - 2, width=icon_size, height=icon_size, mask='auto')
            except: pass
        
        c.drawString(x + 22, curr_y + 1, label)
        curr_y -= 15
        
    c.setFillColor(COLORS['red_carmin'])
    c.rect(x + 8, curr_y - 2, 10, 10, fill=1, stroke=1)
    c.setFillColor(COLORS['black'])
    c.drawString(x + 22, curr_y + 1, "Couleur Liturgique")
    
    c.restoreState()

def draw_month(c, x, y, width, height, year, month, global_data):
    """Dessine le bloc d'un mois."""
    days = get_days_in_month(year, month)
    month_data = get_month_data(month)
    month_color_key = MONTH_COLORS.get(month, 'blue_royal')
    primary_color = COLORS.get(month_color_key, COLORS['blue_royal'])
    c.saveState()
    c.setStrokeColor(primary_color)
    c.setLineWidth(1)
    c.roundRect(x, y, width, height, 8, stroke=1, fill=0)
    c.setFillColor(primary_color)
    c.roundRect(x, y + height - 18, width, 18, 5, fill=1, stroke=1)
    c.setFillColor(COLORS['white'])
    c.setFont("Helvetica-Bold", 9)
    month_names = ["JANVIER / JANOARY", "FÉVRIER / FEBROARY", "MARS / MARTSA", "AVRIL / APRILY", "MAI / MAY", "JUIN / JONA", "JUILLET / JOLAY", "AOÛT / AOGOSITRA", "SEPTEMBRE / SEPTAMBRA", "OCTOBRE / OKTOBRA", "NOVEMBRE / NOVAMBRA", "DÉCEMBRE / DESAMBRA"]
    c.drawCentredString(x + width/2, y + height - 12, month_names[month-1])
    c.restoreState()
    available_h = height - 20
    day_heights = [calculate_day_height(d, month_data) for d in days]
    total_req = sum(day_heights)
    scale = min(1.0, available_h / total_req)
    scaled_heights = [h * scale for h in day_heights]
    curr_y = y + available_h
    for d, row_h in zip(days, scaled_heights):
        curr_y -= row_h
        draw_day_row(c, x, curr_y, width, row_h, d, month_data=month_data, global_data=global_data)

def draw_page(c, year, start_month, end_month, page_num, page_size=PAGE_SIZE):
    """Dessine une page : 1 col (2 photos + légende) | 6 mois."""
    width, height = page_size
    is_a4 = (page_size == PAGE_SIZE_A4)
    
    # Marges standards pour l'impression (env. 1cm = 28.3 pts)
    margin_x = 30
    margin_y = 30
    header_h = height * 0.216 # En-tête réduit pour maximiser le calendrier
    
    photo_col_width = (width - 2 * margin_x) * 0.18
    months_area_width = width - photo_col_width - 2 * margin_x
    month_col_width = months_area_width / 6
    num_cols = 6
    num_rows = 1

    global_data = get_global_data()
    draw_header(c, width, height, page_num, global_data)
    draw_wave_decoration(c, width, height, COLORS['gold'], 'bottom')

    # Zone utile sous le header
    content_h = height - header_h - 2 * margin_y
    photo_h = content_h * 0.40
    legend_h = content_h * 0.18
    
    start_y = height - header_h - margin_y
    
    for i in range(2):
        photo_idx = (page_num - 1) * 2 + i + 1
        photo_path = f"assets/images/photo{photo_idx}.jpg"
        if os.path.exists(photo_path):
            img_y = start_y - (i + 1) * photo_h
            c.saveState()
            c.setStrokeColor(COLOR_GRID)
            c.roundRect(margin_x, img_y + 10, photo_col_width - 5, photo_h - 15, 8, stroke=1, fill=0)
            c.drawImage(photo_path, margin_x + 2, img_y + 12, width=photo_col_width - 9, height=photo_h - 19, preserveAspectRatio=True, anchor='c')
            c.restoreState()
    
    legend_y = margin_y + 5
    draw_technical_legend(c, margin_x, legend_y, photo_col_width - 5, legend_h)

    for i, month in enumerate(range(start_month, end_month + 1)):
        x = margin_x + photo_col_width + i * month_col_width
        draw_month(c, x, margin_y + 5, month_col_width - 6, height - header_h - margin_y - 15, year, month, global_data)

def generate_calendar():
    """Génère le PDF final."""
    if not os.path.exists("output"): os.makedirs("output")
    
    # Version A3
    c3 = canvas.Canvas("output/calendrier_A3.pdf", pagesize=PAGE_SIZE)
    year = 2026
    for page in [1, 2]:
        c3.setFillColor(COLOR_BACKGROUND)
        c3.rect(0, 0, PAGE_SIZE[0], PAGE_SIZE[1], fill=1, stroke=0)
        draw_page(c3, year, 1 if page == 1 else 7, 6 if page == 1 else 12, page, PAGE_SIZE)
        c3.showPage()
    c3.save()

    # Version A4
    c4 = canvas.Canvas("output/calendrier_A4.pdf", pagesize=PAGE_SIZE_A4)
    for page in [1, 2]:
        c4.setFillColor(COLOR_BACKGROUND)
        c4.rect(0, 0, PAGE_SIZE_A4[0], PAGE_SIZE_A4[1], fill=1, stroke=0)
        draw_page(c4, year, 1 if page == 1 else 7, 6 if page == 1 else 12, page, PAGE_SIZE_A4)
        c4.showPage()
    c4.save()
    print("PDFs générés avec succès.")

if __name__ == "__main__":
    generate_calendar()
