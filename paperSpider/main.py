# -*- coding: utf-8 -*-
# @Time     : 2020-02-18 15:52
# @Author   : beking
from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(["scrapy", "crawl", "baidu"])
