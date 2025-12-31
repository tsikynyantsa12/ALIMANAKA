import os
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from config.page import PAGE_SIZE
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
        direction = 1
    else:
        y_base = wave_height
        direction = -1
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
    header_height = height * 0.18 # Augmenté pour couvrir le texte
    logo_size = header_height * 0.5

    draw_wave_decoration(c, width, height, COLORS['blue_royal'], 'top')
    center_y = height - header_height / 2

    if os.path.exists(logo_eglise):
        c.drawImage(logo_eglise, 40, center_y - logo_size/2, width=logo_size, height=logo_size, mask='auto')
    if os.path.exists(logo_agri):
        c.drawImage(logo_agri, width - 40 - logo_size, center_y - logo_size/2, width=logo_size, height=logo_size, mask='auto')

    if not global_data["entetes"].empty:
        entetes_df = global_data["entetes"].sort_values('ligne')
        curr_y = height - 25
        for idx, (_, row) in enumerate(entetes_df.iterrows()):
            text_content = str(row['texte']).strip()
            if idx == 0:
                size = SIZE_HEADER_MAIN
                c.setFont("Helvetica-Bold", size)
                c.setFillColor(COLORS['white'])
                c.drawCentredString(width/2, curr_y, text_content)
            else:
                size = SIZE_HEADER_MAIN * 0.6
                c.setFont("Helvetica-Bold", size)
                c.setFillColor(COLORS['white'])
                c.drawCentredString(width/2, curr_y, text_content)
            curr_y -= size + 5

def draw_technical_legend(c, x, y, width, height):
    """Dessine une légende technique (lunes, cultures, actions, couleurs)."""
    c.saveState()
    c.setStrokeColor(COLOR_GRID)
    c.setLineWidth(0.5)
    c.rect(x, y, width, height, stroke=1, fill=0)
    
    curr_y = y + height - 12
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(COLOR_HEADER)
    c.drawString(x + 5, curr_y, "LÉGENDE TECHNIQUE")
    curr_y -= 10
    
    c.setFont("Helvetica", 6)
    c.setFillColor(COLORS['black'])
    legends = [
        "● Phase Lunaire",
        "🌱 Culture / Travail",
        "🚜 Action Agricole",
        "■ Couleur Liturgique"
    ]
    for text in legends:
        c.drawString(x + 5, curr_y, text)
        curr_y -= 8
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
    c.rect(x, y, width, height, stroke=1, fill=0)
    c.setFillColor(primary_color)
    c.rect(x, y + height - 18, width, 18, fill=1, stroke=1)
    c.setFillColor(COLORS['white'])
    c.setFont("Helvetica-Bold", 9)
    month_names = ["JANVIER", "FÉVRIER", "MARS", "AVRIL", "MAI", "JUIN", "JUILLET", "AOÛT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DÉCEMBRE"]
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

def draw_page(c, year, start_month, end_month, page_num, format='A3'):
    """Dessine une page avec 1 col photo/légende et 6 mois."""
    width, height = (PAGE_SIZE if format == 'A3' else (841, 595)) # Approx A4 landscape in points
    margin_x = 20
    margin_y = 20
    header_h = height * 0.18
    
    photo_col_width = width * 0.18 # Un peu plus de place
    months_area_width = width - photo_col_width - 2 * margin_x
    month_col_width = months_area_width / 6
    
    global_data = get_global_data()
    draw_header(c, width, height, page_num, global_data)
    draw_wave_decoration(c, width, height, COLORS['gold'], 'bottom')

    # Colonne de gauche : 2 photos + légende technique
    photo_h = (height - header_h - 2 * margin_y) / 4
    for i in range(2):
        photo_idx = (page_num - 1) * 2 + i + 1
        photo_path = f"assets/images/photo{photo_idx}.jpg"
        if os.path.exists(photo_path):
            img_y = height - header_h - margin_y - (i + 1) * photo_h
            c.saveState()
            c.setStrokeColor(COLOR_GRID)
            # Bordures arrondies simulées avec roundRect
            c.roundRect(margin_x, img_y, photo_col_width - 5, photo_h - 5, 8, stroke=1, fill=0)
            c.drawImage(photo_path, margin_x + 2, img_y + 2, width=photo_col_width - 9, height=photo_h - 9, preserveAspectRatio=True, anchor='c')
            c.restoreState()
    
    # Légende technique sous les photos
    legend_y = margin_y + 10
    draw_technical_legend(c, margin_x, legend_y, photo_col_width - 5, photo_h)

    # Mois
    for i, month in enumerate(range(start_month, end_month + 1)):
        x = margin_x + photo_col_width + i * month_col_width
        draw_month(c, x, margin_y + 5, month_col_width - 6, height - header_h - margin_y - 10, year, month, global_data)

def generate_calendar():
    """Génère les versions A3 et A4."""
    if not os.path.exists("output"): os.makedirs("output")
    
    # Version A3
    c_a3 = canvas.Canvas("output/calendrier_A3.pdf", pagesize=PAGE_SIZE)
    year = 2026
    for page in [1, 2]:
        c_a3.setFillColor(COLOR_BACKGROUND)
        c_a3.rect(0, 0, PAGE_SIZE[0], PAGE_SIZE[1], fill=1, stroke=0)
        draw_page(c_a3, year, 1 if page == 1 else 7, 6 if page == 1 else 12, page, format='A3')
        c_a3.showPage()
    c_a3.save()
    
    # Version A4
    from reportlab.lib.pagesizes import A4, landscape
    A4_LANDSCAPE = landscape(A4)
    c_a4 = canvas.Canvas("output/calendrier_A4_simplifie.pdf", pagesize=A4_LANDSCAPE)
    for page in [1, 2]:
        c_a4.setFillColor(COLOR_BACKGROUND)
        c_a4.rect(0, 0, A4_LANDSCAPE[0], A4_LANDSCAPE[1], fill=1, stroke=0)
        draw_page(c_a4, year, 1 if page == 1 else 7, 6 if page == 1 else 12, page, format='A4')
        c_a4.showPage()
    c_a4.save()

if __name__ == "__main__":
    generate_calendar()
