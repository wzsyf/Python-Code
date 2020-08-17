#!/usr/bin/env python

from api import *
from user_emails import *
from slugify import slugify
from backend import *
import random


# data["slug"] = slugify(title)
class RelationsNewV3:
    postVideoIdsDic = {}
    postImageIdDic = {}

    # 视频帖子
    def UpLoadVideo(self, email, flag=None, limit=-1):
        bk = Backend()

        countVideo = 0
        # 视频帖子的postId
        postsVideo = bk.PostVedio(email)
        for postVideo in postsVideo:
            postId = postVideo.get("postId")
            if flag:
                Voila.AddFlagToPost(postId, flag)
                countVideo += 1

                self.postVideoIdsDic[email] = postId
            if limit > 0 and countVideo >= limit:
                break

    # 图片帖子
    def UpdateRelations(self, email, pwd, flags=[], minScore=0.4, flag=None, limit=-1):
        bk = Backend()
        loginInfo = Voila.login(email, pwd)
        auth = loginInfo.get("token")
        result = False

        # 图文帖子的相关信息
        postsNeedUpdate = bk.PostsHaveNoRelations(email, flags)
        count = 0
        for post in postsNeedUpdate:
            postId = post.get("id")
            image = post.get("image") or None
            if not image:
                continue
            productsSimilar = VoilaGo.SearchSimilarProducts(image, minScore)
            if len(productsSimilar) > 0:
                print postId, email
                Voila.PostRelations(auth, postId, productsSimilar)
                if flag:
                    Voila.AddFlagToPost(postId, flag)

                # 将图文帖子添加到帖子Id数组
                self.postImageIdDic[postId] = email

                count += 1
                result = True
            if limit > 0 and count >= limit:
                break

            refresh_token = loginInfo.get("refresh_token")
            _loginInfo = Voila.refresh_token(refresh_token)
            if _loginInfo:
                loginInfo = _loginInfo
            auth = loginInfo.get("token")

            # result = True

        return result

    # 对帖子进行公开
    def postsEnable(self, email, pwd, postId):

        loginInfo = Voila.login(email, pwd)
        auth = loginInfo.get("token")

        # 对帖子进行公开
        Voila.EnablePost(auth, postId)


if __name__ == "__main__":

    rn = RelationsNewV3()

    monthFlags = ["month-apr", "month-may", "month-jun", "month-jul", "month-aug", "month-sept", "month-oct"]

    # 图片帖子字典
    userImageArrayList = {}
    # 视频帖子字典
    userVideoArrayList = {}

    userImageArrayList["petite"] = ["kennedyfrazer", "fashion_jackson", "itsallchictome", "audreymadstowe",
                                    "almost_readyblog", "karinastylediaries", "_thefab3", "styleandlatte",
                                    "brittanypuerto", "lglora", "heatherpoppie", "taymbrown", "almost_readyblog",
                                    "kristincpressley", "shealeighmills", "rubyholley_", "solarpowered_blonde",
                                    "indiaamoon", "twentiesgirlstyle", "shopdandy", "lisa.onuoha", "lawoffashionblog",
                                    "mataleiataua", "onesmallblonde", "sandycarvs", "uniquelyjulz"]

    userVideoArrayList["petite"] = ["sarahmtimet", "sterlingmonett", "brittany.xavier",
                                    "bustle", "katgu3rra", "isseyeehaw", "samiraradmehr", "summerrachelwarren",
                                    "jadeleslie99", "kikalateef", "carolinehxr", "maijakarppinen", "valerie_lisitsyna",
                                    "sophhirose", "shopddmine", "rachelward_e", "shandarogers_", "roanmclean"]
    userVideoArrayList["fitness"] = ["naomiboyer", "alexgeorgy", "bbycailey", "hope.cee", "jessthrowiton",
                                     "kaylaseah", "elizabethkando", "inthesejeans", "mscrisssy", "thais.talo"
                                     ]

    bumpEmail = userEmails.get("maternitywear") or None
    result = rn.UpdateRelations(bumpEmail, "demo", monthFlags, 0.51, "bump-style", 1)

    # 图片帖子
    userFlagMap = {}
    for key, userArray in userImageArrayList.items():
        flag = slugify(key)
        for user in userArray:
            userFlagMap[user] = flag

    userLimit = 19
    userCount = 0
    users = userFlagMap.keys()
    print len(users)
    random.shuffle(users)

    for user in users:
        flag = userFlagMap.get(user) or None
        if not flag:
            continue

        email = userEmails.get(user) or None
        print email
        if email:
            result = rn.UpdateRelations(email, "demo", monthFlags, 0.51, flag, 1)

            if result:
                userCount += 1
                if userCount >= userLimit:
                    break

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
            rn.UpLoadVideo(videoEmail, flag, 1)

            userVideoCount += 1
            if userVideoCount >= userVideoLimit:
                break

    # 随机对图片帖子和视频帖子进行公开
    postVideoIdsMap = rn.postVideoIdsDic
    postImageIdMap = rn.postImageIdDic

    randomEmailVideoPostKeys = postVideoIdsMap.keys()
    random.shuffle(randomEmailVideoPostKeys)

    emailImagePostKeys = postImageIdMap.keys()
    random.shuffle(emailImagePostKeys)
    random.shuffle(emailImagePostKeys)

    postIdKeys = []
    emailVideoLen = len(randomEmailVideoPostKeys)

    count = 0
    for emailImagePostKey in emailImagePostKeys:
        count = count + 1
        postIdKeys.append(emailImagePostKey)

        if count == 2:
            if (emailVideoLen - 1) > 1:
                postIdKeys.append(randomEmailVideoPostKeys[0])
                postIdKeys.append(randomEmailVideoPostKeys[1])

        elif count == 3:
            if (emailVideoLen - 1) > 2:
                postIdKeys.append(randomEmailVideoPostKeys[2])

        elif count == 5:
            if (emailVideoLen - 1) > 3:
                postIdKeys.append(randomEmailVideoPostKeys[3])

        elif count == 8:
            if (emailVideoLen - 1) > 5:
                postIdKeys.append(randomEmailVideoPostKeys[4])
                postIdKeys.append(randomEmailVideoPostKeys[5])

        elif count == 11:
            if (emailVideoLen - 1) > 6:
                postIdKeys.append(randomEmailVideoPostKeys[6])

        elif count == 13:
            if (emailVideoLen - 1) > 7:
                postIdKeys.append(randomEmailVideoPostKeys[7])

        elif count == 15:
            if (emailVideoLen - 1) > 8:
                postIdKeys.append(randomEmailVideoPostKeys[8])


        elif count == 17:
            if (emailVideoLen - 1) > 9:
                postIdKeys.append(randomEmailVideoPostKeys[9])

    for postIdKey in postIdKeys:

        postImageEmail = postImageIdMap.get(postIdKey)

        if postImageEmail is None:
            postVideoId = postVideoIdsMap.get(postIdKey)
            Voila.AddFlagToPost(postVideoId, "popular-post")
            rn.postsEnable(postIdKey, "demo", postVideoId)
        else:
            Voila.AddFlagToPost(postIdKey, "popular-post")
            rn.postsEnable(postImageEmail, "demo", postIdKey)