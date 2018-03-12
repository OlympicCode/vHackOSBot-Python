from network import Network
from utils import Utils

class run():
    ut = Utils()
    network = Network(ut)
    network.attackTarget()

if __name__ == '__main__':
    while 1:
       main = run()