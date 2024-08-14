import os
import pdfkit
from flask import request, jsonify, send_file, render_template

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/generate_pdf', methods=['POST'])
    def generate_pdf_route():
        data = request.json
        topic = data.get('topic', 'No Topic')
        messages = data.get('messages', [])

        # HTML 생성
        html_content = render_template('pdf_template.html', topic=topic, messages=messages)
        with open('temp.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

        # CSS
        css_path = os.path.join(os.getcwd(), 'static', 'style.css')

        # wkhtmltopdf에 필요한 옵션 설정
        options = {
            'enable-local-file-access': None  # 로컬 파일 액세스 허용
        }

        # HTML을 PDF로 변환 (CSS 경로를 절대 경로로 명시)
        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        pdfkit.from_file('temp.html', 'chat_history.pdf', configuration=config, options=options, css=css_path)

        return send_file('chat_history.pdf', as_attachment=True)
