# -*- coding: utf-8 -*-
import scrapy

# This is for cooking blog search
# directory = 'output/'


class FsblogSpider(scrapy.Spider):
    name = 'fsblog'
    # OFF Line
    # start_urls = ['file:///' +
    #               'home/azam/py3projects/feedspot/' + directory + 'cooking.html']
    # Online
    start_urls = ['https://blog.feedspot.com/home_cooking_blogs/']

    def parse(self, response):
        divs = response.css('div#fsb p.trow')
        for node in divs[0:]:
            location = node.css('span.location::text').extract_first()
            urls = node.css('a.ext::attr(href)').extract_first()

            yield {
                "locations": location,
                "urls": urls,
            }
