import scrapy


class AptekaruSpider(scrapy.Spider):
    name = "aptekaru"
    allowed_domains = ["apteka-ot-sklada.ru"]
    start_urls = ["https://apteka-ot-sklada.ru"]

    def parse(self, response):
        pass
