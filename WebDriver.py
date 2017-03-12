"""模拟登录豆瓣，知乎，百度和新浪微博，使用selenium库基于Chrome浏览器,使用时请填写自己对应的帐号密码"""
from selenium import webdriver
import time
import requests

#知乎header
zhihuheader = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Host':'www.zhihu.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}


class Login():
    def __init__(self):
        self.S = requests.session()

    #储存cookie，登录直接用cookie登录
    def GetCookie(self,cookie):
        c = {}
        for item in cookie:
            c[item["name"]] = item["value"]
        return c

    #豆瓣登录
    def DouBan(self):
        loginurl = "https://www.douban.com/accounts/login"
        indexurl = "https://www.douban.com/"
        browser = webdriver.Chrome()
        browser.get(loginurl)
        time.sleep(1)
        browser.find_element_by_xpath('//input[@id="email"]').send_keys("doubanusername")
        browser.find_element_by_xpath('//input[@id="password"]').send_keys("password")
        browser.find_element_by_xpath('//input[@type="submit"]').click()
        time.sleep(1)
        cookie = browser.get_cookies()
        browser.close()
        Cookie = self.GetCookie(cookie)
        r = self.S.get(indexurl,cookies=Cookie)
        print(r.text)

    #百度帐号登录
    def BaiDu(self):
        browser = webdriver.Chrome()
        url = "http://i.baidu.com/welcome/"
        browser.get(url)
        time.sleep(1)
        browser.find_element_by_xpath('//a[@class="ibx-header-login ibx-login-btn"]').click()
        browser.find_element_by_xpath('//input[@id="TANGRAM__PSP_8__userName"]').send_keys("baiduusername")
        browser.find_element_by_xpath('//input[@id="TANGRAM__PSP_8__password"]').send_keys("password")
        browser.find_element_by_xpath('//input[@id="TANGRAM__PSP_8__submit"]').click()
        time.sleep(1)
        cookie = browser.get_cookies()
        Cookie = self.GetCookie(cookie)
        browser.close()
        r = self.S.get(url,cookies=Cookie)
        print(r.text)

    #知乎用户登录
    def ZhiHu(self):
        loginurl = "https://www.zhihu.com/#signin"
        indexurl = "https://www.zhihu.com/"
        browser = webdriver.Chrome()
        browser.get(loginurl)
        time.sleep(1)
        browser.find_element_by_xpath('//input[@name="account"]').send_keys("zhihuusername")
        browser.find_element_by_xpath('//input[@name="password"]').send_keys("password")
        browser.find_element_by_xpath('//button[@class="sign-button submit"]').click()
        time.sleep(1)
        cookie = browser.get_cookies()
        browser.close()
        Cookie = self.GetCookie(cookie)
        print(Cookie)
        r = self.S.get(indexurl,headers=zhihuheader,cookies=Cookie)
        print(r.text)

    #微博登录
    def WeiBo(self):
        loginurl = "http://weibo.com/"
        browser = webdriver.Chrome()
        browser.get(loginurl)
        time.sleep(1)
        browser.find_element_by_xpath('//input[@id="loginname"]').send_keys('weibousername')
        browser.find_element_by_xpath('//input[@name="password"]').send_keys('password')
        browser.find_element_by_xpath('//span[@node-type="submitStates"]').click()
        time.sleep(1)
        cookie = browser.get_cookies()
        browser.close()
        Cookie = self.GetCookie(cookie)
        r = self.S.get(loginurl,cookies=Cookie)
        print(r.text)

    #使用phantomJs无浏览器登录
    def douban(self):
        loginurl = "https://www.douban.com/accounts/login"
        indexurl = "https://www.douban.com/"
        browser = webdriver.PhantomJS()
        browser.get(loginurl)
        browser.find_element_by_xpath('//input[@id="email"]').send_keys("doubanusername")
        browser.find_element_by_xpath('//input[@id="password"]').send_keys("password")
        browser.find_element_by_xpath('//input[@type="submit"]').click()
        cookie = browser.get_cookies()
        browser.close()
        Cookie = self.GetCookie(cookie)
        r = self.S.get(indexurl,cookies=Cookie)
        print(r.text)


if __name__ == '__main__':
    login = Login()
    login.douban()