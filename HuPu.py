"""虎扑论坛步行街热贴抓取，包括回复量，亮个数，浏览量和热评"""
import requests
from lxml import etree
import re

header = {
    ':authority':'bbs.hupu.com',
    ':method':'GET',
    ':path':'',
    ':scheme':'https',
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'accept-encoding':'gzip, deflate, sdch, br',
    'accept-language':'zh-CN,zh;q=0.8',
    'cache-control':'max-age=0',
    'upgrade-insecure-requests':'1',
    'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

class Spider():
    def __init__(self):
        self.indexurl = "https://bbs.hupu.com/all-gambia"
        self.originurl = "https://bbs.hupu.com"
        self.S = requests.session()

    #获取每个热帖的url
    def GetUrlList(self):
        content = self.S.get(self.indexurl,headers=header).content
        page = etree.HTML(content)
        UrlTail = page.xpath('//span[@class="textSpan"]/a/@href')
        self.UrlList = [self.originurl + u for u in UrlTail]

    #获取热帖信息
    def GetInfo(self,url):
        Text = self.S.get(url,headers=header).content
        page = etree.HTML(Text)
        title = page.xpath('//div[@class="bbs-hd-h1"]/h1/text()')[0]    #热帖标题
        view = page.xpath('//span[@class="browse"]/text()')[0]          #回复数，亮个数，浏览量
        content = page.xpath('//table[@class="case"]/tr/td/div[2]')[0]
        info = content.xpath('string(.)')
        info = info.replace('\n','').replace(' ','').strip()                #发帖人发的内容
        number = re.compile(r'/(\d*)亮')                                     #亮个数
        numbers = number.findall(view)[0]
        n = int(numbers)+10
        light = page.xpath('//table[@class="case"]/tr/td/text()')[3:n]
        L = [x.replace('\r\n\r\n','') for x in light if x!='\r\n\r\n']      #亮回复
        print('标题：'+title)
        print('链接：'+url)
        print('关注度：'+view)
        print(len(L))
        print('发帖人：'+info)
        print('热门回复:',end='')
        print(L)



if __name__ =='__main__':
    HuPu = Spider()
    HuPu.GetUrlList()
    for i in HuPu.UrlList:
        HuPu.GetInfo(i)