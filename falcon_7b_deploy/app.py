import gradio as gr

from backend import generate


EXAMPLES = [
    ["Who is Bola Ahmed Tinubu?"],
    ["What is the largest city by land mass in Nigeria"],
    ["Who invented the C# programming language"],
]

additional_inputs = [
    gr.Textbox("", label="Optional system prompt", lines=5),
    gr.Slider(
        label="Max new tokens",
        info="The maximum of new tokens generated as reply",
        minimum=0,
        maximum=1024,
        step=32,
        value=256,
        interactive=True,
    ),
    gr.Slider(
        label="Top-p",
        info="Controls response randomness. Higher values sample more tokens",
        minimum=0.0,
        maximum=0.99,
        step=0.05,
        value=0.9,
        interactive=True,
    ),
]

with gr.Blocks() as demo:
    with gr.Column():
        gr.Markdown("# Falcon-7 Chat Demo")

    gr.ChatInterface(
        fn=generate, examples=EXAMPLES, additional_inputs=additional_inputs
    )

demo.queue().launch(debug=True)
