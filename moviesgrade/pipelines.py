# -*- coding: utf-8 -*-
'''Pipelines'''
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging

from twisted.enterprise import adbapi







class MySqlPipeline(object):
    """A pipeline to store the item in a MySQL database.
    This implementation uses Twisted's asynchronous database API.
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        '''init connection string'''
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
            cp_reconnect=True)
        dbpool = adbapi.ConnectionPool('pymysql', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):

        query = self.dbpool.runInteraction(self._conditional_insert, item,spider)  # 调用插入的方法
        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item


    def _conditional_insert(self,conn,item,spider):
        item.setdefault('name', None)
        item.setdefault('movieDate', None)
        item.setdefault('Grade', None)
        item.setdefault('gradePeople', None)
        item.setdefault('five', None)
        item.setdefault('four', None)
        item.setdefault('three', None)
        item.setdefault('two', None)
        item.setdefault('one', None)
        item.setdefault('good', None)
        item.setdefault('bad', None)
        item.setdefault('music', None)
        item.setdefault('story', None)
        item.setdefault('director', None)
        item.setdefault('frames', None)
        item.setdefault('want', None)
        item.setdefault('piaofang', None)

        conn.execute("""replace into tbl_moviegrade (name,movieDate,Grade,gradePeople,five,four,three,two
                ,one,good,bad,music,story,director,frames,want,piaofang,website,createdtime,crawldate,filmid)
                  values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""",
                     (item['name'], item['movieDate'], item['Grade'], item['gradePeople'],
                      item['five'], item['four'], item['three'], item['two'], item['one'],item["good"]
                      ,item["bad"],item["music"],item["story"],item["director"],item["frames"],item["want"],
                      item["piaofang"],item["comefrom"],item["createdtime"],item["crawldate"],item["filmid"]))

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        logging.error(failure)


