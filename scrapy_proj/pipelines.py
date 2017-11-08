# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class ScrapyProjPipeline(object):
    def process_item(self, item, spider):
        return item

class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        image_path = ""
        for k, v in results:
            try:
                image_path = v["path"]
            except:
                pass
        item["front_image_path"] = image_path
        return item

#会使数据库崩溃
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect("localhost","root","123456","scrapy",charset='utf8',use_unicode=True)
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

class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        db_params = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DB"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset = "utf8",
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **db_params)
        return cls(dbpool)

    def process_item(self, item, spider):
        q = self.dbpool.runInteraction(self.do_insert, item)
        q.addErrback(self.handle_error, item, spider) #异常处理

    def handle_error(self, error, item, spider):
        print error

    def do_insert(self, cursor, item):
        sql = '''INSERT INTO jobbole(title,create_date,url,url_object_id,
                                            front_image_url,front_image_path,comment_nums,fav_nums,
                                            praise_nums,tags,content)
         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        cursor.execute(sql, (item['title'], item['create_date'], item['url']
                                  , item['url_object_id'], item['front_image_url'], item['front_image_path']
                                  , item['comment_nums'], item['fav_nums'], item['praise_nums']
                                  , item['tags'], item['content']))

