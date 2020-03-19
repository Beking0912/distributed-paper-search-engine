# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PaperspiderItem(scrapy.Item):
    paper_title = scrapy.Field()  # 论文题目
    paper_writer = scrapy.Field()  # 作者
    paper_time = scrapy.Field()  # 发表年代
    paper_cite_count = scrapy.Field()  # 被引用量
    paper_source = scrapy.Field()  # 来源
    paper_abstract = scrapy.Field()  # 摘要
    paper_keywords = scrapy.Field()  # 关键词
    paper_DOI = scrapy.Field()  # DOI
    paper_download_link = scrapy.Field()  # 下载地址
