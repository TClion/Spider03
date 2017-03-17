"""微博热搜爬虫，抓取热搜榜上新闻的标题，链接和热度"""
from selenium import webdriver
import time


def GetInfo():
    url = "http://s.weibo.com/top/summary?cate=homepage"    #热搜榜主页
    Url = []
    Star = []
    Title = []
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(5)
    href = browser.find_elements_by_xpath('//a[@target="_blank"]')
    for i in href:
        Href = i.get_attribute('href')
        t = i.text
        if 'Refer=top' in Href:
            Title.append(t)
            Url.append(Href)
    hot = browser.find_elements_by_xpath('//p[@class="star_num"]/span')
    for i in hot:
        Star.append(i.text)
    info = list(zip(Title,Url,Star))    #标题，链接和热度
    print(len(info))
    for i in info:
        print(i)
    browser.close()


if __name__ =='__main__':
    GetInfo()
