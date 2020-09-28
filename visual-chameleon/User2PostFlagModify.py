#!/usr/bin/env python

from api import *
from user_emails import *
from slugify import slugify
from backend import *
import random
import json

class User2PostFlagModify:


    def updatePreFlagToPost(self, email, bk, flag):

        posts = bk.PostVedio(email)
        for post in posts:

            postId = post.get("postId")
            flags = post.get("flags")

            print flags
            if "vintage-style" in flags:
                bk.updateFlagsToPost(postId, "vintage-style", flag)
            else:
                Voila.AddFlagToPost(postId, flag)




if __name__ == "__main__":

    bk = Backend()

    u2pfm = User2PostFlagModify()

    userArrayList = {}

    userArrayList["petite"] = ["elaisaya", "sabrinacsari", "claudiagraziano", "fakerstrom", "lauraslittlelocket",
                               "sandrarossi03", "lydiajanetomlinson", "linneafunks", "marvadel", "yxcvanessa",
                               "chloehelenmiles", "ameliecheval31", "solenelara", "ariadibari", "frenchgirldaily",
                               "bertillecnt", "juliesfi", "lestylealafrancaise", "modedamour", "andicsinger"]

    userFlagMap = {}
    for key, userArray in userArrayList.items():
        flag = slugify(key)
        for user in userArray:
            userFlagMap[user] = flag

    users = userFlagMap.keys()
    print len(users)
    random.shuffle(users)

    for user in users:
        flag = userFlagMap.get(user) or None
        if not flag:
            continue

        email = userEmails.get(user) or None
        if email:
            result = u2pfm.updatePreFlagToPost(email, bk, flag)