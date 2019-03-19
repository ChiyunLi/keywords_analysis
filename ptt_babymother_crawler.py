#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 18:22:32 2018

@author: rikigei
"""

'''
爬爆文（標題,內文,推文）
'''
import requests 
from bs4 import BeautifulSoup
import re
import pandas as pd

rows=[['title','content','push']] 

for i in range(7515,7505,-1): #2018下半年頁數：7515-6865
    url = 'https://www.ptt.cc/bbs/BabyMother/index'+str(i)+'.html'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    list1 = soup.find_all('div',re.compile('title'))
    
    try:
        for ii in list1:
            if len(ii)!=1:
                print(ii.a['href'])  #先抓到所有超連結
                    
                #然後是一篇文章的
                pre_url = 'https://www.ptt.cc'+str(ii.a['href'])
                resp = requests.get(pre_url,verify=False)  
                soup = BeautifulSoup(resp.text,'html.parser')    
                 
                #推文（大於一百才抓）
                listc = soup.find_all('span',re.compile('f3 push-content'))                               
                if len(listc) >= 100:
                    for iii in listc:
                        listc1 = iii.text
                        listc1
                                       
                    #標題1
                    lista = soup.find_all('div',re.compile('article-metaline'))
                    a = lista[2].find_all('span',re.compile('article-meta-value'))
                    a[0].text

                    #內文
                    listb = soup.find('div',re.compile('bbs-screen bbs-content'))
                    b = listb.text
                    b1 = b.split('2018')
                    b1[1]
                    b2 = b1[1].split('※ 發信站: 批踢踢實業坊(ptt.cc)')
                    b2[0]
                               
                else:
                    print(None)  
      
        tmp = [a[0].text,
               b2[0],
               listc1]
                    
        rows.append(tmp)
        
    except Exception as err:
        print(err)  
        

df = pd.DataFrame(rows, columns = rows.pop(0))
df.to_csv('001.csv', encoding='utf-8-sig')


'''
資料處理
'''
data = pd.read_excel('001.xls')

data = data.drop_duplicates()  #去重
data.to_excel('0001.xls')

data = pd.read_excel('2018_6.xls')
data.to_csv('2018_6.txt', sep='\t', index=False)


data1 = data['title']  #取title
data1.to_csv('002txt.txt', sep='\t', index=False)

data2 = data['content']  #取content
data2.to_csv('003txt.txt', sep='\t', index=False)

data3 = data['push']  #取push
data3.to_csv('004txt.txt', sep='\t', index=False)




