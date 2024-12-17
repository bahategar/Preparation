from selectolax.parser import Node, HTMLParser
from typing import Union


def parse_raw_attributes(base: Union[Node, HTMLParser], items: list) -> dict :
    if not issubclass(Node, type(base)) or not issubclass(HTMLParser, type(base)):
        ValueError("Make sure the node type is str ot Node selectolax.")
    
    parsed = {}
    for item in items:
        match = item.get("match")
        type_ = item.get("type")
        selector = item.get("selector")
        name = item.get("name")

        if match == "all":
            matched = base.css(selector)
            if matched:
                if type_ == 'text':
                    parsed[name] = [n.text() for n in matched]
                elif type_ == 'node':
                    parsed[name] = matched
            else:
                parsed[name] = ''

        elif match == 'first':
            matched = base.css_first(selector)

            if matched:
                if type_ == 'text':
                    parsed[name] = matched.text()
                elif type_ == 'node':
                    parsed[name] = matched
            else:
                parsed[name] = ''

    return parsed