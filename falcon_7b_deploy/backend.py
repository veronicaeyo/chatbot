import boto3
import json


sagemaker_client = boto3.client("sagemaker-runtime")

endpoint_name = "falcon-7b-instruct"

STOP_WORDS = ["\nUser", "<|endoftext|>", " User", " System:"]

# def format_chat_prompt(message: str, history, system_prompt: str):
#     prompt = ""
#     if system_prompt:
#         prompt += f"System: {system_prompt}\n"

#     for user_prompt, bot_response in history:
#         prompt += f"User: {user_prompt}\n"
#         prompt += f"Assistant: {bot_response}\n"

#     prompt += f"User: {message}\n Assistant:"

#     return prompt


def format_chat_prompt(message: str, history, system_prompt: str) -> str:
    prompt = ""
    if system_prompt:
        prompt += f"System: {system_prompt}\n"
    for user_message, bot_message in history:
        prompt += f"{prompt}\nUser: {user_message}\nMini: {bot_message}"
    prompt += f"{prompt}\nUser: {message}\nMini:"
    return prompt


def generate(message, history, system_prompt="", max_new_tokens=40, top_p=0.9):
    prompt = format_chat_prompt(message, history, system_prompt)

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_new_tokens,
            "return_full_text": False,
            "do_sample": True,
            "top_p": top_p,
            "stop": STOP_WORDS,
        },
    }

    # Send the request to the SageMaker endpoint
    response = sagemaker_client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="application/json",
        Body=json.dumps(payload),
    )

    # Parse the response and extract the embeddings vector
    response_body = response["Body"].read().decode("utf-8")
    response_json = json.loads(response_body)

    stream = response_json[0]["generated_text"]
    output = ""

    for res in stream:
        output += res
        for word in STOP_WORDS:
            if output.endswith(word):
                output = output[: -len(word)]
                output = output.rstrip()
                yield output
        yield output
    # output = output.replace("\n", "").strip("?")

    return output


if __name__ == "__main__":
    generate()
