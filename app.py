from news_client import get_latest_headlines
from bbc_scraper import get_text_from_url, is_bbc_news_article


def main():
    news_articles = get_latest_headlines()

    for i in range(len(news_articles)):
        url = news_articles[i]["redirect_url"]
        title = news_articles[i]["title"]

        print(i + 1, title, url)

        if is_bbc_news_article(url):
            article = get_text_from_url(url)
            print('\n' + article)

        print(100*'-' + 3*'\n')


if __name__ == '__main__':
    main()
