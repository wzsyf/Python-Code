#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import subprocess
import re
import requests
import hashlib

from api import *
# from user_map import *
from user_emails import *
from keep_flags import *
from backend import *

hashtag_re = re.compile("(?:^|\s)[＃#]{1}(\w+)", re.UNICODE)
hashtag_re = re.compile('(#\w+)', re.UNICODE)

mention_re = re.compile("(?:^|\s)[＠ @]{1}([^\s#<>[\]|{}]+)", re.UNICODE)

monthArray = [
    "unknown",
    "jan",
    "feb",
    "mar",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sept",
    "oct",
    "nov",
    "dec"
]


class InstagramReader:

    root_dir = "/home/ubuntu/igAccountData"

    def __init__(self):
        pass

    def if_is_not_imported(self, img_hash):
        try:
            resp = requests.head("https://fashion-data-mining.s3.amazonaws.com/{0}".format(img_hash))
            return resp.status_code == 403
        except:
            return False

    def upload(self, root, userName, email, customerId):

        try:

            print userName, email
            path = os.path.join(root, userName)

            idFile = os.path.join(path, "id")
            with open(idFile) as f:
                userId = f.read()
                userId = userId.strip()

            zipFile = os.path.join(path, "{0}_{1}.json.xz".format(userName, userId))


            xzCommand = "xz -d {0}".format(zipFile)
            os.system(xzCommand)

            for f in os.listdir(path):
                try:

                    if f.endswith(".txt"):
                        base = os.path.splitext(f)[0]

                        baseParts = base.split("_")
                        datePart = baseParts[0]
                        dateParts = datePart.split("-")
                        if len(dateParts) < 3:
                            continue
                        month = dateParts[1]
                        month = int(month)
                        month = monthArray[month]
                        monthFlag = "month-{0}".format(month)

                        # print "{0} {1}".format(userName, base)
                        jsonPostZip = os.path.join(path, "{0}.json.xz".format(base))
                        jsonPost = os.path.join(path, "{0}.json".format(base))
                        imageFile = os.path.join(path, "{0}.jpg".format(base))
                        if not os.path.exists(imageFile):
                            imageFile = os.path.join(path, "{0}_1.jpg".format(base))

                        if not os.path.exists(imageFile):
                            continue

                        xzCommand = "xz -d {0}".format(jsonPostZip)
                        os.system(xzCommand)

                        likes = 0
                        text = ""
                        tags = []

                        with open(jsonPost) as f:
                            data = f.read()
                            data = json.loads(data)
                            if data and data.get("node") and data.get("node").get(
                                    "edge_media_preview_like") and data.get("node").get("edge_media_preview_like").get(
                                "count"):
                                likes = data.get("node").get("edge_media_preview_like").get("count")

                            if data and data.get("node") and data.get("node").get("edge_media_to_caption") and data.get(
                                    "node").get("edge_media_to_caption").get("edges"):
                                edges = data.get("node").get("edge_media_to_caption").get("edges")
                                if len(edges) > 0:
                                    edge = edges[0]
                                    text = edge.get("node").get("text")
                                    hashtags = hashtag_re.findall(text)
                                    sorted_hashtags = sorted(hashtags, key=lambda i: len(i), reverse=True)
                                    for hashtag in hashtags:
                                        tags.append(hashtag.replace("#", ""))

                                    for hashtag in sorted_hashtags:
                                        text = text.replace(hashtag, "")

                                    text = text.strip()
                                    # print mention_re.findall(text)

                        xzCommand = "xz {0}".format(jsonPost)
                        os.system(xzCommand)

                        file_md5 = ""
                        with open(imageFile, 'rb') as fp:
                            data = fp.read()
                            file_md5 = hashlib.md5(data).hexdigest()

                        if not self.if_is_not_imported(file_md5):
                            print file_md5, "existed"
                            continue
                        else:
                            print file_md5, "no existed"

                        imId = VoilaGo.PostImageNoAuth(customerId, imageFile)

                        postId = VoilaGo.PostPostNoAuth(customerId, imId, tags, "Like:{0} test".format(likes), text, likes)

                        flags = []
                        flags.append(monthFlag)
                        for tag in tags:
                            if tag in KeepFlags:
                                flags.append(tag)

                        print postId

                        if postId:
                            for flag in flags:
                                Voila.AddFlagToPost(postId, flag)

                except Exception, ex:
                    print ex
        except Exception, ex:
            print ex

    def getIGAccountAndUpload(self, igAccount):

        bk = Backend()
        email, customerId = bk.getIGAccountEmail(igAccount)

        self.upload(self.root_dir, igAccount, email, customerId)


if __name__ == "__main__":
    ir = InstagramReader()
    ir.all_instagramer()
