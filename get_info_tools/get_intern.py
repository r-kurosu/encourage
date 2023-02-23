from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import urllib.request as req
import urllib
import os
import time
from urllib.parse import urljoin
from selenium.common.exceptions import NoSuchElementException
import pandas as pd


browser = webdriver.Chrome()
    
browser.get('https://job.mynavi.jp/24/pc/corpinfo/searchCorpListByGenCond/index/?cond=IS_OP:3/')
#     #ここまでで検索

#     #ここからはデータ取得

sleep(2)

a = [['企業名','コア事業','本社所在','インターン題目','開催地域','開催時期','締め切り','開催期間']]
i=0    
while i<6:
    getData()
    cNext_ = browser.find_element_by_class_name('center.paging.quantity')
    cNexts = cNext_.find_elements_by_tag_name('li')
    try:
        cNexts[i+1].click()
        i+=1
    except:
        break

while True:
    getData()
    cNext_ = browser.find_element_by_class_name('center.paging.quantity')
    cNexts = cNext_.find_elements_by_tag_name('li')
    try:
        try:
            print(cNexts[6].find_element_by_tag_name('span'))
            break
        except NoSuchElementException:
            cNexts[6].click()
            i+=1

    except:
        break

i=7
while i<10:
    getData()
    cNext_ = browser.find_element_by_class_name('center.paging.quantity')
    cNexts = cNext_.find_elements_by_tag_name('li')
    try:
        cNexts[i].click()
        i+=1
    except:
        break

#print(a)
df = pd.DataFrame(a)
df.to_csv(y+'.csv')
