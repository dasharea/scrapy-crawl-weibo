 # -*- coding: utf-8 -*-
import scrapy
import re
import urllib.request
from weibocrawl.items import WeibocrawlItem
from scrapy.http import Request

class LjSpider(scrapy.Spider):
    name = 'lj'
    allowed_domains = ['hexun.com']
    uid="14755969"
    def start_requests(self):
        yield Request("http://"+str(self.uid)+".blog.hexun.com/p1/default.html",headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"})
    def parse(self, response):
        item=WeibocrawlItem()
        item["name"]=response.xpath("//span[@class='ArticleTitleText']/a/text()").extract()
        item["url"]=response.xpath("//span[@class='ArticleTitleText']/a/@href").extract()
        pat1='<script type="text/javascript" src="(http://click.tool.hexun.com/.*?)">'  #存储评论数量的正则表达式

        hcurl=re.compile(pat1).findall(str(response.body))[0]
        headers2=("User-Agent","Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36")
        opener=urllib.request.build_opener()
        opener.addheaders=[headers2]
        urllib.request.install_opener(opener)
        data=urllib.request.urlopen(hcurl).read()
        click="click\d*?','(\d*?)'"
        comment="comment\d*?','(\d*?)'"
        item['hits']=re.compile(click).findall(str(data))
        item['comment']=re.compile(comment).findall(str(data))
        yield item
        page="blog.hexun.com/p(.*?)/"    #提取列表页总页数
        data2=re.compile(page).findall(str(response.body))
        if(len(data2)>=2):
            totalurl=data[-2]
        else:
            totalurl=1
        print("the total pages:"+str(totalurl))
        for i in range(2,int(totalurl)+1):
            nexturl="http://"+str(self.uid)+".blog.hexun.com/p"+str(i)+"/default.html"
            yield Request(nexturl,callback=self.parse,headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"})