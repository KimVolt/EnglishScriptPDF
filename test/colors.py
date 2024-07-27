from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.colors import Color

def generate_colors_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)
    margin = 40
    y = height - margin

    # colors 모듈의 모든 색상 이름을 가져옴
    color_names = [name for name in dir(colors) if not name.startswith('_') and isinstance(getattr(colors, name), (Color, tuple))]

    for color_name in color_names:
        if y < margin:
            c.showPage()
            y = height - margin
            c.setFont("Helvetica", 12)

        color = getattr(colors, color_name)
        c.setFillColor(color)
        c.rect(margin, y - 10, 50, 20, fill=1)
        c.setFillColor(colors.black)
        c.drawString(margin + 60, y, color_name)
        y -= 30

    c.save()

# 생성할 PDF 파일 이름
pdf_filename = "color.pdf"
generate_colors_pdf(pdf_filename)
