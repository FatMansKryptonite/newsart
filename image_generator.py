from openai import OpenAI
import json

with open('api_keys/openai_api_key.txt') as f:
    api_key = f.read()
client = OpenAI(api_key=api_key)


def make_image(prompt: str, configuration_name: str = 'cheap'):
    with open('settings/dall_e_configurations.json') as f:
        configurations_file = json.load(f)
    settings = configurations_file[configuration_name]
    settings['prompt'] = prompt

    response = client.images.generate(**settings)

    return response
