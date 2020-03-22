from django.views.generic.base import View
from django.http import HttpResponse
from search.models import PaperType
import json


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