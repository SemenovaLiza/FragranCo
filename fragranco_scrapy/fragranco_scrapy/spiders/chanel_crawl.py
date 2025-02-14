import scrapy


class ChanelCrawlSpider(scrapy.Spider):
    name = "chanel_crawl"
    allowed_domains = ["chanel.com"]
    start_urls = ["https://chanel.com"]

    def parse(self, response):
        pass
