import json
from openai import OpenAI
from gpt_client import prompt_gpt

with open('api_keys/openai_api_key.txt') as f:
    api_key = f.read()
client = OpenAI(api_key=api_key)


def make_keyword_map(articles: list) -> dict:
    keyword_map = {}

    with open('settings/interesting_topics.json') as f:
        interesting_keywords = json.load(f)
    keyword_map['interesting_topics_list'] = str(interesting_keywords)

    titles = [article['title'] for article in articles]
    title_list_string = f'[{", ".join(titles)}]'
    keyword_map['title_list'] = title_list_string

    with open('settings/covered_keywords.json') as f:
        covered_keywords = json.load(f)
    keyword_map['recent_topics_keyword_list'] = str(covered_keywords[:100])

    return keyword_map


def get_article_score(articles: list) -> list:
    response = prompt_gpt('article_scoring', keyword_map=make_keyword_map(articles))
    scores = response['scores']

    return scores



