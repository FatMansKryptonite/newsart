import requests
import json


def get_api_key() -> str:
    with open('api_keys/news_api_key.txt') as f:
        api_key = f.read()

    return api_key


def get_query_params(settings: dict) -> dict:
    query_params = {key: settings[key] for key in ["source", "sortBy"]}
    query_params['apiKey'] = get_api_key()

    return query_params


def get_main_url(settings: dict) -> str:
    main_url = settings["main_url"]

    return main_url


def get_query_params_and_url(settings_file: str = "settings/news_client.json") -> (dict, str):
    with open(settings_file) as f:
        settings = json.load(f)

    query_params = get_query_params(settings)
    main_url = get_main_url(settings)

    return query_params, main_url


def get_latest_headlines():
    query_params, main_url = get_query_params_and_url()

    response = requests.get(main_url, params=query_params)
    open_bbc_page = response.json()
    articles = open_bbc_page["articles"]

    return articles

