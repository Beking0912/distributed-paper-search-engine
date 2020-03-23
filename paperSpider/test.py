# -*- coding: utf-8 -*-
# @Time     : 2020-03-23 12:18
# @Author   : beking

import redis
redis_cli = redis.StrictRedis()
redis_cli.incr("baidu_count")
