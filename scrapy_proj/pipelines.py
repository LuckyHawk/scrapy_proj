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
        self.conn = MySQLdb.connect("localhost","root","","scrapy",charset='utf8',use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = '''INSERT INTO jobbole(title,create_date,url,url_object_id,
                                    front_image_url,front_image_path,comment_nums,fav_nums,
                                    praise_nums,tags,content)
 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        self.cursor.execute(sql, (item['title'],item['create_date'],item['url']
                                  , item['url_object_id'],item['front_image_url'],item['front_image_path']
                                  , item['comment_nums'],item['fav_nums'],item['praise_nums']
                                  , item['tags'],item['content']))
        self.conn.commit()