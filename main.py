from network import Network
from utils import Utils

class run():
    def __init__(self, ut):
        network = Network(ut)
        network.attackTarget()

if __name__ == '__main__':
    ut = Utils()
    while 1:
       main = run(ut)