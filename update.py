from utils import Utils
from player import Player
import os, time, random

class Update():
    def __init__(self, ut):
        self.ut = ut
        self.Configuration = self.ut.readConfiguration()
        self.store = self.ut.requestString("store.php",
                                           accesstoken=self.Configuration["accessToken"])
        self.startFunctionUpdate()

    def startFunctionUpdate(self):

        # get money info
        if "money" in self.store and "apps" in self.store:
            money = int(self.store["money"])
            apps = self.store["apps"]
        else:
            apps = []
            money = 0

        p = Player(self.ut)

        getTask = self.ut.requestString("tasks.php", accesstoken=self.Configuration["accessToken"])

        if 'updateCount' in getTask.keys():
            update = int(getTask['updateCount'])
        else:
            update = 0
            
        # get applications and update this
        for count_update, applications in enumerate(apps):
            # update application


            if (count_update+update) < 9:
                Appid = int(applications["appid"])
                random.shuffle(self.Configuration["update"])
                for list_update in self.Configuration["update"]:
                    time.sleep(0.3)
                    application_update = int(p.getHelperApplication()[list_update]["appid"])
                    if money >= int(applications["price"]):
                        result = self.ut.requestString("store.php",
                                                        accesstoken=self.Configuration["accessToken"],
                                                        appcode=application_update,
                                                        action="100")
                        money = money - int(applications["price"])
                        if result['result'] == '0':
                            update = update+1
                            self.ut.viewsPrint("showMsgUpdate", "[{}] - Update for your {} +1".format(os.path.basename(__file__), list_update))
                            time.sleep(0.5)
                    else:
                        self.ut.viewsPrint("showMsgUpdate", "[{}] - you have not money to upgrade {}".format(os.path.basename(__file__), list_update))
                        time.sleep(0.5)
            else:
                self.ut.viewsPrint("showMsgUpdatefull", "[{}] - full task used please wait.".format(os.path.basename(__file__)))
                time.sleep(0.5)
                # install application if level required < level
                if int(applications["require"]) <= int(self.store["level"]) and int(applications["level"]) == 0:
                    result = self.ut.requestString("store.php",
                                                    accesstoken=self.Configuration["accessToken"],
                                                    appcode=applications["appid"],
                                                    action="200")
                    self.ut.viewsPrint("showMsgInstalleApp", "[{}] - Installed new application.".format(os.path.basename(__file__)))
                break
