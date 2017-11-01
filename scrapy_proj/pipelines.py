# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import MySQLdb


class ScrapyProjPipeline(object):
    def process_item(self, item, spider):
        return item

class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for k, v in results:
            image_path = v["path"]
        item["front_image_path"] = image_path
        return item

class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect("localhost","root","","jobbole",charset='utf-8',use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = "INSERT INTO jobbole "
        self.cursor.execute()