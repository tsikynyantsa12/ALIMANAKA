import os
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from config.page import PAGE_SIZE, PAGE_SIZE_A4, MARGIN
from layout.day_row import draw_day_row, calculate_day_height
from utils.date_utils import get_days_in_month
from utils.csv_loader import get_month_data, get_global_data, get_config_value, get_month_name, get_photos_for_page
from config.fonts import SIZE_HEADER_MAIN
from config.colors import COLORS, MONTH_COLORS, COLOR_TEXT_SECONDARY, COLOR_HEADER, COLOR_BACKGROUND, COLOR_GRID, COLOR_HEADER_BG
from reportlab.lib.units import mm
import math

def draw_wave_decoration(c, width, height, color, position='top'):
    """Dessine une vague décorative moderne centrée sur la zone imprimable."""
    wave_height = 80
    wave_amplitude = 20
    c.saveState()
    c.setFillColor(color)
    
    # Points de contrôle pour une courbe de Bézier harmonieuse
    if position == 'top':
        y_base = height - wave_height
        p = c.beginPath()
        p.moveTo(MARGIN, height - MARGIN)
        p.lineTo(MARGIN, y_base)
        p.curveTo(MARGIN + (width - 2*MARGIN) * 0.25, y_base + wave_amplitude * 2, 
                  MARGIN + (width - 2*MARGIN) * 0.75, y_base - wave_amplitude * 2, 
                  width - MARGIN, y_base)
        p.lineTo(width - MARGIN, height - MARGIN)
    else:
        y_base = MARGIN + wave_height
        p = c.beginPath()
        p.moveTo(MARGIN, MARGIN)
        p.lineTo(MARGIN, y_base)
        p.curveTo(MARGIN + (width - 2*MARGIN) * 0.25, y_base + wave_amplitude * 2, 
                  MARGIN + (width - 2*MARGIN) * 0.75, y_base - wave_amplitude * 2, 
                  width - MARGIN, y_base)
        p.lineTo(width - MARGIN, MARGIN)
        
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()

def draw_header(c, width, height, page_num, global_data):
    """Dessine l'en-tête ultra-compact centré sur la zone imprimable."""
    logo_eglise = "assets/images/logo_eglise.png"
    # Hauteur de l'en-tête par rapport à la zone utile
    header_height = (height - 2*MARGIN) * 0.08
    usable_width = width - 2*MARGIN
    
    c.saveState()
    # Ligne de séparation sous l'en-tête
    c.setStrokeColor(HexColor('#1A237E'))
    c.setLineWidth(0.8)
    c.line(MARGIN, height - MARGIN - header_height, width - MARGIN, height - MARGIN - header_height)
    
    # 1. Colonne Gauche : Logo
    logo_size = header_height * 0.85
    if os.path.exists(logo_eglise):
        c.drawImage(logo_eglise, MARGIN + 10, height - MARGIN - header_height + (header_height - logo_size)/2, width=logo_size, height=logo_size, mask='auto')
    
    # 2. Colonne Centrale
    c.setFillColor(HexColor('#1A237E'))
    if not global_data["entetes"].empty:
        curr_y = height - MARGIN - 5
        for i, row in global_data["entetes"].iterrows():
            text = str(row.get('texte', '')).strip()
            if text:
                if i == 0:
                    c.setFont("Helvetica-Bold", 12)
                elif i == 1:
                    c.setFont("Helvetica-Bold", 10)
                else:
                    c.setFont("Helvetica", 8)
                c.drawCentredString(width/2, curr_y, text)
                curr_y -= (c._fontsize + 2)
    
    # 3. Colonne Droite
    c.setFont("Helvetica-Bold", 18)
    year_str = get_config_value('annee', '2026', global_data)
    c.drawCentredString(width - MARGIN - 30, height - MARGIN - header_height * 0.5, str(year_str))
    
    c.restoreState()
    return header_height

