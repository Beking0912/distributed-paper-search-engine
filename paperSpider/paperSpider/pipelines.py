# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
from scrapy.exporters import JsonItemExporter
import MySQLdb


class PaperspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', '123456', 'paper_spider_data', charset='utf8',
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into paper_info(paper_title,paper_writer,paper_time,paper_cite_count,paper_source,paper_abstract,paper_keywords,paper_DOI,paper_download_link)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = list()
        params.append(item.get('paper_title', ''))
        params.append(item.get('paper_writer', ''))
        params.append(item.get('paper_time', ''))
        params.append(item.get('paper_cite_count', ''))
        params.append(item.get('paper_source', ''))
        params.append(item.get('paper_abstract', ''))
        params.append(item.get('paper_keywords', ''))
        params.append(item.get('paper_DOI', ''))
        params.append(item.get('paper_download_link', ''))
        self.cursor.execute(insert_sql, tuple(params))
        self.conn.commit()

        return item


class JsonExporterPipeline(object):
    def __init__(self):
        self.file = open('paper_export.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def spider_closed(self):
        self.exporter.finish_exporting()
        self.file.close()
