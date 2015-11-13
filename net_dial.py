#!/usr/bin/env python
# coding: utf-8

# __buildin__ modules
import sys
import time
import socket
import struct
import hashlib
import argparse
import urllib2

try:
    import simplejson as json
except ImportError:
    import json

# project modules
from net_ping import do_one
from net_router import model

BANNER = r'''
    ____              __            ____        _ __
   / __ \____  __  __/ /____  _____/ __ \____ _(_) /
  / /_/ / __ \/ / / / __/ _ \/ ___/ / / / __ `/ / /
 / _, _/ /_/ / /_/ / /_/  __/ /  / /_/ / /_/ / / /
/_/ |_|\____/\__,_/\__/\___/_/  /_____/\__,_/_/_/  (alhpa-0.1)

    Author: Purpleroc@0xfa.club
  Modified: RickGray@0xfa.club     |
      Date: 2015-10-22             |
    Update: 2015-10-22             |
___________________________________|
'''


_OPTIONS_HELP_ = {
    'USERNAME': 'Network account username (e.g. 1621744@cqupt)',
    'PASSWORD': 'Network account password',
    'AUTH': 'Router auth username and password (e.g. admin:admin)',
    'MODE': 'Router models (Already exist Models are:' +  "\t".join(dir(model)[0:-3]) + ")",
}


def parse_command():
    """ 命令行参数解析和设置 """
    parse = argparse.ArgumentParser()

    account = parse.add_argument_group('account')
    account.add_argument('-u', dest='USERNAME', type=str,
                         required=True, help=_OPTIONS_HELP_['USERNAME'])
    account.add_argument('-p', dest='PASSWORD', type=str,
                         required=True, help=_OPTIONS_HELP_['PASSWORD'])

    router = parse.add_argument_group('router')
    router.add_argument('-a', dest='AUTH', type=str, help=_OPTIONS_HELP_['AUTH'])
    router.add_argument('-m', dest='MODEL', type=str, help=_OPTIONS_HELP_['MODE'])

    return parse.parse_args()


def md5(string):
    """ 返回字符串md5值 """
    return hashlib.md5(str(string)).hexdigest()


def get_encrypted_username(username):
    """ 使用特殊加密算法得到拨号用户名前缀PIN值 """
    rad = 'cqxinliradius002'  # 加密参数
    us = username
    time_hash = [0] * 4

    # 考虑运行延迟，增加4秒进行计算
    cur_time = int(time.time() + 4) / 5
    for i in range(0, 4):
        for j in range(0, 8):
            time_hash[i] += (((cur_time >> (i + 4 * j)) & 1) << (7 - j))

    bm = struct.pack('>I', cur_time) + (us.split('@')[0] + rad).encode('ascii')
    pk = md5(bm)[0:2]
    pin27 = [0] * 6
    pin27[0] = ((time_hash[0] >> 2) & 0x3F)
    pin27[1] = ((time_hash[0] & 0x03) << 4 & 0xff) | ((time_hash[1] >> 4) & 0x0F)
    pin27[2] = ((time_hash[1] & 0x0F) << 2 & 0xff) | ((time_hash[2] >> 6) & 0x03)
    pin27[3] = time_hash[2] & 0x3F
    pin27[4] = ((time_hash[3] >> 2) & 0x3F)
    pin27[5] = ((time_hash[3] & 0x03) << 4 & 0xff)
    for i in range(6):
        pin27[i] = {True: (pin27[i] + 0x20) & 0xff,
                    False: (pin27[i] + 0x21) & 0xff}[((pin27[i] + 0x20) & 0xff) < 0x40]

    pin2 = ''
    for i in range(6):
        pin2 += chr(pin27[i])
    pin = pin2 + pk + us
    encrypted_username = '%0D%0A' + urllib2.quote(pin)  # 拨号时特定用户名格式

    return encrypted_username


def check_net_connection():
    """ 通过尝试向baidu.com发送ICMP包判断网络连通性 """
    timeout = 2
    status = False
    for _ in range(5):
        try:
            delay = do_one('baidu.com', timeout)
        except socket.gaierror, ex:
            break

        if delay:
            continue
        else:
            status = True
            break

    return status


def run(args):
    """ 主函数 """
    username = args.USERNAME
    password = args.PASSWORD
    auth = args.AUTH

    mode = args.MODEL.upper()
    if mode:
        if hasattr(model, mode):
            e_user = get_encrypted_username(username)
            getattr(model, mode)(mode, auth, e_user, password)
        pass
    else:
        print 'Router model required'
        sys.exit()

if __name__ == '__main__':
    print BANNER
    run(parse_command())
