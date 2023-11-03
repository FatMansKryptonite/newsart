from news_client import get_latest_headlines
from bbc_scraper import get_text_from_url, is_supported_article
from article_scorer import give_article_score


def print_articles(articles: list, scores=None) -> None:
    for i in range(len(articles)):
        url = articles[i]["redirect_url"]
        title = articles[i]["title"]

        header_string = f'{i}: {title} {url}'
        if scores is not None:
            header_string = f'{i}: SCORE: {scores[i]} {title} {url}'
        print(header_string)

        if is_supported_article(url):
            article = get_text_from_url(url)
            print('\n' + article)

        print(100*'-' + 3*'\n')


def main():
    articles = get_latest_headlines()

    supported_articles = []
    for article in articles:
        if is_supported_article(article["redirect_url"]):
            supported_articles.append(article)

    scores = give_article_score(supported_articles)

    print_articles(supported_articles, scores)


if __name__ == '__main__':
    main()
