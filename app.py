from news_client import get_latest_headlines
from bbc_scraper import get_text_from_url, is_supported_article
from article_scorer import get_article_score
from dalle_prompt_designer import get_dalle_prompt


def print_articles(articles: list, scores=None) -> None:
    for i in range(len(articles)):
        url = articles[i]["redirect_url"]
        title = articles[i]["title"]

        header_string = f'{i}: {title} {url}'
        if scores is not None:
            header_string = f'{i}: SCORE: {scores[i]} {title} {url}'
        print(header_string)

        if is_supported_article(url):
            print('\n' + articles[i]['content'])

        print(100*'-' + 3*'\n')


def main():
    articles = get_latest_headlines()

    supported_articles = []
    for article in articles:
        if is_supported_article(article["redirect_url"]):
            article['content'] = get_text_from_url(article["redirect_url"])
            supported_articles.append(article)

    scores = get_article_score(supported_articles)
    print_articles(supported_articles, scores)

    max_score = max(scores)
    chosen_article_index = scores.index(max_score)
    chosen_articles = [supported_articles[chosen_article_index]]

    dalle_prompt = get_dalle_prompt('romanticism', chosen_articles)
    print(dalle_prompt)


if __name__ == '__main__':
    main()
