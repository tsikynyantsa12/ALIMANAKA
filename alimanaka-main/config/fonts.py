from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_BOLD = "Helvetica-Bold"
FONT_REGULAR = "Helvetica"
FONT_ITALIC = "Helvetica-Oblique"

# Font sizes optimized for readability and proportion
SIZE_MONTH_TITLE = 9
SIZE_DAY_NUM = 7
SIZE_DAY_NAME = 5.2  # Reduced from 5.5 for better proportion
SIZE_PROGRAM = 5.5  # Reduced from 6 (better hierarchy)
SIZE_VERSE = 4.8  # Reduced from 5 (consistent scaling)

# Significantly larger header font
SIZE_HEADER_MAIN = 18
