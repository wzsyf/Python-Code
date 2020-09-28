#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from api import *


class ModifyMultiUser:

    root = "/home/ec2-user/task3_0420"

    def modifyMultiUser(self):


        for userName, email in self.userEmailsDic().items():

            # 已知路径和用户名成做拼接，组成抓取用户的用户目录的路径
            path = os.path.join(self.root, userName)


            # 父用户的头像图片的位置
            fatherUserImage = os.path.join(path, "{0}.jpg".format(userName))

            # 以注册的用户进行登陆
            loginInfo = Voila.login(email, "demo")
            # 获取登录验证时的token令牌
            auth = loginInfo.get("token")

            # 判断父用户头像图片是否存在，若存在则进行上传
            if os.path.isfile(fatherUserImage):
                Voila.PostAvatar(auth, fatherUserImage)


    def userEmailsDic(self):
        userEmails = {
            "rubyholley_": "312@a.com"
        }

        return userEmails


if __name__ == "__main__":
    mmu = ModifyMultiUser()
    mmu.modifyMultiUser()
