import json
import re
import openai
import ast
import numbers

with open('api_keys/openai_api_key.txt') as f:
    openai.api_key = f.read()


def make_keyword_map(articles: list) -> dict:
    keyword_map = {}

    titles = [article['title'] for article in articles]
    title_list_string = f'[{", ".join(titles)}]'
    keyword_map['title_list'] = title_list_string

    with open('settings/covered_keywords.json') as f:
        covered_keywords = json.load(f)
    covered_keywords_string = f'{"; ".join(covered_keywords[:100])}'
    keyword_map['recent_topics_keyword_list'] = covered_keywords_string

    return keyword_map


def parse_message(messages: list, keyword_map: dict) -> list:

    message = messages[-1]['content']
    matches = re.findall(r'\$(?:[a-z]|_)+\$', message)

    for match in matches:
        message = message.replace(match, keyword_map[match[1:-1]])

    messages[-1]['content'] = message
    return messages


def get_scores_from_gpt(messages: dict) -> list:
    chat = openai.ChatCompletion.create(
        model="gpt-4", messages=messages
    )

    response = chat.choices[0].message.content
    try:
        response_list = ast.literal_eval(response)
        if not type(response_list) == list\
                or not all(isinstance(elem, numbers.Number) for elem in response_list):
            raise ValueError
    except ValueError:
        raise ValueError("GPT response not on valid format.")

    return response_list


def give_article_score(articles: list, prompt_name: list = None) -> list:
    if prompt_name is None:
        prompt_name = 'article_scoring_prompt'

    with open('settings/gpt_prompts.json') as f:
        gpt_prompts = json.load(f)
    messages = gpt_prompts[prompt_name]['messages']

    messages = parse_message(messages, keyword_map=make_keyword_map(articles))
    scores = get_scores_from_gpt(messages)

    return scores



