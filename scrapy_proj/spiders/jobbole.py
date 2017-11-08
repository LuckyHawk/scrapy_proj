# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
import urlparse
from scrapy_proj.items import JobBoleArticleItem
from scrapy_proj.utils.common import get_md5
import datetime
from scrapy.loader import ItemLoader

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
        article_item = JobBoleArticleItem()

        front_image_url = response.meta.get("front_image_url","")
        title = response.xpath('//h1/text()').extract_first()
        create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first().strip()[:10]

        praise_nums = response.xpath('//h10/text()').extract_first()
        if praise_nums is None:
            praise_nums = 0
        else:
            praise_nums = int(praise_nums)
        fav_nums = response.xpath('//div[@class="post-adds"]/span[2]/text()').extract_first()
        re_fav_num = re.match(r'.*?(\d+).*',fav_nums)
        if re_fav_num:
            fav_nums = int(re_fav_num.group(1))
        else:
            fav_nums = 0

        comment_nums = response.xpath('//div[@class="post-adds"]/a/span/text()').extract_first()
        re_comments_nums = re.match(r'.*?(\d+).*', comment_nums)
        if re_comments_nums:
            comment_nums = int(re_comments_nums.group(1))
        else:
            comment_nums = 0

        content = response.xpath('//div[@class="entry"]').extract_first()
        tags = ','.join(response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract())

        try:
            create_date = datetime.datetime.strptime(create_date,"%Y/%m/%d").date()
        except Exception as e:
            create_date = datetime.datetime.now().date()

        article_item["front_image_url"] = [front_image_url]
        article_item["title"] = title
        article_item["create_date"] = create_date
        article_item["praise_nums"] = praise_nums
        article_item["fav_nums"] = fav_nums
        article_item["comment_nums"] = comment_nums
        article_item["content"] = content
        article_item["tags"] = tags
        article_item["url"] = response.url
        article_item["url_object_id"] = get_md5(response.url)

        #通过ItemLoader加载item
        item_loader = ItemLoader(item = JobBoleArticleItem(), response = response)
        item_loader.add_xpath("title", '//h1/text()')
        item_loader.add_xpath("create_date",'//p[@class="entry-meta-hide-on-mobile"]/text()')
        item_loader.add_xpath("praise_nums",'//h10/text()')
        item_loader.add_xpath("fav_nums",'//div[@class="post-adds"]/span[2]/text()')
        item_loader.add_xpath("comment_nums",'//div[@class="post-adds"]/a/span/text()')
        item_loader.add_xpath("content",'//div[@class="entry"]')
        item_loader.add_xpath("tags",'//p[@class="entry-meta-hide-on-mobile"]/a/text()')
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_value("front_image_url",[front_image_url])

        article_item = item_loader.load_item()

        yield article_item