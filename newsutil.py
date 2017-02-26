import requests
import re
import os
from bs4.element import *
from threading import Thread
class pageCleaner():
    def getHtml(self,_,url):
        self._html=requests.get(url).content.decode('utf-8')
    def filter(self):
        pass
    def __init__(self,html,**kwargs):
        self._html=html
        #self.baseurl=self.getBaseUrl()
        self._imgfolder='.'
        self._folder='.'
        if 'imgfolder' in kwargs:
            self._imgfolder=kwargs['imgfolder']
        if 'folder' in kwargs:
            self._folder = kwargs['folder']
        pass
    @property
    def html(self):
        return self._html
    @property
    def imgfolder(self):
        return self._imgfolder
    @imgfolder.setter
    def imgfolder(self,imgf='.'):
        if not os.path.exists(imgf):
            os.mkdir(imgf)
        self._imgfolder=imgf
    @property
    def folder(self):
        return self.folder
    @folder.setter
    def folder(self,f='.'):
        if not f:
            self.folder='.'
            return
        if not os.path.exists(f):
            os.mkdir(f)
        self.folder=f
    def getBaseUrl(self,url=''):
        if not url:
            url=self.url
        return url[:url.rfind('\\')]
    def absLink(self,rellink,baseurl=''):
        if not baseurl:
            baseurl=self.baseurl
        if not rellink:
            return ''
        if  rellink.startswith('http') or rellink.startswith(baseurl):
            return rellink
        if baseurl and baseurl[-1]=='\\':
            baseurl=baseurl[0:-1]
        if rellink.startswith('.\\'):
            return baseurl+rellink[1:]
        if rellink.startswith('..\\'):
            return baseurl[0:baseurl.rfind('\\')]+rellink[2:]
    def getImgLink(self,html=''):
        if not html:
            html=self.html
        p = re.compile('<img .*src=[\'"](.*?\.(png|jpg|gif))[\'"].*?>')
        imgs = re.findall(p, html)
        return imgs
    def saveImg(self,src=[],dest=[]):
        if src:
            s=requests.get(src)
        try:
            with open(dest,'wb') as f:
                for c in s.iter_content(chunk_size=1024):
                    if c:
                        f.write(c)
                        f.flush()


        except Exception as e:
            print(e)
            return False
        return True
    #from functools import reduce
    def replaceImage(self):
        imgs=self.getImgLink()
        for img,ext in imgs:
            src=img
            filename=img[img.rfind('/')+1:]
            dest=self.imgfolder+'/'+filename
            self.saveImg(src,dest)
            self._html=self.rplLink(src,dest,self.html)
        return self._html

    def rplLink(self,sub,rpl,rawstr):

        rawstr=rawstr.replace(sub,rpl)
        return rawstr



class page():
    def getHtml(self,_,url):
        self._html=requests.get(url).content.decode('utf-8')
    def filter(self):
        pass
    def __init__(self,url,**kwargs):
        self.url=url
        self.baseurl=self.getBaseUrl()
        global t
        t=Thread(target=self.getHtml,args=(None,url))
        t.start()
        t.join()
        #self.folder=''
        #self.imgfolder=''
        if 'imgfolder' in kwargs:
            self.imgfolder=kwargs['imgfolder']
        if 'folder' in kwargs:
            self.folder = kwargs['folder']
        pass
    @property
    def html(self):
        global t
        if not t.is_alive():
            return self._html
    @property
    def imgfolder(self):
        return self.imgfolder
    @imgfolder.setter
    def imgfolder(self,imgf='.'):
        if not os.path.exists(imgf):
            os.mkdir(imgf)
        self.imgfolder=imgf
    @property
    def folder(self):
        return self.folder
    @folder.setter
    def folder(self,f='.'):
        if not f:
            self.folder='.'
            return
        if not os.path.exists(f):
            os.mkdir(f)
        self.folder=f
    def getBaseUrl(self,url=''):
        if not url:
            url=self.url
        return url[:url.rfind('\\')]
    def absLink(self,rellink,baseurl=''):
        if not baseurl:
            baseurl=self.baseurl
        if not rellink:
            return ''
        if  rellink.startswith('http') or rellink.startswith(baseurl):
            return rellink
        if baseurl and baseurl[-1]=='\\':
            baseurl=baseurl[0:-1]
        if rellink.startswith('.\\'):
            return baseurl+rellink[1:]
        if rellink.startswith('..\\'):
            return baseurl[0:baseurl.rfind('\\')]+rellink[2:]
    def getImgLink(self,html=''):
        if not html:
            html=self.html
        p = re.compile('<img .*src=[\'"](.*?\.(png|jpg|))[\'"].*?>')[0]
        imgs = re.findall(p, html)
        return imgs
    def saveImg(self,src=[],dest=[]):
        if not src:
            s=requests.get(src)
        try:
            with open(dest,'wb') as f:
                f.write(s)
                f.flush()
        except Exception as e:
            print(e)
            return False
        return True
    #from functools import reduce
    def rplLink(self,sub,rpl,rawstr):
        for s,r in zip(sub,rpl):
            rawstr=rawstr.replace(s,r)
        return rawstr

