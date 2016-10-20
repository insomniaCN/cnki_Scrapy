#!/usr/bin/python
# -*- coding:utf-8 -*-

import os 
from Tkinter import *
from PIL import Image, ImageTk
import time
from selenium import webdriver
from __builtin__ import True
from scrapy.selector import Selector
from selenium.common.exceptions import NoSuchElementException
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class SpiderGUI:
    
    def __init__(self):
        #设置爬虫接入时的网址
        self.start_url = 'http://epub.cnki.net/kns/brief/result.aspx?dbprefix=scdb&action=scdbsearch&db_opt=SCDB'
        #GUI界面设计
        self.top = Tk()
        self.top.title("Spider System v1.0")
        
        self.canvas = Canvas(self.top,
                    width = 500 ,
                    height = 100, 
                    bg = 'white')
        self.image = Image.open(r'F:\Pythonworkspace\cnki_scrapy\cnkiSpider_master\cnkiSpider\spiders\img.jpg')
        self.im = ImageTk.PhotoImage(self.image)
        
        self.canvas.create_image(250,50,
                    image = self.im)
        self.canvas.create_text(250,50,
                    font=(u'楷体', 25, 'bold'), 
                    text = u'知网爬虫系统' + 'v1.0',
                    fill ='red')
        self.canvas.create_text(400,80,
                    font=('Helvetica',10, 'bold'), 
                    text = 'NLP Lab, Soochow University')
        self.canvas.pack()
        
        self.conditfm =Frame()
        self.warn1 = Label(self.conditfm,width= 21,
                font=('Helvetica',8, ), fg='red',
                text = u'输入内容检索条件:')
        self.variable1 = StringVar(self.conditfm)
        self.variable1.set(u"主题")      
        self.w = OptionMenu(self.conditfm, self.variable1,
                 u"主题", u"篇名", u"主题词", u"摘要", u"全文", u"参考文献", u"中图分类号",
               )
        self.w.pack(side=LEFT)
        self.conditext = Entry(self.conditfm,)
        self.warn1.pack(side=TOP)
        self.conditext.pack(side=BOTTOM,)
        self.conditfm.pack(pady=20)
        
        self.sourcefm =Frame()
        self.warn2 = Label(self.sourcefm,width= 21, 
            font=('Helvetica',8, ), fg='red', 
            text = u'输入检索控制条件：')
        self.warn2.pack(side=TOP)
        self.sourcevar = StringVar()
        self.source = Label(self.sourcefm, text = u'论文来源')
        self.sourcetext = Entry(self.sourcefm, textvariable=self.sourcevar)
        self.source.pack(side=LEFT)
        self.sourcetext.pack(side=LEFT)
        self.sourcefm.pack()
        
        self.startfm =Frame()
        self.startvar = StringVar()
        self.startdate = Label(self.startfm, text=u'起始日期')
        self.starttext = Entry(self.startfm, textvariable=self.startvar)
        self.startdate.pack(side=LEFT)
        self.starttext.pack(side=LEFT)
        self.startfm.pack()  
        
        self.endingfm =Frame()
        self.endingvar = StringVar()
        self.endingdate = Label(self.endingfm, text=u'终止日期')
        self.endingtext = Entry(self.endingfm, textvariable=self.endingvar)
        self.endingdate.pack(side=LEFT)
        self.endingtext.pack(side=LEFT)
        self.endingfm.pack()      
        
        self.fundfm =Frame()
        self.fundvar = StringVar()
        self.fundate = Label(self.fundfm, text=u'支持基金')
        self.fundtext = Entry(self.fundfm,textvariable=self.fundvar)
        self.fundate.pack(side=LEFT)
        self.fundtext.pack(side=LEFT)
        self.fundfm.pack()  
        
        self.authorfm =Frame()
        self.authorvar = StringVar()
        self.authordate = Label(self.authorfm, text=u'作      者')
        self.authortext = Entry(self.authorfm, textvariable=self.authorvar)
        self.authordate.pack(side=LEFT)
        self.authortext.pack(side=LEFT)
        self.authorfm.pack()      
        
        self.time1 = ''
        self.clock = Label(self.top, font=('times', 20, 'bold'), bg='gray')
        self.clock.pack(side=RIGHT)
        self.tick()
        
        
        self.funcfm = Frame()
        self.submit = Button(self.funcfm,text=u'链接获取',\
            command=None, \
            activeforeground='white', \
            activebackground='green')
        self.location = Button(self.funcfm,text=u'打开文件位置',\
            command=self.getlocation, \
            activeforeground='white', \
            activebackground='red')
        self.quit = Button(self.funcfm, text=u'内容爬取', \
            command=self.top.quit, \
            activeforeground='white', \
            activebackground='blue')        
        self.submit.pack(side=LEFT,padx = 18)
        self.quit.pack(side=LEFT,padx = 18)
        self.location.pack(side=LEFT, padx = 24)
        self.funcfm.pack(pady = 20)
    
    #显示时间功能函数
    def tick(self):
        # 从运行程序的计算机上面获取当前的系统时间
        time2 = time.strftime('%H:%M:%S')
        # 如果时间发生变化，代码自动更新显示的系统时间
        if time2 != self.time1:
            self.time1 = time2
            self.clock.config(text=time2)
            # calls itself every 200 milliseconds
            # to update the time display as needed
            # could use >200 ms, but display gets jerky
        self.clock.after(200, self.tick)   
    #显示时间功能函数
    def tick(self):
        # 从运行程序的计算机上面获取当前的系统时间
        time2 = time.strftime('%H:%M:%S')
        # 如果时间发生变化，代码自动更新显示的系统时间
        if time2 != self.time1:
            self.time1 = time2
            self.clock.config(text=time2)
            # calls itself every 200 milliseconds
            # to update the time display as needed
            # could use >200 ms, but display gets jerky
        self.clock.after(200, self.tick)   
    
    #获取当前位置    
    def getlocation(self):
        fileposition = os.getcwd()
        #print fileposition
        os.system("explorer.exe %s" % fileposition)
    
    #爬取待获取文献的链接
    def one_search(self, driver, search_formula, pubulished_date_from, pubulished_date_to):
    #         search_formula = u'软件学报'
    #         pubulished_date_from = '2012-1-1'
    #         pubulished_date_to = '2015-1-1'
#         print search_formula
        #模拟浏览器操作，进行填值
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
        #search_formula = raw_input("input the theme you want to search for: ").decode(sys.stdin.encoding)
        #         print search_formula
        print type(self.sourcevar)
        search_formula = self.sourcevar.get()
        print search_formula
        #pubulished_date_from = raw_input("The beginning of time period is: ")
        pubulished_date_from = self.startvar.get()
        pubulished_date_to =  self.endingvar.get()
        print search_formula, pubulished_date_from, pubulished_date_to
        #pubulished_date_to = raw_input("The end of time period is: ")
        driver = webdriver.Firefox()
        driver.get(self.start_url)
        #driver.maximize_window()
        time.sleep(5)
        self.one_search(driver, search_formula, pubulished_date_from, pubulished_date_to )
        driver.close()    
   
# 
# def main():
#     s = SpiderGUI()
#     mainloop()
#         
# if __name__ == '__main__':           
#     main()