import time
import zxing
from socket import*
from email.mime.text import MIMEText
from random import*
import smtplib
import requests
import json
from cefpython3 import cefpython as cef
import platform
import sys
import urllib.request ,re,os
import time
from re import*
import requests
from urllib.request import*
import json
def getversion():
    return "0.0.5"
def cleardevice():
    print("\033[2J")
    print("\033[99999999999999999999999999999999A", end='')
def baidubaike(text):
    html=urllib.request.urlopen("http://gop.asunc.cn/baike.html").read().decode("utf-8")
    url=html+urllib.parse.quote(text)
    html=urllib.request.urlopen(url).read().decode("utf-8")
    par = '(<meta name="description" content=")(.*?)(">)'
    try:
        data = re.search(par,html).group(2)
        return data
    except:
        return -1
def translate(string):
    data = {'doctype': 'json','type': 'AUTO','i':string}
    url = "http://fanyi.youdao.com/translate"
    r = requests.get(url,params=data)
    result = r.json()
    result = result['translateResult'][0][0]["tgt"]
    return result
def getweather(province,city):
    tf=0
    data = {'doctype': 'json','type': 'AUTO','i':province}
    url = "http://fanyi.youdao.com/translate"
    r = requests.get(url,params=data)
    result = r.json()
    province = result['translateResult'][0][0]["tgt"]
    data = {'doctype': 'json','type': 'AUTO','i':city}
    url = "http://fanyi.youdao.com/translate"
    r = requests.get(url,params=data)
    result = r.json()
    city = result['translateResult'][0][0]["tgt"]
    try:
        wurl="https://tianqi.moji.com/weather/china/{}/{}".format(province,city)
        html = urllib.request.urlopen(wurl).read().decode("utf-8")
    except:
        return -1
        tf=1
    try:
        par = '(<meta name="description" content=")(.*?)(">)'
        data = re.search(par,html).group(2)
        data = data.replace(",","，").replace("。","，").replace("墨迹天气建议您","爱搜天气助手建议您")
    except:
        return -1
        tf=1
    if tf!=1:
        return data
def get_news():
    now = time.strftime("%Y-%m-%d", time.localtime())
    print(now,"最新新闻资讯,转载于人民日报。\n")
    now = time.strftime("%Y%m%d", time.localtime())
    now1 = time.strftime("%Y-%m/%d", time.localtime())
    print("今日新闻资讯:")
    for i in range(1,10):
        try:
            url="http://paper.people.com.cn/rmrb/html/"+now1+"/nw.D110000renmrb_"+now+"_3-0"+str(i)+".htm"
            html=urlopen(url).read().decode("utf-8")
            html=html.replace("<br>","")
            html=html.replace("&nbsp;","")
            html=html.replace("<P>","")
            html=html.replace("</P>","")
            a1=html.index("<title>")+len("<title>")
            b1=html.index("</title>")
            a=html.index("<!--enpcontent-->")+19
            b=html.index("<!--/enpcontent-->")
            print(i,".",end="")
            while a1<b1:
                print(html[a1],end="")
                a1+=1
            print("\n")
        except:
            last=i-1
            break
    try:
        number=int(input("您需要的看点:"))
    except:
        return -1
    if number>last or number<1:
        return -1
    url="http://paper.people.com.cn/rmrb/html/"+now1+"/nw.D110000renmrb_"+now+"_3-0"+str(number)+".htm"
    html=urlopen(url).read().decode("utf-8")
    html=html.replace("<P>","")
    html=html.replace("</P>","")
    html=html.replace("<br>","")
    html=html.replace("&nbsp;","")
    a1=html.index("<title>")+len("<title>")
    b1=html.index("</title>")
    a=html.index("<!--enpcontent-->")+19
    b=html.index("<!--/enpcontent-->")
    print("标题:")
    while a1<b1:
        print(html[a1],end="")
        a1+=1
    print("\033[33m")
    while a1<b1:
        print(html[a1],end="")
        a1+=1
    print("\033[0m")
    print("\n内容:")
    print("\033[44m",end="  ")
    while a<b:
        print(html[a],end="")
        a+=1
    print("\033[0m")

def check_browser_versions():
    ver = cef.GetVersion()
    print("[hello_world.py] CEF Python {ver}".format(ver=ver["version"]))
    print("[hello_world.py] Chromium {ver}".format(ver=ver["chrome_version"]))
    print("[hello_world.py] CEF {ver}".format(ver=ver["cef_version"]))
    print("[hello_world.py] Python {ver} {arch}".format(
           ver=platform.python_version(),
           arch=platform.architecture()[0]))
    assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"
def searchweb(text,title):
    try:
        html = urllib.request.urlopen(text).read().decode("utf-8")
        sys.excepthook = cef.ExceptHook
        cef.Initialize()
        cef.CreateBrowserSync(url=text,window_title=title)
        cef.MessageLoop()
    except:
        return -1
def get_imformation(pid):
    try:
        url="http://code.xueersi.com/api/compilers/"+str(pid)+"?id="+str(pid)
        headers = {'Content-Type':'application/json'}
        a=requests.get(url=url, headers=headers)
        null,false,list_get,string=0,0,[],''
        p=json.loads(a.text)
        likes=p["data"]["likes"]
        unlikes=p["data"]["unlikes"]
        return likes,unlikes,p["data"]["username"],p["data"]["user_id"]
    except:
        return -1
