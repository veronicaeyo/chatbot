# render gradio interface

import gradio as gr
import random
import time

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])
    
    audio = gr.Audio(source="microphone")

    def respond(message, chat_history):
        bot_message = random.choice(["How are you?", "I love you", "I'm very hungry"])
        chat_history.append((message, bot_message))
        # time.sleep(2)
        return "", chat_history

    msg.submit(fn=respond, inputs=[msg, chatbot], outputs=[msg, chatbot])

demo.launch()
