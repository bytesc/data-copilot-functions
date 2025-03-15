import random
import string

import pandas as pd
import pygwalker as pyg
from agent.utils.get_config import config_data
STATIC_URL = config_data['static_path']

def generate_random_string(length=8):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string


def get_html(df: pd.DataFrame):
    try:
        html_str = pyg.to_html(df, appearance='light')
    except Exception as e:
        print("df err", e)
        html_str = ""
    return html_str


def pd_to_walker(df: pd.DataFrame):
    file_path = "./tmp_imgs/" + generate_random_string(12)+".html"
    html = get_html(df)
    with open(file_path, 'w') as file:
        file.write(html)
    return STATIC_URL + file_path[2:]
