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

DESIGNER_INFO = "Design & Mise en page : [NOM DU DESIGNER] | Contact : [NUMÉRO DE TÉLÉPHONE]"

def draw_wave_decoration(c, width, height, color, position='top'):
    """Dessine une vague décorative moderne"""
    wave_height = 80
    wave_amplitude = 20
    c.saveState()
    c.setFillColor(color)
    
    # Points de contrôle pour une courbe de Bézier harmonieuse
    if position == 'top':
        y_base = height - wave_height
        p = c.beginPath()
        p.moveTo(0, height)
        p.lineTo(0, y_base)
        # Courbe cubique pour un aspect plus fluide
        p.curveTo(width * 0.25, y_base + wave_amplitude * 2, 
                  width * 0.75, y_base - wave_amplitude * 2, 
                  width, y_base)
        p.lineTo(width, height)
    else:
        y_base = wave_height
        p = c.beginPath()
        p.moveTo(0, 0)
        p.lineTo(0, y_base)
        # Courbe identique mais inversée ou décalée pour le bas
        p.curveTo(width * 0.25, y_base + wave_amplitude * 2, 
                  width * 0.75, y_base - wave_amplitude * 2, 
                  width, y_base)
        p.lineTo(width, 0)
        
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()

def draw_header(c, width, height, page_num, global_data):
    """Dessine l'en-tête modernisé en 3 colonnes."""
    logo_eglise = "assets/images/logo_eglise.png"
    header_height = height * 0.15
    
    c.saveState()
    # Ligne de séparation sous l'en-tête
    c.setStrokeColor(HexColor('#1A237E'))
    c.setLineWidth(1)
    c.line(0, height - header_height, width, height - header_height)
    
    # 1. Colonne Gauche : Logo
    logo_size = header_height * 0.7
    if os.path.exists(logo_eglise):
        c.drawImage(logo_eglise, 40, height - header_height + (header_height - logo_size)/2, width=logo_size, height=logo_size, mask='auto')
    
    # 2. Colonne Centrale : Titre principal
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(HexColor('#1A237E'))
    title = "FIANGONANA LOTERANA MALAGASY"
    c.drawCentredString(width/2, height - header_height + header_height * 0.6, title)
    
    if not global_data["entetes"].empty:
        entetes_df = global_data["entetes"].sort_values('ligne')
        if len(entetes_df) > 1:
            subtitle = str(entetes_df.iloc[1]['texte']).strip()
            c.setFont("Helvetica", 14)
            c.drawCentredString(width/2, height - header_height + header_height * 0.3, subtitle)
            
    # 3. Colonne Droite : Détails année
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width - 80, height - header_height + header_height * 0.5, "2026")
    
    c.restoreState()

def draw_technical_legend(c, x, y, width, height, global_data):
    """Dessine une légende technique stylisée avec icônes réelles."""
    from utils.icon_mapper import get_moon_icon, get_agri_icon, get_culture_icon
    c.saveState()
    # Couleur de fond jaune doux
    c.setFillColor(HexColor('#FFF9C4'))
    c.roundRect(x, y, width, height, 8, fill=1, stroke=0)
    
    c.setStrokeColor(HexColor('#E0E0E0'))
    c.setLineWidth(0.5)
    c.roundRect(x, y, width, height, 8, stroke=1, fill=0)
    
    c.setFillColor(HexColor('#1A237E'))
    c.roundRect(x, y + height - 15, width, 15, 5, fill=1, stroke=0)
    c.setFillColor(COLORS['white'])
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(x + width/2, y + height - 10, "LÉGENDE")
    
    curr_y = y + height - 25
    c.setFont("Helvetica", 6)
    c.setFillColor(COLORS['black'])
    
    icon_size = 8
    
    # Phases lunaires réelles
    if not global_data["phases"].empty:
        c.setFont("Helvetica-Bold", 6)
        c.drawString(x + 5, curr_y, "Lunes:")
        curr_y -= 8
        for _, row in global_data["phases"].head(4).iterrows():
            icon_id = str(row['id']).strip().lower()
            label = str(row['phase']).strip()
            icon_path = get_moon_icon(icon_id)
            if icon_path and os.path.exists(icon_path):
                try:
                    c.drawImage(icon_path, x + 5, curr_y - 2, width=icon_size, height=icon_size, mask='auto')
                except: pass
            c.drawString(x + 15, curr_y, label)
            curr_y -= 10

    # Cultures réelles
    if not global_data["cultures"].empty:
        curr_y -= 5
        c.setFont("Helvetica-Bold", 6)
        c.drawString(x + 5, curr_y, "Cultures:")
        curr_y -= 8
        for _, row in global_data["cultures"].head(4).iterrows():
            icon_id = str(row['id']).strip().lower()
            label = str(row['culture']).strip()
            icon_path = get_culture_icon(icon_id)
            if icon_path and os.path.exists(icon_path):
                try:
                    c.drawImage(icon_path, x + 5, curr_y - 2, width=icon_size, height=icon_size, mask='auto')
                except: pass
            c.drawString(x + 15, curr_y, label)
            curr_y -= 10
            
    # Actions réelles
    if not global_data["actions"].empty:
        curr_y -= 5
        c.setFont("Helvetica-Bold", 6)
        c.drawString(x + 5, curr_y, "Actions:")
        curr_y -= 8
        for _, row in global_data["actions"].head(4).iterrows():
            icon_id = str(row['id']).strip().lower()
            label = str(row['action']).strip()
            icon_path = get_agri_icon(icon_id)
            if icon_path and os.path.exists(icon_path):
                try:
                    c.drawImage(icon_path, x + 5, curr_y - 2, width=icon_size, height=icon_size, mask='auto')
                except: pass
            c.drawString(x + 15, curr_y, label)
            curr_y -= 10
            
    c.restoreState()

