# -*- coding: utf-8 -*-
# @Time     : 2020-03-21 13:37
# @Author   : beking

import redis
import json

rd = redis.Redis("127.0.0.1", decode_responses=True)
rd.lpush('baidu:start_urls',
         'http://xueshu.baidu.com/s?wd=machine+learning&rsv_bp=0&tn=SE_baiduxueshu_c1gjeupa&rsv_spt=3&ie=utf-8&f=8&rsv_sug2=1&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D')

urls = [('', 3, 'parse_detail'), ('', 4, 'parse_detail')]

for url in urls:
    rd.rpush("baidu:new_urls", json.dumps(url))
