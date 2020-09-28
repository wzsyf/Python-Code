#!/usr/bin/env python

from api import *
from user_emails import *
from slugify import slugify
from backend import *
import random

class AddToFlagPostOfUser:
    def addFlagToPost(self, email, flag):

        bk = Backend()
        posts = bk.PostVedio(email)
        for post in posts:
            postId = post.get("postId")
            print(email, postId, flag)
            Voila.AddFlagToPost(postId, flag)
            print("da-shang-le")

    def addMonthFlagToPost(self, email):
        bk = Backend()
        posts = bk.PostVedio(email)
        monthFlag = ["month-apr","month-may", "month-jun", "month-jul", "month-aug", "month-sept", "month-oct"]

        for post in posts:
            flag = monthFlag[random.randint(0, len(monthFlag) - 1)]
            print flag
            postId = post.get("postId")
            print(email, postId, flag)
            Voila.AddFlagToPost(postId, flag)
            print("da-shang-le")


if __name__ == "__main__":

    afpou = AddToFlagPostOfUser()

    userArrayList = {}

    userArrayList["workwear"] = ["ewelinakanty", "asaqueenatwork"]
    userArrayList["beachwear"] = ["asaqueenatbeach"]

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
            # result = afpou.addFlagToPost(email, flag)
            result = afpou.addMonthFlagToPost(email)
