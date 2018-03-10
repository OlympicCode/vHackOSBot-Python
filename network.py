from utils import Utils


class Network():
    def __init__(self, ut):
        Configuration = ut.readConfiguration()
        self.network = ut.requestString("network.php", accesstoken=Configuration["accessToken"], debug=True) #debug=True <- add debug for just developer in params

    def getList(self):
        return self.network

    def Attack(self):
    	return ""