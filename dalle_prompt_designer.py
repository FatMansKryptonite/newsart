import json
import re
from openai import OpenAI

with open('api_keys/openai_api_key.txt') as f:
    api_key = f.read()
client = OpenAI(api_key=api_key)


def make_keyword_map(art_style: str, articles: list) -> dict:
    keyword_map = {}

    keyword_map['art_style'] = art_style

    contents = [article['content'] for article in articles]
    contents_list_string = f'[{", ".join(contents)}]'
    keyword_map['article_list'] = contents_list_string

    return keyword_map


def parse_message(messages: list, keyword_map: dict) -> list:

    message = messages[-1]['content']
    matches = re.findall(r'\$(?:[a-z]|_)+\$', message)

    for match in matches:
        message = message.replace(match, keyword_map[match[1:-1]])

    messages[-1]['content'] = message
    return messages


def get_prompt_from_gpt(messages: dict) -> list:
    chat = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )

    response = chat.choices[0].message.content
    response = response.replace("'", '')
    response = response.replace('"', '')
    return response


def get_dalle_prompt(art_style: str, articles: list, prompt_name: list = None) -> str:
    if prompt_name is None:
        prompt_name = 'make_dalle_prompt_prompt'

    with open('settings/gpt_prompts.json') as f:
        gpt_prompts = json.load(f)
    messages = gpt_prompts[prompt_name]['messages']

    messages = parse_message(messages, keyword_map=make_keyword_map(art_style, articles))
    dalle_prompt = get_prompt_from_gpt(messages)

    return dalle_prompt