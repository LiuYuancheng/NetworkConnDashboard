#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        influxClient.py
#
# Purpose:     This module will run as the bridge(data manager) between the influxDB
#              database and all the report-clients. It will collect the message from
#              the ping clients, do data filtering and insert valid data in the
#              database.
#
# Author:      Yuancheng Liu
#
# Created:     2022/10/12
# Copyright:   
# License:     
#-----------------------------------------------------------------------------

import threading
from influxdb import InfluxDBClient

import udpCom

# Init the global value:
UDP_PORT = 3001
TEST_MODE = False       # test mode flag.
TB_NAME = 'gatewayDB'   # influx DB table name.

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
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
        try:
            self.dbClient = InfluxDBClient(ip, port, user, pwd, dbName)
        except Exception as e:
            print("Can not connect to the data base, please check whether the influxDB service is running. \n" 
                + "- Windows:   go to D:\\Tools\\InfluxDB\\influxdb-1.8.1-1 and run influxd.exe \n"
                + "- Ubuntu:    sudo systemctl start influxdb" )
            exit()
        # state the UDP server:
        self.udpServer = ServThread(self, 0, "server thread")
        print("inited")

#-----------------------------------------------------------------------------
    def startService(self):
        print("Service started")
        self.udpServer.start()


#-----------------------------------------------------------------------------
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
    client = InfluxCli(ipAddr=('localhost', 8086), dbInfo=('root', 'root', TB_NAME))
    client.startService()

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
