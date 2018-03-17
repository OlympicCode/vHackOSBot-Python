from utils import Utils
import os, time

class Network():
    def __init__(self, ut):
        self.ut = ut
        self.Configuration = self.ut.readConfiguration()
        self.targetBruted = self.ut.requestString("tasks.php", accesstoken=self.Configuration["accessToken"])
        self.network = self.ut.requestString("network.php", accesstoken=self.Configuration["accessToken"])
        self.attackTarget(self.Configuration["attack_mode"])

    def attackTarget(self, mode):
        your_exploit = self.ut.exploit()
        
        list_ip_exist = set()
        list_ip_dontexist = set()
        try:
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
        except:
            list_ip_exist = []
            list_ip_dontexist = []

        list_ip_dontexist = set(list_ip_exist)^set(list_ip_dontexist)
        
        self.ut.viewsPrint("showMsgTotalBruteForceInfo", "[{}] - Total Target Bruteforced ({}), and try to ({}) not bruteforced".format(os.path.basename(__file__), len(list_ip_exist), len(list_ip_dontexist)))
        
            
        if mode == "ip_list":
            # get money to bruteforce list
            if int(your_exploit) > 0:
                for target in list_ip_exist:
                    s1 = self.targetHack = self.ut.requestString("exploit.php", target=str(target), accesstoken=self.Configuration["accessToken"])
                    s2 = self.targetHack = self.ut.requestString("remote.php", target=str(target), accesstoken=self.Configuration["accessToken"])
                    self.ut.viewsPrint("showAttacktarget", "[{}] - attack to '{}'".format(os.path.basename(os.path.basename(__file__)), target))
                    self.getBanking(str(target))


        if mode == "new":
            self.network = self.ut.requestString("network.php", accesstoken=self.Configuration["accessToken"])
            if int(your_exploit) > 0:
                # search new user bruteforce and start bruteforce.
                for targetNetwork in self.network["ips"]:
                    self.targetHack = self.ut.requestString("exploit.php", lang="fr", target=str(targetNetwork["ip"]), accesstoken=self.Configuration["accessToken"])
                    if self.targetHack["result"] == "0":
                        self.ut.viewsPrint("showAttacktarget", "[{}] - attack to '{}'".format(os.path.basename(os.path.basename(__file__)), str(targetNetwork["ip"])))
                        self.targetHack = self.ut.requestString("remote.php", lang="fr", target=str(targetNetwork["ip"]), accesstoken=self.Configuration["accessToken"])
                        self.getBanking(targetNetwork)
                    elif self.targetHack["result"] == "2":
                        self.ut.viewsPrint("showMsgErrorSdk=0", "[{}] - don't possible to hack sdk exploit = 0 wait.".format(os.path.basename(os.path.basename(__file__))))
            else:
                self.ut.viewsPrint("showMsgErrorSdk=0", "[{}] - don't possible to hack sdk exploit = 0 wait.".format(os.path.basename(os.path.basename(__file__))))

        if mode == "bank_scan":
            yourbank = self.ut.requestString("banking.php", lang="fr", accesstoken=self.Configuration["accessToken"])
            whitelist = set()
            for info in yourbank["transactions"]:
                if int(info["to_id"]) == self.Configuration["uID"]:
                    whitelist.add(info["from_ip"])

            for target in whitelist:
                self.ut.viewsPrint("showbanquinuser", "[{}] - Hack target from bank '{}'".format(os.path.basename(os.path.basename(__file__)), target))
                s2 = self.targetHack = self.ut.requestString("remote.php", target=str(target), accesstoken=self.Configuration["accessToken"])
                try:
                    if s2["result"] is not None and s2["withdraw"] > 0:
                        self.getBanking(str(target))
                except:
                    pass


    def getBanking(self, ip):
        reqBanking = self.ut.requestString("remotebanking.php", target=ip, accesstoken=self.Configuration["accessToken"])
        if reqBanking['result'] is not None:
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

