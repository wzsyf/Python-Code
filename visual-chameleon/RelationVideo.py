#!/usr/bin/env python

from api import *
from user_emails import *
from slugify import slugify
from backend import *
import random


# data["slug"] = slugify(title)
class RelationsVideo:
    postIdsDic = {}

    # 视频帖子
    def UpLoadVideo(self, email, pwd, flags=[],flag=None):
        bk = Backend()

        # 视频帖子的postId
        postsVideo = bk.PostVedio(email, flags)
        for postVideo in postsVideo:
            postId = postVideo.get("postId")

            if flag:
                Voila.AddFlagToPost(postId, flag)

            # 将视频帖子的帖子Id添加到帖子Id数组
            self.postIdsDic[email] = postId


    # 对帖子进行公开
    def postsEnable(self, email, pwd, postId):

        loginInfo = Voila.login(email, pwd)
        auth = loginInfo.get("token")

        bk = Backend()

        # 对帖子进行公开
        Voila.EnablePost(auth, postId)

        bk.randomVideoUpdateTime(postId)



if __name__ == "__main__":

    rv = RelationsVideo()

    monthFlags = ["month-apr", "month-may", "month-jun", "month-jul", "month-aug", "month-sept", "month-oct"]

    # 视频帖子字典
    userVideoArrayList = {}

    userVideoArrayList["Petite"] = ["sarahmtimet", "fashioninflux", "sterlingmonett", "americanthreads", "brittany.xavier"]
    userVideoArrayList["Fitness"] = ["naomiboyer", "jujhavens", "paudictado", "whatverowears", "maarvelous", "alexgeorgy"]


    # 视频帖子
    userVideoFlagMap = {}
    for key, userArray in userVideoArrayList.items():
        flag = slugify(key)
        for user in userArray:
            userVideoFlagMap[user] = flag

    userVideoLimit = 10
    userVideoCount = 0
    userVideos = userVideoFlagMap.keys()
    print len(userVideos)
    random.shuffle(userVideos)

    for userVideo in userVideos:
        flag = userVideoFlagMap.get(userVideo) or None
        if not flag:
            continue

        videoEmail = userEmails.get(userVideo) or None
        if videoEmail:
            rv.UpLoadVideo(videoEmail, "demo", flag)

            userVideoCount += 1
            if userVideoCount >= userVideoLimit:
                break

    # 随机对图片帖子和视频帖子进行公开
    postIdDic = rv.postIdsDic

    randomEmailKeys = postIdDic.keys()
    random.shuffle(randomEmailKeys)

    for randomEmailKey in randomEmailKeys:
        postId = postIdDic.get(randomEmailKey)
        Voila.AddFlagToPost(postId, "popular-post")
        rv.postsEnable(randomEmailKey, "demo", postId)