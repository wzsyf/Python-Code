#!/usr/bin/env python

from api import *
from user_emails import *
from slugify import slugify
from backend import *
import random

class MatchNewUser:


    def newUserRegisterAndLogin(self, email, userName):
        Voila.register(email, userName, "demo")

        loginInfo = Voila.login(email, "demo")
        auth = loginInfo.get("token")

        # 提交用户名
        Voila.PutAccount(auth, {"firstName": userName})


    def oldUserAndNewUserRelation(self):
        oldUser2NewUserDic = {}

        oldUser2NewUserDic["266@a.com"] = ["301@a.com", "302@a.com", "303@a.com"]
        oldUser2NewUserDic["268@a.com"] = ["304@a.com", "305@a.com", "306@a.com"]

        return oldUser2NewUserDic


    def emailOfNewUser(self):

        newUser2Email = {}

        newUser2Email["workstyle"] = ["301@a.com"]
        newUser2Email["dailyworkwear"] = ["302@a.com"]
        newUser2Email["chicworkwear"] = ["303@a.com"]
        newUser2Email["swimwear"] = ["304@a.com"]
        newUser2Email["beachstyle"] = ["305@a.com"]
        newUser2Email["bikinistyle"] = ["306@a.com"]

        return newUser2Email


if __name__ == "__main__":

    mnu = MatchNewUser()

    newUser2Email = mnu.emailOfNewUser()
    for userNameKey, emailValue in newUser2Email.items():
        mnu.newUserRegisterAndLogin(emailValue, userNameKey)