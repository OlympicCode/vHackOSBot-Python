from update import Update
from network import Network
from utils import Utils
from miner import Miner
import sys
import os
try:
   import fcntl
except:
	pass

class run():
    def __init__(self, ut):
        update = Update(ut)
        network = Network(ut)
        miner = Miner(ut)

if __name__ == '__main__':
    ut = Utils()
    try:
        fl = fcntl.fcntl(sys.stdin.fileno(), fcntl.F_GETFL)
        fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, fl | os.O_NONBLOCK)
    except:
    	  pass
    while 1:
        main = run(ut)