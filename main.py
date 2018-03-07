from utils import Utils





ut = Utils()
u = ut.requestString("update.php")
u = ut.requestString("buy.php", info="1")
print(u)