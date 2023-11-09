import ast
import json
import re
from openai import OpenAI

with open('api_keys/openai_api_key.txt') as f:
    api_key = f.read()
client = OpenAI(api_key=api_key)


def parse_message(messages: list, keyword_map: dict) -> list:
    for i in range(len(messages)):
        message = messages[i]['content']
        matches = re.findall(r'\$(?:[a-z]|_)+\$', message)
        for match in matches:
            message = message.replace(match, keyword_map[match[1:-1]])

        messages[i]['content'] = message
    return messages


def get_prompt_from_gpt(messages: dict, functions: list) -> list:
    chat = client.chat.completions.create(
        model='gpt-4',
        messages=messages,
        functions=functions,
        function_call={"name": functions[0]['name']}
    )

    response = chat.choices[0].message.function_call.arguments
    return response


def clean_response(str_response: str) -> object:
    response = ast.literal_eval(str_response)
    return response


def prompt_gpt(prompt_name: str, keyword_map: dict = None) -> str:
    with open('settings/gpt_interfaces.json') as f:
        gpt_prompts = json.load(f)

    for prompt in gpt_prompts:
        if prompt['name'] == prompt_name:
            break

    messages = prompt['messages']
    if keyword_map is not None:
        messages = parse_message(messages, keyword_map)

    str_response = get_prompt_from_gpt(messages, prompt['functions'])
    response = clean_response(str_response)

    return response
