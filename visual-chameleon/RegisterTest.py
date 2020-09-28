#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import subprocess
import re
import requests
import hashlib

from api import *
# from user_map import *
from user_emails import *
from keep_flags import *
from backend import *



class InstagramReader:
    rootDir = "/home/ec2-user/tiktok"

    def __init__(self):
        pass


    def single_instagramer(self, rootDir, userName, email):
        path = os.path.join(rootDir, userName)
        print userName, email

        resp = Voila.register(email, userName, "demo")
        print resp
        loginInfo = Voila.login(email, "demo")
        auth = loginInfo.get("token")

        jsonFile = os.path.join(path, "{0}.json".format(userName))

        with open(jsonFile) as JSOnFile:
            data1 = JSOnFile.read()
            data2 = json.loads(data1)

            avatarImgResp = requests.get(data2['avatar']).content
            avatarImgPath = os.path.join(path, "{0}.jpg".format(userName))
            with open(avatarImgPath, 'wb') as f:
                f.write(avatarImgResp)

            res = Voila.PostAvatar(auth, avatarImgPath)
            print res

            cmd = "rm {0}".format(avatarImgPath)
            os.system(cmd)


    def all_instagramer(self):

        usersArr = ["lynntamis"]
        for root, dirs, files in os.walk(self.rootDir):
            for f in dirs:

                if not f in usersArr:
                    continue
                email = userEmails.get(f) or None
                if not email:
                    continue

                self.single_instagramer(self.rootDir, f, email)


if __name__ == "__main__":
    ir = InstagramReader()
    ir.all_instagramer()
