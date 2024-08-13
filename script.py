from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.colors import HexColor

class ChatScript:
    def __init__(self):
        self.topic = ""
        self.script = {}
        self.idx = 0

    def set_topic(self, topic):
        self.topic = topic

    def add_script(self, talker, message):
        if talker not in self.script:
            self.script[talker] = []
                   
        self.script[talker].append((self.idx, message))
        self.idx += 1

    def add_name(self, talkers: list):
        for talker in talkers:
            if talker not in self.script:
                self.script[talker] = []

    def get_script(self, talker):
        return self.script[talker]
    
    def get_talker(self):
        return list(self.script.keys())

class PDFGenerator:
    def __init__(self, topic):
        self.buffer = []
        self.page_width, self.page_height = letter
        self.topic = topic
        
        self.colors = {
            'left': HexColor("#00BFA5"),  # Teal
            'right': HexColor("#FFC107")  # Amber
        }

    def add_message(self, name, message):
        formatted_message = self.format_message(message)
        self.buffer.append((name, formatted_message))

    def save_pdf(self, filename):
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = self.page_width, self.page_height

        # 배경 색상 추가
        c.setFillColor(HexColor("#F5F5F5"))  # Light grey background
        c.rect(0, 0, width, height, fill=1)

        # Header styling
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(HexColor("#37474F"))
        c.drawCentredString(width / 2.0, height - inch, self.topic)
        c.setFont("Helvetica", 12)
        margin = 1 * inch
        y = height - 2 * inch  # Adjusted for more space around title

        max_bubble_width = (width - 2 * margin) * 2 / 3

        for name, message in self.buffer:
            if y < margin + 80:  # Adjusted to allow space for text
                c.showPage()
                c.setFillColor(HexColor("#F5F5F5"))  # Reapply background color
                c.rect(0, 0, width, height, fill=1)
                y = height - 2 * inch
                c.setFont("Helvetica", 12)

            if name == self.buffer[0][0]:  # 첫 번째 talker는 왼쪽
                self.draw_bubble(c, margin, y, max_bubble_width, name, message, self.colors['left'], align='left')
                y -= (80 + self.get_text_height(message, max_bubble_width))
            else:  # 두 번째 talker는 오른쪽
                self.draw_bubble(c, width - margin - max_bubble_width, y, max_bubble_width, name, message, self.colors['right'], align='right')
                y -= (80 + self.get_text_height(message, max_bubble_width))

        c.save()

    def draw_bubble(self, c, x, y, max_width, name, text, color, align='left'):
        padding = 8
        styles = getSampleStyleSheet()
        
        # Define styles for name and text separately
        name_style = ParagraphStyle(name='Name', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, alignment=TA_LEFT if align == 'left' else TA_RIGHT, textColor=HexColor("#37474F"))
        text_style = ParagraphStyle(name='Text', parent=styles['Normal'], fontName='Helvetica', fontSize=12, alignment=TA_JUSTIFY, textColor=HexColor("#263238"))

        # Create Paragraph for name and text
        name_para = Paragraph(name, name_style)
        text_para = Paragraph(text, text_style)

        name_width, name_height = name_para.wrap(max_width - 2 * padding, y)
        text_width, text_height = text_para.wrap(max_width - 2 * padding, y)
        bubble_width = max(name_width, text_width) + 2 * padding
        bubble_height = name_height + text_height + 2 * padding

        bubble_y = y - bubble_height

        # Modern rounded bubble with a light shadow
        c.setFillColor(color)
        c.roundRect(x, bubble_y, bubble_width, bubble_height, 10, fill=1)
        c.setFillColor(HexColor("#263238"))

        name_para.drawOn(c, x + padding, bubble_y + bubble_height - name_height - padding)
        text_para.drawOn(c, x + padding, bubble_y + padding)
    
    def get_text_height(self, text, max_width):
        styles = getSampleStyleSheet()
        text_style = ParagraphStyle(name='Text', parent=styles['Normal'], fontName='Helvetica', fontSize=12, alignment=TA_JUSTIFY, textColor=HexColor("#263238"))
        text_para = Paragraph(text, text_style)
        _, text_height = text_para.wrap(max_width - 10, 0)
        return text_height

    def format_message(self, message):
        return message.replace('\n', '<br/>')