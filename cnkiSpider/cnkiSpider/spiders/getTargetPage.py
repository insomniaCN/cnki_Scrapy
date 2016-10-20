#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
from selenium import webdriver
from __builtin__ import True
import scrapy
from scrapy.selector import Selector
from selenium.common.exceptions import NoSuchElementException
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



class TargetPage:
    start_url = 'http://epub.cnki.net/kns/brief/result.aspx?dbprefix=scdb&action=scdbsearch&db_opt=SCDB'
    #定位到所要爬取链接的位置并保存
    def one_search(self, driver, search_formula, pubulished_date_from, pubulished_date_to):
#         search_formula = u'软件学报'
#         pubulished_date_from = '2012-1-1'
#         pubulished_date_to = '2015-1-1'
        print search_formula
        driver.find_element_by_name('magazine_value1').send_keys(search_formula.decode('utf-8'))
        driver.find_element_by_name('publishdate_from').send_keys(pubulished_date_from)
        driver.find_element_by_name('publishdate_to').send_keys(pubulished_date_to)
        driver.find_element_by_xpath('//*[@id="btnSearch"]').click()
        time.sleep(10)
        flag = True
        page_num = 1
        driver.switch_to_frame('iframeResult')
        fp = open('linksSet.txt','wb+')
        while flag:
            #save href links
            page = driver.page_source
            #print driver.page_source
            hrefs = Selector(text = page).xpath('//a[contains(@class,"fz14")]/@href').extract()
            print hrefs
            while hrefs:
                #print processing_links
                href = hrefs.pop()
                real_href = 'http://www.cnki.net' + href.replace('kns', 'KCMS')
                fp.write(str(real_href) + "\r\n")
                print '----------------------------'
                print hrefs
                if hrefs:
                    continue
                else:
                    try:
                        next_page = driver.find_element_by_xpath('//*[@id="Page_next"]')
                        next_page.click()
                        page_num += 1
                        time.sleep(5)
                        break  
                    except NoSuchElementException:
                        print "last page has reached,total nums of page is %d" % page_num
                        flag = False

    def get_target_page(self):
        print "CNKI spider is starting..."
        search_formula = raw_input("input the theme you want to search for: ").decode(sys.stdin.encoding)
#         print search_formula
        pubulished_date_from = raw_input("The beginning of time period is: ")
        pubulished_date_to = raw_input("The end of time period is: ")
        driver = webdriver.Firefox()
        driver.get(self.start_url)
        #driver.maximize_window()
        time.sleep(5)
        self.one_search(driver, search_formula, pubulished_date_from, pubulished_date_to )
        driver.close()


