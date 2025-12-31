import os
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from config.page import PAGE_SIZE
from layout.day_row import draw_day_row, calculate_day_height
from utils.date_utils import get_days_in_month
from utils.csv_loader import get_month_data, get_global_data
from config.fonts import SIZE_HEADER_MAIN
from config.colors import COLOR_TEXT_SECONDARY, COLOR_HEADER, COLOR_BACKGROUND, COLOR_GRID, COLOR_HEADER_BG

def draw_background(c, width, height):
    """Dessine le fond de la page (couleur blanche unie)."""
    c.saveState()
    c.setFillColor(COLOR_BACKGROUND)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    c.restoreState()

def draw_header(c, width, height, page_num, global_data):
    """Dessine l'en-tête avec les logos et les titres de l'église et agriculture."""
    logo_eglise = "assets/images/logo_eglise.png"
    logo_agri = "assets/images/logo_agri.png"

    # Hauteur de l'en-tête (15% de la page)
    header_height = height * 0.15 
    logo_size = header_height * 0.6

    # Ligne horizontale de séparation
    c.saveState()
    c.setStrokeColor(COLOR_HEADER)
    c.setLineWidth(1)
    c.line(20, height - header_height - 5, width - 20, height - header_height - 5)
    c.restoreState()

    center_y = height - header_height / 2

    # Affichage des logos (gauche et droite uniquement)
    if os.path.exists(logo_eglise):
        c.drawImage(logo_eglise, 40, center_y - logo_size/2, width=logo_size, height=logo_size, mask='auto')
    if os.path.exists(logo_agri):
        c.drawImage(logo_agri, width - 40 - logo_size, center_y - logo_size/2, width=logo_size, height=logo_size, mask='auto')

    # Affichage des textes d'en-tête chargés depuis le CSV
    if not global_data["entetes"].empty:
        entetes_df = global_data["entetes"].sort_values('ligne')
        curr_y = height - 25
        for idx, (_, row) in enumerate(entetes_df.iterrows()):
            text_content = str(row['texte']).strip()
            if idx == 0:
                size = SIZE_HEADER_MAIN
                c.setFont("Helvetica-Bold", size)
                c.setFillColor(COLOR_HEADER)
                c.drawCentredString(width/2, curr_y, text_content)
            else:
                size = SIZE_HEADER_MAIN * 0.6
                c.setFont("Helvetica-Bold", size)
                c.setFillColor(COLOR_TEXT_SECONDARY)
                c.drawCentredString(width/2, curr_y, text_content)
            curr_y -= size + 5

def generate_calendar():
    """Génère le PDF complet (A3 Paysage, 2 pages)."""
    if not os.path.exists("output"):
        os.makedirs("output")
    c = canvas.Canvas("output/calendrier_A3.pdf", pagesize=PAGE_SIZE)
    year = 2026
    
    # Page 1 : Janvier à Juin
    draw_background(c, PAGE_SIZE[0], PAGE_SIZE[1])
    draw_page(c, year, 1, 6, 1)
    c.showPage()
    
    # Page 2 : Juillet à Décembre
    draw_background(c, PAGE_SIZE[0], PAGE_SIZE[1])
    draw_page(c, year, 7, 12, 2)
    c.showPage()
    
    c.save()

def draw_page(c, year, start_month, end_month, page_num):
    """Dessine une page avec une colonne de 3 photos à gauche et 6 mois à droite."""
    width, height = PAGE_SIZE
    margin_x = 20
    margin_y = 20
    header_h = height * 0.15
    
    # Largeur de la colonne photo augmentée (20% au lieu de 15%)
    photo_col_width = width * 0.20
    months_area_width = width - photo_col_width - 2 * margin_x
    month_col_width = months_area_width / 6
    
    global_data = get_global_data()
    draw_header(c, width, height, page_num, global_data)
    
    # Affichage des 3 photos à gauche (uniques par page)
    # On ajoute un espacement vertical entre les photos
    photo_h = (height - header_h - 2 * margin_y) / 3
    for i in range(3):
        # Index de photo : 1-3 pour page 1, 4-6 pour page 2
        photo_idx = (page_num - 1) * 3 + i + 1
        photo_path = f"assets/images/photo{photo_idx}.jpg"
        if os.path.exists(photo_path):
            # img_y calculé pour descendre les photos sous l'en-tête
            img_y = height - header_h - margin_y - (i + 1) * photo_h + 10
            # Dessin de la photo avec bordure stylisée
            c.saveState()
            c.setStrokeColor(COLOR_GRID)
            c.setLineWidth(0.8)
            # Rectangle pour la photo
            img_w = photo_col_width - 15
            img_h_box = photo_h - 20
            # Ombre légère simulée
            c.setFillColor(Color(0,0,0, alpha=0.05))
            c.rect(margin_x + 1, img_y - 1, img_w, img_h_box, stroke=0, fill=1)
            # Bordure
            c.setFillColor(HexColor("#FFFFFF"))
            c.rect(margin_x, img_y, img_w, img_h_box, stroke=1, fill=1)
            # Photo centrée dans le cadre
            c.drawImage(photo_path, margin_x + 4, img_y + 4, width=img_w - 8, height=img_h_box - 8, preserveAspectRatio=True, anchor='c')
            c.restoreState()

    # Affichage des 6 mois de la page
    for i, month in enumerate(range(start_month, end_month + 1)):
        x = margin_x + photo_col_width + i * month_col_width
        draw_month(c, x, margin_y, month_col_width - 6, height - header_h - margin_y - 10, year, month, global_data)

def draw_month(c, x, y, width, height, year, month, global_data):
    """Dessine le bloc d'un mois spécifique avec bordures stylisées."""
    days = get_days_in_month(year, month)
    month_data = get_month_data(month)
    
    # Bordure extérieure du mois (Bordures arrondies simulées)
    c.saveState()
    c.setStrokeColor(COLOR_GRID)
    c.setLineWidth(0.8)
    c.rect(x, y, width, height, stroke=1, fill=0)
    
    # Titre du mois avec fond stylisé
    c.setFillColor(COLOR_HEADER_BG)
    c.rect(x, y + height - 18, width, 18, fill=1, stroke=1)
    c.setFillColor(COLOR_HEADER)
    c.setFont("Helvetica-Bold", 9)
    month_names = ["JANVIER", "FÉVRIER", "MARS", "AVRIL", "MAI", "JUIN", "JUILLET", "AOÛT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DÉCEMBRE"]
    c.drawCentredString(x + width/2, y + height - 12, month_names[month-1])
    c.restoreState()
    
    # Calcul de la hauteur disponible et mise à l'échelle des lignes de jours
    available_h = height - 20
    day_heights = [calculate_day_height(d, month_data) for d in days]
    total_req = sum(day_heights)
    scale = min(1.0, available_h / total_req)
    scaled_heights = [h * scale for h in day_heights]
    
    curr_y = y + available_h
    for d, row_h in zip(days, scaled_heights):
        curr_y -= row_h
        draw_day_row(c, x, curr_y, width, row_h, d, month_data=month_data, global_data=global_data)

if __name__ == "__main__":
    generate_calendar()
