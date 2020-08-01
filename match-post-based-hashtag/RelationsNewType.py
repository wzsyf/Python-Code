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
            if limit > 0 and countVideo >= limit:
                break
            self.postVideoIdsDic[email] = postId


    def UpdateRelations(self, flags=[], minScore=0.4, limit=-1):
        bk = Backend()

        workWearArrs, loungeWearArrs, beachWearArrs = bk.PostsTypeHaveNoRelations(flags)
        typeDic = {}
        typeDic["Work Wear"] = workWearArrs
        typeDic["Lounge Wear"] = loungeWearArrs
        typeDic["Beach Wear"] = beachWearArrs

        self.imagePostsMatch(typeDic, minScore, limit)



    def imagePostsMatch(self, postsDic, minScore, limit = -1):

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

                    postId = post.get("id")
                    postDic[postId] = post

                    while True:

                        postDicKeyIds = postDic.keys()
                        random.shuffle(postDicKeyIds)

                        index = random.randint(0, len(postDicKeyIds) - 1)
                        postDickey = postDicKeyIds[index]

                        postDicValue = postDic.get(postDickey)

                        postIdOfDic = postDicValue.get("id")
                        image = postDicValue.get("image") or None

                        email = bk.queryEmailByPostId(postIdOfDic)

                        loginInfo = Voila.login(email, "demo")
                        auth = loginInfo.get("token")

                        print(postIdOfDic, email, key)

                        productsSimilar = VoilaGo.SearchSimilarProducts(image, minScore)
                        if len(productsSimilar) > 0:
                            print postIdOfDic, email
                            Voila.PostRelations(auth, postIdOfDic, productsSimilar)
                            if flag:
                                print ""
                                Voila.AddFlagToPost(postIdOfDic, flag)

                            self.postImageIdDic[postIdOfDic] = email

                            count += 1
                            result = True
                        if limit > 0 and count >= limit:
                            break


                postId = post.get("id")
                image = post.get("image") or None
                if not image:
                    continue

                email = bk.queryEmailByPostId(postId)
                if email in emailArr:
                    postDic[postId] = post
                    continue
                emailArr.append(email)



                loginInfo = Voila.login(email, "demo")
                auth = loginInfo.get("token")

                print(postId, email, key)

                productsSimilar = VoilaGo.SearchSimilarProducts(image, minScore)
                if len(productsSimilar) > 0:
                    print postId, email
                    Voila.PostRelations(auth, postId, productsSimilar)
                    if flag:
                        print ""
                        Voila.AddFlagToPost(postId, flag)

                    self.postImageIdDic[postId] = email

                    count += 1
                    result = True
                if limit > 0 and count >= limit:
                    break

        return result



    def postsEnable(self, email, pwd, postId):

        loginInfo = Voila.login(email, pwd)
        auth = loginInfo.get("token")

        Voila.EnablePost(auth, postId)



if __name__ == "__main__":

    rn = RelationsNews()
    bk = Backend()

    monthFlags = ["month-apr","month-may", "month-jun", "month-jul", "month-aug", "month-sept", "month-oct"]

    userVideoArrayList = {}

    userVideoArrayList["Petite"] = ["sarahmtimet", "fashioninflux", "sterlingmonett", "americanthreads", "brittany.xavier",
                                    "bustle", "katgu3rra", "isseyeehaw", "samiraradmehr", "summerrachelwarren",
                                    "jadeleslie99","kikalateef", "carolinehxr","maijakarppinen", "valerie_lisitsyna", "albinamart",
                                    "sophhirose", "shopddmine", "rachelward_e", "shandarogers_", "roanmclean"]
    userVideoArrayList["Fitness"] = ["naomiboyer", "jujhavens", "paudictado", "whatverowears", "maarvelous", "alexgeorgy",
                                     "bbycailey","hope.cee", "jessthrowiton", "kaylaseah","elizabethkando", "inthesejeans",
                                     "mscrisssy", "thais.talo"
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

    postIdKeys = []

    count = 0
    for emailImagePostKey in emailImagePostKeys:
        count = count + 1
        postIdKeys.append(emailImagePostKey)

        if count == 2:
            postIdKeys.append(randomEmailVideoPostKeys[0])
            postIdKeys.append(randomEmailVideoPostKeys[1])

        elif count == 5:
            postIdKeys.append(randomEmailVideoPostKeys[2])

        elif count == 8:
            postIdKeys.append(randomEmailVideoPostKeys[3])

        elif count == 10:
            postIdKeys.append(randomEmailVideoPostKeys[4])
            postIdKeys.append(randomEmailVideoPostKeys[5])

        elif count == 12:
            postIdKeys.append(randomEmailVideoPostKeys[6])

        elif count == 15:
            postIdKeys.append(randomEmailVideoPostKeys[7])

        elif count == 17:
            postIdKeys.append(randomEmailVideoPostKeys[8])


        elif count == 20:
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