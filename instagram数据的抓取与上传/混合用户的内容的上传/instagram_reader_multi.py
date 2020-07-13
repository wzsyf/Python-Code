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
from user_emails_multi import *
from user_emails_multi import *
from keep_flags import *

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
    root_dir = "../mini_datastore"
    root_dir = "../DataStore"
    root_dir = "../task2"
    root_dir = "../task3_04200"
    root_dir = "/home/ec2-user/task3_0420"

    def __init__(self):
        pass

    def if_is_not_imported(self, img_hash):
        try:
            resp = requests.head("https://fashion-data-mining.s3.amazonaws.com/{0}".format(img_hash))
            return resp.status_code == 403
        except:
            return False

    def multi_instagramer(self, root, userName, email):
        try:

            print userName, email

            # 拼接的名字做分割，第一个子用户名，第二个为父用户名
            userNameArr = userName.split("+")
            userNameOne = userNameArr[0]
            userNameTwo = userNameArr[1]

            # 已知路径和用户名成做拼接，组成抓取用户的用户目录的路径
            path = os.path.join(root, userNameOne)
            path1 = os.path.join(root, userNameTwo)

            # 父用户的头像图片的位置
            fatherUserImage = os.path.join(path1, "{0}.jpg".format(userNameTwo))

            idFile = os.path.join(path, "id")
            with open(idFile) as f:
                userId = f.read()
                userId = userId.strip()

            zipFile = os.path.join(path, "{0}_{1}.json.xz".format(userNameOne, userId))
            jsonFile = os.path.join(path, "{0}_{1}.json".format(userNameOne, userId))


            # 注册用户
            # Voila.register(email, userNameOne, "demo")
            Voila.register(email, userNameTwo, "demo")

            # 以注册的用户进行登陆
            loginInfo = Voila.login(email, "demo")
            # 获取登录验证时的token令牌
            auth = loginInfo.get("token")

            # 拼接解压缩命令，解压缩以xz结尾的压缩文件
            xzCommand = "xz -d {0}".format(zipFile)
            # 执行命令
            os.system(xzCommand)


            # 判断父用户头像图片是否存在，若存在则进行上传
            if os.path.isfile(fatherUserImage):
                Voila.PostAvatar(auth, fatherUserImage)


            with open(jsonFile) as f:
                # 读取json文件中的数据
                data = f.read()
                # 加载为JSON格式
                data = json.loads(data)

                # 获取JSON字段中对应的值
                node = data.get("node")
                # 用户图片url
                profile_pic_url = node.get("profile_pic_url")
                fullname = node.get("full_name")
                fullnames = fullname.split(" ")

                avatarImage = "{0}.jpg".format(userNameOne)

                # 请求图片信息
                r = requests.get(profile_pic_url)
                # 以二进制写形式写到文件avatarImage中
                with open(avatarImage, "wb") as f:
                    f.write(r.content)
                firstName = ""
                lastName = ""
                firstName = fullnames[0]
                if len(fullnames) > 1:
                    lastName = fullnames[1]

                # 请求后台接口做更新操作
                Voila.PutAccount(auth, {"firstName": firstName, "lastName": lastName})

                if os.path.exists(avatarImage):
                    # 头像--将之前写入文件的图片二进制内容添加到数据库中
                    Voila.PostAvatar(auth, avatarImage)

                # 添加好之后删除已经添加的存放图片二进制内容的文件
                cmd = "rm {0}".format(avatarImage)
                os.system(cmd)

            # 压缩json文件
            xzCommand = "xz {0}".format(jsonFile)
            os.system(xzCommand)

            # 列举子用户目录下的所有文件
            for f in os.listdir(path):
                try:
                    refresh_token = loginInfo.get("refresh_token")
                    loginInfo = Voila.refresh_token(refresh_token)
                    auth = loginInfo.get("token")

                    # 文件以.txt结尾
                    if f.endswith(".txt"):
                        # 2019-06-19_13-46-02_UTC.txt
                        # 2019-06-19_13-46-02_UTC
                        base = os.path.splitext(f)[0]

                        # 2019-06-19_13-46-02_UTC.txt
                        baseParts = base.split("_")
                        # 2019-06-19
                        datePart = baseParts[0]
                        # 2019 06 19
                        dateParts = datePart.split("-")
                        if len(dateParts) < 3:
                            continue
                        # 获取月份
                        month = dateParts[1]
                        month = int(month)
                        month = monthArray[month]
                        monthFlag = "month-{0}".format(month)

                        # print "{0} {1}".format(userName, base)
                        # 2020-01-25_13-34-34_UTC.json.xz
                        jsonPostZip = os.path.join(path, "{0}.json.xz".format(base))
                        # aliciabonora_507187201.json
                        # 用户名_用户id.json
                        jsonPost = os.path.join(path, "{0}.json".format(base))
                        # 2019-10-18_14-36-24_UTC.jpg
                        imageFile = os.path.join(path, "{0}.jpg".format(base))

                        if not os.path.exists(imageFile):
                            imageFile = os.path.join(path, "{0}_1.jpg".format(base))

                        if not os.path.exists(imageFile):
                            continue

                        # 解压缩以.json.xz结尾的文件
                        xzCommand = "xz -d {0}".format(jsonPostZip)
                        os.system(xzCommand)

                        likes = 0
                        text = ""
                        tags = []

                        # 读取解压缩之后JSON中字段对应的值
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

                        # 将图片添加的后台接口对应的数据库中
                        imId = Voila.PostImage(auth, imageFile)

                        # 将各项获取到的数据添加到后台接口对应的数据库中
                        postId = Voila.PostPost(auth, imId, tags, "Like:{0} test".format(likes), text, likes)

                        # 添加flag到后台接口对应的数据库中
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

    def all_instagramer(self):

        for root, dirs, files in os.walk(self.root_dir):
            for f in dirs:

                if not f in Fresh:
                    continue


                userNames = None
                email = None
                for key, value in FreshDic.items():
                    if f in value:
                        userNames = f + "+" + key
                        email = userEmails.get(key)

                self.multi_instagramer(self.root_dir, userNames, email)


if __name__ == "__main__":
    ir = InstagramReader()
    ir.all_instagramer()
