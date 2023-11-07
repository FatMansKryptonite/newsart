from openai.types.images_response import ImagesResponse
from app_config import AppConfig
from datetime import datetime


class NewsArt:

    def __init__(self,
                 articles: list = None,
                 article_keywords: list = None,
                 art_style: str = None,
                 dall_e_response: ImagesResponse = None,
                 app_config: AppConfig = None):
        self.articles = articles
        self.article_keywords = article_keywords
        self.art_style = art_style
        self.dall_e_response = dall_e_response
        self.app_config = app_config

        self.time_stamp = datetime.now()

    def save_to_file(self, location: str) -> None:
        pass
