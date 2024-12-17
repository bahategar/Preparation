from selectolax.parser import Node
from datetime import datetime
import re
import pandas as pd
from typing import Union


def get_attrs_from_node(node: Node, attr: str) -> str:
    if not node:
        return None
    if not issubclass(Node, type(node)):
        raise ValueError("The function expects a selecolax node to be provided")

    return node.attributes.get(attr)


def date_formatting(date: str, from_format: str, to_format: str = "%Y-%m-%d"):
    date_obj = datetime.strptime(date, from_format)

    formatted_date = date_obj.strftime(to_format)
    return formatted_date


def join_url(base, relative):
    if not base.endswith('/'):
        base += '/'
    return base + relative.lstrip('/')

def get_config_by_name(name: str, items: list):
    for i in items:
        if i['name'] == name:
            return i
    return None


def format_and_transform(parsed: dict) -> dict:
    transforms = {
        'tags': lambda x: ", ".join(x),
        'next_button': lambda n: get_attrs_from_node(n, attr='href'),
    }

    for k, v in transforms.items():
        if k in parsed:
            parsed[k] = v(parsed[k])

    return parsed

def save_to_file(filename: str = 'extract', data: Union[list[dict], dict] = None):
    if data is None:
        raise ValueError("The function expects data to be provided as a list of dictionaries or dictionary")
    
    df = pd.DataFrame(data)
    filename = f"{datetime.now().strftime('%Y_%m_%d')}_{filename}.csv"
    df.to_csv(filename, index=False)