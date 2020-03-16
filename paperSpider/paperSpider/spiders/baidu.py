# -*- coding: utf-8 -*-
import re
from urllib import parse

import scrapy
from scrapy import Request


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['xueshu.baidu.com']
    start_urls = [
        'http://xueshu.baidu.com/s?wd=machine+learning&rsv_bp=0&tn=SE_baiduxueshu_c1gjeupa&rsv_spt=3&ie=utf-8&f=8&rsv_sug2=1&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D']

    def parse(self, response):
        paper_nodes = response.xpath('//*[@class="sc_content"]')
        for paper_node in paper_nodes:
            paper_url = paper_node.css('h3 a::attr(href)').extract_first('')

            paper_title = paper_node.css('h3 a::text').extract()
            paper_title_em = paper_node.css('h3 a em::text').extract()
            keyword = ' '.join([str(i) for i in paper_title_em])
            for x in paper_title:
                if x == ' ':
                    paper_title[paper_title.index(x)] = keyword
            paper_title = ''.join([str(i) for i in paper_title])

            paper_writer = paper_node.css('.sc_info span:first-child a::text').extract()
            cite_count = paper_node.css('.sc_cite_cont::text').extract_first(0)
            re.sub(r'\s+', '', cite_count)
            cite_count = str(cite_count).strip()

            paper_allversion = paper_node.css('.sc_allversion .v_item_span .v_source::text').extract()
            for i in range(0, len(paper_allversion)):
                re.sub(r'\s+', '', paper_allversion[i])
                paper_allversion[i] = str(paper_allversion[i]).strip()

            paper_abstract = paper_node.css('.c_abstract::text').extract_first('')
            paper_abstract = str(paper_abstract).strip()

            paper_time = paper_node.css('.sc_time::text').extract_first('暂无')
            re.sub(r'\s+', '', paper_time)
            paper_time = str(paper_time).strip()

            self.log('*************************')
            self.log('*************************')
            self.log('*************************')
            self.log('url: %s' % paper_url)
            self.log('论文题目: %s' % paper_title)
            self.log('论文作者: %s' % paper_writer)
            self.log('发表年代: %s' % paper_time)
            self.log('被引用量: %s' % cite_count)
            self.log('论文来源: %s' % paper_allversion)
            self.log('论文简介: %s' % paper_abstract)

            yield Request(url=parse.urljoin(response.url, paper_url), meta={'front_paper_url': paper_url},
                          callback=self.parse_detail)

        next_url = response.css('#page a::last-child::attr(href)').extract_first('')
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        abstract = response.css('.abstract::text').extract_first('')

        keywords = response.css('.kw_wr .kw_main span a::text').extract()

        DOI = response.css('.doi_wr .kw_main::text').extract_first('')
        re.sub(r'\s+', '', DOI)
        DOI = str(DOI).strip()

        # paper_source = response.css('#allversion_wr .dl_item_span a::attr(href)').extract()
        download_link = response.css('#savelink_wr .dl_item_span a::attr(href)').extract()

        self.log('摘要: %s' % abstract)
        self.log('关键词: %s' % keywords)
        self.log('DOI: %s' % DOI)
        self.log('下载地址: %s' % download_link)
        # self.log('论文来源: %s' % paper_source)
