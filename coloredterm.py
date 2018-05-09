from colorama import init
from colorama import Fore, Back, Style


init()


class colored():
    def __init__(self, msglog, message):
        self.mlog = msglog
        self.msg = message

    def autocolored(self):
        color = {

            #global message
            "ErorRequest": Fore.RED,
            "ErrorJson": Fore.RED,

            # update message
            "showMsgUpdatefull":  Fore.BLUE,
            "showMsgUpdate":  Fore.BLUE,

            # Network message
            "showMsgEndAttack": Fore.GREEN,
            "showMsgErrorAPI": Fore.GREEN,
            "showMsgDoesntPossibleAttack": Fore.BLUE,
            "showMsgWriteLog":  Fore.YELLOW,
            "showMsgCollectMoneyUser":  Fore.BLUE,
            "showMsgErrorSdk=0":  Fore.BLUE,
            "showMsgCollectMoneyUser":  Fore.BLUE,
            "showMsgCollectMoneyUser":  Fore.BLUE,
            "showMsgGenerateMWK":  Fore.BLUE,

            #Miner message
            "MinerMsgLeft": Fore.BLUE,
            "MinerStarting": Fore.BLUE,
            "MinerMsgTime": Fore.BLUE
        }

        return "{} {} {}".format(color[self.mlog], self.msg, Style.RESET_ALL)
