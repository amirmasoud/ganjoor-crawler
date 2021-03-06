# -*- coding: utf-8 -*-
import scrapy

class RumiFiheMafiSpider(scrapy.Spider):
    name = "fihe_mafi"
    allowed_domains = ["ganjoor.net"]
    start_urls = ['https://ganjoor.net/moulavi/fhmfh/sh0']
    order = 1

    def parse(self, response):
        index = 0
        sh = {}
        sh['type'] = 'mix'
        sh['text'] = {}
        for i, poem in enumerate(response.css('div.poem>article>div')):
            if poem.css('p:first-child::text').extract_first() is None:
                continue
            if index == 0:
                sh['title'] = response.css('div.poem>article>h2>a::text').extract_first()
                sh['order'] = self.order
                self.order = self.order + 1
            if poem.css("div.b"):
                sh['text'][index] = {
                    'm1': poem.css('div.m1>p::text').extract_first(),
                    'm2': poem.css('div.m2>p::text').extract_first(),
                }
            else:
                sh['text'][index] = {
                    'p': poem.css('p:first-child::text').extract_first(),
                }
            index = index + 1
        yield sh
        next_page = response.css('div.navigation>div.navleft>a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
