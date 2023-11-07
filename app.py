from news_client import get_latest_headlines
from bbc_scraper import get_text_from_url, is_supported_article
from article_scorer import get_article_score
from dall_e_prompt_designer import get_dalle_prompt
from image_generator import make_image
from style_selector import get_style


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
    chosen_articles = [supported_articles[chosen_article_index]]

    # Make DALL E prompt
    chosen_style = get_style()
    dall_e_prompt = get_dalle_prompt(chosen_style, chosen_articles)
    print(dall_e_prompt)

    # Generate image
    dall_e_response = make_image(dall_e_prompt, configuration_name='quality')
    print(dall_e_response.data[0].url)


if __name__ == '__main__':
    main()
