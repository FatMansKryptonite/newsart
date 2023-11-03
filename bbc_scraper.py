import requests
from bs4 import BeautifulSoup
import re


def is_bbc_news_article(url: str) -> bool:
    # TODO Add to external settings file
    supported_subsites = ['uk',
                          'world-us-canada',
                          'business',
                          'world-australia',
                          'world-asia-india',
                          'entertainment-arts']
    pattern = rf'https?:\/\/www\.bbc\.(co\.uk|com)\/news\/({"|".join(supported_subsites)})-\d{{8}}'
    is_news_article = re.fullmatch(pattern, url) is not None

    return is_news_article


def get_elements_from_url(url: str) -> list:
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    divs = soup.find_all('div', attrs={'data-component': ['text-block', 'subheadline-block']})

    extracted_elements = [soup.find('h1', id='main-heading')]
    for div in divs:
        extracted_elements += div.find_all(['p', 'h2'])

    return extracted_elements


def get_text_from_elements(elements: list) -> str:
    text_list = [paragraph.text for paragraph in elements]

    return '\n'.join(text_list)


def get_text_from_url(url: str) -> str:
    # TODO Doesn't pick up unordered-list-blocks from articles
    elements = get_elements_from_url(url)
    text = get_text_from_elements(elements)

    return text
