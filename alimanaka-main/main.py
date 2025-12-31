import os
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from config.page import PAGE_SIZE
from layout.day_row import draw_day_row, calculate_day_height
from utils.date_utils import get_days_in_month, get_weekday_fr
from utils.csv_loader import get_month_data, get_global_data
from config.fonts import SIZE_HEADER_MAIN
from config.colors import COLOR_TEXT, COLOR_GRID, COLOR_DARK_BLUE, COLOR_HEADER_BG, COLOR_HEADER_ACCENT

def draw_background(c, width, height):
    bg_path = "assets/images/background_betafo.jpg"
    if os.path.exists(bg_path):
        c.saveState()
        # Full page background - stretch to fill completely without deformation
        # Image is drawn from 0,0 to cover entire page
        c.drawImage(bg_path, 0, 0, width=width, height=height, mask='auto')
        
        # Very subtle overlay (7% opacity) for enhanced text readability
        # without hiding the background image
        c.setFillColor(HexColor("#FFFFFF"))
        c.setFillAlpha(0.07)
        c.rect(0, 0, width, height, fill=1, stroke=0)
        c.setFillAlpha(1.0)
        c.restoreState()

def draw_header(c, width, height, page_num, global_data):
    from config.colors import COLOR_HEADER
    
    logo_eglise = "assets/images/logo_eglise.png"
    logo_agri = "assets/images/logo_agri.png"
    rose_luther = "assets/images/rose_luther.png"
    photo_l = f"assets/images/photo{1 if page_num == 1 else 3}.jpg"
    photo_r = f"assets/images/photo{2 if page_num == 1 else 4}.jpg"

    # Optimized header: reduced height (22% instead of 25%), larger images
    header_height = height * 0.22
    logo_size = header_height * 0.55
    photo_size = header_height * 0.75  # Increased from 0.6 (25% larger)
    rose_size = header_height * 0.35   # Slightly increased

    # Subtle header separator line
    c.saveState()
    c.setStrokeColor(COLOR_HEADER)
    c.setLineWidth(1.5)
    c.line(15, height - header_height - 3, width - 15, height - header_height - 3)
    c.restoreState()

    # Center point for image alignment
    center_y = height - header_height/2

    # Left logo (church)
    if os.path.exists(logo_eglise):
        c.drawImage(logo_eglise, 30, center_y - logo_size/2, width=logo_size, height=logo_size, mask='auto')
    
    # Center rose (decorative)
    if os.path.exists(rose_luther):
        c.drawImage(rose_luther, width/2 - rose_size/2, height - rose_size - 5, width=rose_size, height=rose_size, mask='auto')
    
    # Left photo (between left logo and center)
    if os.path.exists(photo_l):
        c.drawImage(photo_l, 30 + logo_size + 15, center_y - photo_size/2, width=photo_size, height=photo_size, mask='auto')
    
    # Right photo (between center and right logo)
    if os.path.exists(photo_r):
        c.drawImage(photo_r, width - 30 - logo_size - 15 - photo_size, center_y - photo_size/2, width=photo_size, height=photo_size, mask='auto')
    
    # Right logo (agriculture)
    if os.path.exists(logo_agri):
        c.drawImage(logo_agri, width - 30 - logo_size, center_y - logo_size/2, width=logo_size, height=logo_size, mask='auto')

    # Header text (title + subtitles) with enhanced typography per design spec
    if not global_data["entetes"].empty:
        from config.colors import COLOR_HEADER_ACCENT, COLOR_HEADER_BG
        
        entetes_df = global_data["entetes"].sort_values('ligne')
        curr_y = height - 28  # Reduced from 35 (saves 7pt)
        
        # Background rectangle for text area (semi-transparent)
        text_area_height = (len(entetes_df) * SIZE_HEADER_MAIN * 0.7) + 20
        text_area_y = curr_y - text_area_height
        c.setFillColor(COLOR_HEADER_BG)
        c.rect(50, text_area_y, width - 100, text_area_height, fill=1, stroke=0)
        
        curr_y = height - 28
        for idx, (_, row) in enumerate(entetes_df.iterrows()):
            text_content = str(row['texte']).strip()
            
            if idx == 0:
                # Main title: larger, white, with shadow effect
                size = SIZE_HEADER_MAIN
                c.setFont("Helvetica-Bold", size)
                
                # Shadow effect (dark blue, offset)
                c.setFillColor(COLOR_DARK_BLUE)
                c.setFillAlpha(0.4)
                c.drawCentredString(width/2 + 1, curr_y - 1, text_content)
                
                # Main text (white)
                c.setFillColor(COLOR_HEADER)
                c.setFillAlpha(1.0)
                c.drawCentredString(width/2, curr_y, text_content)
                
            elif idx == len(entetes_df) - 1:
                # Last subtitle: gold accent
                size = SIZE_HEADER_MAIN * 0.65
                c.setFont("Helvetica-Bold", size)
                c.setFillColor(COLOR_HEADER_ACCENT)
                c.drawCentredString(width/2, curr_y, text_content)
                
            else:
                # Middle subtitles: white
                size = SIZE_HEADER_MAIN * 0.7
                c.setFont("Helvetica-Bold", size)
                c.setFillColor(COLOR_HEADER)
                c.drawCentredString(width/2, curr_y, text_content)
            
            curr_y -= size + 4  # Reduced from 6 (tighter spacing)

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
    margin = 12  # Optimized margin (reduced from 15)
    col_width = (width - 2 * margin) / 6
    global_data = get_global_data()
    header_height_req = height * 0.22  # Optimized header height
    draw_header(c, width, height, page_num, global_data)

    for i, month in enumerate(range(start_month, end_month + 1)):
        x = margin + i * col_width
        # Visual separation by thin lines (reduced spacing)
        if i > 0:
            c.setStrokeColor(COLOR_GRID)
            c.setLineWidth(0.5)
            c.line(x - 3, margin, x - 3, height - header_height_req - 8)
            
        # Optimized month layout (compact spacing, more content area)
        draw_month(c, x, margin, col_width - 6, height - header_height_req - 12, year, month, global_data)

def draw_month(c, x, y, width, height, year, month, global_data):
    from config.colors import COLOR_HEADER
    
    days = get_days_in_month(year, month)
    month_data = get_month_data(month)
    
    # Month Border (subtle frame - removed for cleaner look)
    # (Using thin lines only, no background fills)
    
    # Month Title (Uppercase, Bold, Compact spacing)
    c.saveState()
    c.setFillColor(COLOR_TEXT)
    c.setFont("Helvetica-Bold", 11)  # Reduced from 12 for better proportion
    month_names = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    c.drawCentredString(x + width/2, y + height - 8, month_names[month-1].upper())  # Reduced padding from 10 to 8
    
    # Underline for month title (thin, subtle)
    c.setStrokeColor(COLOR_HEADER)
    c.setLineWidth(1.0)
    c.line(x + 8, y + height - 12, x + width - 8, y + height - 12)  # Reduced from 10/14
    c.restoreState()
    
    available_height = height - 16  # Reduced from 20 (saves 4pt)
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
