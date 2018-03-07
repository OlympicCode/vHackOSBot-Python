#!/usr/bin/python2.7
# -*- coding: utf-8

import base64
import hashlib
import time
import requests
import ssl
import logging
import json
import ruamel.yaml as yaml
from ruamel.yaml.scalarstring import SingleQuotedScalarString, DoubleQuotedScalarString
import sys
import io
#logger = logging.getLogger(__name__)

# open configuration
with open("config.yml", 'r') as stream:
    try:
        Configuration = yaml.load(stream, Loader=yaml.RoundTripLoader)
    except yaml.YAMLError as exc:
        print("{} [{}]".format("Error in your config.yml please check in", exc))


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


USER_AGENT = ['Dalvik/2.1.0 (Linux; U; Android 5.0.1; GT-I9508V Build/LRX22C)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.1; MX4 Build/LRX22C)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; D5322 Build/19.3.A.0.472)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; D816w Build/LRX22G)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; HTC D816v Build/LRX22G)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; HTC E9pw Build/LRX22G)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; HTC M8t Build/LRX22G)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; HTC One M8s Build/LRX22G)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; LG-F320L Build/LRX22G)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; Letv X500 Build/DBXCNOP5500912251S)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; Nexus 5 Build/LRX22G)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; SM-N9005 Build/LRX22G)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0; ASUS_Z00ADB Build/LRX21V)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0; Nexus 5 Build/LPX13D)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1 Build/LYZ28N)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; 2014811 MIUI/6.1.26)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; A0001 Build/LMY47V)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; A0001 Build/LMY48Y)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; D5833 Build/23.4.A.1.232)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; GT-I9152 Build/LMY48Y)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; LG-D802 Build/LMY48W)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; MI 2 Build/LMY48B)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; MI 2SC Build/LMY47V)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; MI 3 Build/LMY48Y)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Mi-4c MIUI/6.1.14)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; NX403A Build/LMY48Y)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; ONE A2001 Build/LMY47V)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; R7Plusm Build/LMY47V)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Redmi Note 2 Build/LMY48Y)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-J3109 Build/LMY47X)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-N9200 Build/LMY47X)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Sparkle V Build/LMY47V)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Xperia Z2 Build/LMY48Y)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; titan Build/LMY48W)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; HTC M9w Build/LMY47O)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; HTC One M9 Build/LMY47O)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; LG-H818 Build/LMY47D)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; MX5 Build/LMY47I)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; XT1060 Build/LPA23.12-39.7)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; XT1085 Build/LPE23.32-53)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; m1 note Build/LMY47D)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; m2 Build/LMY47D)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; m2 note Build/LMY47D)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; 2014813 Build/MMB29U)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; A0001 Build/MMB29M)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; ASUS_Z00A Build/MMB29T)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MI 4LTE Build/MMB29M)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Mi-4c Build/MMB29U)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Moto G 2014 Build/MMB29M)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Moto G 2014 LTE Build/MMB29T)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus 4 Build/MMB29M)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus 5 Build/MMB29K)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Sensation Build/MMB29U)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Z1 Build/MMB29T)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0; MI 2 Build/MRA58K)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0; MI 2A Build/MRA58K)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0; Moto G 2014 Build/MDB08M)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0; XT1097 Build/MPE24.49-18)']


