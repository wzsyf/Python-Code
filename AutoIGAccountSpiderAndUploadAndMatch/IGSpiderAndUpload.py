#!/usr/bin/env python
# -*- coding: utf-8 -*-

from instagramUpload import *
from backend import *
import os

class IGSpiderAndUpload:

    def spiderIGAndUpload(self, igAccount, modifyEmail, modifyPwd):
        bk = Backend()
        cmd = "sh /home/ubuntu/projects/debug/VoilaGo/scripts/igSpider.sh {0}".format(igAccount)
        os.system(cmd)

        ir = InstagramReader()
        ir.getIGAccountAndUpload(igAccount)

        originalEmail, customerId = bk.getIGAccountEmail(igAccount)

        postArr, result = self.UpdateRelations(originalEmail, modifyEmail, modifyPwd, [], 0.51, None)
        self.postsEnable(modifyEmail, modifyPwd, postArr)



    # 图片帖子
    def UpdateRelations(self, originalEmail, modifyEmail, pwd, flags=[], minScore=0.4, flag=None):
        postArr = []

        bk = Backend()
        loginInfo = Voila.login(modifyEmail, pwd)
        auth = loginInfo.get("token")
        result = False

        # 图文帖子的相关信息
        postsNeedUpdate = bk.PostsHaveNoRelations(originalEmail, flags)
        for post in postsNeedUpdate:
            postId = post.get("id")
            image = post.get("image") or None
            if not image:
                continue
            productsSimilar = VoilaGo.SearchSimilarProducts(image, minScore)
            if len(productsSimilar) > 0:
                print postId, originalEmail
                Voila.PostRelations(auth, postId, productsSimilar)
                if flag:
                    Voila.AddFlagToPost(postId, flag)

                postArr.append(postId)


            refresh_token = loginInfo.get("refresh_token")
            _loginInfo = Voila.refresh_token(refresh_token)
            if _loginInfo:
                loginInfo = _loginInfo
            auth = loginInfo.get("token")


        return postArr, result

    # 对帖子进行公开
    def postsEnable(self, email, pwd, postArr):

        loginInfo = Voila.login(email, pwd)
        auth = loginInfo.get("token")

        for postId in postArr:
            # 对帖子进行公开
            Voila.EnablePost(auth, postId)

if __name__ == "__main__":
    igAccount = "shuaiyunzhang"
    isau = IGSpiderAndUpload()
    isau.spiderIGAndUpload(igAccount, "jorsion@foxmail.com", "123456")

