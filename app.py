# render gradio interface

import random
import time

import gradio as gr

from backend import add_text, generate_response, calc_cost


def user(user_message, history):
    return gr.update(value="", interactive=False), history + [[user_message, ""]]


def bot(history):
    bot_message = random.choice(["How are you?", "I love you", "I'm very hungry"])
    for character in bot_message:
        history[-1][1] += character
        time.sleep(0.05)
        yield history




with gr.Blocks() as demo:
    gr.Markdown("<h1><center>Order Bot</center></h1>")
    chatbot = gr.Chatbot()

    with gr.Row():
        with gr.Column(scale=0.9):
            msg = gr.Textbox(label="\n", placeholder="Send a message and press Enter")

        with gr.Column(scale=0.1):
            cost_view = gr.Number(label="Usage in $", value=0)

    clear = gr.ClearButton([msg, chatbot, cost_view])

    models = gr.Radio(
        value="gpt-3.5-turbo",
        choices=["gpt-3.5-turbo", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-16k"],
        label="Models",
    )

    response = (
        msg.submit(
            fn=add_text, inputs=[msg, chatbot], outputs=[msg, chatbot], queue=False
        )
        .then(fn=generate_response, inputs=[chatbot, models], outputs=chatbot)
        .then(fn=calc_cost, outputs=cost_view)
    )

    response.then(lambda: gr.update(interactive=True), None, [msg], queue=False)

demo.queue()
demo.launch()
