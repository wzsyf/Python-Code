#!/usr/bin/env python
# -*- coding: utf-8 -*-

from backend import *
from api import *

class UpdatePostFlagOfUser:

    def updatePostFlag(self, email):
        bk = Backend()
        flag = "blocked-post"
        postIdArrs = bk.getEnabledPost(email)

        for postIdArr in postIdArrs:
            postId = postIdArr.get("postId")
            Voila.AddFlagToPost(postId, flag)


    def emailOfUser(self):
        emailArr = ["ihayavq@gmail.com", "butoolhelal@icloud.com"]
        for email in emailArr:
            self.updatePostFlag(email)

if __name__ == '__main__':
    upfou = UpdatePostFlagOfUser()
    upfou.emailOfUser()