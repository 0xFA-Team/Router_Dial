#!/usr/bin/env python
# -*- coding: utf-8 -*-
__Url__ = 'Http://www.purpleroc.com'
__author__ = 'Tracy_梓朋'

"""
This script is for people who want to dial with router under the limit of Netkeeper environment.
"""

import time,hashlib,struct,sys,urllib2,json
from Crypto.Cipher import AES
from Crypto.Cipher import DES3


des = DES3.new('1234ZHEJIANGXINLIWANGLEI',2,'12345678')
aes = AES.new('xlzjhrprotocol3x',1)

g_u = 'username@cqupt' # Username for PPPOE
g_p = 'password' # Password for PPPOE

g_router_acc = 'admin' # username for router manager
g_router_pw = 'admin' # Password for router manager


def getPIN(): # Encrypt the username
    global g_u
    us = g_u
    RAD = "cqxinliradius002"
    timeHash = [0, 0, 0, 0]
    temp = int(time.time() + 4) # Consider about the delay, plus 4 seconds
    timedivbyfive=temp//5
    for i in range(0, 4):
        for j in range(0, 8):
            timeHash[i] = timeHash[i] + (((timedivbyfive >> (i + 4 * j)) & 1) << (7 - j))
    m = hashlib.md5()
    bm = struct.pack('>I', timedivbyfive) + (us.split('@')[0] + RAD).encode('ascii')
    m.update(bm)
    pk = m.hexdigest()[0:2]
    PIN27 = [0, 0, 0, 0, 0, 0]
    PIN2 = ''
    PIN27[0] = ((timeHash[0] >> 2) & 0x3F)
    PIN27[1] = ((timeHash[0] & 0x03) << 4 & 0xff) | ((timeHash[1] >> 4) & 0x0F)
    PIN27[2] = ((timeHash[1] & 0x0F) << 2 & 0xff) | ((timeHash[2] >> 6) & 0x03)
    PIN27[3] = timeHash[2] & 0x3F
    PIN27[4] = ((timeHash[3] >> 2) & 0x3F)
    PIN27[5] = ((timeHash[3] & 0x03) << 4 & 0xff)
    for i in range(6):
        PIN27[i] = {True:(PIN27[i] + 0x20) & 0xff, False:(PIN27[i] + 0x21) & 0xff}[((PIN27[i] + 0x20) & 0xff) < 0x40]

    for i in range(6):
        PIN2 = PIN2 + chr(PIN27[i])
    PIN = PIN2 + pk + us #'\x0D\x0A'+
    return PIN


def TP_Dail(): # dial process for TP_Link 
    TP_url = '''http://192.168.1.1/userRpm/PPPoECfgRpm.htm?
&wan=0&wantype=2&VnetPap=201&linktype=4&waittime=&Connect=%%C1%%AC+%%BD%%D3
&acc=%s&psw=%s'''.replace('\n','') # Dial url

    TP_dis_url='''http://192.168.1.1/userRpm/PPPoECfgRpm.htm?
wan=0&wantype=2&acc=%s&psw=%s&confirm=%s&specialDial=100&SecType=0&
sta_ip=0.0.0.0&sta_mask=0.0.0.0&linktype=4&waittime2=0
&Disconnect=%%B6%%CF+%%CF%%DF'''.replace('\n','') # Disconnect Url

    global g_router_acc, g_router_pw, g_p
    PIN = '%0D%0A' + urllib2.quote(getPIN()) 
    auth = '%s:%s'%(g_router_acc, g_router_pw)
    auth = auth.encode("base64")[0:-1]
    dial_url = TP_url % (PIN, g_p)
    dis_url = TP_dis_url % ("admin", "pass", "pass")

    # At first stop the auto dial function
    dis_req = urllib2.Request(url = dis_url, headers = {'Authorization':
         'Basic ' + auth})
    dis_res = urllib2.urlopen(dis_req, timeout=200)
    dis_res.close()

    # Then dial
    dial_req = urllib2.Request(url = dial_url, headers = {'Authorization':
         'Basic ' + auth})  # 用户名和密码
    dial_res = urllib2.urlopen(dial_req, timeout=200)
    dial_res.close()


def getIP(): # Get IP address
    try:
        res = urllib2.urlopen('http://whois.pconline.com.cn/ipJson.jsp',timeout=2000)
    except:
        return None
    if res.getcode() != 200:
        return None
    re = res.read().decode('gbk').encode('utf8')
    res.close()
    re = re[re.rfind('{'):re.find('}')+1]
    return json.loads(re)


def Help():
    print '''This script for routers dial in Netkeeper environment:\n
    Usage:
    \tpython Router_dial.py [Routers]
    Routers list:
    tp\t:\tTP-Link

    Example:
    \tpython Router_dial.py tp'''


def main():
    arg = sys.argv
    if (len(arg) > 1):
        if arg[1] == 'tp':
            while True:
                if not getIP():
                    time.sleep(5)
                    TP_Dail()
        else:
            Help()
    else: # Default is TP-Link
        TP_Dail()

if __name__=='__main__':
    main()
