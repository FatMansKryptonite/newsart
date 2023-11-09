import json
import re
from openai import OpenAI

from gpt_client import prompt_gpt
from news_art import NewsArt

with open('api_keys/openai_api_key.txt') as f:
    api_key = f.read()
client = OpenAI(api_key=api_key)


def make_keyword_map(news_art: NewsArt) -> dict:
    keyword_map = {}

    keyword_map['art_style'] = news_art.art_style

    contents = [article['content'] for article in news_art.articles]
    contents_list_string = f'[{", ".join(contents)}]'
    keyword_map['article_list'] = contents_list_string

    return keyword_map


def get_dall_e_prompt(news_art: NewsArt) -> str:
    response = prompt_gpt('make_dall_e_prompt', keyword_map=make_keyword_map(news_art))
    dall_e_prompt = response['prompt']

    return dall_e_prompt
