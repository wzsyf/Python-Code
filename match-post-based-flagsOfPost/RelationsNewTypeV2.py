#!/usr/bin/env python

from api import *
from user_emails import *
from slugify import slugify
from backend import *
import random


class RelationsNews:
    postVideoIdsDic = {}
    postImageIdDic = {}

    # 视频帖子
    def UpLoadVideo(self, email, flag=None, limit = -1):
        bk = Backend()

        countVideo = 0
        postsVideo = bk.PostVedio(email)
        for postVideo in postsVideo:
            postId = postVideo.get("postId")
            if flag:
                print ""
                Voila.AddFlagToPost(postId, flag)
                countVideo += 1

                self.postVideoIdsDic[email] = postId
            if limit > 0 and countVideo >= limit:
                break


    def UpdateRelations(self, flags=[], minScore=0.4, limit=-1):
        bk = Backend()

        vintageStyleArr, streetStyleArr, travelStyleArr = bk.PostsTypeHaveNoRelations(flags)
        typeDic = {}
        typeDic["vintage-style"] = vintageStyleArr
        typeDic["street-style"] = streetStyleArr
        typeDic["travel-style"] = travelStyleArr

        self.imagePostsMatch(typeDic, minScore, limit)



    def imagePostsMatch(self, postsDic, minScore, limit = -1):

        disabledEmailArr = ["99@a.com", "100@a.com", "101@a.com", "102@a.com", "196@a.com",
                            "197@a.com", "198@a.com", "199@a.com", "200@a.com", "201@a.com",
                            "202@a.com", "203@a.com", "204@a.com", "217@a.com"]
        bk = Backend()

        for key, arr in postsDic.items():

            flag = slugify(key)

            count = 0
            emailArr = []
            postDic = {}
            arrLen = len(arr)

            random.shuffle(arr)

            for post in arr:
                arrLen = arrLen - 1

                if arrLen == 1 and count < 10:
                    print("bugou")
                    postId = post.get("id")
                    lastEmail = bk.queryEmailByPostId(postId)

                    lastArr = postDic.get(lastEmail)
                    if lastArr is None:
                        postsArr = []
                        postsArr.append(post)
                        postDic[lastEmail] = postsArr
                    else:
                        lastArr.append(post)
                        postDic[lastEmail] = lastArr

                    postDicKeyEmails = postDic.keys()
                    postDicKeyEmailsLen = len(postDicKeyEmails)
                    postDicKeyEmailsIndexLen = postDicKeyEmailsLen - 1
                    while True:

                        print postDicKeyEmails

                        if postDicKeyEmailsIndexLen == -1:
                            postDicKeyEmailsIndexLen = postDicKeyEmailsLen - 1

                        email = postDicKeyEmails[postDicKeyEmailsIndexLen]
                        postDicKeyEmailsIndexLen -= 1
                        print email
                        postArr = postDic.get(email)

                        postDicValue = postArr[random.randint(0, len(postArr) - 1)]

                        postIdOfDic = postDicValue.get("id")
                        image = postDicValue.get("image") or None

                        loginInfo = Voila.login(email, "demo")
                        auth = loginInfo.get("token")

                        print(postIdOfDic, email, key)

                        result = bk.judgePostIsMatchProduct(postIdOfDic)
                        if len(result) > 0:
                            print("yi-pi-pei")
                            count += 1
                            self.postImageIdDic[postIdOfDic] = email
                            print count
                            if limit > 0 and count >= limit:
                                break
                        else:
                            print("wei-pi-pei")
                            productsSimilar = VoilaGo.SearchSimilarProducts(image, minScore)
                            if len(productsSimilar) > 0:
                                print postIdOfDic, email
                                Voila.PostRelations(auth, postIdOfDic, productsSimilar)
                                # if flag:
                                #     print ""
                                #     Voila.AddFlagToPost(postIdOfDic, flag)

                                self.postImageIdDic[postIdOfDic] = email

                                count += 1
                                print count
                            if limit > 0 and count >= limit:
                                break


                postId = post.get("id")
                image = post.get("image") or None
                if not image:
                    continue

                email = bk.queryEmailByPostId(postId)
                if email in disabledEmailArr:
                    continue

                if email in emailArr:
                    arr = postDic.get(email)
                    if arr is None:
                        postsArr = []
                        postsArr.append(post)
                        postDic[email] = postsArr
                    else:
                        arr.append(post)
                        postDic[email] = arr

                    continue
                emailArr.append(email)
                print emailArr


                loginInfo = Voila.login(email, "demo")
                auth = loginInfo.get("token")

                print(postId, email, key)

                res = bk.judgePostIsMatchProduct(postId)
                if len(res) != 0:
                    count += 1
                    self.postImageIdDic[postId] = email

                    if limit > 0 and count >= limit:
                        break

                else:

                    productsSimilar = VoilaGo.SearchSimilarProducts(image, minScore)
                    if len(productsSimilar) > 0:
                        print postId, email
                        Voila.PostRelations(auth, postId, productsSimilar)
                        # if flag:
                        #     print ""
                        #     Voila.AddFlagToPost(postId, flag)

                        self.postImageIdDic[postId] = email

                        count += 1
                    if limit > 0 and count >= limit:
                        break




    def postsEnable(self, email, pwd, postId):

        loginInfo = Voila.login(email, pwd)
        auth = loginInfo.get("token")

        Voila.EnablePost(auth, postId)



