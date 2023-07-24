# handle communcation with openai API

import os
import json
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
    system_role: str = """
    You are OrderBot, an automated service to collect orders for food menus 
    for Emmanuel Cuisine. You first welcome the customer with 
    'Welcome to Emmanuel Cuisine, your tastebuds would be satisfied!!!', then 
    collect the customer order, and the asks if it is a pickup or delivery.
    You wait to collect the entire order, then summarize it and check for a  
    final time if the customer wants anything else. 
    If it is delivery, ask for customer address. Finally you collect the payment.
    You respond in a short, very conventional friendly style. 
    For each swallow, ask how many scoops the customer wants and multiply the price 
    of each menu item with the amount of scoops, after the customer has provided the swallows, 
    ask for the soup the customer prefers form the soups section. For proteins ask how many pieces
    the customer want, do the same for drinks
    The menu includes
    Swallows:
    Amala 100
    Fufu 70
    Pounded yam 150
    
    Proteins:
    Pomo 30
    Meat 80
    Chicken 90
    Fish 90
    
    Soups:
    Awedu 0
    Vegetable 0
    
    Drinks:
    Pepsi 10
    Coke 10
    Sprite 10
    Bottled water 5
    """,
):
    global message_history
    message_history += [{"role": "system", "content": system_role}]
    message_history += [{"role": "user", "content": user_message}]

    return gr.update(value="", interactive=False), history + [[user_message, ""]]


def get_completion_from_message(model: str = "gpt-3.5-turbo"):
    global message_history
    global cost

    completion = openai.ChatCompletion.create(
        model=model,
        messages=message_history,
    )

    # calculate cost for each request sent
    cost += completion.usage.total_tokens * (0.002 / 1_000)

    # reply gotten from the bot, i.e assistant message
    return completion["choices"][0]["message"]["content"]


def generate_response(history: List[list], model: str = "gpt-3.5-turbo"):
    global message_history, cost

    bot_message = get_completion_from_message(model)

    message_history += [{"role": "assistant", "content": bot_message}]

    for character in bot_message:
        history[-1][1] += character
    return history


def get_json_output():
    global message_history

    message_history += [
        {
            "role": "system",
            "content": """Create a JSON summary of the just concluded order after the order has been completed. 
                         The fields should contain 1) a generated id 2) swallows 3) proteins 4) drinks 5) delivery address (if any) 6) total price. 
                         The function should always return the JSON summary of the order.""",
        }
    ]

    return get_completion_from_message()


def calc_cost():
    global cost

    return cost


if __name__ == "__main__":
    add_text()
    generate_response()
    calc_cost()
