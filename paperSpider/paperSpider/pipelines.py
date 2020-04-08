# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# import codecs
# from scrapy.exporters import JsonItemExporter
import redis
from paperSpider.models.es_types import PaperType

from elasticsearch_dsl.connections import connections

es = connections.create_connection(PaperType._doc_type.using)

redis_cli = redis.StrictRedis()

# import MySQLdb


def gen_suggests(index, info_tuple):
    # 根据字符串生成搜索建议数组
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            # 调用 es 的 analyze 接口分析字符串
            words = es.indices.analyze(index=index, analyzer="ik_smart", params={'filter': ["lowercase"]}, body=text)
            analyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
            new_words = analyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input": list(new_words), "weight": weight})
            used_words = used_words.union(new_words)

    return suggests


class PaperspiderPipeline(object):
    def process_item(self, item, spider):
        return item


# class MysqlPipeline(object):
#     def __init__(self):
#         self.conn = MySQLdb.connect('127.0.0.1', 'root', '123456', 'paper_spider_data', charset='utf8',
#                                     use_unicode=True)
#         self.cursor = self.conn.cursor()
#
#     def process_item(self, item, spider):
#         insert_sql = """
#             insert into paper_info(paper_title,paper_writer,paper_time,paper_cite_count,paper_source,paper_abstract,paper_keywords,paper_DOI,paper_download_link)
#             values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         params = list()
#         params.append(item.get('paper_title', ''))
#         params.append(item.get('paper_writer', ''))
#         params.append(item.get('paper_time', ''))
#         params.append(item.get('paper_cite_count', ''))
#         params.append(item.get('paper_source', ''))
#         params.append(item.get('paper_abstract', ''))
#         params.append(item.get('paper_keywords', ''))
#         params.append(item.get('paper_DOI', ''))
#         params.append(item.get('paper_download_link', ''))
#         self.cursor.execute(insert_sql, tuple(params))
#         self.conn.commit()
#
#         return item
#
#
# class JsonExporterPipeline(object):
#     def __init__(self):
#         self.file = open('paper_export.json', 'wb')
#         self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
#         self.exporter.start_exporting()
#
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item
#
#     def spider_closed(self):
#         self.exporter.finish_exporting()
#         self.file.close()


class ElasticsearchPipeline(object):
    def process_item(self, item, spider):
        # 将 item 转化为 es 的数据
        paper = PaperType()
        paper.paper_title = item['paper_title']
        paper.paper_writer = item['paper_writer']
        paper.paper_abstract = item['paper_abstract']
        paper.paper_keywords = item['paper_keywords']
        paper.paper_DOI = item['paper_DOI']
        paper.paper_time = item['paper_time']
        paper.paper_cite_count = item['paper_cite_count']
        paper.paper_source = item['paper_source']
        paper.paper_download_link = item['paper_download_link']
        paper.meta.id = item['paper_source']

        paper.suggest = gen_suggests(PaperType._doc_type.index,
                                     ((paper.paper_title, 10), (paper.paper_keywords, 5), (paper.paper_abstract, 2)))

        paper.save()
        redis_cli.incr("baidu_count")

        return item
