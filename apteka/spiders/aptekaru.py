import scrapy
from scrapy.http import HtmlResponse


class AptekaruSpider(scrapy.Spider):
    name = "aptekaru"
    allowed_domains = ["apteka-ot-sklada.ru"]
    start_urls = [
        "https://apteka-ot-sklada.ru/catalog/medikamenty-i-bady/zabolevaniya-pecheni-i-zhelchnogo-puzyrya/gepatoprotektory"]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//span[text()='Далее']/ancestor::a/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//div[@itemtype='https://schema.org/Product']//a/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.products_parse)

    def products_parse(self, response: HtmlResponse):
        pass
