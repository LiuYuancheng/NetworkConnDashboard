#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        pingClient.py
#
# Purpose:     This module will ping the destination ip/url dict periodically, save 
#              the ping result in local disk and report result to the server side.
#
# Author:      Yuancheng Liu
#
# Version:     v_0.1
# Created:     2022/10/12
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------

import os
import time
from pythonping import ping
import requests
from datetime import datetime
from statistics import mean
import udpCom
import Log



# Config the local data/log storage folder
print("Current working directory is : %s" % os.getcwd())
dirpath = os.path.realpath(__file__)
print("Current source code location : %s" % dirpath)
APP_NAME = ('pingClient', 'ping')

# Init the log module
TOPDIR = 'src'
idx = dirpath.find(TOPDIR)
gTopDir = dirpath[:idx + len(TOPDIR)] if idx != -1 else dirpath   # found it - truncate right after TOPDIR
#print('Top dir: %s' %str(gTopDir))
Log.initLogger(gTopDir, 'Logs', APP_NAME[0], APP_NAME[1], historyCnt=100, fPutLogsUnderDate=True)

TEST_MD = True  # Test mode flag.

HUB_IP = ('127.0.0.1', 3001) if TEST_MD else ('172.18.178.6', 3001) 
PING_TM = 100

# test address:
# ipAdrrDict = {
#     'Google':'www.google.com.sg',
#     'CR1': '172.18.178.10',
#     'Sutd': '202.94.70.56'
# }

ipAdrrDict = {
    'Google':   'www.google.com.sg',
    'CR1':      '172.18.178.10',
    'Sutd':     '202.94.70.56',
    'Singtel':  'www.singtel.com.sg',
    'Gov_sg':   'gov.sg',
    'Bbc_co_uk':'BBC.CO.UK'
}

pingRst = {
    'Google': [],
    'CR1': [],
    'Sutd': [],
    'Singtel': [],
    'Gov_sg': [],
    'Bbc_co_uk': [],
}

count = 5 # used to count the time 

BOT_TOKEN = "refer to the file <pingClientRun.py>"
CHAT_ID = "-1001547453974"

# BBC.CO.UK
# 172.16.1.10 (vcentre)
# 172.18.178.6 
# singtel.com.sg
# gov.sg

# UDP report connector
iConnector = udpCom.udpClient(HUB_IP)

#for _ in range(PING_TM):
while True:
    for item in ipAdrrDict.items():
        key, val = item
        data = ping(val, timeout=1, verbose=False)
        print(" Peer [%s] ping min: %s ms, avg: %s ms, max: %s ms" % (key, str(data.rtt_min_ms),  str(data.rtt_avg_ms), str(data.rtt_max_ms)))
        Log.info('[%s]: min:%s,avg:%s,max:%s', key, str(data.rtt_min_ms), str(data.rtt_avg_ms), str(data.rtt_max_ms))
        pingRst[key].append(data.rtt_avg_ms)
        msg = ';'.join((key, str(data.rtt_min_ms), str(data.rtt_avg_ms), str(data.rtt_max_ms)))
        resp = iConnector.sendMsg(msg, resp=False)
        time.sleep(5)
    count -= 1
    # call telegram API to message the reuslt to group 
    if count == 0:
        timeStr = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        msg = 'NCL-MPH Connection HUB report: \n'
        msg+= 'Time: %s \n' %timeStr
        msg+= 'During passed 5 min each peers avg ping are: \n'
        for item in pingRst.items(): 
            key, val = item
            msg += str(' - '+ key +' : '+ str( round(mean(val),3))+' ms \n')
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
            requests.get(url).json()
            pass 
        except Exception as e:
            Log.error('report to telegram error:')
            Log.info(str(e))
            pass
        # reset the reault:
        pingRst = {
            'Google': [],
            'CR1': [],
            'Sutd': [],
            'Singtel': [],
            'Gov_sg': [],
            'Bbc_co_uk': [],
        }
        count = 6
    time.sleep(30)

Log.info("Finished the ping test.")
