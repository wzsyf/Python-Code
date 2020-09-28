#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from api import *


class ModifyTikTokUserName:


    def modifyTikTokUserName(self):


        for userName, email in self.userEmailsDic().items():


            # 注册用户
            Voila.register(email, userName, "demo")

            # 以注册的用户进行登陆
            loginInfo = Voila.login(email, "demo")
            # 获取登录验证时的token令牌
            auth = loginInfo.get("token")

            # 提交用户名
            Voila.PutAccount(auth, {"firstName": userName})


    def userEmailsDic(self):
        userEmails = {
            "sarahmtimet":"230@a.com",
            "fashioninflux":"231@a.com",
            "sterlingmonett":"232@a.com",
            "americanthreads":"233@a.com",
            "brittany.xavier":"234@a.com",
            "naomiboyer":"235@a.com",
            "jujhavens":"236@a.com",
            "paudictado":"237@a.com",
            "whatverowears":"238@a.com",
            "maarvelous":"239@a.com",
            "alexgeorgy":"240@a.com",
            "bustle":"241@a.com",
            "katgu3rra":"242@a.com",
            "isseyeehaw":"243@a.com",
            "samiraradmehr":"244@a.com",
            "summerrachelwarren":"245@a.com",
            "jadeleslie99":"246@a.com",
            "kikalateef":"247@a.com",
            "carolinehxr":"248@a.com",
            "maijakarppinen":"249@a.com",
            "valerie_lisitsyna":"250@a.com",
            "bbycailey":"251@a.com",
            "hope.cee":"252@a.com",
            "jessthrowiton":"253@a.com",
            "kaylaseah":"254@a.com",
            "elizabethkando":"255@a.com",
            "inthesejeans":"256@a.com",
            "mscrisssy":"257@a.com"
        }

        return userEmails


if __name__ == "__main__":
    mtu = ModifyTikTokUserName()
    mtu.modifyTikTokUserName()
