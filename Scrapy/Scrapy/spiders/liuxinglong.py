# -*- coding: utf-8 -*-
import scrapy


class LiuxinglongSpider(scrapy.Spider):
    name = "liuxinglong"
    #allowed_domains = ["liuxinglong.top"]
    start_urls = ['http://www.liuxinglong.top/','http://xiaozhao.liuxinglong.top','https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=12306&oq=%2526lt%253Bannot%2520create%2520a%2520spider%2520with%2520the%2520same%2520name%2520as%2520your%2520project&rsv_pq=8172466d0001d966&rsv_t=a20bo4yTs3a6kaKW2PnNfmtArb09haDtVVtoXWPbH5MMVNeRqGf61rx9XRY&rqlang=cn&rsv_enter=1&inputT=833&rsv_sug3=3&rsv_sug1=1&rsv_sug7=100&bs=Cannot%20create%20a%20spider%20with%20the%20same%20name%20as%20your%20project']

    def parse(self, response):
        for sel in response.xpath('//a/@href').extract():
            print(sel)        