if __name__ == "__main__":

    rn = RelationsNews()
    bk = Backend()

    monthFlags = ["month-apr","month-may", "month-jun", "month-jul", "month-aug", "month-sept", "month-oct"]

    userVideoArrayList = {}

    userVideoArrayList["petite"] = ["sarahmtimet", "sterlingmonett", "brittany.xavier",
                                    "bustle", "katgu3rra", "isseyeehaw", "samiraradmehr", "summerrachelwarren",
                                    "jadeleslie99","kikalateef", "carolinehxr","maijakarppinen", "valerie_lisitsyna",
                                    "sophhirose", "shopddmine", "rachelward_e", "shandarogers_", "roanmclean"]
    userVideoArrayList["fitness"] = ["naomiboyer", "alexgeorgy","bbycailey","hope.cee", "jessthrowiton",
                                     "kaylaseah","elizabethkando", "inthesejeans","mscrisssy", "thais.talo"
                                     ]



    result = rn.UpdateRelations(monthFlags, 0.51, 10)



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

        if count == 3:
            if (emailVideoLen - 1) > 1:
                postIdKeys.append(randomEmailVideoPostKeys[0])
                postIdKeys.append(randomEmailVideoPostKeys[1])

        elif count == 6:
            if (emailVideoLen - 1) > 2:
                postIdKeys.append(randomEmailVideoPostKeys[2])

        elif count == 9:
            if (emailVideoLen - 1) > 3:
                postIdKeys.append(randomEmailVideoPostKeys[3])

        elif count == 12:
            if (emailVideoLen - 1) > 5:
                postIdKeys.append(randomEmailVideoPostKeys[4])
                postIdKeys.append(randomEmailVideoPostKeys[5])

        elif count == 15:
            if (emailVideoLen - 1) > 6:
                postIdKeys.append(randomEmailVideoPostKeys[6])

        elif count == 18:
            if (emailVideoLen - 1) > 7:
                postIdKeys.append(randomEmailVideoPostKeys[7])

        elif count == 21:
            if (emailVideoLen - 1) > 8:
                postIdKeys.append(randomEmailVideoPostKeys[8])

        elif count == 24:
            if (emailVideoLen - 1) > 9:
                postIdKeys.append(randomEmailVideoPostKeys[9])


    for postIdKey in postIdKeys:

        postImageEmail = postImageIdMap.get(postIdKey)

        if postImageEmail is None:
            postVideoId = postVideoIdsMap.get(postIdKey)
            Voila.AddFlagToPost(postVideoId, "popular-post")
            rn.postsEnable(postIdKey, "demo", postVideoId)
        else:
            print ""
            Voila.AddFlagToPost(postIdKey, "popular-post")
            rn.postsEnable(postImageEmail, "demo", postIdKey)