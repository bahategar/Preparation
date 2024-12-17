from selectolax.parser import HTMLParser
import pandas as pd

from utils.parse import parse_raw_attributes
from utils.extract import extract_full_body_html
from utils.process import format_and_transform, save_to_file, join_url, get_config_by_name
from config.tool import get_config


# GET CONFIGURATION
config = get_config()
BASE = config.get("meta").get("base_url")
URL = config.get("url")


def scrape_all_quotes(url: str) -> dict:
    storage = {
        'quote': [],
        'author':[],
        'tags':[],
        }

    # Get Configuration Items per-Container
    quote_items = get_config_by_name("quote_divs", config.get("containers")).get("items")
    
    while True:
        # Extract HTML
        html = extract_full_body_html(url)

        # If html is empty string, break
        if not html:
            break

        # Get Bases Containers
        bases = parse_raw_attributes(base=HTMLParser(html), items=config.get("containers"))
        bases = format_and_transform(bases)

        # Handling quote div elements
        quote_nodes = bases.get("quote_divs")
        for node in quote_nodes:
            parsed = parse_raw_attributes(base=node, items=quote_items)
            parsed = format_and_transform(parsed)
            storage["quote"].append(parsed.get("quote"))
            storage["author"].append(parsed.get("author"))
            storage["tags"].append(parsed.get("tags"))

        url = bases.get("next_button")
        if url:
            url = join_url(BASE, url)
        else:
            break
        
    return storage

storage = scrape_all_quotes(URL)
# save_to_file(data=storage)
df = pd.DataFrame(storage)
print(df)