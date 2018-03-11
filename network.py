from utils import Utils


class Network():
    def __init__(self, ut):
        self.ut = ut
        self.Configuration = self.ut.readConfiguration()
        self.network = self.ut.requestString("network.php", accesstoken=self.Configuration["accessToken"]) #debug=True <- add debug for just developer in params
        self.targetBruted = self.ut.requestString("tasks.php", accesstoken=self.Configuration["accessToken"]) #debug=True <- add debug for just developer in params

    def getListNetwork(self, option):
        if option == "cm":
            return self.network["cm"]
        elif option == "ips":
            return self.network["ips"]

    def getListBruteforce(self):
        return self.targetBruted["brutes"]

    def attackTarget(self):
        list_ip_exist = set()
        list_ip_dontexist = set()
        for targetBrute in self.getListBruteforce():
           for targetNetwork in self.getListNetwork("cm"):
              if targetBrute["user_ip"] == targetNetwork["ip"]:
                  list_ip_exist.add(targetBrute["user_ip"])
              else:
                  list_ip_dontexist.add(targetNetwork["ip"])
        list_ip_dontexist = set(list_ip_exist)^set(list_ip_dontexist)
        print("Total Target Bruteforced ({0}), and try to ({1}) not bruteforced".format(len(list_ip_exist), len(list_ip_dontexist)))
        
        # scan don't exist ip in bruteforce list
        for target in list_ip_dontexist:
            self.targetHack = self.ut.requestString("exploit.php", target=str(target), accesstoken=self.Configuration["accessToken"])
            self.targetHack = self.ut.requestString("remote.php", target=str(target), accesstoken=self.Configuration["accessToken"])
            self.getBanking(str(target))

        # get money to bruteforce list
        for target in list_ip_exist:
            self.targetHack = self.ut.requestString("exploit.php", target=str(target), accesstoken=self.Configuration["accessToken"])
            self.targetHack = self.ut.requestString("remote.php", target=str(target), accesstoken=self.Configuration["accessToken"])
            self.getBanking(str(target))

        # search new user bruteforce and start bruteforce.
        for targetNetwork in self.getListNetwork("ips"):
            print(targetNetwork["ip"])
            self.targetHack = self.ut.requestString("exploit.php", target=str(targetNetwork["ip"]), accesstoken=self.Configuration["accessToken"])
            print(self.targetHack["result"])
            if self.targetHack["result"] == "0":
                self.targetHack = self.ut.requestString("remote.php", target=str(targetNetwork["ip"]), accesstoken=self.Configuration["accessToken"])
            elif self.targetHack["result"] == "2":
                print("don't possible to hack sdk exploit = 0")
                break

    def getBanking(self, ip):
        reqBanking = self.ut.requestString("remotebanking.php", target=ip, accesstoken=self.Configuration["accessToken"])
        try:
            reqBanking["transactions"]
            if int(reqBanking['withdraw']) > 0:
               print("Already '{}' Bruteforced collect money again...".format(ip))
               reqMoney = self.ut.requestString("remotebanking.php", target=ip, accesstoken=self.Configuration["accessToken"], action="100", lang="fr")
               print(reqMoney)
            else:
               print("target '{}' Money Null".format(ip))
        except KeyError:
           try:
              reqBanking["remotepassword"]
              print("Already '{}' Bruteforced but password Fail.".format(ip))
           except KeyError:
              self.bruteForceBanking(ip)

    def bruteForceBanking(self, ip):
        reqBruteForcebanking = self.ut.requestString("startbruteforce.php", target=ip, accesstoken=self.Configuration["accessToken"]) 
        print(reqBruteForcebanking)

    def retryBruteForce(self, ip):
        pass

    def CollectMoney(self, ip):
        pass