#!/usr/bin/env python
# -*- coding: utf-8 -*-

from api import *
from user_emails import *
from slugify import slugify
from backend import *
import random

from redis import StrictRedis, ConnectionPool



class RelationsNewV5:

    pool = ConnectionPool(host='localhost', port=3001, db=0)
    redis = StrictRedis(connection_pool=pool)

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



    def matchPost(self):

        monthFlags = ["month-apr", "month-may", "month-jun", "month-jul", "month-aug", "month-sept", "month-oct"]

        # 图片帖子字典
        userImageArrayList = {}
        # 视频帖子字典
        userVideoArrayList = {}

        userImageArrayList["petite"] = ["poseandrepeat", "brit_harvey", "vivianeaudi", "amandampn", "cerecampbell",
                                        "annaastrup", "michelleinfusino", "chloemonchamp", "oliviabynature",
                                        "belajuliana_",
                                        "mari_malibu", "victoriawaldau", "emmanuellek_", "shaniakufner_", "amyz_k",
                                        "saskia_freitas", "jetamoure", "bethanmccoy", "monmccallion", "syd.and.ash",
                                        "katherine_bondd",
                                        "freyakillin", "dariafoldes", "lena.summer.fashion", "danielleebrownn",
                                        "jamielynkane",
                                        "denimcdermott", "kazkamwi", "dee_opaleye", "sallyhildi", "elaisaya",
                                        "sabrinacsari",
                                        "claudiagraziano", "fakerstrom", "lauraslittlelocket", "sandrarossi03",
                                        "lydiajanetomlinson",
                                        "linneafunks", "marvadel", "yxcvanessa", "chloehelenmiles", "ameliecheval31",
                                        "solenelara",
                                        "ariadibari", "frenchgirldaily", "bertillecnt", "juliesfi",
                                        "lestylealafrancaise", "modedamour",
                                        "andicsinger", "kennedyfrazer", "fashion_jackson", "itsallchictome",
                                        "audreymadstowe",
                                        "almost_readyblog", "karinastylediaries", "_thefab3", "styleandlatte",
                                        "brittanypuerto", "lglora", "heatherpoppie", "taymbrown", "almost_readyblog",
                                        "kristincpressley", "shealeighmills", "rubyholley_", "solarpowered_blonde",
                                        "indiaamoon", "twentiesgirlstyle", "shopdandy", "lisa.onuoha",
                                        "lawoffashionblog",
                                        "mataleiataua", "onesmallblonde", "sandycarvs", "uniquelyjulz", "jscott24",
                                        "brantlywyatt", "natalie_keinan", "jademariekingxx", "hattiebourn",
                                        "tessa_port",
                                        "cellajaneblog", "daphnie.pearl", "anniepapi", "livguy_", "courtcdavis",
                                        "theeditbutton",
                                        "americanvibe", "dailyoutfits", "howtotstyle"]

        userImageArrayList["fitness"] = ["juliadamon", "soniaheartsfashion", "anpaulinas", "daniellemetz",
                                         "katherine_bondd", "ohheylisa_", "mariafedulova", "paulinenavy",
                                         "jessiefrizzell", "aliciabonora",
                                         "amyfuchsia", "aliciabonora", "amyfuchsia", "itslibes", "x_carms",
                                         "freyakillin",
                                         "taliacupcake", "okevaaa", "bresheppard", "nitsanraiter", "amyfuchsia",
                                         "jenniferxlauren",
                                         "blakehealey", "ruby190", "bethanmccoy", "helenacritchley", "sophieottewell",
                                         "sarahjoholder",
                                         "charliemariedoe", "lradwell", "festus.marika", "itsbee____",
                                         "dbzdutch", "lianatambini",
                                         "sophieottewell", "molly.mcfarlane", "yemayaguzman", "deboragabriella_",
                                         "vitaliia", "alexxcoll"]

        userImageArrayList["bump-style"] = ["maternitywear"]

        userImageArrayList["vintage-style"] = ["tendancehunter", "shirinatra", "_constance_d", "audreyrivet"]

        userImageArrayList["Street Style"] = ["streetstyle__outfits", "woman__streetstyles",
                                              "best_street_styles", "minimalstreetstyle", "street_style_corner"]

        userImageArrayList["travel-style"] = ["katie.one", "emilyrosehannon", "callia_m",
                                              "simona.julia", "margusha____", "lenasaibel", "lulouisaa",
                                              "annchristiiiin"]

        userImageArrayList["workwear"] = ["ewelinakanty", "asaqueenatwork", "voilaworkstyle", "workstyle",
                                          "dailyworkwear", "chicworkwear"]

        userImageArrayList["beachwear"] = ["asaqueenatbeach", "voilabeachstyle", "swimwear", "beachstyle",
                                           "bikinistyle"]

        userImageArrayList["party-wear"] = ["asaqueenatparty"]

        userImageArrayList["vans"] = ["vanslovers"]

        userImageArrayList["nike"] = ["nikeaddict"]

        userImageArrayList["converse"] = ["coverselovers"]

        userImageArrayList["asos"] = ["asosgirls"]

        userImageArrayList["style"] = ["fashionlady"]

        userImageArrayList["shein"] = ["sheinlovers"]

        userVideoArrayList["petite"] = ["sarahmtimet", "sterlingmonett", "brittany.xavier",
                                        "bustle", "katgu3rra", "isseyeehaw", "samiraradmehr", "summerrachelwarren",
                                        "jadeleslie99", "kikalateef", "carolinehxr", "maijakarppinen",
                                        "valerie_lisitsyna",
                                        "sophhirose", "shopddmine", "rachelward_e", "shandarogers_", "roanmclean",
                                        "kaylaseah", "camilacoelho", "kristinakacheeva", "mackk.peters"]
        userVideoArrayList["fitness"] = ["naomiboyer", "alexgeorgy", "bbycailey", "hope.cee", "jessthrowiton",
                                         "kaylaseah", "elizabethkando", "inthesejeans", "mscrisssy", "thais.talo"
                                         ]

        # 图片帖子
        userFlagMap = {}
        for key, userArray in userImageArrayList.items():
            flag = slugify(key)
            for user in userArray:
                userFlagMap[user] = flag

        userLimit = 60
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
                result = self.UpdateRelations(email, "demo", monthFlags, 0.51, flag, 1)

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

        userVideoLimit = 16
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
                self.UpLoadVideo(videoEmail, flag, 1)

                userVideoCount += 1
                if userVideoCount >= userVideoLimit:
                    break

        # 随机对图片帖子和视频帖子进行公开
        postVideoIdsMap = self.postVideoIdsDic
        postImageIdMap = self.postImageIdDic

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

            if count == 7:
                if (emailVideoLen - 1) > 1:
                    postIdKeys.append(randomEmailVideoPostKeys[0])
                    postIdKeys.append(randomEmailVideoPostKeys[1])

            elif count == 14:
                if (emailVideoLen - 1) > 3:
                    postIdKeys.append(randomEmailVideoPostKeys[2])
                    postIdKeys.append(randomEmailVideoPostKeys[3])

            elif count == 21:
                if (emailVideoLen - 1) > 5:
                    postIdKeys.append(randomEmailVideoPostKeys[4])
                    postIdKeys.append(randomEmailVideoPostKeys[5])

            elif count == 28:
                if (emailVideoLen - 1) > 7:
                    postIdKeys.append(randomEmailVideoPostKeys[6])
                    postIdKeys.append(randomEmailVideoPostKeys[7])

            elif count == 35:
                if (emailVideoLen - 1) > 9:
                    postIdKeys.append(randomEmailVideoPostKeys[8])
                    postIdKeys.append(randomEmailVideoPostKeys[9])

            elif count == 42:
                if (emailVideoLen - 1) > 11:
                    postIdKeys.append(randomEmailVideoPostKeys[10])
                    postIdKeys.append(randomEmailVideoPostKeys[11])

            elif count == 49:
                if (emailVideoLen - 1) > 13:
                    postIdKeys.append(randomEmailVideoPostKeys[12])
                    postIdKeys.append(randomEmailVideoPostKeys[13])


            elif count == 56:
                if (emailVideoLen - 1) > 15:
                    postIdKeys.append(randomEmailVideoPostKeys[14])
                    postIdKeys.append(randomEmailVideoPostKeys[15])

        for postIdKey in postIdKeys:

            postImageEmail = postImageIdMap.get(postIdKey)

            if postImageEmail is None:
                postVideoId = postVideoIdsMap.get(postIdKey)
                self.redis.rpush("postId", postVideoId)

            else:
                self.redis.rpush("postId", postIdKey)

        self.redis.close()

if __name__ == "__main__":

    rn = RelationsNewV5()
    rn.matchPost()