def draw_month(c, x, y, width, height, year, month, global_data):
    """Dessine le bloc d'un mois."""
    days = get_days_in_month(year, month)
    month_data = get_month_data(month)
    primary_color = HexColor('#1A237E') # Bleu logo pour tous les en-têtes de mois
    c.saveState()
    c.setStrokeColor(HexColor('#E0E0E0'))
    c.setLineWidth(0.25)
    c.roundRect(x, y, width, height, 8, stroke=1, fill=0)
    
    c.setFillColor(primary_color)
    c.roundRect(x, y + height - 18, width, 18, 5, fill=1, stroke=0)
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
    
    # Échelle pour A4 (rapport entre A4 landscape et A3 landscape)
    # A3 landscape: 1190.55 x 841.89
    # A4 landscape: 841.89 x 595.28
    # Rapport: ~0.707 (1/sqrt(2))
    scale_factor = 0.707 if is_a4 else 1.0
    
    # Marges ajustées
    margin_x = 30 * scale_factor
    margin_y = 30 * scale_factor
    header_h = height * 0.216 
    
    photo_col_width = (width - 2 * margin_x) * 0.18
    months_area_width = width - photo_col_width - 2 * margin_x
    month_col_width = months_area_width / 6
    
    global_data = get_global_data()
    
    # Application de l'échelle globale pour A4 si nécessaire
    if is_a4:
        c.saveState()
        # On pourrait utiliser c.scale(0.707, 0.707) mais ça affecterait les coordonnées.
        # Il est préférable de passer le scale_factor aux fonctions de dessin ou d'ajuster les polices.
        pass

    draw_header(c, width, height, page_num, global_data)
    draw_wave_decoration(c, width, height, COLORS['gold'], 'bottom')

    # Zone utile sous le header
    content_h = height - header_h - 2 * margin_y
    photo_h = content_h * 0.40
    legend_h = content_h * 0.18
    
    # Remonter les composants (start_y augmenté pour remonter le tout)
    start_y = height - header_h - margin_y + 20 * scale_factor
    
    # Marges entre mois augmentées
    month_margin = 10 * scale_factor
    
    for i in range(2):
        photo_idx = (page_num - 1) * 2 + i + 1
        photo_path = f"assets/images/photo{photo_idx}.jpg"
        if os.path.exists(photo_path):
            img_y = start_y - (i + 1) * photo_h
            c.saveState()
            c.setStrokeColor(COLOR_GRID)
            c.roundRect(margin_x, img_y + 10 * scale_factor, photo_col_width - 5 * scale_factor, photo_h - 15 * scale_factor, 8 * scale_factor, stroke=1, fill=0)
            c.drawImage(photo_path, margin_x + 2 * scale_factor, img_y + 12 * scale_factor, width=photo_col_width - 9 * scale_factor, height=photo_h - 19 * scale_factor, preserveAspectRatio=True, anchor='c')
            c.restoreState()
    
    legend_y = margin_y + 5 * scale_factor
    draw_technical_legend(c, margin_x, legend_y, photo_col_width - 5 * scale_factor, legend_h, global_data)

    for i, month in enumerate(range(start_month, end_month + 1)):
        x = margin_x + photo_col_width + i * month_col_width
        draw_month(c, x, margin_y + 5 * scale_factor, month_col_width - 6 * scale_factor, height - header_h - margin_y - 15 * scale_factor, year, month, global_data)

    # Signature Designer
    c.saveState()
    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor(HexColor('#444444'))
    # Aligné à la limite droite du dernier mois
    right_edge = margin_x + photo_col_width + 6 * month_col_width - 6 * scale_factor
    c.drawRightString(right_edge, margin_y - 15 * scale_factor, DESIGNER_INFO)
    c.restoreState()

def generate_calendar():
    """Génère le PDF final."""
    print("Début de la génération des calendriers...")
    if not os.path.exists("output"): 
        os.makedirs("output")
        print("Dossier 'output' créé.")
    
    # Version A3
    print("Génération du PDF A3...")
    c3 = canvas.Canvas("output/calendrier_A3.pdf", pagesize=PAGE_SIZE)
    year = 2026
    for page in [1, 2]:
        print(f"Dessin de la page {page} (A3)...")
        c3.setFillColor(COLOR_BACKGROUND)
        c3.rect(0, 0, PAGE_SIZE[0], PAGE_SIZE[1], fill=1, stroke=0)
        draw_page(c3, year, 1 if page == 1 else 7, 6 if page == 1 else 12, page, PAGE_SIZE)
        c3.showPage()
    c3.save()
    print("Fichier A3 sauvegardé : output/calendrier_A3.pdf")

    # Version A4
    print("Génération du PDF A4...")
    c4 = canvas.Canvas("output/calendrier_A4.pdf", pagesize=PAGE_SIZE_A4)
    for page in [1, 2]:
        print(f"Dessin de la page {page} (A4)...")
        c4.setFillColor(COLOR_BACKGROUND)
        c4.rect(0, 0, PAGE_SIZE_A4[0], PAGE_SIZE_A4[1], fill=1, stroke=0)
        draw_page(c4, year, 1 if page == 1 else 7, 6 if page == 1 else 12, page, PAGE_SIZE_A4)
        c4.showPage()
    c4.save()
    print("Fichier A4 sauvegardé : output/calendrier_A4.pdf")
    print("Tous les PDFs ont été générés avec succès.")

if __name__ == "__main__":
    generate_calendar()
