from network import Network
from utils import Utils
import sys
import os
import fcntl

class run():
    def __init__(self, ut):
        network = Network(ut)
        network.attackTarget()

if __name__ == '__main__':
    ut = Utils()
    fl = fcntl.fcntl(sys.stdin.fileno(), fcntl.F_GETFL)
    fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, fl | os.O_NONBLOCK)
    while 1:
       main = run(ut)