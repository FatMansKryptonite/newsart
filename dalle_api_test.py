import openai


with open('api_keys/openai_api_key.txt') as f:
    openai.api_key = f.read()

style = "Post-Impressionism"
PROMPT = f"Generate an image in {style} of Belgians racing boats made of giant pumpkins."
PROMPT = f"Generate an image in Surrealist style depicting a regatta where Belgians are racing boats made of giant, intricately carved pumpkins floating on a whimsical river under a sky filled with swirling, dream-like clouds."

response = openai.Image.create(
    prompt=PROMPT,
    n=4,
    size="1024x1024",
)

for img in response['data']:
    print(img["url"])
