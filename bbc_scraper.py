import requests
from bs4 import BeautifulSoup
import re
import json


with open('utils/supported_article_formats.json') as f:
    supported_article_formats = json.load(f)


def is_supported_article(url: str) -> (bool, str):
    for format in supported_article_formats:
        pattern = supported_article_formats[format]['url_pattern']

        if re.fullmatch(pattern, url) is not None:
            supported = supported_article_formats[format]['supported']

            return supported, format

    return False, None


def get_elements_from_news_article(soup: BeautifulSoup) -> list:
    divs = soup.find_all('div', attrs={'data-component': ['text-block', 'subheadline-block']})

    extracted_elements = [soup.find('h1', id='main-heading')]
    for div in divs:
        extracted_elements += div.find_all(['p', 'h2'])

    return extracted_elements


def get_elements_from_video_article(soup: BeautifulSoup) -> list:
    extracted_elements = [soup.find('h1', id='main-heading')]
    div = soup.find('div', attrs={'data-testid': ['reveal-text-wrapper']})
    extracted_elements += div.find_all(['p'])

    return extracted_elements


def get_elements_from_url(url: str, format: str) -> list:
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    if format == 'news':
        extracted_elements = get_elements_from_news_article(soup)
    elif format == 'video':
        extracted_elements = get_elements_from_video_article(soup)
    else:
        raise ValueError(f'Format {format} not supported. '
                         f'Check utils/supported_article_formats.json for supported formats.')

    return extracted_elements


def get_text_from_elements(elements: list) -> str:
    text_list = [elem.text for elem in elements]

    return '\n'.join(text_list)


def get_text_from_url(url: str, format: str) -> str:
    # TODO Doesn't pick up unordered-list-blocks from articles
    elements = get_elements_from_url(url, format)
    text = get_text_from_elements(elements)

    return text
