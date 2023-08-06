#coding=utf-8
from uiautomator import device as d
import chardet
import json

headers = {"Accept":"text/html:application/xhtml+xml, */*",
           "Accept-Language": "zh-CN",
           "Accept-Encoding": "gzip, deflate",
           "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
           }

print d.request.post("http://www.youtaocc.com/",headers=headers)

