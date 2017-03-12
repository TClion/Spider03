"""顺风物流网实时抓取爬虫，抓取物流信息"""
import requests
import time
from lxml import etree
import pymysql

header = {
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Host':'w.sfzxwlw.com',
    'Origin':'http://w.sfzxwlw.com',
    'Referer':'http://w.sfzxwlw.com/',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36',
    'X-MicrosoftAjax':'Delta=true',
    'X-Requested-With':'XMLHttpRequest'
}

Str = "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"

#将username，password，phone，yourname填写成注册时的用户名，密码，手机和姓名
data= {
    'ScriptManager1':'UpdatePanel7|Timer2',
    'txtUserName':'username',
    'txtUserpass':'password',
    'txtCode':'',
    'Text22':'username',
    'Text21':'username',
    'xxlxyz':'1',
    'DrpInfoType':'货源',
    'vali_days':'3天',
    'd1':'货物数量',
    'd2':'吨',
    'd4':'车辆数量',
    'd5':'车长',
    'd8':'吨',
    'c1':'车辆数量',
    'c4':'货物数量',
    'c5':'吨',
    'rel2':'yourname',
    'userid2':'username',
    'tel2':'phone',
    'cfsj':'10',
    '__EVENTTARGET':'Timer2',
    '__VIEWSTATE':Str,
    '__PREVIOUSPAGE':'kNP4_TFCVxH96YYxOhWhfTlj87y9cJHv4hlfhp4ZQGasrtvWwG4o3vaAtzB0HxuP8PzcOY7WPmjlqx5mS5GjTm54QfOgPd35oVgr6c1miSs1',
    '__EVENTVALIDATION':'/wEWKgL4vPCtAgLjx7G7DgLRl8KzBwKfsM/xCQLnoqrRBQK1/ebABgLq65jvBQL/0/StCQL569w/AtyXwrMHAtLCmdMIAqXVsrMJAquUkZICAsKE/MMNAoGT4Z8LAt2DvusMAvOUobAKAvaUobAKAvWUobAKAviUobAKAveUobAKAvqUobAKAvmUobAKAuyUobAKAuuUobAKAvOU4bAKAvOU3bAKAvOU6bAKAvOU5bAKAvOU8bAKAvaU6bAKAvaU3bAKArf+uiMC6uukzgQC89PgmgwCy+/q7wwC08HVHALSwtXkAgLsz8KCDgKT3o20AwLqz8KCDgLSxundDtQGM1I25NAOE2VpaUy0Lx2+P9i434E5qXTGclgYsgfv',
    '__ASYNCPOST':'true'
}


class Spider():

    def __init__(self):
        self.Url = "http://w.sfzxwlw.com/"      #抓取的网页url
        self.ImgUrl = "http://w.sfzxwlw.com/CheckCode.aspx" #验证码url
        self.S = requests.session()
        self.db = pymysql.connect('localhost','root','databasepwd','table',charset='utf8') #连接数据库
        self.cursor = self.db.cursor()
        self.db.autocommit(True)
        self.oldlist = []   #  去重

    #登录
    def Login(self):
        if data['txtCode'] == '':
            img = self.S.get(self.ImgUrl,stream=True)
            with open ('顺风验证码.jpg','wb') as f:
                for chunk in img.iter_content(1024):
                    if chunk:
                        f.write(chunk)
            captcha = input('请输入验证码:')
            data['txtCode'] = captcha
        r = self.S.post(self.Url,headers=header,data=data)

    #获取信息
    def getInfo(self):
        while(True):
            text = self.S.post(self.Url,headers=header,data=data).text
            page = etree.HTML(text)
            From = page.xpath('//td[@style="width: 100%; height: 30px"]/font[2]/text()')
            To = page.xpath('//td[@style="width: 100%; height: 30px"]/font[5]/text()')
            Info = page.xpath('//td[@style="width: 100%; height: 30px"]/font[6]/text()')
            Phone = page.xpath('//font[@style="line-height: 20px; font-size: 15px; color:red"]/text()')
            Date = page.xpath('//td[@style="width: 100%; height: 30px"]/font[9]/text()')
            F = [x.replace('\r\n','').strip() for x in From]
            T = [x.replace('\r\n','').strip() for x in To]
            I = [x.replace('\r\n','').strip() for x in Info]
            P = [x.replace('\r\n','').strip() for x in Phone]
            D = [x.replace('\r\n','').strip() for x in Date]
            L = list(set(list(zip(F,T,I,P,D))))
            for i in L:
                if i not in self.oldlist:
                    print(i)
                    #self.savemysql(i)
            self.oldlist = self.oldlist+L
            if len(self.oldlist)>200:       #简单的去重
                self.oldlist = []
            time.sleep(10)


    #存库
    def savemysql(self,L):
        sql1 = """create table if not exists %s (
                  fromplace char(20) not null,
                  inf char(200) not null,
                  phone char(100) not null,
                  updatetime char(100) not null
)""" % L[0]
        sql2 = """insert into %s values""" % L[0]
        sql2 += """ (%s,%s,%s,%s)"""
        try:
            self.cursor.execute(sql1)
            self.cursor.execute(sql2,L)
        except Exception as e:
            print(e)
            self.db.rollback()



if __name__ == '__main__':
    shunfeng = Spider()
    shunfeng.Login()
    shunfeng.getInfo()