class Utils:
    def __init__(self):
        self.secret = "aeffI"
        self.url = "https://api.vhack.cc/mobile/6/"
        self.username = Configuration["username"]
        self.password = Configuration["password"]
        if self.username is None or self.password is None:
          print("please Change Username/Password to config.yml")
          exit(0)
        self.user_agent = self.generateUA(self.username + self.password)
        try:
            self.accessToken = Configuration["accessToken"]
        except:
            self.accessToken = None
        try:
            self.uID = Configuration["uID"]
        except KeyError: 
            self.uID = None

    def generateUA(self, identifier):
        pick = int(self.md5hash(identifier), 16)
        user_agents = tuple(USER_AGENT)
        return user_agents[pick % len(user_agents)]

    def getTime(self):
        return int(round(time.time()))

    def md5hash(self, txt):
        m = hashlib.md5()
        m.update(txt.encode('utf-8'))
        return m.hexdigest()

    def generateUser(self, bArr):
        b64 = base64.urlsafe_b64encode(bArr.encode('UTF-8')).decode('ascii')
        return b64.replace("=", "")

    def Login(self, php, username, password):

        passmd5 = self.md5hash(password)
        jsonString = {'username': username, 'password': passmd5}
        jsonString = json.dumps(jsonString, separators=(',', ':'))

        str8 = self.md5hash("{}{}{}".format(jsonString, jsonString,
                                            self.md5hash(jsonString)))

        return "{}{}?user={}&pass={}".format(self.url, php, 
                                             self.generateUser(jsonString), str8)

    def generateURL(self, uid, php, **kwargs):
        jsonString = {'uid': self.uID, 'accesstoken': str(self.accessToken)}
        jsonString = json.dumps(jsonString, default=set_default)

        str8 = self.md5hash("{}{}{}".format(jsonString, jsonString,
                                            self.md5hash(jsonString)))

        return "{}{}?user={}&pass={}".format(self.url, php, self.generateUser(jsonString), str8)

    def CheckServerError(self, code_return):
        try:
          code_return = code_return["result"]
        except (TypeError, IndexError):
          code_return = 0

        t = None
        if code_return == u"5":
            t = (5, "Check your Internet.")
        elif code_return == u"8":
            t = (8, "User/Password wrong!")
        elif code_return == u"10": 
            t = (10, "API is updated.")
        elif code_return == u"15":
            t = (10, "You are Banned sorry :(")
        elif code_return == u"99":
            t = (99, "Server is down for Maintenance, please be patient.")
        return t

    def requestString(self, php, **kwargs):
        # print("Request: {}, {}".format(php, self.uID))
        self.user_agent = self.generateUA("testtest")
        time.sleep(0.5)
        i = 0
        while True:
            if i > 10:
                exit(0)
            if self.uID is None or self.accessToken is None:
                # connect login.
                request = requests.Session()
                request.headers.update({'User-agent': self.user_agent})
                url_login = self.Login('login.php', self.username, self.password)
                result = request.get(url_login)
                result.encoding = 'UTF-8'
                parseJson = result.json()

                check_return_server = self.CheckServerError(parseJson)
                if check_return_server is not None:
                    return "Server Error: [{}] {}".format(check_return_server[0], check_return_server[1])

                self.accessToken = str(parseJson["accesstoken"])
                self.uID = int(parseJson["uid"].encode("UTF-8"))

                # append uID/accessToken in configuration file.
                Configuration['username'] = self.username
                Configuration['password'] = self.password
                Configuration['uID'] = self.uID
                Configuration['accessToken'] = self.accessToken
                
                Configuration.yaml_add_eol_comment("# <- Your Username Account", 'username', column=5)
                Configuration.yaml_add_eol_comment("# <- Tour Password Account\n\n", 'password', column=5)
                Configuration.yaml_add_eol_comment("# <- Automatical uID for your account don't change /!\\", 'uID', column=5)
                Configuration.yaml_add_eol_comment("# <- Automatical accessToken for your account don't change /!\\", 'accessToken', column=5)
                with io.open('config.yml', 'w') as outfile:
                    yaml.dump(Configuration, stream=outfile, default_flow_style=False, Dumper=yaml.RoundTripDumper, indent=4, block_seq_indent=1)
              
                # Create First request.
                result = request.get(self.generateURL(self.uID, php, **kwargs))
                return result.text

            else:
                request = requests.Session()
                request.headers.update({'User-agent': self.user_agent})
                
                # return just request don't login before.
                result = request.get(self.generateURL(self.uID, php, **kwargs))
                result.encoding = 'UTF-8'
                parseJson = result.json()
                try:
                   self.accessToken = str(parseJson["accesstoken"])
                except KeyError:
                   pass

            i = i + 1
            return result.text