from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_BOLD = "Helvetica-Bold"
FONT_REGULAR = "Helvetica"
FONT_ITALIC = "Helvetica-Oblique"

# Aggressive font reduction for body to reclaim space for header
SIZE_MONTH_TITLE = 9
SIZE_DAY_NUM = 7
SIZE_DAY_NAME = 4
SIZE_PROGRAM = 6
SIZE_VERSE = 5

# Significantly larger header font
SIZE_HEADER_MAIN = 18
