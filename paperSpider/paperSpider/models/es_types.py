# -*- coding: utf-8 -*-
# @Time     : 2020-03-22 13:35
# @Author   : beking

from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, Completion, Keyword, Text, Integer
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=["localhost"])


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])


class PaperType(DocType):
    suggest = Completion(analyzer=ik_analyzer)  # 用于自动补全

    paper_title = Text(analyzer="ik_max_word")
    paper_writer = Keyword()
    paper_time = Integer()
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
