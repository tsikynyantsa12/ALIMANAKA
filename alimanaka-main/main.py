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
    """Dessine l'en-tête avec les logos et les titres de l'église et agriculture."""
    logo_eglise = "assets/images/logo_eglise.png"
    logo_agri = "assets/images/logo_agri.png"

    header_height = height * 0.15 
    logo_size = header_height * 0.6

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

def draw_legend_box(c, x, y, width, height, month, global_data):
    """Dessine la zone de légendes en bas (remplace les photos)."""
    month_color_key = MONTH_COLORS.get(month, 'blue_royal')
    primary_color = COLORS.get(month_color_key, COLORS['blue_royal'])
    
    c.saveState()
    c.setStrokeColor(primary_color)
    c.setLineWidth(1)
    c.rect(x, y, width, height, stroke=1, fill=0)
    
    c.setFillColor(primary_color)
    c.rect(x, y + height - 15, width, 15, fill=1, stroke=0)
    
    c.setFillColor(COLORS['white'])
    c.setFont("Helvetica-Bold", 8)
    month_names = ["JANVIER", "FÉVRIER", "MARS", "AVRIL", "MAI", "JUIN", "JUILLET", "AOÛT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DÉCEMBRE"]
    c.drawCentredString(x + width/2, y + height - 10, f"LÉGENDES & ÉVÉNEMENTS - {month_names[month-1]} 2026")
    
    month_data = get_month_data(month)
    curr_ly = y + height - 25
    c.setFillColor(COLORS['black'])
    c.setFont("Helvetica", 6)
    
    if not month_data["dimanches"].empty:
        for _, row in month_data["dimanches"].head(5).iterrows():
            text = f"• {row['date'].split('-')[-1]} : {row['nom_dimanche']}"
            if len(text) > 40: text = text[:37] + "..."
            c.drawString(x + 5, curr_ly, text)
            curr_ly -= 8
            if curr_ly < y + 5: break
            
    c.restoreState()

def draw_month(c, x, y, width, height, year, month, global_data):
    """Dessine le bloc d'un mois spécifique avec bordures stylisées."""
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

def draw_page(c, year, start_month, end_month, page_num):
    """Dessine une page avec 6 mois et des légendes en bas."""
    width, height = PAGE_SIZE
    margin_x = 20
    margin_y = 20
    header_h = height * 0.15
    legend_h = 80
    
    months_area_width = width - 2 * margin_x
    month_col_width = months_area_width / 6
    
    global_data = get_global_data()
    draw_header(c, width, height, page_num, global_data)
    
    draw_wave_decoration(c, width, height, COLORS['gold'], 'bottom')

    for i, month in enumerate(range(start_month, end_month + 1)):
        x = margin_x + i * month_col_width
        draw_month(c, x, margin_y + legend_h + 5, month_col_width - 6, height - header_h - legend_h - margin_y - 20, year, month, global_data)
        draw_legend_box(c, x, margin_y + 5, month_col_width - 6, legend_h, month, global_data)

def generate_calendar():
    """Génère le PDF complet (A3 Paysage, 2 pages)."""
    if not os.path.exists("output"):
        os.makedirs("output")
    c = canvas.Canvas("output/calendrier_A3.pdf", pagesize=PAGE_SIZE)
    year = 2026
    
    c.setFillColor(COLOR_BACKGROUND)
    c.rect(0, 0, PAGE_SIZE[0], PAGE_SIZE[1], fill=1, stroke=0)
    draw_page(c, year, 1, 6, 1)
    c.showPage()
    
    c.setFillColor(COLOR_BACKGROUND)
    c.rect(0, 0, PAGE_SIZE[0], PAGE_SIZE[1], fill=1, stroke=0)
    draw_page(c, year, 7, 12, 2)
    c.showPage()
    
    c.save()

if __name__ == "__main__":
    generate_calendar()
