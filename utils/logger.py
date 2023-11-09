import base64
import os

from news_art import NewsArt
import json


def log_keywords(news_art: NewsArt, log_path: str = 'utils/covered_keywords.json') -> None:
    with open(log_path, 'r') as f:
        keyword_list = json.load(f)

    keyword_list += news_art.keywords

    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(keyword_list, f, ensure_ascii=False, indent=2)


def log_news_art(news_art: NewsArt, log_path: str = "news_art_archive") -> str:
    data_path = os.path.join(log_path, 'data', news_art.time_stamp + '.json')
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(news_art.summary(), f, ensure_ascii=False, indent=2)

    image_path = os.path.join(log_path, 'images', news_art.time_stamp + '.png')
    with open(image_path, "wb") as f:
        f.write(base64.decodebytes(news_art.dall_e_response.data[0].b64_json.encode('utf-8')))

    return image_path