import time
from bs4 import BeautifulSoup
class rule():
    DEL=0
    KEEP=1
    def __init__(self,root):
        self.root=root
        self.eles=[]

    def findEles(self, tag, root=None, *args, **kwargs):
        if not root:
            root=self.root
        args = args if args else []
        kwargs = kwargs if kwargs else {}
        #print(root)
        return root.find_all(tag,*args,**kwargs)
    def unwrap(self,tag,root=None,*args,**kwargs):
        eles = self.findEles(tag, root, *args, **kwargs)
        if eles:
            for e in eles:
                e.unwrap()
        return root
    @property
    def elements(self):
        return self.eles
    def keep(self,tag,*args,**kwargs):

        eles=self.findEles(tag,self.root,  *args, **kwargs)
        for ele in eles:
            self.eles.append(ele)
        return eles
    def delete(self,tag,root=None,*args,**kwargs):
        if isinstance(root,ResultSet):
            for r in root:
                self.delete(tag,r,*args,**kwargs)
            return root

        eles=self.findEles(tag, root, *args, **kwargs)
        if eles:
            for e in eles:
                e.decompose()
        return root
class filter():
    pass
class ruleParser():
    def __init__(self):
        pass

class FenghuangNet(page):
    def __init__(self,url='http://tech.ifeng.com/listpage/800/0/1/rtlist.shtml'):
        super().__init__(url)
    def filter(self):
        '''
        定义网页过滤的原则，将网页中不属于正文的部分过滤掉
        :return:
        '''
        while not self.html:
            time.sleep(0.1)
        #print(self.html)
        bs=BeautifulSoup(self.html,'lxml')
        bs2 = BeautifulSoup(self.html, 'lxml')
        r=rule(bs2)
        meta=bs.find_all('meta',{'charset':re.compile('.*?')})[0]
        #print(meta)
        meta2=r.findEles('meta',**{'charset':re.compile('.*?')})[0]
        #print(meta2)
        css=bs.find_all('link',rel='stylesheet')
        css2 = r.findEles('link', rel='stylesheet')
        #print(css)
        #print(css2)
        h1=bs.find_all('h1')[0]
        h2=bs.find('div',id="artical_sth")
        div=bs.find_all('div',class_='js_selection_area')[0]
        rt=r.findEles('div',class_='js_selection_area')[0]
        print('div==rt : %s'%(str(div)==str(rt)))
        shares=div.find_all('a',class_='bds_tsina js_content_share_btn')
        for s in shares:
            s.decompose()
        r.delete('a',root=rt,class_='bds_tsina js_content_share_btn')
        print('after delete div==rt : %s' % (str(div) == str(rt)))
        iframes=div.find_all('iframe')
        for ifr in iframes:
            ifr.decompose()
        style=bs.find_all('style')
        with open('123.html','wt',encoding='utf-8') as f:
            f.write(str(meta))
            f.write('\n')
            for c in css:
                f.write(str(c))
                f.write('\n')
            for c in style:
                f.write(str(c))
                f.write('\n')
            f.write(str(h1))
            f.write('\n')
            f.write(str(h2))
            f.write('\n')
            f.write(str(div))
            f.write('\n')
            f.flush()
        return div