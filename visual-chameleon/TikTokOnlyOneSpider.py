# -*- coding: utf-8 -*-

import os
import time
import json
import requests
from TikTokUrls import *


class TiktokSpider:

    def __init__(self):

        self.headers = {
            "Accpet":"application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36",
            "Accpet-Encoding": "gzip"
        }


    # 视频图片文件的持久化
    def persistFile(self, processWay, content, userDir, fileType, fileNamePre):
        # resp = requests.get(fileMsg).content

        # Ture--代表视频类型
        if fileType == True:
            videoFileMp4 = os.path.join(userDir, "{0}.mp4".format(fileNamePre))

            with open(videoFileMp4, processWay) as dataFile:
                dataFile.write(content)

        # False--代表图片类型
        elif fileType == False:
            imgFileJpg = os.path.join(userDir, "{0}.jpg".format(fileNamePre))

            with open(imgFileJpg, processWay) as dataFile:
                dataFile.write(content)

        # None--代表JSON文件类型
        else:
            JSONFile = os.path.join(userDir, "{0}.json".format(fileNamePre))

            with open(JSONFile, processWay) as dataFile:
                dataFile.write(content)


    def getMsgsAndPersist(self):

        rootDir = "/home/ec2-user/tiktok"


        # 忽略警告
        requests.packages.urllib3.disable_warnings()

        # 依次请求TikTokUrls中的URL
        for tiktokUrl in TikTokUrls:

            # 请求URL
            resp = requests.get(tiktokUrl, headers=self.headers, verify=False)

            if resp.statusCode != requests.codes.OK:
                print("获取视频列表失败.")
                return None

            # 获取响应的信息体部分，是一个包含多个JSON对象的数组
            # if 'items' not in resp.json().keys():
            #     continue

            items = resp.json()['itemInfo']['itemStruct']

            if items is None:
                continue

            # 用户名
            uniqueId = items['author']['uniqueId']

            # 用户目录的路径
            userDir = os.path.join(rootDir, "{0}".format(uniqueId))

            if not os.path.exists(os.path.join(rootDir, uniqueId)):
                # 创建用户目录
                uniqueIdDir = os.path.join(rootDir, uniqueId)
                createFileCommand = 'mkdir ' + uniqueIdDir
                os.system(createFileCommand)




                # 用户信息
                authorInfos = {
                    'nickname': items['author']['nickname'],
                    'uid': uniqueId,
                    'avatar': items['author']['avatarMedium']
                }

                # 将JSON格式转换为字符串格式
                jsonStr = json.dumps(authorInfos)
                # 持久化到本地
                self.persistFile('w', jsonStr, userDir, None, uniqueId)

            else:
                print("directory already exists!")



            # 遍历数组中的每个JSON对象，获取想要得到的信息
            # for item in items:
            # if items['stats']['diggCount'] >= 10000:

            video_msg = items['video']

            createTime = str(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(items['createTime'])))

            path = os.path.join(rootDir, uniqueId)
            cmd = "find " + path + " -name " + createTime + ".mp4"
            mp4Res = os.popen(cmd).readlines()

            if mp4Res != None:

                print("mp4 video already exists!")

            else:
                # 视频持久化到本地
                videoResp = requests.get(video_msg['playAddr']).content
                self.persistFile('wb', videoResp, userDir, True, createTime)

                # 视频封面持久化到本地
                coverResp = requests.get(video_msg['cover']).content
                self.persistFile('wb', coverResp, userDir, False, createTime)

                tags = []
                name = 'textExtra'
                if name in items.keys():
                    hashTags = items['textExtra']

                    for hashTag in hashTags:
                        hashTag = hashTag['hashtagName']
                        tags.append(hashTag)


                descStr = items['desc']

                likes = items['stats']['diggCount']

                videoMsgs = {
                    "tags":tags,
                    "descStr":descStr,
                    "likes":likes
                }

                # 将JSON格式转换为字符串格式
                jsonStr = json.dumps(videoMsgs)
                # 持久化到本地
                self.persistFile('w', jsonStr, userDir, None, createTime)



if __name__ == "__main__":
    ts = TiktokSpider()
    ts.getMsgsAndPersist()