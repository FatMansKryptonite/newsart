from openai import OpenAI

with open('api_keys/openai_api_key.txt') as f:
    api_key = f.read()
client = OpenAI(api_key=api_key)


def make_image(prompt: str):
    response = client.images.generate(
        model="dall-e-3",
        quality="hd",
        style="vivid",
        prompt=prompt,
        n=1,
        size="1024x1024",
    )

    return response
