import json
import re
from openai import OpenAI
from news_art import NewsArt

with open('api_keys/openai_api_key.txt') as f:
    api_key = f.read()
client = OpenAI(api_key=api_key)


def parse_message(messages: list, paramter_map: dict) -> list:

    message = messages[-1]['content']
    matches = re.findall(r'\$(?:[a-z]|_)+\$', message)

    for match in matches:
        message = message.replace(match, paramter_map[match[1:-1]])

    messages[-1]['content'] = message
    return messages


def get_prompt_from_gpt(messages: dict) -> list:
    chat = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )

    response = chat.choices[0].message.content
    return response


def prompt_gpt(prompt_name: str, paramter_map: dict) -> str:
    if prompt_name is None:
        prompt_name = 'make_dalle_prompt_prompt'

    with open('settings/gpt_prompts.json') as f:
        gpt_prompts = json.load(f)
    messages = gpt_prompts[prompt_name]['messages']

    messages = parse_message(messages, paramter_map=paramter_map)
    prompt = get_prompt_from_gpt(messages)

    return dalle_prompt