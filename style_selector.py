import json
from numpy.random import choice
import numpy as np


with open('utils/art_styles.json', encoding='utf-8') as f:
    style_dict = json.load(f)


def get_style(n: int = 1):
    probabilities = np.array(list(style_dict.values())) / sum(style_dict.values())
    chosen_styles = choice(list(style_dict.keys()), n, p=probabilities)

    return chosen_styles[0]
