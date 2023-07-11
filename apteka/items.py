import scrapy
from itemloaders.processors import TakeFirst, MapCompose


def removing_spaces(value):
    return value.strip()


def removing_spaces_in_list(data_list):
    return removing_spaces(data_list[0])


def process_stock(stock):
    removing_spaces_in_list(stock)
    stock_dict = {}
    stock_bool = True if "В наличии" in stock[0] else False

    stock_dict['in_stock'] = stock_bool
    stock_dict['count'] = 0
    return stock_dict


def process_marketing_tags(value):
    if value:
        value = removing_spaces_in_list(value)
    else:
        value = []
    return value


class AptekaItem(scrapy.Item):
    timestamp = scrapy.Field(output_processor=TakeFirst())
    RPC = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    marketing_tags = scrapy.Field(input_processor=MapCompose(process_marketing_tags))
    brand = scrapy.Field(output_processor=TakeFirst())
    section = scrapy.Field()
    price_data = scrapy.Field()
    stock = scrapy.Field(input_processor=MapCompose(process_stock), output_processor=TakeFirst())
    assets = scrapy.Field()
    metadata = scrapy.Field()
    variants = scrapy.Field(output_processor=TakeFirst())
