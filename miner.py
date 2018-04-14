from utils import Utils
from player import Player
import os, time, datetime, sys

class Miner():
    def __init__(self, ut):
        self.ut = ut
        self.Configuration = self.ut.readConfiguration()
        self.store = self.ut.requestString("store.php",
                                           accesstoken=self.Configuration["accessToken"])
        self.myinfo = self.ut.account()
        self.runMiner()

    def runMiner(self):
        if 'minerLeft' in self.myinfo.keys():
            self.minefinish = int(self.myinfo['minerLeft'])
            self.ut.viewsPrint("MinerMsgLeft", "minerLeft {}".format(self.minefinish))
        else:
            self.ut.viewsPrint("MinerMsgError", 'Unexpected myinfo string {}'.format(self.myinfo))
            sys.exit()
        if self.minefinish > 0:
            self.ut.viewsPrint("MinerMsgTime", "waiting until {} --- {}".format(self.ut.tuntin(self.minefinish), datetime.timedelta(seconds=(self.minefinish))))

        else:
            result = self.MinerInfo()
            self.ut.viewsPrint("MinerMsgError", result)
            if result['result'] == '0':
                if result['running'] == '2' and result['claimed'] == '0':
                    collectresult = self.doCollect()
                    if collectresult['result'] != '0':
                        self.ut.viewsPrint("MinerMsgerror", 'something went wrong collecting')
                        sys.exit()
                elif result['running'] == '0' and result['claimed'] == '0':
                    mineresult = self.doMine()
                    if mineresult['result'] != '0':
                        self.ut.viewsPrint("MinerMsgerror", 'something went wrong collecting')
                        sys.exit()
                    elif mineresult['result'] == '0':
                        self.ut.viewsPrint("MinerStarting", " started mining {} --- {}".format(self.ut.tuntin(int(mineresult['left'])), datetime.timedelta(seconds=(int(mineresult['left'])))))

    def doMine(self):
        result = self.ut.requestString("mining.php", accesstoken=self.Configuration["accessToken"], action="100")
        return result

    def doCollect(self):
        result = self.ut.requestString("mining.php", accesstoken=self.Configuration["accessToken"], action="200")
        return result

    def MinerInfo(self):
        result = self.ut.requestString("mining.php", accesstoken=self.Configuration["accessToken"])
        return result
