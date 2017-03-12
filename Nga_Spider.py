"""多线程抓取Nga论坛网事杂谈区的帖子，利用代理ip，线程池等技术，需要制作cookie"""
import requests
from lxml import etree
import time
import random
from multiprocessing.dummy import Pool
import re
import json


NgaHeader = {
    'Host':'bbs.ngacn.cc',
    'Referer':'http://bbs.ngacn.cc',
    'Upgrade-Insecure-Requests':'1',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2970.0 Safari/537.36'
}

Cookie = "CNZZDATA1256638887=387034225-1473526614-http%253A%252F%252Fbbs.ngacn.cc%252F%7C1474861498; CNZZDATA1256638943=416101362-1485108725-http%253A%252F%252Fbbs.ngacn.cc%252F%7C1485260168; CNZZDATA1256638851=877720674-1473296994-%7C1485615639; CNZZDATA1256638874=2101736710-1480823144-http%253A%252F%252Fbbs.ngacn.cc%252F%7C1485658319; CNZZDATA1256638919=1762027141-1473042225-%7C1485718200; CNZZDATA1259004010=1371435890-1472957561-http%253A%252F%252Fbbs.ngacn.cc%252F%7C1486658928; CNZZDATA1256638858=645675298-1474022976-null%7C1486692276; ngaPassportUid=guest0589d4a4f5e70b; CNZZDATA1256638869=1833171124-1473452654-http%253A%252F%252Fbbs.ngacn.cc%252F%7C1486701580; CNZZDATA1256638828=749395385-1484571587-http%253A%252F%252Fbbs.ngacn.cc%252F%7C1486702182; guestJs=1486706114; __utmt=1; CNZZDATA30043604=cnzz_eid%3D51638811-1472957993-null%26ntime%3D1486701499; CNZZDATA30039253=cnzz_eid%3D250465023-1472954100-null%26ntime%3D1486705059; CNZZDATA1256638820=1897381269-1479529542-http%253A%252F%252Fbbs.ngacn.cc%252F%7C1486701594; __utma=240585808.1651564605.1472958692.1486697206.1486703198.511; __utmc=240585808; __utmz=240585808.1486703198.511.468.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; lastvisit=1486706144; lastpath=/thread.php?fid=-7&rand=444; bbsmisccookies=%7B%22insad_refreshid%22%3A%7B0%3A%22/6441a76143caa6bc5904540be25d%22%2C1%3A1487302005%7D%2C%22pv_count_for_insad%22%3A%7B0%3A-192%2C1%3A1486746090%7D%2C%22insad_views%22%3A%7B0%3A2%2C1%3A1486746090%7D%7D; __utmb=240585808.34.10.1486703198"


class Spider():

    def __init__(self):
        self.OriginUrl = "https://bbs.nga.cn/thread.php?fid=-7" #网事杂谈区url
        self.HeadUrl = "https://bbs.nga.cn"
        self.S = requests.session()
        self.IpList = []
        self.UrlList = []

    #制作cookie
    def Getcookie(self):
        self.cookie = {}
        for line in Cookie.split(';'):
            key,value = line.split('=',1)
            self.cookie[key] = value
        Time = int(time.time())
        self.cookie[' lastvisit'] = str(Time)        #必须提交的cookie值，最后浏览的时间
        self.cookie[' guestJs'] = str(Time-20)

    #从ip.txt中获取ip列表
    def GetIpList(self):
        f = open('ip.txt','r')
        lines = f.readlines()
        for i in lines:
            p = json.loads(i.replace('\'','\"'))
            self.IpList.append(p)
        f.close()

    #获取网事杂谈区每个主题和链接，默认是1页
    def GetUrl(self,page=1):
        for i in range(1,page+1):
            pro = random.choice(self.IpList)
            Url = '%s&page=%d' %(self.OriginUrl,i)
            content = self.S.get(Url,headers=NgaHeader,proxies=pro,cookies=self.cookie).content
            page = etree.HTML(content)
            title = page.xpath("//a[@class='topic']/text()")
            href = page.xpath("//a[@class='topic']/@href")
            Href = [self.HeadUrl+u for u in href]
            self.UrlList += list(zip(title,Href))

    #获取每个主题论坛水友发表的回复
    def Getinfo(self,T,Url):
        number = 2
        pro = random.choice(self.IpList)
        Text = self.S.get(Url,headers=NgaHeader,cookies=self.cookie,proxies=pro).content
        try:
            content = Text.decode('gbk')
        except:
            return
        if '下一页' in content:                #如果不止一页，继续抓取
            pagenumber = re.compile(r'\',1:(.?),')
            number = int(pagenumber.findall(content)[0])+1       #一共有多少页
        print(T)
        for i in range(1,number):
            u = Url+'&page='+str(i)
            print('第%d页的评论' % i)
            pro = random.choice(self.IpList)
            try:
                Content = self.S.get(u,headers=NgaHeader,cookies=self.cookie,proxies=pro).content
                Page = etree.HTML(Content)
                t = Page.xpath("//span[@class='postcontent ubbcode']/text()")
                print(t)
            except Exception as f:
                print(f)



if __name__ == '__main__':
    Nga = Spider()
    Nga.Getcookie()
    Nga.GetIpList()
    Nga.GetUrl()
    pool = Pool(processes=1)    #设置线程池
    for T,url in Nga.UrlList:
        pool.apply_async(Nga.Getinfo,(T,url))
    pool.close()
    pool.join()