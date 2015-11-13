#!/usr/bin/env python
# coding: utf-8

"""
各个型号的路由器登陆模块
"""
import urllib2

class model:

    def __init__(self):
        pass

    @staticmethod
    def TL_WR740N(self, auth, pin, pwd): # dial process for TP_Link
        con_url = '''http://192.168.1.1/userRpm/PPPoECfgRpm.htm?
&wan=0&wantype=2&VnetPap=201&linktype=4&waittime=&Connect=%%C1%%AC+%%BD%%D3
&acc=%s&psw=%s'''.replace('\n','') # Dial url

        discon_url='''http://192.168.1.1/userRpm/PPPoECfgRpm.htm?
wan=0&wantype=2&acc=%s&psw=%s&confirm=%s&specialDial=100&SecType=0&
sta_ip=0.0.0.0&sta_mask=0.0.0.0&linktype=4&waittime2=0
&Disconnect=%%B6%%CF+%%CF%%DF'''.replace('\n','') # Disconnect Url

        auth = auth.encode("base64")[0:-1]
        dial_url = con_url % (pin, pwd)
        dis_url = discon_url % ("admin", "pass", "pass")


        print dis_url

        # At first stop the auto dial function
        dis_req = urllib2.Request(url = dis_url, headers = {'Authorization': 'Basic ' + auth})
        dis_res = urllib2.urlopen(dis_req, timeout=200)
        dis_res.close()

        print dial_url
        # Then dial
        dial_req = urllib2.Request(url = dial_url, headers = {'Authorization': 'Basic ' + auth})  # 用户名和密码
        dial_res = urllib2.urlopen(dial_req, timeout=200)
        dial_res.close()

