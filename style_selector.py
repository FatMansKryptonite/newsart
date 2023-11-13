import json
from random import sample


with open('utils/art_styles.json', encoding='utf-8') as f:
    style_dict = json.load(f)


def get_style():
    style = sample(list(style_dict.keys()), 1)[0]

    return style
