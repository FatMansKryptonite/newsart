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
        self.article_keywords = article_keywords
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

        self.article_keywords = keywords

    def save_to_file(self, location: str = "news_art_archive") -> str:
        data = {
            'time_stamp': self.time_stamp,
            'title': self.articles[0]['title'],  # TODO add support for multiple articles
            'url': self.articles[0]['redirect_url'],
            'format': self.articles[0]['format'],
            'score': self.articles[0]['score'],
            'content': self.articles[0]['content'],
            'article_keywords': self.article_keywords,
            'art_style': self.art_style,
            'dall_e_prompt': self.dall_e_prompt,
            'dall_e_revised_prompt': self.dall_e_response.data[0].revised_prompt,
            'app_config': str(self.app_config)
        }

        data_path = os.path.join(location, 'data', self.time_stamp + '.json')
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        image_path = os.path.join(location, 'images', self.time_stamp + '.png')
        with open(image_path, "wb") as f:
            f.write(base64.decodebytes(self.dall_e_response.data[0].b64_json.encode('utf-8')))

        return image_path