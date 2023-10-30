from news_client.news_client import get_latest_headlines


def main():
    news_articles = get_latest_headlines()

    results = []
    for article in news_articles:
        results.append(article["title"])

    for i in range(len(results)):
        print(i + 1, results[i])


if __name__ == '__main__':
    main()
