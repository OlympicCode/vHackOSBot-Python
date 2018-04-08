from utils import Utils
from player import Player
import os, time

class Network():
    def __init__(self, ut):
        self.ut = ut
        self.Configuration = self.ut.readConfiguration()
        self.targetBruted = self.ut.requestString("tasks.php",
                                                  accesstoken=self.Configuration["accessToken"])
        self.network = self.ut.requestString("network.php",
                                             accesstoken=self.Configuration["accessToken"], lang="en")
        startFunctionAttack = self.startFunctionAttack()
        if startFunctionAttack == True:
            self.ut.viewsPrint("showMsgEndAttack", "[{}] - End Attack Loop Success.".format(os.path.basename(__file__)))
        self.RecoltMoney()

    def startFunctionAttack(self):
        # collect information in network.
        collect_scan_player = [(x["ip"], x["fw"], x["open"], x["level"]) \
                                for x in self.network["ips"]]

        p = Player(self.ut)
        for info_player in collect_scan_player:
            ip = str(info_player[0])
            firewall = int(info_player[1])
            
            # define the rule for attack ennemy
            if firewall > int(p.getHelperApplication()["SDK"]["level"]):
                # don't possible to attack user Firewall is to strong pass other player
                self.ut.viewsPrint("showMsgDoesntPossibleAttack", "[{}] - Don't Attack Your SDK ({}) vs Target Firewall ({}) on ip : '{}' :(".format(os.path.basename(__file__),int(p.getHelperApplication()["SDK"]["level"]), firewall, ip))
                time.sleep(1)
            else:
                # attack ip if firewall ennemy < your SDK
                self.AttackTarget(ip)
        return True


    def AttackTarget(self, ip):
        your_exploit = self.ut.exploit()
        if int(your_exploit) > 0:

            # get information in device.
            targetHack = self.ut.requestString("exploit.php", lang="en", target=ip, accesstoken=self.Configuration["accessToken"])
            resultHack = int(targetHack["result"])

            # if result is good you are access to connect in device now
            if resultHack == 0:
                # connect to the device
                targetRemote = self.ut.requestString("remote.php", lang="en", target=ip, accesstoken=self.Configuration["accessToken"])
                resultRemote = int(targetRemote["result"])
            else:
                return self.ut.result(result="don't return 0 weird", code=1)

            # if result is good you are possibly launch bruteforce to get money.
            if resultRemote == 0:
                bankingRemote = self.ut.requestString("remotebanking.php", target=ip, accesstoken=self.Configuration["accessToken"])
                resultbanking = int(bankingRemote["result"])
                passwordbanking = str(bankingRemote["remotepassword"])
            else:
                return self.ut.result(result="don't return 0 weird", code=1)

            # if banque don't have password the banque not cracked ... start bruteforce
            if passwordbanking == "":
                reqBruteForce = self.ut.requestString("startbruteforce.php", target=ip, accesstoken=self.Configuration["accessToken"])
                resultBruteforce = int(reqBruteForce["result"])
            else:
                return self.ut.result(result="don't return '' weird", code=1)

            # verify your command target
            if resultBruteforce == 0:
                self.ut.viewsPrint("showMsgCollectMoneyUser", "[{}] - \033[32m{} '{}'\033[0m".format(os.path.basename(__file__), "\033[32mStart Bruteforce to", ip))
                time.sleep(0.5)

            # if result is return 2 you SDK level is == 0.
            # don't possibly for you to hack wait time for
            # regenerate SDK.
            elif resultHack == 2:
                pass
        else:
            self.ut.viewsPrint("showMsgErrorSdk=0", "[{}] - don't possible to hack sdk exploit = 0 wait.".format(os.path.basename(os.path.basename(__file__))))
            time.sleep(0.5)

    def RecoltMoney(self):
        # collect information in bruteforce list.
        collect_brute_player = [(x["username"], x["end"], x["user_ip"], x["start"], x["result"], x["now"], x["id"]) \
                                for x in self.targetBruted["brutes"]]

        for PlayerBrute in collect_brute_player:
            PlayerBruteUsername = PlayerBrute[0]
            PlayerBruteIP = PlayerBrute[2]
            reqBanking = self.ut.requestString("remotebanking.php", target=PlayerBruteIP, accesstoken=self.Configuration["accessToken"])
            try:
                money = int(reqBanking["money"])
            except KeyError:
                money = 0
            if money > 0:
                reqMoney = self.ut.requestString("remotebanking.php", target=PlayerBruteIP, accesstoken=self.Configuration["accessToken"], action="100", amount=money,  lang="en")
                self.ut.viewsPrint("showMsgCollectMoneyUser", "[{}] - \033[32m{} {} to '{}'\033[0m".format(os.path.basename(__file__), "\033[32myou are collected +", money, PlayerBruteIP))
                time.sleep(0.5)
            else:
                self.ut.viewsPrint("showMsgCollectMoneyUser", "[{}] - \033[33m{} {} to '{}'\033[0m".format(os.path.basename(__file__), "money = 0 no possible to get money", money, PlayerBruteIP))
                time.sleep(0.5)