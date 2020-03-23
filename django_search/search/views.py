import json
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from elasticsearch import Elasticsearch

from search.models import PaperType

client = Elasticsearch(hosts=["127.0.0.1"])


class SearchSuggest(View):
    def get(self, request):
        key_words = request.GET.get('s', '')
        re_datas = []
        if key_words:
            s = PaperType.search()
            s = s.suggest('suggest', key_words, completion={
                "field": "suggest", "fuzzy": {
                    "fuzziness": 2  # 编辑距离
                }, "size": 10
            })
            suggestions = s.execute_suggest()
            for match in suggestions.suggest[0].options:
                source = match._source
                re_datas.append(source["paper_title"])
        return HttpResponse(json.dumps(re_datas), content_type="application/json")


class SearchView(View):
    def get(self, request):
        key_words = request.GET.get('q', '')
        page = request.GET.get("q", "1")
        try:
            page = int(page)
        except:
            page = 1

        start_time = datetime.now()
        response = client.search(
            index="baidu",
            body={
                "query": {
                    "multi_match": {
                        "query": key_words,
                        "fields": ["paper_title", "paper_keywords", "paper_abstract"]
                    }
                },
                "from": (page-1)*10,
                "size": 10,
                "highlight": {
                    "pre_tags": ['<span class="keyWord">'],
                    "post_tags": ['</span>'],
                    "fields": {
                        "paper_title": {},
                        "paper_abstract": {}
                    }
                }
            }
        )

        end_time = datetime.now()
        last_seconds = (end_time - start_time).total_seconds()

        total_nums = response["hits"]["total"]
        if(page % 10) > 0:
            page_nums = int(total_nums/10+1)
        else:
            page_nums = int(total_nums / 10)

        hit_list = []
        for hit in response["hits"]["hits"]:
            hit_dict = {}
            if "highlight" in hit:
                if "paper_title" in hit["highlight"]:
                    hit_dict["paper_title"] = "".join(hit["highlight"]["paper_title"])
                else:
                    hit_dict["paper_title"] = hit["_source"]["paper_title"]

                if "paper_abstract" in hit["highlight"]:
                    hit_dict["paper_abstract"] = "".join(hit["highlight"]["paper_abstract"])[:500]
                else:
                    hit_dict["paper_abstract"] = hit["_source"]["paper_abstract"][:500]

            hit_dict["paper_writer"] = hit["_source"]["paper_writer"]
            hit_dict["paper_time"] = hit["_source"]["paper_time"]
            hit_dict["paper_cite_count"] = hit["_source"]["paper_cite_count"]
            hit_dict["paper_source"] = hit["_source"]["paper_source"]
            # hit_dict["paper_keywords"] = hit["_source"]["paper_keywords"]
            hit_dict["paper_DOI"] = hit["_source"]["paper_DOI"]
            # hit_dict["paper_download_link"] = hit["_source"]["paper_download_link"]
            hit_dict["score"] = hit["_score"]

            hit_list.append(hit_dict)

        return render(request, "result.html", {"page": page,
                                               "all_hits": hit_list,
                                               "key_words": key_words,
                                               "total_nums": total_nums,
                                               "page_nums": page_nums,
                                               "last_seconds": last_seconds})

