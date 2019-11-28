# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class MatchItem(scrapy.Item):
    pr = scrapy.Field()
    date = scrapy.Field()
    match = scrapy.Field()
    score = scrapy.Field()
    result = scrapy.Field()


class NCrawler(scrapy.Spider):
    name = 'n'
    allowed_domains = ['nesine.com']
    start_urls = ['https://www.nesine.com/sportoto/mac-sonuclari']

    def parse(self, response):
        options = response.xpath("//select[@name='pNo']/option/@value").extract()
        for option in options:
            yield scrapy.FormRequest.from_response(
                response,
                formxpath="//form[@class='form-inline']",
                formdata={'pNo': option},
                callback=self.fetch
            )

    def fetch(self, response):
        pr = response.xpath("//select[@name='pNo']/option[@selected]/text()").extract_first()
        elements = response.xpath("//table[@class='table table-striped sportoto-results']/tbody/tr")
        for elem in elements:
            table = elem.xpath("td")
            item = MatchItem()
            item["pr"] = pr
            item["date"] = table[2].xpath("text()").extract_first()
            item["match"] = table[3].xpath("text()").extract_first()
            item["score"] = table[4].xpath("text()").extract_first()
            item["result"] = table[5].xpath("text()").extract_first()
            yield item


if __name__ == "__main__":
    s = get_project_settings()
    s['FEED_FORMAT'] = 'csv'
    s['FEED_URI'] = 'matches.csv'
    process = CrawlerProcess(s)
    process.crawl(NCrawler)
    process.start()
