# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class Phase3Pipeline:
    def process_item(self, item, spider):
        return item

class BookScraperPipeline:
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)

        # String all whitespace from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                # Get the current value
                value = adapter.get(field_name)
                # Modify item value for each name except description
                adapter[field_name] = value.strip()

        # Category & Product Type make it lowercase
        lowercase_keys = ['category', 'product_type']
        for key in lowercase_keys:
            value = adapter.get(key)
            adapter[key] = value.lower()

        # Price --> convert to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for key in price_keys:
            # Get the current key value
            value = adapter.get(key)
            # Remove the money symbol
            value = value.replace('£', '')
            # Modify item for current key value
            adapter[key] = float(value)
        
        # Availability --> extract number of books in stock
        availability_string = adapter.get('availability')
        split_string_array = availability_string.split('(')
        if len(split_string_array) < 2:
            adapter['availability'] = 0
        else:
            availability_array = split_string_array[1].split(' ')
            adapter['availability'] = int(availability_array[0])
        
        # Reviews --> convert string to number
        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)

        # Stars --> convert text to number
        stars_string = adapter.get('stars')
        split_stars_array = stars_string.split(' ')
        stars_text_value = split_stars_array[1].lower()

        if stars_text_value == 'zero':
            adapter['stars'] = 0
        elif stars_text_value == 'one':
            adapter['stars'] = 1
        elif stars_text_value == 'two':
            adapter['stars'] = 2
        elif stars_text_value == 'three':
            adapter['stars'] = 3
        elif stars_text_value == 'four':
            adapter['stars'] = 4
        elif stars_text_value == 'five':
            adapter['stars'] = 5
        
        return item