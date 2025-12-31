from reportlab.lib.pagesizes import A3, A4, landscape, portrait
from reportlab.lib.units import mm

PAGE_SIZE = landscape(A3)
PAGE_SIZE_A4 = landscape(A4)
MARGIN = 10 * mm  # Marge de sécurité de 10mm
COLUMN_SPACING = 3 * mm
ROW_SPACING = 1.5 * mm