def draw_technical_legend(c, x, y, width, height, global_data):
    """Dessine une légende technique centrée sur son espace."""
    from utils.icon_mapper import get_moon_icon, get_agri_icon, get_culture_icon
    c.saveState()
    c.setFillColor(HexColor('#FFF9C4'))
    c.roundRect(x, y, width, height, 8, fill=1, stroke=0)
    
    c.setStrokeColor(HexColor('#E0E0E0'))
    c.setLineWidth(0.5)
    c.roundRect(x, y, width, height, 8, stroke=1, fill=0)
    
    c.setFillColor(HexColor('#1A237E'))
    header_rect_h = 12
    c.roundRect(x, y + height - header_rect_h, width, header_rect_h, 4, fill=1, stroke=0)
    c.setFillColor(COLORS['white'])
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(x + width/2, y + height - header_rect_h + 3, "LÉGENDE")
    
    icon_size = 7
    curr_y = y + height - 22
    col1_x = x + 5
    col2_x = x + width/2 + 2
    
    if not global_data["phases"].empty:
        c.setFont("Helvetica-Bold", 6)
        c.setFillColor(HexColor('#1A237E'))
        c.drawString(col1_x, curr_y, "• Lunes")
        c.setFillColor(COLORS['black'])
        temp_y = curr_y - 10
        for _, row in global_data["phases"].head(3).iterrows():
            icon_id = str(row['id']).strip().lower()
            label = str(row['phase']).strip()
            icon_path = get_moon_icon(icon_id)
            if icon_path and os.path.exists(icon_path):
                try: c.drawImage(icon_path, col1_x, temp_y - 2, width=icon_size, height=icon_size, mask='auto')
                except: pass
            c.setFont("Helvetica", 5.5)
            c.drawString(col1_x + 10, temp_y, label[:15])
            temp_y -= 9

    if not global_data["cultures"].empty:
        c.setFont("Helvetica-Bold", 6)
        c.setFillColor(HexColor('#1A237E'))
        c.drawString(col2_x, curr_y, "• Cultures")
        c.setFillColor(COLORS['black'])
        temp_y = curr_y - 10
        for _, row in global_data["cultures"].head(3).iterrows():
            icon_id = str(row['id']).strip().lower()
            label = str(row['culture']).strip()
            icon_path = get_culture_icon(icon_id)
            if icon_path and os.path.exists(icon_path):
                try: c.drawImage(icon_path, col2_x, temp_y - 2, width=icon_size, height=icon_size, mask='auto')
                except: pass
            c.setFont("Helvetica", 5.5)
            c.drawString(col2_x + 10, temp_y, label[:15])
            temp_y -= 9

    if not global_data["actions"].empty:
        # On affiche les actions en bas sur toute la largeur de la légende
        temp_y = y + 5
        c.setFont("Helvetica-Bold", 6)
        c.setFillColor(HexColor('#1A237E'))
        c.drawString(col1_x, temp_y + 10, "• Actions")
        c.setFillColor(COLORS['black'])
        curr_act_x = col1_x
        # On affiche 4 actions max sur une ligne
        step_x = (width - 10) / 4
        for _, row in global_data["actions"].head(4).iterrows():
            icon_id = str(row['id']).strip().lower()
            label = str(row['action']).strip()
            icon_path = get_agri_icon(icon_id)
            if icon_path and os.path.exists(icon_path):
                try: c.drawImage(icon_path, curr_act_x, temp_y, width=icon_size, height=icon_size, mask='auto')
                except: pass
            c.setFont("Helvetica", 5)
            c.drawString(curr_act_x + 9, temp_y + 2, label[:10])
            curr_act_x += step_x
    
    # Couleurs liturgiques en bas
    if not global_data["couleurs"].empty:
        temp_y = y + 5
        c.setFont("Helvetica-Bold", 6)
        c.setFillColor(HexColor('#1A237E'))
        c.drawString(col2_x, temp_y + 10, "• Couleurs")
        c.setFillColor(COLORS['black'])
        color_y = temp_y
        for _, row in global_data["couleurs"].iterrows():
            color_name = str(row['couleur']).strip()
            hex_code = str(row['code_hex']).strip()
            try:
                color_obj = HexColor(hex_code)
            except:
                color_obj = HexColor("#a8d5ba")
            
            c.setFillColor(color_obj)
            c.setLineWidth(0.3)
            c.setStrokeColor(HexColor('#333333'))
            c.rect(col2_x, color_y - 4, 6, 6, fill=1, stroke=1)
            
            c.setFillColor(COLORS['black'])
            c.setFont("Helvetica", 5)
            c.drawString(col2_x + 8, color_y - 2, color_name[:12])
            color_y -= 8
            
    c.restoreState()

