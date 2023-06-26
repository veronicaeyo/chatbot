# handle communcation with openai API

import os
from typing import List, Dict
from dotenv import load_dotenv

import gradio as gr
import openai

load_dotenv()

openai.api_key = os.getenv("API_KEY")

# messages to pass to openai API
message_history: List[Dict[str, str]] = []
cost = 0


# history: input messages and chatbot reply messages
def add_text(
    user_message: str,
    history: List[list],
    system_role: str = "You are a great assistant",
):
    global message_history
    message_history += [{"role": "system", "content": system_role}]
    message_history += [{"role": "user", "content": user_message}]
    return gr.update(value="", interactive=False), history + [[user_message, ""]]


def generate_response(history: List[list], model: str = "gpt-3.5-turbo"):
    global message_history, cost 

    completion = openai.ChatCompletion.create(
        model=model,
        messages=message_history,
    )
    bot_message = completion["choices"][0]["message"]["content"]
    
    # calculate cost for each request sent 
    cost +=completion.usage.total_tokens * (0.002/1_000)

    message_history += [{"role": "assistant", "content": bot_message}]

    for character in bot_message:
        history[-1][1] += character
        yield history
        
def calc_cost():
    global cost 
    return cost 

if __name__ == "__name__":
    add_text()
    generate_response()
    calc_cost()
