from datetime import datetime

import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from project.apteka.items import AptekaItem

only_one_variant = 1


class AptekaruSpider(scrapy.Spider):
    name = "aptekaru"
    allowed_domains = ["apteka-ot-sklada.ru"]
    start_urls = [
        "https://apteka-ot-sklada.ru/catalog/medikamenty-i-bady/zabolevaniya-pecheni-i-zhelchnogo-puzyrya/gepatoprotektory",
        "https://apteka-ot-sklada.ru/catalog/medikamenty-i-bady/zabolevaniya-serdechno_sosudistoy-sistemy/antigipoksanty",
        "https://apteka-ot-sklada.ru/catalog/medikamenty-i-bady/obezbolivayushchie-sredstva/bolevoy-sindrom-silnyy"
    ]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//span[text()='Далее']/ancestor::a/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//div[@itemtype='https://schema.org/Product']//a/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.products_parse)

    def products_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=AptekaItem(), response=response)

        dt = datetime.now()
        ts = datetime.timestamp(dt)
        loader.add_value("timestamp", ts)

        loader.add_xpath("RPC", "//div[@data-product-id]/@data-product-id")
        loader.add_value("url", response.url)
        loader.add_xpath("title", "//h1/span/text()")
        loader.add_xpath("marketing_tags", "//span[contains(@class, 'ui-tag')]/text()")
        loader.add_xpath("brand", "//div[@itemprop='manufacturer']/span[2]/text()")
        loader.add_xpath("section", "//a[@itemprop='item']/span/span/text()")
        loader.add_xpath("price_data", "//span[contains(@class, 'goods-offer-panel')]/text() "
                                       "| //aside//span[@class='ui-link__text']/span/text()")
        loader.add_xpath("stock", "//aside//span[@class='ui-link__text']/text()")
        loader.add_xpath("assets", "//div[contains(@class, 'goods-details-page')]//img/@src")
        loader.add_xpath("metadata", "//div[@itemprop='manufacturer']/span[1]/text() "
                                     "| //section[@id='description']//h2/text() "
                                     "| //section//h2/following-sibling::p//text() "
                                     "| //section//h3/text() "
                                     "| //section//h3/following-sibling::p//text() "
                                     "| //section//h3/following-sibling::ul//text() "
                                     "| //section//p/following-sibling::p/text()  ")
        loader.add_value("variants", only_one_variant)

        yield loader.load_item()
