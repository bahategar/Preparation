import json


_config = {
    "url": "https://quotes.toscrape.com/js",
    "meta": {
        "name": "Quotes scraper",
        "description": "Extract all quotes",
        "author": "Quentin Bauer",
        "base_url": "https://quotes.toscrape.com/",
        "version": 0.1,
    },
    "containers": [
        {
            "name": "quote_divs",
            "selector": "div.quote",
            "match": "all",
            "type": "node",
            "items": [
                {
                    "name": "quote",
                    "selector": "*[class='text']",
                    "match": "first", 
                    "type": "text"
                },
                {
                    "name": "author",
                    "selector": "*[class='author']",
                    "match": "first",
                    "type": "text"
                },
                {
                    "name": "tags",
                    "selector": "*[class='tag']",
                    "match": "all",
                    "type": "text"
                }
            ],
        },
        {
            "name": "next_button",
            "selector": ".pager .next a",
            "match": "first",
            "type": "node",
            "items": []
        },
    ]
}

def get_config(load_from_file=False):
    if load_from_file:
        with open("config.json", "r") as f:
            return json.load(f)
            
    return _config

def generate_config():
    with open("config.json", "w") as f:
        json.dump(_config, f, indent=4)


if __name__ == "__main__":
    generate_config()