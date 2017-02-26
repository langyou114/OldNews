from OldNews.OldNews.newsutil import rule
from bs4 import BeautifulSoup
import requests
from threading import Thread
import time
import re
class therule():
    def downurl(self,url):
        c=requests.get(url).content
        self._html=c
    def __init__(self,url):
        self.t=Thread(target=self.downurl,args=(url,))
        self.t.start()
    @property
    def html(self):
        while self.t.is_alive():
            time.sleep(0.1)
        return self._html

    def getNews(self):
        bs = BeautifulSoup(self.html, 'lxml')
        r = rule(bs)
        return r.eles
        pass
class SinaTechRule(therule):
    def downurl(self,url):
        c=requests.get(url).content
        self._html=c
        #print(c)
    def __init__(self,url):
        if not re.search('tech.sina.com.cn',url):
            raise ValueError('%s 不是有效的新浪科技新闻网址'%url)
        self.t=Thread(target=self.downurl,args=(url,))
        self.t.start()
    @property
    def html(self):
        while self.t.is_alive():
            time.sleep(0.1)
        return self._html
    def getNews(self):
        bs=BeautifulSoup(self.html,'lxml')
        r=rule(bs)
        r.keep('meta',**{'content':re.compile('.*charset')})
        r.keep('h1',**{'id':'main_title'})
        maincontent=r.keep('div',**{'id':'artibody'})
        r.delete('ins',root=maincontent[0])
        r.delete('div',root=maincontent,**{'id':re.compile('ad')})
        r.unwrap('a',root=maincontent[0],**{'class':'wt_article_link'})
        r.unwrap('span',root=maincontent[0],**{'id':re.compile('.*stock')})
        r.unwrap('a', root=maincontent[0], **{'class': re.compile('keyword')})
        eles=r.eles
        html=''
        for e in eles:
            html+=str(e)+'\n'
        return html

