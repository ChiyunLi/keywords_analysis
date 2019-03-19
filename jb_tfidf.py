#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 04:12:53 2018

@author: rikigei
"""

import jieba
import jieba.analyse

import numpy
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.pyplot import gca
from matplotlib.font_manager import FontProperties

article = open("push.txt", "r").read()

'''
切詞
'''
### 精準切詞 ###
seglist = []
sl = jieba.cut(article, cut_all = False)
for sl1 in sl:
    if len(sl1) > 1 and sl1 != '\n':
        seglist.append(sl1)

#加入停用詞        
seglist_df = pd.DataFrame({'seglist':seglist})
stopwords = pd.read_csv('stopwords.txt',index_col=False,quoting=3,sep='，',names=['stopword'],encoding="utf-8",engine='python')
seglist_df = seglist_df[~seglist_df.seglist.isin(stopwords.stopword)]

#計數
seglist_stat = seglist＿df.groupby(by=['seglist'])['seglist'].agg({"count":numpy.size})
seglist_stat = seglist_stat.reset_index().sort_values(by=["count"],ascending=False)
seglist_stat1 = seglist_stat.head(150)

#輸出至Excel
df = pd.DataFrame(seglist_stat1)
df.to_excel('seglist_push.xls')
######


'''
抓取關鍵字
'''
### TF-IDF ###
#加入停用詞
jieba.analyse.set_stop_words('stopwords.txt')

#提取關鍵字
ti = jieba.analyse.extract_tags(article, topK=200, withWeight=True, allowPOS=())
ti1 = str(ti)

with open("tfidf2018_6_200.txt","a") as f:
    for i in ti1:
        f.write(i)


### TextRank(補充) ###
#加入停用詞        
jieba.analyse.set_stop_words('stopwords.txt')

#提取關鍵字
tr = jieba.analyse.textrank(article, topK=200, withWeight=True)
tr1 = str(tr)

with open("TextRank2018_6_200.txt","a") as f:
    for i in tr1:
        f.write(i)
######

'''
文字雲
'''
words_frequence = {x[0]:x[1] for x in seglist_stat.values}  #將dataframe轉成dict

font = r"/anaconda3/lib/fonts/simhei.ttf"  #繁體字庫路徑
wordcloud = WordCloud(font_path=font)
wordcloud.fit_words(words_frequence)
plt.figure(figsize=(14,14))
plt.imshow(wordcloud)

fig = plt.gcf()
fig.set_size_inches(16.5, 10.5)
fig.savefig('push_wordcloud2.png', dpi=300) # 存檔且設定解析度
plt.show()


'''
詞頻統計圖
'''
import xlrd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import gca
from matplotlib.font_manager import FontProperties

myfont=FontProperties(fname=r'/anaconda3/lib/fonts/simhei.ttf',size=14) #設定字型絕對路徑
plt.rcParams['font.family']='sans-serif' #用來正常顯示中文標籤
plt.rcParams['axes.unicode_minus']=False #用來正常顯示負號

### seaborn ###
x = ['小孩','媽媽','老公','寶寶','醫生','婆婆','保母','尿布','女兒','工作']
y = [876,510,327,293,224,223,152,150,148,136]
sns.barplot(x,y)

a = gca()
a.set_xticklabels(a.get_xticklabels(), fontProperties= myfont)
a.set_yticklabels(a.get_yticks(), fontProperties= myfont)
plt.show()


### matplotlib ###
book = xlrd.open_workbook('seglist_content.xls') #open_workbook: 打開文件
sh = book.sheet_by_index(0) #sheet_by_index(0): 獲取第一個工作表
sh.nrows #查看總列數
alldata=[] #開啟新列表

for row in range(1,sh.nrows):
    dic = {}
    dic['keywords'] = sh.cell_value(rowx=row,colx=1)
    dic['frequency'] = sh.cell_value(rowx=row,colx=2)
    alldata.append(dic)  #將字典加入列表中

alldata_df = pd.DataFrame(alldata)  #將列表轉成dataframe
x = alldata_df['keywords']
y = alldata_df['frequency']
index = ['小孩','媽媽','老公','寶寶','醫生','婆婆','保母','尿布','女兒','工作']

plt.bar(x,y)
plt.title('BabyMother',fontproperties = myfont)
plt.xticks(x, index)

a = gca()
a.set_xticklabels(a.get_xticklabels(), fontProperties= myfont)
a.set_yticklabels(a.get_yticks(), fontProperties= myfont)
plt.show()
