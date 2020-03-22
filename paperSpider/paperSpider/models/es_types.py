# -*- coding: utf-8 -*-
# @Time     : 2020-03-22 13:35
# @Author   : beking

from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, Completion, Keyword, Text, Integer
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=["localhost"])


class PaperType(DocType):
    paper_title = Text(analyzer="ik_max_word")
    paper_writer = Text()
    paper_time = Text()
    paper_cite_count = Integer()
    paper_source = Keyword()
    paper_abstract = Text(analyzer="ik_max_word")
    paper_keywords = Text(analyzer="ik_max_word")
    paper_DOI = Text()
    paper_download_link = Text()

    class Meta:
        index = "baidu"
        doc_type = "paper"


if __name__ == "__main__":
    PaperType.init()
