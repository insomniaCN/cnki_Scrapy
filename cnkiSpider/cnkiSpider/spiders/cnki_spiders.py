# -*- coding:utf-8 -*-
# from getTargetPage import TargetPage

from Tkinter import mainloop
from spiderGUI import SpiderGUI
from scrapy import log
from scrapy.spiders import Spider
from scrapy.selector.unified import Selector
import sys
from cnkiSpider.items import CnkispiderItem
import os


# pages = TargetPage()
# pages.get_target_page()
# print os.getcwd()
#主界面启动
s = SpiderGUI()
mainloop()


class CNKI_Spiders(Spider):
    #设置spider名称
    name = "cnki_on"
    allowed_domains = ["cnki.net"]
    start_urls = []    
    fr = open('linksSet.txt','rb')
    #将链接填入列表中
    for line in fr.readlines():
        lineArr = line.strip()
        start_urls.append(lineArr)
    print start_urls
    #爬取文件的详细信息
    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@class="mainleft"]')
        itemlist= []
        
        for site in sites:
            item = CnkispiderItem()
            
            title = site.xpath('//*[@id="chTitle"]/text()').extract()
            #将相应的值填入到item对应的属性中去
            item['title'] = [t.encode('utf-8') for t in title] 
            author = site.xpath('//*[@id="content"]/div[1]/div[3]/div[2]/p[1]/a/text()').extract()
            if author == None:
                author = site.xpath('//*[@id="content"]/div[1]/div[2]/p[1]/a/text()').extract()
            item['author'] = [a.encode('utf-8') for a in author]
            institution = site.xpath('//*[@id="content"]/div[1]/div[3]/div[2]/p[3]/a/text()').extract()
            item['institution'] = [i.encode('utf-8') for i in institution]
            abstract = site.xpath('//*[@id="ChDivSummary"]/text()').extract()
            item['abstract'] = [a.encode('utf-8') for a in abstract]
            keyWord = site.xpath('//*[@id="ChDivKeyWord"]/a/text()').extract()
            item['keyWord'] = [k.encode('utf-8') for k in keyWord]
            downloadFreq = site.xpath('//*[@id="content"]/div[1]/div[5]/ul/li/text()').re(u'\s*【下载频次】(.*)')
            item['downloadFreq'] = [d.encode('utf-8') for d in downloadFreq]
            quoteFreq = site.xpath('//*[@id="rc3"]/text()').re('\W(\d+)\W')
            item['quoteFreq'] = [q.encode('utf-8') for q in quoteFreq]
            
            itemlist.append(item)
            
            #加入日志记录，级别为info
            log.msg("Appending item...", level=log.INFO)
        #生成日志
        log.msg("Append done.", level=log.INFO)
        return itemlist



# if __name__ == "__main__":
#     sys.path.append('F:\Pythonworkspace\cnkiSpider_master\cnkiSpider\cnkiSpider')
#     cnki = CNKI_Spiders()
# #     print os.getcwd()
#     print cnki
#         