def draw_month(c, x, y, width, height, year, month, global_data):
    """Dessine le bloc d'un mois."""
    days = get_days_in_month(year, month)
    month_data = get_month_data(month)
    primary_color = HexColor('#1A237E')
    c.saveState()
    c.setStrokeColor(HexColor('#E0E0E0'))
    c.setLineWidth(0.25)
    c.roundRect(x, y, width, height, 8, stroke=1, fill=0)
    
    c.setFillColor(primary_color)
    c.roundRect(x, y + height - 18, width, 18, 5, fill=1, stroke=0)
    c.setFillColor(COLORS['white'])
    c.setFont("Helvetica-Bold", 9)
    month_name = get_month_name(month, global_data)
    c.drawCentredString(x + width/2, y + height - 12, month_name)
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
    """Dessine une page en respectant les marges de sécurité."""
    width, height = page_size
    is_a4 = (page_size == PAGE_SIZE_A4)
    scale_factor = 0.707 if is_a4 else 1.0
    
    global_data = get_global_data()
    header_h = draw_header(c, width, height, page_num, global_data)
    draw_wave_decoration(c, width, height, COLORS['gold'], 'bottom')

    # Zone utile
    photo_col_width = (width - 2 * MARGIN) * 0.18
    months_area_width = width - photo_col_width - 2 * MARGIN
    month_col_width = months_area_width / 6
    
    content_h = height - header_h - 2 * MARGIN - 10 * scale_factor
    photo_h = content_h * 0.43
    legend_h = content_h * 0.18
    
    start_y = height - MARGIN - header_h - 5 * scale_factor
    
    photos = get_photos_for_page(page_num, global_data)
    for i, photo_info in enumerate(photos[:2]):
        photo_path = photo_info.get('chemin', '')
        if photo_path and os.path.exists(photo_path):
            img_y = start_y - (i + 1) * photo_h
            c.saveState()
            c.setStrokeColor(COLOR_GRID)
            c.roundRect(MARGIN, img_y + 10 * scale_factor, photo_col_width - 5 * scale_factor, photo_h - 15 * scale_factor, 8 * scale_factor, stroke=1, fill=0)
            c.drawImage(photo_path, MARGIN + 2 * scale_factor, img_y + 12 * scale_factor, width=photo_col_width - 9 * scale_factor, height=photo_h - 19 * scale_factor, preserveAspectRatio=True, anchor='c')
            c.restoreState()
    
    legend_y = MARGIN + 5 * scale_factor
    draw_technical_legend(c, MARGIN, legend_y, photo_col_width - 5 * scale_factor, legend_h, global_data)

    for i, month in enumerate(range(start_month, end_month + 1)):
        x = MARGIN + photo_col_width + i * month_col_width
        draw_month(c, x, MARGIN + 5 * scale_factor, month_col_width - 6 * scale_factor, height - MARGIN - header_h - MARGIN - 5 * scale_factor, year, month, global_data)

    # Signature Designer alignée sur la marge droite
    c.saveState()
    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor(HexColor('#444444'))
    designer_info = get_config_value('designer_info', 'Design & Mise en page : [NOM]', global_data)
    c.drawRightString(width - MARGIN, MARGIN / 2, str(designer_info))
    c.restoreState()

def generate_calendar():
    """Génère le PDF final."""
    print("Début de la génération des calendriers...")
    if not os.path.exists("output"): 
        os.makedirs("output")
        print("Dossier 'output' créé.")
    
    global_data = get_global_data()
    year = int(get_config_value('annee', '2026', global_data))
    
    # Version A3
    print("Génération du PDF A3...")
    c3 = canvas.Canvas("output/calendrier_A3.pdf", pagesize=PAGE_SIZE)
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
