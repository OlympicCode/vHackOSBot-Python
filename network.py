import ruamel.yaml as yaml
from utils import Utils


class Network():
    def __init__(self):
        ut = Utils()
        Configuration = ut.readConfiguration()
        try:
            self.network = ut.requestString("network.php", accesstoken=Configuration["accessToken"], debug=False) #debug=True <- add debug for just developer in params
        except KeyError:
        	ut.generateConfiguration()
        	self.network = ut.requestString("network.php", accesstoken=Configuration["accessToken"], debug=False)

    def getList(self):
        return self.network

    def Attack(self):
    	return ""