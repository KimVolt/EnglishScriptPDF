import gradio as gr
import base64

from script import ChatScript, PDFGenerator

class WebUI:
    def __init__(self, title):
        self.title = title
        self.script = ChatScript()
        self.pdf = None
        self.pdf_path = "./history.pdf"
        
        # components
        self.display = None
        self.dropdown = None
    
    def launch(self):
        with gr.Blocks() as app:
            self.get_topic_tab()
            self.get_chat_tab()
        app.launch()
            
    def get_topic_tab(self):
        with gr.Tab("Topic"):
            topic = gr.Textbox(label="Topic")
            with gr.Row():
                talker1 = gr.Textbox(label="Talker 1")
                talker2 = gr.Textbox(label="Talker 2")            
            btn_topic = gr.Button("Confirm")
            btn_topic.click(self.btn_topic_event, inputs=[topic, talker1, talker2])
    
    def btn_topic_event(self, topic, talker1, talker2):
        try:
            self.script.add_name([talker1, talker2])
            self.script.set_topic(topic)
            self.pdf = PDFGenerator(topic)
            return gr.update(choices=[talker1, talker2])
        except Exception as e:
            return str(e)
        
    def get_chat_tab(self):
        with gr.Tab("Chat"):
            self.display = gr.HTML() # display chat history as PDF
            with gr.Row():
                with gr.Column():
                    self.dropdown = gr.Dropdown(label="Talker")
                    btn_refresh = gr.Button("Refresh")
                message_input = gr.Textbox(label="Message")
            btn_add = gr.Button("Add")
            
            btn_refresh.click(self.refresh_dropdown, outputs=self.dropdown)
            btn_add.click(self.add_chat, inputs=[self.dropdown, message_input], outputs=self.display)
                    
    def add_chat(self, name, message):
        try:
            self.script.add_script(name, message)
            self.pdf.add_message(name, message)
            self.pdf.save_pdf(self.pdf_path)
            return self.display_pdf(self.pdf_path)
        except Exception as e:
            return str(e)
    
    def refresh_dropdown(self):
        talkers = self.script.get_talker()
        return gr.update(choices=talkers)
        
    def display_pdf(self, path):
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        return f'<iframe src="data:application/pdf;base64,{encoded}" width="100%" height="600px"></iframe>'

    def format_chat_history(self):
        history = []
        for name, message in self.script.get_script():
            history.append(message)
        return history