from news_client import get_latest_headlines


def main():
    news_articles = get_latest_headlines()

    for i in range(len(news_articles)):
        print(i + 1, news_articles[i]["title"], news_articles[i]["url"])


if __name__ == '__main__':
    main()
