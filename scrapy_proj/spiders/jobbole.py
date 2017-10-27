# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
import urlparse

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['http://blog.jobbole.com/']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_nodes = response.xpath("//div[@id='archive']/div[@class='post floated-thumb']/div[@class='post-thumb']/a")
        for post_node in post_nodes:
            front_image_url = post_node.xpath('img/@src').extract_first("")
            post_url = post_node.xpath('@href').extract_first("")
            yield Request(url=urlparse.urljoin(response.url, post_url), meta={"front_image_url":front_image_url} , callback=self.parse_detail, dont_filter=True)

        next_page = urlparse.urljoin(response.url,response.xpath('//a[contains(@class,"next")]/@href').extract_first())
        if next_page:
            yield Request(url=urlparse.urljoin(response.url, next_page), callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        title = response.xpath('//h1/text()').extract_first()
        create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first().strip()[:10]
        prase_num = int(response.xpath('//h10/text()').extract_first())
        fav_num = response.xpath('//div[@class="post-adds"]/span[2]/text()').extract_first()
        re_fav_num = re.match(r'.*?(\d+).*',fav_num)
        if re_fav_num:
            fav_num = re_fav_num.group(1)
        else:
            fav_num = 0
        print title, prase_num, fav_num
