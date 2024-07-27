from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch

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
        
        # custom configuration
        self.colors = {
            'left': colors.lightcyan,
            'right': colors.lightgoldenrodyellow
        }
        
        """
        pdfmetrics.registerFont(TTFont('NotoSans', 'C:\\Windows\\Fonts\\NotoSans-Regular.ttf'))
        pdfmetrics.registerFont(TTFont('NotoSans-Medium', 'C:\\Windows\\Fonts\\NotoSans-Medium.ttf'))
        pdfmetrics.registerFont(TTFont('NotoSans-Bold', 'C:\\Windows\\Fonts\\NotoSans-Bold.ttf'))
               
        self.fonts = {
            'normal': 'NotoSans',
            'medium': 'NotoSans-Medium',
            'bold': 'NotoSans-Bold' 
        }"""
        
        self.fonts = {
            'normal': 'Helvetica',
            'bold': 'Helvetica-Bold'
        }  

    def add_message(self, name, message):
        self.buffer.append((name, message))

    def save_pdf(self, filename):
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = self.page_width, self.page_height

        c.setFont(self.fonts['bold'], 16)
        c.drawCentredString(width / 2.0, height - inch, self.topic)
        c.setFont(self.fonts['normal'], 12)
        margin = 1 * inch
        y = height - 1.5 * inch

        for name, message in self.buffer:
            if y < margin + 40:
                c.showPage()
                y = height - 1.5 * inch
                c.setFont("Helvetica", 12)

            if name == self.buffer[0][0]:  # 첫 번째 talker는 왼쪽
                self.draw_bubble(c, margin, y, width - 2 * margin, name, message, self.colors['left'], align='left')
                y -= 60
            else:  # 두 번째 talker는 오른쪽
                self.draw_bubble(c, margin, y, width - 2 * margin, name, message, self.colors['right'], align='right')
                y -= 60

        c.save()

    def draw_bubble(self, c, x, y, max_width, name, text, color, align='left'):
        padding = 5
        text_width = c.stringWidth(text, self.fonts['normal'], 12)
        name_width = c.stringWidth(name, self.fonts['bold'], 12) + padding
        bubble_width = max(text_width, name_width) + 2 * padding
        bubble_height = 40

        if align == 'left':
            bubble_x = x
            text_align = 'left'
        else:
            bubble_x = x + max_width - bubble_width
            text_align = 'right'

        bubble_y = y - bubble_height

        c.setFillColor(color)
        c.roundRect(bubble_x, bubble_y, bubble_width, bubble_height, 5, fill=1)
        c.setFillColor(colors.black)
        c.setFont(self.fonts['normal'], 12)
        c.drawString(bubble_x + padding, bubble_y + bubble_height - 15, name)
        c.setFont(self.fonts['normal'], 12)
        if text_align == 'left':
            c.drawString(bubble_x + padding, bubble_y + 10, text)
        else:
            c.drawRightString(bubble_x + bubble_width - padding, bubble_y + 10, text)
