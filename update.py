from utils import Utils
from player import Player
import os, time

class Update():
    def __init__(self, ut):
        self.ut = ut
        self.Configuration = self.ut.readConfiguration()
        self.store = self.ut.requestString("store.php",
                                           accesstoken=self.Configuration["accessToken"])
        self.startFunctionUpdate()

    def startFunctionUpdate(self):

        # get money info
        money = self.store["money"]
        p = Player(self.ut)

        
        # get applications and update this
        for applications in self.store["apps"]:
            getTask = self.ut.requestString("tasks.php",
                                            accesstoken=self.Configuration["accessToken"])
            if len(getTask["updates"]) < 10:
                Appid = int(applications["appid"])
                for list_update in self.Configuration["update"]:
                    time.sleep(0.3)
                    application_update = int(p.getHelperApplication()[list_update]["appid"])
                    if Appid == application_update:
                        if money >= applications["price"]:
                            result = self.ut.requestString("store.php",
                                                               accesstoken=self.Configuration["accessToken"],
                                                               appcode=application_update,
                                                               action="100")
                            self.ut.viewsPrint("showMsgUpdate", "[{}] - Update for your {} +1".format(os.path.basename(__file__), list_update))
                            time.sleep(0.5)
                        else:
                            self.ut.viewsPrint("showMsgUpdate", "[{}] - you have not money to upgrade {}".format(os.path.basename(__file__), list_update))
                            time.sleep(0.5)
            else:
            	self.ut.viewsPrint("showMsgUpdatefull", "[{}] - full task used please wait.".format(os.path.basename(__file__)))
            	time.sleep(0.5)
            	return False


