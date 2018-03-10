from utils import Utils


class Network():
    def __init__(self, ut):
        self.ut = ut
        self.Configuration = self.ut.readConfiguration()
        self.network = self.ut.requestString("network.php", accesstoken=self.Configuration["accessToken"]) #debug=True <- add debug for just developer in params
        self.targetBruted = self.ut.requestString("tasks.php", accesstoken=self.Configuration["accessToken"]) #debug=True <- add debug for just developer in params

    def getListNetwork(self):
        return self.network["cm"]

    def getListBruteforce(self):
        return self.targetBruted["brutes"]

    def attackTarget(self):
        for i, target in enumerate(self.getListNetwork()):
           self.targetHack = self.ut.requestString("exploit.php", target=str(target["ip"]), accesstoken=self.Configuration["accessToken"])
           self.targetHack = self.ut.requestString("remote.php", target=str(target["ip"]), accesstoken=self.Configuration["accessToken"])
           self.getBanking(str(target["ip"]))

    def getBanking(self, ip):
        reqBanking = self.ut.requestString("remotebanking.php", target=ip, accesstoken=self.Configuration["accessToken"])
        try:
           reqBanking["transactions"]
           print("Already Bruteforced")
        except KeyError:
           try:
              reqBanking["remotepassword"]
              print("Already Bruteforced but password Fail.")
           except KeyError:
              self.bruteForceBanking(ip)

    def bruteForceBanking(self, ip):
        reqBruteForcebanking = self.ut.requestString("startbruteforce.php", target=ip, accesstoken=self.Configuration["accessToken"]) 
        print(reqBruteForcebanking)

    def retryBruteForce(self, ip):
        pass

    def CollectMoney(self, ip):
        pass
