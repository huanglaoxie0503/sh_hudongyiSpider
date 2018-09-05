# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import pymysql
import logging
from scrapy.exporters import JsonItemExporter

from .settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME, MYSQL_TABLE


class HudongyiShCodePipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    """同步的方式将数据保存到数据库：方法一"""

    def __init__(self):
        self.conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWORD,
            db=MYSQL_DBNAME,
            charset="utf8",
            use_unicode=True,
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            insert_sql = """
                              insert into {0}(questionId,questioner,shortName,stockCode,questionContent,replyContent,questionTime,replyTime,last_time)
                              VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                              ON DUPLICATE KEY UPDATE questionId=VALUES(questionId),questioner=VALUES (questioner),shortName=VALUES (shortName),
                              stockCode=VALUES (stockCode),questionContent=VALUES (questionContent),replyContent=VALUES (replyContent),
                              questionTime=VALUES (questionTime),replyTime=VALUES (replyTime),last_time=VALUES (last_time)
                              """.format(
                MYSQL_TABLE
            )

            parms = (
                item["questionId"],
                item["questioner"],
                item["shortName"],
                item["stockCode"],
                item["questionContent"],
                item["replyContent"],
                item["questionTime"],
                item["replyTime"],
                item["db_write_time"],
            )
            self.cursor.execute(insert_sql, parms)
            self.conn.commit()
            logging.info("----------------insert success-----------")
        except pymysql.Error as e:
            print(e)
            logging.info("----------------insert faild-----------")

    def close_spider(self, spider):
        try:
            self.conn.close()
            logging.info("----------------mysql close-----------")
        except Exception as e:
            print(e)
