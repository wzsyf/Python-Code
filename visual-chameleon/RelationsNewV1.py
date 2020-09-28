#!/usr/bin/env python
# -*- coding: utf-8 -*-

from api import *
from user_emails import *
from slugify import slugify
from backend import *
import random


# data["slug"] = slugify(title)
class RelationsNews:
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
                self.postIdsDic[email] = postId

            #     Voila.EnablePost(auth, postId)
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

    rn = RelationsNews()

    monthFlags = ["month-jun", "month-jul", "month-aug"]

    # 图片帖子字典
    userImageArrayList = {}
    # 视频帖子字典
    userVideoArrayList = {}

    userImageArrayList["Petite Girls"] = ["poseandrepeat", "brit_harvey", "vivianeaudi", "amandampn", "cerecampbell",
                                     "annaastrup", "michelleinfusino", "chloemonchamp", "oliviabynature","belajuliana_",
                                    "mari_malibu", "victoriawaldau", "emmanuellek_", "shaniakufner_", "amyz_k", "saskia_freitas", "jetamoure",
                                    "bethanmccoy", "monmccallion", "syd.and.ash"]
    # userImageArrayList["Curves"] = ["noelledowning", "javierittaaa", "erikaaguileraa", "oshawaiters", "pinkbesos_", "shayzanco_",
    #                                 "janaegirard", "____mkay", "98smlc", "michellejulietnaylaa", "maryalicejenni", "sandra_salic",
    #                                 "baystayfit", "fashiononcurvy"]
    userImageArrayList["Good Shape"] = ["juliadamon", "soniaheartsfashion", "anpaulinas", "daniellemetz", "katherine_bondd",
                                   "ohheylisa_", "mariafedulova", "paulinenavy", "jessiefrizzell", "aliciabonora",
                                   "amyfuchsia", "aliciabonora", "amyfuchsia", "itslibes", "x_carms", "freyakillin",
                                   "taliacupcake", "okevaaa", "bresheppard", "nitsanraiter", "amyfuchsia",
                                   "jenniferxlauren"]
    userImageArrayList["Vintage Style"] = ["heyhegia", "bertillecnt", "frenchgirldaily", "ceciliemoosgaard", "ariadibari",
                                      "parisianvibe", "juliesfi", "ameliecheval31", "elaisaya", "solenelara",
                                      "chloehelenmiles", "larmoiredesoso", "sabrinacsari", "claudiagraziano",
                                      "yxcvanessa", "marvadel", "linneafunks", "modedamour", "lydiajanetomlinson",
                                      "sandrarossi03", "anoukyve", "apollinethibault", "fakerstrom",
                                      "lauraslittlelocket", "livia_auer", "filippahagg", "leasy_inparis", "andicsinger",
                                      "lestylealafrancaise", "tendancehunter"]
    userImageArrayList["Travel Style"] = ["lucyinthesskyy", "katie.one", "emilyrosehannon", "callia_m", "simona.julia", "margusha____"
                                          "lenasaibel", "lulouisaa", "annchristiiiin"]

    userImageArrayList["Fitness"] = ["juliadamon", "soniaheartsfashion", "anpaulinas", "daniellemetz", "katherine_bondd",
                                     "ohheylisa_", "mariafedulova", "paulinenavy", "jessiefrizzell", "aliciabonora",
                                     "amyfuchsia", "aliciabonora", "amyfuchsia", "itslibes", "x_carms", "freyakillin",
                                     "taliacupcake", "okevaaa", "bresheppard", "nitsanraiter", "amyfuchsia", "jenniferxlauren",
                                     "blakehealey", "ruby190", "bethanmccoy", "helenacritchley", "sophieottewell", "sarahjoholder",
                                     "charliemariedoe", "lradwell", "festus.marika", "salmabe__", "itsbee____", "dbzdutch", "lianatambini",
                                     "sophieottewell", "molly.mcfarlane", "yemayaguzman"]

    userImageArrayList["Street Style"] = ["streetstyle__outfits", "woman__streetstyles", "best_street_styles",
                                          "minimalstreetstyle", "street_style_corner"]

    userImageArrayList["Mixed"] = ["americanvibe", "dailyoutfits", "howtotstyle", "nikeaddict", "vanslovers",
                                   "coverselovers", "asosgirls", "fashionlady", "sheinlovers"]

    userVideoArrayList["Petite"] = ["sarahmtimet", "fashioninflux", "sterlingmonett", "americanthreads", "brittany.xavier",
                                    "bustle", "katgu3rra", "isseyeehaw", "samiraradmehr", "summerrachelwarren",
                                    "jadeleslie99","kikalateef", "carolinehxr","maijakarppinen", "valerie_lisitsyna", "albinamart", "sophhirose",
                                    "shopddmine", "rachelward_e", "shandarogers_", "roanmclean"]
    userVideoArrayList["Fitness"] = ["naomiboyer", "jujhavens", "paudictado", "whatverowears", "maarvelous", "alexgeorgy",
                                     "bbycailey","hope.cee", "jessthrowiton", "kaylaseah","elizabethkando", "inthesejeans", "mscrisssy", "thais.talo"
                                     ]

    # 图片帖子
    userFlagMap = {}
    for key, userArray in userImageArrayList.items():
        flag = slugify(key)
        for user in userArray:
            userFlagMap[user] = flag

    userLimit = 40
    userCount = 0
    users = userFlagMap.keys()
    print len(users)
    random.shuffle(users)


    for user in users:
        flag = userFlagMap.get(user) or None
        if not flag:
            continue

        email = userEmails.get(user) or None
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

    userVideoLimit = 11
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
            rn.UpLoadVideo(videoEmail, "demo", flag)

            userVideoCount += 1
            if userVideoCount >= userVideoLimit:
                break

    # 随机对图片帖子和视频帖子进行公开
    postIdDic = rn.postIdsDic

    randomEmailKeys = postIdDic.keys()
    random.shuffle(randomEmailKeys)

    for randomEmailKey in randomEmailKeys:
        postId = postIdDic.get(randomEmailKey)
        Voila.AddFlagToPost(postId, "popular-post")
        rn.postsEnable(randomEmailKey, "demo", postId)