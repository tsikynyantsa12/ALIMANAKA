import os
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from config.page import PAGE_SIZE
from layout.day_row import draw_day_row, calculate_day_height
from utils.date_utils import get_days_in_month, get_weekday_fr
from utils.csv_loader import get_month_data, get_global_data
from config.fonts import SIZE_HEADER_MAIN
from config.colors import COLOR_TEXT, COLOR_GRID

def draw_background(c, width, height):
    bg_path = "assets/images/background_eglise.jpg"
    if os.path.exists(bg_path):
        c.saveState()
        # Full HD, 100% visible, sharp
        c.drawImage(bg_path, 0, 0, width=width, height=height, mask='auto')
        c.restoreState()

def draw_header(c, width, height, page_num, global_data):
    from config.colors import COLOR_HEADER
    
    logo_eglise = "assets/images/logo_eglise.png"
    logo_agri = "assets/images/logo_agri.png"
    rose_luther = "assets/images/rose_luther.png"
    photo_l = f"assets/images/photo{1 if page_num == 1 else 3}.jpg"
    photo_r = f"assets/images/photo{2 if page_num == 1 else 4}.jpg"

    header_height = height * 0.25
    logo_size = header_height * 0.5
    photo_size = header_height * 0.6
    rose_size = header_height * 0.3

    # Subtle header background line for cohesion
    c.saveState()
    c.setStrokeColor(COLOR_HEADER)
    c.setLineWidth(1.5)
    c.line(15, height - header_height - 5, width - 15, height - header_height - 5)
    c.restoreState()

    if os.path.exists(logo_eglise):
        c.drawImage(logo_eglise, 40, height - header_height/2 - logo_size/2, width=logo_size, height=logo_size, mask='auto')
    if os.path.exists(logo_agri):
        c.drawImage(logo_agri, width - 40 - logo_size, height - header_height/2 - logo_size/2, width=logo_size, height=logo_size, mask='auto')
    if os.path.exists(rose_luther):
        c.drawImage(rose_luther, width/2 - rose_size/2, height - rose_size - 10, width=rose_size, height=rose_size, mask='auto')

    if os.path.exists(photo_l):
        c.drawImage(photo_l, 40 + logo_size + 20, height - header_height/2 - photo_size/2, width=photo_size, height=photo_size, mask='auto')
    if os.path.exists(photo_r):
        c.drawImage(photo_r, width - 40 - logo_size - 20 - photo_size, height - header_height/2 - photo_size/2, width=photo_size, height=photo_size, mask='auto')

    if not global_data["entetes"].empty:
        c.setFillColor(COLOR_HEADER)
        entetes_df = global_data["entetes"].sort_values('ligne')
        curr_y = height - 35
        for idx, (_, row) in enumerate(entetes_df.iterrows()):
            if idx == 0:
                size = SIZE_HEADER_MAIN
            elif idx == len(entetes_df) - 1:
                size = SIZE_HEADER_MAIN * 0.65
            else:
                size = SIZE_HEADER_MAIN * 0.7
            c.setFont("Helvetica-Bold", size)
            c.drawCentredString(width/2, curr_y, str(row['texte']).strip())
            curr_y -= size + 6

def generate_calendar():
    c = canvas.Canvas("output/calendrier_A3.pdf", pagesize=PAGE_SIZE)
    year = 2026
    draw_background(c, PAGE_SIZE[0], PAGE_SIZE[1])
    draw_page(c, year, 1, 6, 1)
    c.showPage()
    draw_background(c, PAGE_SIZE[0], PAGE_SIZE[1])
    draw_page(c, year, 7, 12, 2)
    c.showPage()
    c.save()

def draw_page(c, year, start_month, end_month, page_num):
    width, height = PAGE_SIZE
    margin = 15
    col_width = (width - 2 * margin) / 6
    global_data = get_global_data()
    header_height_req = height * 0.25
    draw_header(c, width, height, page_num, global_data)

    for i, month in enumerate(range(start_month, end_month + 1)):
        x = margin + i * col_width
        # Visual separation by spacing and thin lines
        if i > 0:
            c.setStrokeColor(COLOR_GRID)
            c.setLineWidth(0.5)
            c.line(x - 4, margin, x - 4, height - header_height_req - 10)
            
        draw_month(c, x, margin, col_width - 8, height - header_height_req - 20, year, month, global_data)

def draw_month(c, x, y, width, height, year, month, global_data):
    from config.colors import COLOR_HEADER
    
    days = get_days_in_month(year, month)
    month_data = get_month_data(month)
    
    # Month Border (subtle frame)
    c.saveState()
    c.setStrokeColor(COLOR_HEADER)
    c.setLineWidth(0.75)
    c.setFillAlpha(0.02)
    c.rect(x, y, width, height, fill=0, stroke=1)
    c.setFillAlpha(1.0)
    c.restoreState()
    
    # Month Title (Uppercase, Bold, No background)
    c.saveState()
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica-Bold", 12)
    month_names = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    c.drawCentredString(x + width/2, y + height - 10, month_names[month-1].upper())
    
    # Underline for month title
    c.setStrokeColor(COLOR_HEADER)
    c.setLineWidth(1.2)
    c.line(x + 10, y + height - 14, x + width - 10, y + height - 14)
    c.restoreState()
    
    available_height = height - 20
    day_heights = [calculate_day_height(d, month_data) for d in days]
    total_req = sum(day_heights)
    scale = min(1.0, available_height / total_req)
    scaled_heights = [h * scale for h in day_heights]
    
    curr_y = y + available_height
    for d, row_h in zip(days, scaled_heights):
        curr_y -= row_h
        draw_day_row(c, x, curr_y, width, row_h, d, month_data=month_data, global_data=global_data)

if __name__ == "__main__":
    if not os.path.exists("output"):
        os.makedirs("output")
    generate_calendar()
