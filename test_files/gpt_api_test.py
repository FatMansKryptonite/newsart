
import openai

with open('api_keys/openai_api_key.txt') as f:
    openai.api_key = f.read()


messages = [
    {"role": "system", "content": "You are a intelligent assistant."}
]
while True:
    message = input("User : ")
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-4", messages=messages
        )
    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")
    messages.append({"role": "assistant", "content": reply})
