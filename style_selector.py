import json
from random import sample


with open('utils/styles.json') as f:
    style_list = json.load(f)


def get_style():
    style = sample(style_list, 1)[0]

    return style
