from openai.types.images_response import ImagesResponse
from app_config import AppConfig
from datetime import datetime
from gpt_client import prompt_gpt
import json
import os
import base64


class NewsArt:

    def __init__(self,
                 articles: list = None,
                 article_keywords: list = None,
                 art_style: str = None,
                 dall_e_prompt: str = None,
                 dall_e_response: ImagesResponse = None,
                 app_config: AppConfig = None):
        self.articles = articles
        self.keywords = article_keywords
        self.art_style = art_style
        self.dall_e_prompt = dall_e_prompt
        self.dall_e_response = dall_e_response
        self.app_config = app_config

        self.time_stamp = datetime.now().strftime("%Y-%m-%d_H%HM%MS%S")

    def make_keyword_map(self):
        keyword_map = {}

        keyword_map['article_list'] = str([article['content'] for article in self.articles])

        return keyword_map

    def make_keywords(self):
        response = prompt_gpt('make_article_keywords', keyword_map=self.make_keyword_map())
        keywords = response['keywords']

        self.keywords = keywords

    def summary(self) -> dict:
        data = {
            'time_stamp': self.time_stamp,
            'title': self.articles[0]['title'],  # TODO add support for multiple articles
            'url': self.articles[0]['redirect_url'],
            'format': self.articles[0]['format'],
            'score': self.articles[0]['score'],
            'article_keywords': self.keywords,
            'content': self.articles[0]['content'],
            'art_style': self.art_style,
            'dall_e_prompt': self.dall_e_prompt,
            'dall_e_revised_prompt': self.dall_e_response.data[0].revised_prompt,
            'app_config': str(self.app_config)
        }

        return data

