#-*- coding: UTF-8 -*-
import json

data = []
with open('data_information.json') as f:
    for line in f:
        data.append(json.loads(line), "utf-8")

#print json.dumps(data, ensure_ascii=False)

str = "\r\n"
for item in data:
    #print json.dumps(item)
    str = str + "insert into cnki(title,author,institution,abstract,keyword,downloadFreq,quoteFreq) values "
    str = str + "('%s','%s','%s','%s','%s','%s,%s');\r\n" % (item['title'],item['author'],item['institution'],item['abstract'],item['keyWord'],item['downloadFreq'],item['quoteFreq'])

import codecs
file_object = codecs.open('cnki.sql', 'w' ,"utf-8")
file_object.write(str)
file_object.close()
print "success"
