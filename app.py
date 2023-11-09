import os

from news_client import get_latest_headlines
from bbc_scraper import get_text_from_url, is_supported_article
from article_scorer import get_article_score
from dall_e_prompt_designer import get_dall_e_prompt
from image_generator import make_image
from style_selector import get_style
from news_art import NewsArt
from utils.logger import log_keywords, log_news_art


def print_articles(articles: list) -> None:
    for i, article in enumerate(articles):
        output_str = ''

        output_str += f'''{i}: {article["title"]}
{{
    TITLE: {article["title"]},
    URL: {article["url"]},
    SCORE: {article["score"]},
    FORMAT: {article["format"]},
    SUPPORTED: {article["supported"]}
}}'''

        if article["supported"]:
            output_str += '\n' + articles[i]['content']
        output_str += '\n' + 100*'-' + 2*'\n'

        print(output_str)


def main() -> None:
    # Get articles
    articles = get_latest_headlines()

    # Scrape articles
    supported_articles = []
    for article in articles:
        article['supported'], article['format'] = is_supported_article(article["redirect_url"])

        if article['supported']:
            article['content'] = get_text_from_url(article["redirect_url"], article['format'])
            supported_articles.append(article)

    # Score articles
    scores = get_article_score(supported_articles)
    for article in articles:
        article['score'] = None
    for article, score in zip(supported_articles, scores):
        article['score'] = score
    print_articles(articles)

    # Choose articles
    max_score = max(scores)
    chosen_article_index = scores.index(max_score)
    news_art = NewsArt(articles=[supported_articles[chosen_article_index]])

    # Generate and log news art keywords
    news_art.make_keywords()

    # Define art style
    news_art.art_style = get_style()

    # Make DALL E prompt
    news_art.dall_e_prompt = get_dall_e_prompt(news_art)
    print(news_art.dall_e_prompt)

    # Generate image
    news_art.dall_e_response = make_image(news_art.dall_e_prompt, configuration_name='quality')

    # Log news art
    path_to_image = log_news_art(news_art)
    absolute_path = os.path.abspath(path_to_image).replace('\\', '/')
    print(f'Image available at (clickable on Winodws): file:///{absolute_path}')
    log_keywords(news_art)


if __name__ == '__main__':
    main()
