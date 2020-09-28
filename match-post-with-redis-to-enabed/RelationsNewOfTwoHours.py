#!/usr/bin/env python
# -*- coding: utf-8 -*-

from backend import *
from api import *
from RelationsNewV5 import *
from redis import StrictRedis, ConnectionPool

class RelationsNewOfTwoHours:

    pool = ConnectionPool(host='localhost', port=3001, db=0)
    redis = StrictRedis(connection_pool=pool)

    # 对帖子进行公开
    def postsEnable(self, email, pwd, postId):
        loginInfo = Voila.login(email, pwd)
        auth = loginInfo.get("token")

        # 为帖子添加"popular-post"的flag
        Voila.AddFlagToPost(postId, "popular-post")
        # 对帖子进行公开
        Voila.EnablePost(auth, postId)



    def getPostIdOfPreTwo(self):

        bk = Backend()
        postId1 = self.redis.lpop("postId")
        postId2 = self.redis.lpop("postId")

        email1 = bk.getEmailOfPostId(postId1)
        email2 = bk.getEmailOfPostId(postId2)

        self.postsEnable(email1, "demo", postId1)
        self.postsEnable(email2, "demo", postId2)


    def enbaledPostOfPreTwo(self):

        resArr = self.redis.lrange("postId", 0, 50)
        resArrLen = len(resArr)

        if resArrLen <= 1:
            rn = RelationsNewV5()
            rn.matchPost()
            self.getPostIdOfPreTwo()

        else:
            self.getPostIdOfPreTwo()


if __name__ == '__main__':

    rnoth = RelationsNewOfTwoHours()

    rnoth.enbaledPostOfPreTwo()
    rnoth.redis.close()

