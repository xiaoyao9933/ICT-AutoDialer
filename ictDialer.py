#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# Auto login ICT srun3 network. 
# By Lu CHAO(me@chao.lu) ,2015 08 22.

from urllib2 import build_opener,HTTPCookieProcessor
from urllib import urlencode
from cookielib import CookieJar
import time,sys,hashlib,re
from random import random
global loop
global count
loop=True
count=0


def loginICT(user,password):
    index_page = "http://159.226.39.22/index.html"
    global loop,count
    try:
        hasher= hashlib.md5()
        #获得一个cookieJar实例
        cj = CookieJar()
        #cookieJar作为参数，获得一个opener的实例
        opener=build_opener(HTTPCookieProcessor(cj))
        #伪装成一个正常的浏览器，避免有些web服务器拒绝访问。
        opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
        #生成Post数据，含有登陆用户名密码。
        hasher.update(password)
        data = urlencode({"username":user,"password":hasher.hexdigest()[8:24],"drop":0,"type":1,"n":100})
        #以post的方法访问登陆页面，访问之后cookieJar会自定保存cookie
        opener.open(index_page,timeout=20)
        #以带cookie的方式访问页面ss
        op=opener.open("http://159.226.39.22/cgi-bin/do_login",data,timeout=20)
        #读取页面源码
        data = op.read()
        result = re.match("^[\d]+$",data)
        if result is not None:
            print "%s : Login Success, Response:%s"%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), data)
        else:
            print "%s : Failed, Response:%s"%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),data)
        opener.close()
        return
    except Exception,e:
        print str(e)
        return

def testConnection():
    try:
        opener = build_opener()
        op = opener.open("http://www.baidu.com",timeout=20)
        data = op.read()
        if re.search("baidu.com",data) is not None:
            return True
        else:
            return False
            
    except Exception,e:
        print str(e)
        return False
	

if __name__ == '__main__':
    if len(sys.argv)<3:
        print "Usage: %s [username] [password]"%(sys.argv[0])
        exit()
    print "Working....Please view the autologin.log for detailed information."
    file=open("autologin.log",'w')
    sys.stdout=file
    sys.stderr=file
    while loop:
    #在这里更改你的用户名,密码,归属地
        if testConnection() is False:
            print "%s : Connection is down, trying to reconnect..."%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
            loginICT(sys.argv[1],sys.argv[2])
        #count += 1
        if count%100==1:
            print "%s : Test Counting %d"%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),count)
        elif count>10000:
            count=0
        else:
            None    
        file.flush()
        time.sleep(20+int(random()*5))
