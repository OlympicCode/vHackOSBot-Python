from utils import Utils
import os, time

class Player():
    def __init__(self, ut):
        self.ut = ut
        self.Configuration = self.ut.readConfiguration()
        self.getStore = self.ut.requestString("store.php",
                                              accesstoken=self.Configuration["accessToken"], lang="en")

    def getApplication(self):
        Dict_request = self.getStore["apps"]
        ApplicationCount = []

        for ApplicationUp in enumerate(Dict_request):
            Application = {}
            try:
                Application["baseprice"] = ApplicationUp[1]["baseprice"]
                Application["level"] = ApplicationUp[1]["level"]
                Application["price"] = ApplicationUp[1]["price"]
                Application["factor"] = ApplicationUp[1]["factor"]
                Application["maxlvl"] = ApplicationUp[1]["maxlvl"]
                Application["running"] = ApplicationUp[1]["running"]
                Application["appid"] = ApplicationUp[1]["appid"]
                Application["require"] = ApplicationUp[1]["require"]

            except KeyError as e:
                Application["baseprice"] = None
                Application["level"] = ApplicationUp[1]["level"]
                Application["price"] = ApplicationUp[1]["price"]
                Application["factor"] = None
                Application["maxlvl"] = ApplicationUp[1]["maxlvl"]
                Application["running"] = None
                Application["appid"] = ApplicationUp[1]["appid"]
                Application["require"] = ApplicationUp[1]["require"]

            ApplicationCount.append(Application)

        return ApplicationCount

    def getHelperApplication(self):
        Application = self.getApplication()
        FinalApplication = {}

        for allApplication in Application:
            # AntiVirus
            if int(allApplication["appid"]) == 1:
                FinalApplication["AV"] = allApplication
                
            # Firewall
            if int(allApplication["appid"]) == 2:
                FinalApplication["FW"] = allApplication

            # Spam
            if int(allApplication["appid"]) == 3:
                FinalApplication["SPAM"] = allApplication

            # Brute Force
            if int(allApplication["appid"]) == 4:
                FinalApplication["BRUTE"] = allApplication

            # Bank Protection
            if int(allApplication["appid"]) == 5:
                FinalApplication["BP"] = allApplication

            # Software developement kit
            if int(allApplication["appid"]) == 6:
                FinalApplication["SDK"] = allApplication

            if int(allApplication["appid"]) == 7:
                pass
                #FinalApplication[""] = allApplication

            if int(allApplication["appid"]) == 8:
                pass
                #FinalApplication[""] = allApplication

            if int(allApplication["appid"]) == 9:
                pass
                #FinalApplication[""] = allApplication

            if int(allApplication["appid"]) == 10:
                FinalApplication["IPSP"] = allApplication

            if int(allApplication["appid"]) == 11:
                pass
                #FinalApplication[""] = allApplication

            if int(allApplication["appid"]) == 12:
                pass
                #FinalApplication[""] = allApplication

            if int(allApplication["appid"]) == 13:
                pass
                #FinalApplication[""] = allApplication

            if int(allApplication["appid"]) == 14:
                pass
                #FinalApplication[""] = allApplication

            if int(allApplication["appid"]) == 15:
                pass
                #FinalApplication[""] = allApplication

        return FinalApplication
