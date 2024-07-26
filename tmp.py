import gradio as gr
from fpdf import FPDF

# 수정된 ChatScript 클래스
class ChatScript:
    def __init__(self):
        self.script = {}

    def add_name(self, name):
        if name not in self.script:
            self.script[name] = []
        else:
            raise Exception(f"[ERROR] Name {name} already exists")

    def add_script(self, script):
        # script -> {name: "script"}
        for key, value in script.items():
            if key in self.script:
                self.script[key].append(value)
            else:
                raise Exception(f"[ERROR] Name {key} does not exist")

    def get_script(self, name):
        if name in self.script:
            return self.script[name]
        else:
            raise Exception(f"[ERROR] Name {name} does not exist")

# 인스턴스 생성
chat_script = ChatScript()

# 함수 정의
def add_name(name):
    try:
        chat_script.add_name(name)
        return f"Name {name} added successfully."
    except Exception as e:
        return str(e)

def add_script(name, message):
    try:
        chat_script.add_script({name: message})
        return f"Message from {name} added successfully."
    except Exception as e:
        return str(e)

def save_as_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    
    for name, messages in chat_script.script.items():
        pdf.multi_cell(0, 10, f"{name}:")
        for message in messages:
            pdf.multi_cell(0, 10, f"  {message}")
        pdf.multi_cell(0, 10, "\n")
    
    output_filename = "/mnt/data/chat_history.pdf"
    pdf.output(output_filename)
    return output_filename

# Gradio 인터페이스 설정
with gr.Blocks() as app:
    with gr.Tab("Add Name"):
        name_input = gr.Textbox(label="Name")
        add_name_button = gr.Button("Add Name")
        add_name_output = gr.Textbox(label="Output")
        add_name_button.click(add_name, inputs=name_input, outputs=add_name_output)
        
    with gr.Tab("Add Script"):
        name_input_script = gr.Textbox(label="Name")
        message_input = gr.Textbox(label="Message")
        add_script_button = gr.Button("Add Script")
        add_script_output = gr.Textbox(label="Output")
        add_script_button.click(add_script, inputs=[name_input_script, message_input], outputs=add_script_output)
        
    with gr.Tab("Save as PDF"):
        save_pdf_button = gr.Button("Save as PDF")
        save_pdf_output = gr.File(label="Download Processed PDF")
        save_pdf_button.click(save_as_pdf, inputs=[], outputs=save_pdf_output)

app.launch()
