from fpdf import FPDF
import json
import os

def generate_pdf(json_filepath):
    try:
        with open(json_filepath, 'r') as file:
            chat_data = json.load(file)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for topic, messages in chat_data.items():
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt=topic, ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", size=12)

            for message_data in messages:
                talker = message_data.get('talker', 'Unknown')
                message = message_data.get('message', '')
                pdf.multi_cell(0, 10, f"{talker}: {message}")
                pdf.ln(5)

        output_pdf = "chat_history.pdf"
        pdf.output(output_pdf)
        return output_pdf
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None
