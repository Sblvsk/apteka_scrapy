import scrapy
from itemloaders.processors import TakeFirst, MapCompose


def removing_spaces(value):
    return value.strip()

def removing_spaces_in_list(data_list):
    return removing_spaces(data_list[0])

class AptekaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    timestamp = scrapy.Field(output_processor=TakeFirst())
    RPC = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    marketing_tags = scrapy.Field(input_processor=MapCompose(removing_spaces_in_list))
    brand = scrapy.Field(output_processor=TakeFirst())
    section = scrapy.Field()
    price_data = scrapy.Field()
    stock = scrapy.Field(input_processor=MapCompose(removing_spaces))
    assets = scrapy.Field()
    metadata = scrapy.Field()
    variants = scrapy.Field(output_processor=TakeFirst())
