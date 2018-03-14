from utils import Utils
import os, time

class Network():
    def __init__(self, ut):
        self.ut = ut
        self.Configuration = self.ut.readConfiguration()
        self.attackTarget()

    def attackTarget(self):
        your_exploit = self.ut.exploit()
        
        list_ip_exist = set()
        list_ip_dontexist = set()
        self.targetBruted = self.ut.requestString("tasks.php", accesstoken=self.Configuration["accessToken"])
        self.network = self.ut.requestString("network.php", accesstoken=self.Configuration["accessToken"])

        if len(self.targetBruted["brutes"]) > 0:
            for targetBrute in self.targetBruted["brutes"]:
               for targetNetwork in self.network["cm"]:
                  if targetBrute["user_ip"] == targetNetwork["ip"]:
                      list_ip_exist.add(targetBrute["user_ip"])
                  else:
                      list_ip_dontexist.add(targetNetwork["ip"])
        else:
            try:
                for targetNetwork in self.network["ips"]:
                    list_ip_dontexist.add(targetNetwork["ip"])
            except:
                self.ut.viewsPrint("showMsgBlockBruteForceInfoList", "[{}] - weird, you are not list player attack... :(".format(os.path.basename(__file__), len(list_ip_exist), len(list_ip_dontexist)))

        list_ip_dontexist = set(list_ip_exist)^set(list_ip_dontexist)
        
        self.ut.viewsPrint("showMsgTotalBruteForceInfo", "[{}] - Total Target Bruteforced ({}), and try to ({}) not bruteforced".format(os.path.basename(__file__), len(list_ip_exist), len(list_ip_dontexist)))
        
        if your_exploit > 0:
            # scan don't exist ip in bruteforce list
            for target in list_ip_dontexist:
                #s1 = self.targetHack = self.ut.requestString("exploit.php", target=str(target), accesstoken=self.Configuration["accessToken"])
                #s2 = self.targetHack = self.ut.requestString("remote.php", target=str(target), accesstoken=self.Configuration["accessToken"])
                time.sleep(0.2)
                self.getBanking(str(target))
        
        # get money to bruteforce list
        for target in list_ip_exist:
            #s1 = self.targetHack = self.ut.requestString("exploit.php", target=str(target), accesstoken=self.Configuration["accessToken"])
            #s2 = self.targetHack = self.ut.requestString("remote.php", target=str(target), accesstoken=self.Configuration["accessToken"])
            time.sleep(0.2)
            self.getBanking(str(target))

        self.network = self.ut.requestString("network.php", accesstoken=self.Configuration["accessToken"])
        if int(your_exploit) > 0:
            # search new user bruteforce and start bruteforce.
            for targetNetwork in self.network["ips"]:
                self.targetHack = self.ut.requestString("exploit.php", lang="fr", target=str(targetNetwork["ip"]), accesstoken=self.Configuration["accessToken"])
                if self.targetHack["result"] == "0":
                    self.targetHack = self.ut.requestString("remote.php", lang="fr", target=str(targetNetwork["ip"]), accesstoken=self.Configuration["accessToken"])
                    self.getBanking(self, targetNetwork)
                elif self.targetHack["result"] == "2":
                    self.ut.viewsPrint("showMsgErrorSdk=0", "[{}] - don't possible to hack sdk exploit = 0 wait.".format(os.path.basename(os.path.basename(__file__))))
                    time.sleep(0.8)

        yourbank = self.ut.requestString("banking.php", target=str(targetNetwork["ip"]), accesstoken=self.Configuration["accessToken"])
        whitelist = set()
        for info in yourbank["transactions"]:
            if int(info["to_id"]) == self.Configuration["uID"]:
                whitelist.add(info["from_ip"])

        for target in whitelist:
            self.ut.viewsPrint("showbanquinuser", "[{}] - Hack target from bank '{}'".format(os.path.basename(os.path.basename(__file__)), target))
            self.getBanking(str(target))
            time.sleep(1)


    def getBanking(self, ip):
        reqBanking = self.ut.requestString("remotebanking.php", target=ip, accesstoken=self.Configuration["accessToken"])
        try:
            if int(reqBanking['remotemoney']) > 0:
               self.ut.viewsPrint("showMsgCollectMoneyUser", "[{}] - \033[32mAlready '{}' collect money +{}\033[0m".format(os.path.basename(__file__), ip, reqBanking['remotemoney']))
               reqMoney = self.ut.requestString("remotebanking.php", target=ip, accesstoken=self.Configuration["accessToken"], action="100", lang="fr")
            else:
               self.ut.viewsPrint("showMsgNoMoneyTarget", "[{}] - target '{}' Money Null".format(os.path.basename(__file__), ip))
        except KeyError:
            try:
                if reqBanking["remotepassword"] is not '':
                    self.bruteForceBanking(ip)
                else:
                    reqMoney = self.ut.requestString("remotebanking.php", target=ip, accesstoken=self.Configuration["accessToken"], action="100", lang="fr")
                    self.ut.viewsPrint("showMsgNoMoneyTarget", "[{}] - target '{}' Money Null".format(os.path.basename(__file__), ip))
            except:
                self.bruteForceBanking(ip)

  


    def bruteForceBanking(self, ip):
        reqBruteForcebanking = self.ut.requestString("startbruteforce.php", target=ip, accesstoken=self.Configuration["accessToken"])
        try:
            if int(reqBruteForcebanking["result"]) is 0:
                self.ut.viewsPrint("showMsgCollectMoneyUser", "[{}] - \033[32m{} '{}'\033[0m".format(os.path.basename(__file__), "\033[32mStart Bruteforce to", ip ))
            else:
                self.ut.viewsPrint("showMsgCollectMoneyUser", "[{}] - \033[32m{} '{}'\033[0m".format(os.path.basename(__file__), "\033[31mError start Bruteforce to", ip ))
        except:
            self.ut.viewsPrint("showMsgTasklistisFull", "[{}] - \033[32m{} '{}'\033[0m".format(os.path.basename(__file__), "\033[31mError Task list is probably full", ip ))

