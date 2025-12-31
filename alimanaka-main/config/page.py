from reportlab.lib.pagesizes import A3, A4, landscape, portrait
from reportlab.lib.units import mm

PAGE_SIZE = landscape(A3)
PAGE_SIZE_A4 = portrait(A4)
MARGIN = 12 * mm  # Reduced from 15 (optimized edge spacing)
COLUMN_SPACING = 3 * mm  # Reduced from 5 (compact month separation)
ROW_SPACING = 1.5 * mm  # Reduced from 2 (tighter vertical rhythm)
