from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_JUSTIFY

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
            'left': colors.lightcyan,
            'right': colors.lightgoldenrodyellow
        }

    def add_message(self, name, message):
        self.buffer.append((name, message))

    def save_pdf(self, filename):
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = self.page_width, self.page_height

        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2.0, height - inch, self.topic)
        c.setFont("Helvetica", 12)
        margin = 1 * inch
        y = height - 1.5 * inch

        max_bubble_width = (width - 2 * margin) * 2 / 3

        for name, message in self.buffer:
            if y < margin + 60:  # Adjusted to allow space for text
                c.showPage()
                y = height - 1.5 * inch
                c.setFont("Helvetica", 12)

            if name == self.buffer[0][0]:  # 첫 번째 talker는 왼쪽
                self.draw_bubble(c, margin, y, max_bubble_width, name, message, self.colors['left'], align='left')
                y -= (60 + self.get_text_height(message, max_bubble_width))  # Adjusted to accommodate multi-line text
            else:  # 두 번째 talker는 오른쪽
                self.draw_bubble(c, width - margin - max_bubble_width, y, max_bubble_width, name, message, self.colors['right'], align='right')
                y -= (60 + self.get_text_height(message, max_bubble_width))  # Adjusted to accommodate multi-line text

        c.save()

    def draw_bubble(self, c, x, y, max_width, name, text, color, align='left'):
        padding = 5
        styles = getSampleStyleSheet()
        
        # Define styles for name and text separately
        name_style = ParagraphStyle(name='Name', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, alignment=TA_LEFT if align == 'left' else TA_RIGHT)
        text_style = ParagraphStyle(name='Text', parent=styles['Normal'], fontName='Helvetica', fontSize=12, alignment=TA_JUSTIFY)

        # Create Paragraph for name and text
        name_para = Paragraph(name, name_style)
        text_para = Paragraph(text, text_style)

        # Calculate the width and height of the text
        name_width, name_height = name_para.wrap(max_width - 2 * padding, y)
        text_width, text_height = text_para.wrap(max_width - 2 * padding, y)
        bubble_width = max(name_width, text_width) + 2 * padding
        bubble_height = name_height + text_height + 2 * padding

        bubble_y = y - bubble_height

        # Draw bubble
        c.setFillColor(color)
        c.roundRect(x, bubble_y, bubble_width, bubble_height, 5, fill=1)
        c.setFillColor(colors.black)

        # Draw name and text
        name_para.drawOn(c, x + padding, bubble_y + bubble_height - name_height - padding)
        text_para.drawOn(c, x + padding, bubble_y + padding)
    
    def get_text_height(self, text, max_width):
        styles = getSampleStyleSheet()
        text_style = ParagraphStyle(name='Text', parent=styles['Normal'], fontName='Helvetica', fontSize=12, alignment=TA_JUSTIFY)
        text_para = Paragraph(text, text_style)
        _, text_height = text_para.wrap(max_width - 10, 0)  # Adjust the width with padding
        return text_height