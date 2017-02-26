from OldNews.OldNews import newsutil as nl
from bs4 import BeautifulSoup
import re
import requests
from OldNews.OldNews.rules import SinaTechRule as sinatech
news=sinatech('http://tech.sina.com.cn/i/2017-02-21/doc-ifyarzzv3523689.shtml').getNews()
from OldNews.OldNews.newsutil import pageCleaner as pc
p=pc(news,**{'imgfolder':'imgs'})
h=open('aas.html','wt',encoding='utf-8')
h.write(p.replaceImage())

