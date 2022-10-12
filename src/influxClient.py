#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        databaseMgr.py
#
# Purpose:     This module will provide a influx database manager to collect the 
#              gateway feed back data by UDP and insert to influx database which
#              will be used for the grafana dashboard.
#
# Author:      Yuancheng Liu
#
# Created:     2019/01/15
# Copyright:   
# License:     
#-----------------------------------------------------------------------------

from random import randint
import time
import udpCom
import threading
from statistics import mean
from datetime import datetime

from influxdb import InfluxDBClient
from tcp_latency import measure_latency

UDP_PORT = 3001
TEST_MODE = False   # test mode flag.
LAT_PERIOD = 5      # latency periodic check time.
RPT_PERIOD = 2      # time period to insert the data to data base.


class ServThread(threading.Thread):
    """ Server thread to generate a UDP server to handle the gateway client's
        feedback data.
    """ 
    def __init__(self, parent, threadID, name):
        threading.Thread.__init__(self)
        self.parent = parent
        self.server = udpCom.udpServer(None, UDP_PORT)

    def run(self):
        """ Start the udp server's main message handling loop."""
        print("Server thread run() start.")
        self.server.serverStart(handler=self.parent.msgHandler)
        print("Server thread run() end.")

    def stop(self):
        """ Stop the udp server. Create a endclient to bypass the revFrom() block."""
        self.server.serverStop()
        endClient = udpCom.udpClient(('127.0.0.1', UDP_PORT))
        endClient.disconnect()
        endClient = None

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class InfluxCli(object):
    """ Client to connect to the influx db and insert data."""
    def __init__(self, ipAddr=None, dbInfo=None):
        """ Init the influx DB client to login to the data base. dbInfo: name, 
            password, databaseName. init example: 
            client = InfluxCli(ipAddr=('127.0.0.1', 8086), dbinfo=('root', 'root', 'gatewayDB'))
        """
        (ip, port) = ipAddr if ipAddr else ('localhost', 8086)
        (user, pwd, dbName) = dbInfo if dbInfo and len(
            dbInfo) == 3 else ('root', 'root', 'gatewayDB')
        #self.dbClient = InfluxDBClient('localhost', 8086, 'root', 'root', 'quantumGWDB')
        # link to data base:
        self.dbClient = InfluxDBClient(ip, port, user, pwd, dbName)
        # state the UDP server:
        server = ServThread(self, 0, "server thread")
        server.start()
        print("inited")


    def msgHandler(self, msg=None, ipAddr=None):
        """ handle the feed back message."""
        if isinstance(msg, bytes): msg = msg.decode('utf-8')
        dataList = msg.split(';')
        gwName, minP, avgP, maxP = dataList
        self.writePingData(gwName, float(minP), float(avgP), float(maxP))
        print(msg)


#-----------------------------------------------------------------------------
    def writePingData(self, gwName, minP, avgP, maxP):
        """ Write the gateway data to the related gateway table based on gateway 
            name. 
        """
        print("update database")
        gwDatajson = [
            {
                "measurement": str(gwName),
                "tags": {
                    "Name": "time",
                },
                "fields": {
                    "min": minP,
                    "avg": avgP,
                    "max": maxP,
                }
            }]
        self.dbClient.write_points(gwDatajson)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main():
    client = InfluxCli(ipAddr=('localhost', 8086), dbInfo=('root', 'root', 'gatewayDB'))
    #for i in range(1000):
    #    client.writePingData('www.google.com')
    #    time.sleep(2)

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
