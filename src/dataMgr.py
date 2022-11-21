import json
import time
from statistics import mean

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class dataManager(object):
    def __init__(self) -> None:
        self.pingRptDict = {} # The ping report dict.
        self.stateDict = {}
 
    def peerSign(self, clientID,):
        pass

    def parseData(self, clientID, dataJsonStr):
        clientID = clientID.strip()
        dataDict = json.loads(dataJsonStr)
        rptTime = time.time()
        if clientID in self.pingRptDict.keys():
            self.pingRptDict[clientID]['rptTime'] = rptTime
            for item in dataDict.items():
                key, val = item
                if key in self.pingRptDict[clientID].keys():
                    self.pingRptDict[clientID][key].append(val)
        else:
            self.pingRptDict[clientID] = {}
            self.pingRptDict[clientID]['rptTime'] = rptTime
            for item in dataDict.items():
                key, val = item
                self.pingRptDict[clientID][key] = [val]

    def resetRst(self):
        for id in self.pingRptDict.keys():
            for key in self.pingRptDict[id].keys():
                if key == 'rptTime': continue
                self.pingRptDict[id][key] = []
            
    def getAvg(self):
        avgDict = {}
        for id in self.pingRptDict.keys():
            avgDict[id] = {}
            for key in self.pingRptDict[id].keys():
                if key == 'rptTime': continue
                pingArr = self.pingRptDict[id][key]
                avgPing = round(mean(pingArr),3) if len(pingArr) > 0 else 0
                avgDict[id][key] = avgPing

        return avgDict

    def checkState(self):
        now = time.time
        stateDict = {}
        for id in self.pingRptDict.keys():
            stateDict[id]['connection'] = True
            for key in self.pingRptDict[id].keys():
                # Check the client report
                if key == 'rptTime' and now - self.pingRptDict[id]['rptTime'] > gv.RPT_TH:
                    stateDict[id]['connection'] = False
                    break
                stateDict[id][key] = sum(i > 5 for i in  self.pingRptDict[id][key])
        return stateDict

def testCase(mode):
    if mode == 0:
        









#-----------------------------------------------------------------------------
if __name__ == '__main__':
    testCase(0)