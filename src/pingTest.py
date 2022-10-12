import time
from pythonping import ping

import os
import Log
import udpCom

print("Current working directory is : %s" % os.getcwd())
dirpath = os.path.dirname(__file__)
print("Current source code location : %s" % dirpath)
APP_NAME = ('pingClient', 'ping')

TOPDIR = 'src'
idx = dirpath.find(TOPDIR)
gTopDir = dirpath[:idx + len(TOPDIR)] if idx != -1 else dirpath   # found it - truncate right after TOPDIR
Log.initLogger(gTopDir, 'Logs', APP_NAME[0], APP_NAME[1], historyCnt=100, fPutLogsUnderDate=True)

HubIP = ('172.18.178.6', 3001)

# test address:
ipAdrrDict = {
    'Google':'www.google.com.sg',
    'CR1': '172.18.178.10',
    'Sutd': '202.94.70.56'
}

# BBC.CO.UK
# 172.16.1.10 (vcentre)
# 172.18.178.6 
# singtel.com.sg
# gov.sg
# kongguan.com.sg

BE_IP = ('127.0.0.1', 3001)     # backend server IP address.
iConnector = udpCom.udpClient(BE_IP)

for _ in range(10): 
    for item in ipAdrrDict.items():
        key, val = item
        data = ping( val, timeout = 1, verbose=False)
        print(" Peer [%s] ping min: %s ms, avg: %s ms, max: %s ms" % (key, str(data.rtt_min_ms),  str(data.rtt_avg_ms),str(data.rtt_max_ms)))   
        Log.info( '[%s]: min:%s,avg:%s,max:%s', key, str(data.rtt_min_ms),str(data.rtt_avg_ms), str(data.rtt_max_ms) )
        msg = ';'.join((key, str(data.rtt_min_ms),str(data.rtt_avg_ms), str(data.rtt_max_ms)))
        resp = iConnector.sendMsg(msg, resp=False)
        time.sleep(1)
    time.sleep(3)
