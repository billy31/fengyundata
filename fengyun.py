# coding:utf-8
# author: Darj Lin
import requests, os, datetime, glob, json
from dateutil import tz
from bs4 import BeautifulSoup as bs4
from matplotlib.pyplot import plot as plt
import numpy as np
import http.client
from PIL import Image
from io import BytesIO
http.client._MAXHEADERS = 1000


class fengyun():
    def __init__(self, name=None, passwd=None, outdir=os.path.join(os.getcwd(),
                                                         '/gencodes/')):
        self.mainUrl = 'http://satellite.nsmc.org.cn/Portalsite/'
        self.__index = 'Default.aspx'
        self.__login = 'WebServ/CommonService.asmx/Login'
        self.__code = 'Common/GenCodeImg.aspx'
        self.__info = 'sup/user/ShowUserInfo.aspx'
        self.__headers = {
            'Host': 'satellite.nsmc.org.cn',
            'Proxy-Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,und;q=0.6,hmn;q=0.5,bs;q=0.4',
        }
        self.__gencodeImage = None
        self.__timezone = tz.gettz('Asia/Shanghai')
        self.__session = requests.session()
        self.__shopcart = 'Data/ShoppingCart.aspx'
        self.name = name
        self.passwd = passwd
        self.outdir = outdir
            
    def showonterminal(self, img):
        fill, flag = ' ', '*'
        gen = np.array(img)
        xline = ''
        for x in range(4, gen.shape[0]-4):
            for y in range(gen.shape[1]):
                xline += fill if gen[x, y] > 127 else flag
            print(xline, end='\n')
            xline = ''            

    def getcodeid(self, url):
        currtime = datetime.datetime.now(tz=self.__timezone).strftime('%a %d %b %Y %H:%M:%S GMT+0800 (中国标准时间)')
        with open(os.getcwd() + 'log.txt', 'w') as f:
            f.write('{}'.format(datetime.datetime.now(tz=self.__timezone).strftime('%a %d %b %Y %H:%M:%S')))
        urlx = url + '?data=' + currtime
        try:
            response = self.__session.get(urlx, headers=self.__headers)
            if response.status_code == 200:
                try:
                    image = Image.open(BytesIO(response.content))
                    self.showonterminal(image)
                except:
                    print('Error in open gencode')
        except:
            print('Error in establish connection')
        else:
            code = input('code \n>')
            print(code)
            return code        
        
    def setHeaders(self, addKey, addValues):
        self.__headers[addKey.__str__()] = addValues.__str__()
        
    def login(self, maxTry=3):
        statuscode = 404
        trytimes = 0
        while(statuscode != 200 and trytimes < maxTry):
            print('Now is the {} time\'s try'.format(trytimes + 1))
            code = self.getcodeid(self.mainUrl + self.__code)
            if code == 'q':
                print('Quit!')
                trytimes = 99
            else:
                payload = {}
                payload['userName'] = self.name
                payload['userPwd'] = self.passwd
                payload['isSave'] = 'false'
                payload['veriCode'] = code
                response = self.__session.post(self.mainUrl + self.__login,
                                               headers = self.__headers,                                               
                                               json = payload)
                statuscode = response.status_code
                if(statuscode == 200):
                    print('Succeed in logging in')
                trytimes += 1
        if(statuscode != 200 and trytimes < maxTry):
            print('Max tries and still fails!')        
        
    def saveSession(self):
        return self.__session
    
    def printInfo(self):
        # autologin
        with open(os.getcwd() + 'log.txt', 'r') as f:
            lastw = f.readlines()
        lastlog = datetime.datetime.strptime(lastw[0], '%a %d %b %Y %H:%M:%S')
        deltatime = datetime.datetime.now() - lastlog        
        if self.__session.cookies.items() == [] or deltatime.seconds >= 1800:
            self.login()        
        print('Last log time: {}\nNow is: {}'.format(lastw[0],
                                                     datetime.datetime.now().strftime('%a %d %b %Y %H:%M:%S')))
        language = input('language(type in index): [1]ZH-CN [2]EN-US \n')
        language_str = ''  if language is '1' else '?currentculture=en-US'        
        url = self.mainUrl + self.__info + language_str
        response = self.__session.get(url, headers=self.__headers)
        soup = bs4(response.content, 'lxml')
        items = soup.find_all('div', class_='grxxnrtext1')
        values = soup.find_all('div', class_='grxxnrtext2')
        for i, v in zip(items, values):
            print('{:20s} {}'.format(i.text.strip(), v.text.strip()))

    
'''
#code = 'http://satellite.nsmc.org.cn/Portalsite/Common/GenCodeImg.aspx'
fy = fengyun('username', 'passwd')
fy.login()
sess = fy.saveSession()
print('Finished')
'''
#print('Finished at {}'.format(req))

