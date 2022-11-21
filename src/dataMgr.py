import json
import time
from statistics import mean

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class dataManager(object):
    def __init__(self) -> None:
        self.pingRptDict = {} # The ping report dict.
 
    def getData(self):
        return self.pingRptDict

    def peerSign(self, clientID,):
        pass

    def addData(self, clientID, dataJsonStr):
        clientID = clientID.strip()
        dataDict = json.loads(dataJsonStr)
        rptTime = time.time()
        if clientID in self.pingRptDict.keys():
            self.pingRptDict[clientID]['rptTime'] = rptTime
            for item in dataDict.items():
                key, val = item
                if key in self.pingRptDict[clientID].keys():
                    self.pingRptDict[clientID][key].append(val[1])
        else:
            self.pingRptDict[clientID] = {}
            self.pingRptDict[clientID]['rptTime'] = rptTime
            for item in dataDict.items():
                key, val = item
                self.pingRptDict[clientID][key] = [val[1]]

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

    def checkState(self, timeTH):
        now = time.time()
        stateDict = {}
        for id in self.pingRptDict.keys():
            stateDict[id] = {}
            stateDict[id]['connection'] = True
            for key in self.pingRptDict[id].keys():
                # Check the client report
                if key == 'rptTime':
                    if now - self.pingRptDict[id]['rptTime'] > timeTH:
                        stateDict[id]['connection'] = False
                        break
                else:
                    stateDict[id][key] = sum(i >= 500 for i in self.pingRptDict[id][key])
        return stateDict

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def testCase(mode):
    if mode == 0:
        testMsg = (
            'REP;0001;{"Google": [3.86, 5.72, 9.79], "CR1": [1.88, 2.19, 2.57], "Sutd": [4.78, 5.08, 5.79], "Singtel": [4.19, 4.92, 5.59], "Gov_sg": [3.79, 5.51, 10.33], "Bbc_co_uk": [4.52, 6.95, 11.9]}',
            'REP;0002;{"Google": [4.35, 5.2, 6.49], "CR1": [1.62, 1000, 3.57], "Sutd": [4.79, 5.9, 7.96], "Singtel": [4.83, 5.4, 5.95], "Gov_sg": [4.34, 5.99, 7.65], "Bbc_co_uk": [4.54, 7.69, 11.42]}',
            'REP;0001;{"Google": [4.96, 7.02, 9.35], "CR1": [1.84, 3.38, 4.78], "Sutd": [4.32, 6.06, 9.77], "Singtel": [3.74, 3.91, 4.13], "Gov_sg": [3.82, 4.81, 7.05], "Bbc_co_uk": [4.11, 5.89, 7.73]}',
            'REP;0002;{"Google": [5.0, 6.61, 7.79], "CR1": [1.53, 1000, 4.61], "Sutd": [5.0, 5.32, 5.65], "Singtel": [4.68, 6.19, 7.05], "Gov_sg": [3.75, 4.53, 4.83], "Bbc_co_uk": [5.44, 6.34, 7.13]}',
            'REP;0001;{"Google": [5.0, 6.61, 7.79], "CR1": [1.53, 2.76, 4.61], "Sutd": [5.0, 5.32, 5.65], "Singtel": [4.68, 6.19, 7.05], "Gov_sg": [3.75, 4.53, 4.83], "Bbc_co_uk": [5.44, 6.34, 7.13]}',
            'REP;0002;{"Google": [5.0, 6.61, 7.79], "CR1": [1.53, 1000, 4.61], "Sutd": [5.0, 5.32, 5.65], "Singtel": [4.68, 6.19, 7.05], "Gov_sg": [3.75, 4.53, 4.83], "Bbc_co_uk": [5.44, 6.34, 7.13]}',
            'REP;0001;{"Google": [5.0, 6.61, 7.79], "CR1": [1.53, 2.76, 4.61], "Sutd": [5.0, 5.32, 5.65], "Singtel": [4.68, 6.19, 7.05], "Gov_sg": [3.75, 4.53, 4.83], "Bbc_co_uk": [5.44, 6.34, 7.13]}'
        )
        dataMgr = dataManager()
        for msg in testMsg:
            _, id , dataJson = msg.split(';')
            print("Add data")
            dataMgr.addData(id, dataJson)
            time.sleep(1)
            
        #data = dataMgr.getData()
        #print(json.dumps(data, indent=4))

        rst = dataMgr.getAvg()
        print(json.dumps(rst, indent=4))

        #return
        state = dataMgr.checkState(20)
        print(json.dumps(state, indent=4))

        time.sleep(4)
        state = dataMgr.checkState(5)
        print(json.dumps(state, indent=4))

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    testCase(0)