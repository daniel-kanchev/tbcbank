import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from tbcbank.items import Article


class TbcbankSpider(scrapy.Spider):
    name = 'tbcbank'
    start_urls = ['https://www.tbcbank.ge/web/en/web/guest/tbc-news-new']

    def parse(self, response):
        links = response.xpath('//div[@class="offerbox"]/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//title/text()').get()
        if title:
            title = title.strip()

        content = response.xpath('//td[@class="left-part"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
