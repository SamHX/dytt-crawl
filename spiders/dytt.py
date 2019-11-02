# -*- coding: utf-8 -*-
import scrapy
from items import DyttMoviesItem

class DyttSpider(scrapy.Spider):
    name = 'dytt'
    allowed_domains = ['www.dytt8.net']
    start_urls = ['https://www.dytt8.net/html/gndy/dyzz/index.html']

    def parse(self, response):

        movie_list = response.xpath("//div[@class='co_content8']/ul//table")
        for m_list in movie_list:
            item = DyttMoviesItem()
            item['movie_name'] = m_list.xpath(".//b/a/text()").extract_first()
            item['movie_date'] = m_list.xpath(".//tr[3]/td[2]/font/text()").extract_first()
            item['movie_url'] = "https://www.dytt8.net" + m_list.xpath(".//b/a/@href").extract_first()
            yield item
            next_page = response.xpath("//div[@class='x']//a")
            if next_page:
                for np in next_page:
                    if np.xpath("./text()").extract_first() == "下一页":
                        next_link = np.xpath("./@href").extract()
                        print(next_link)
                        yield scrapy.Request("https://www.dytt8.net/html/gndy/dyzz/" + next_link[0],callback=self.parse)


