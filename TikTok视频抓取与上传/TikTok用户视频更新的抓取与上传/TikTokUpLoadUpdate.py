# -*- coding: utf-8 -*-

import os
from api import *
from TikTokUserEmails import *
from keep_flags import *


class TikTokUpLoadUpdate:

    rootDir = "/home/ec2-user/tiktok"

    def tiktokUpLoad(self, rootDir, userName, email):

        path = os.path.join(rootDir, userName)

        Voila.register(email, userName, "demo")

        loginInfo = Voila.login(email, "demo")
        auth = loginInfo.get("token")


        jsonFile = os.path.join(path, "{0}.json".format(userName))

        # 解析用户信息的JSON文件
        with open(jsonFile) as JSOnFile:

            data1 = JSOnFile.read()
            data2 = json.loads(data1)

            avatarImgResp = requests.get(data2['avatar']).content
            avatarImgPath = os.path.join(path, "{0}.jpg".format(userName))
            with open(avatarImgPath, 'wb') as f:
                f.write(avatarImgResp)

            Voila.PostAvatar(auth, avatarImgPath)

            cmd = "rm {0}".format(avatarImgPath)
            os.system(cmd)


        # 做更新再抓取时使用，已经上传的文件的名字，多个名字使用字符串做拼接
        uploadFileNamePath = os.path.join(path, "{0}.txt".format("alreadyUploadFileName"))

        # 判断是否存在上述文件，若不存在则先创建文件
        if not os.path.exists(uploadFileNamePath):
            createFileCmd = "touch " + uploadFileNamePath
            os.system(createFileCmd)

            alreadyUploadFileName = ''
            # with open(uploadFileNamePath, 'w') as f:
            #     f.write(alreadyUploadFileName)

            # 遍历目录下的文件
            for f in os.listdir(path):

                refresh_token = loginInfo.get("refresh_token")
                loginInfo = Voila.refresh_token(refresh_token)
                auth = loginInfo.get("token")

                if f.endswith('.jpg'):
                    # 分割文件名和后缀
                    fileName = os.path.splitext(f)[0]
                    # 拼接已经上传的文件名
                    alreadyUploadFileName = alreadyUploadFileName + "," + fileName

                    imgFile = os.path.join(path, "{0}.jpg".format(fileName))
                    imgId = Voila.PostImage(auth, imgFile)

                    # 查找与视频封面图片同名的MP4文件
                    cmd = "find " + path + " -name " + fileName + ".mp4"
                    mp4Res = os.popen(cmd).readlines()

                    if mp4Res != None:
                        # mp4 = str(mp4Res[0].split("/")[-1])
                        mp4File = os.path.join(path, "{0}.mp4".format(fileName))
                        VoilaGo.PostVideo(imgId, mp4File)

                    # 查找与视频封面图片同名的JSON文件
                    cmd2 = "find " + path + " -name " + fileName + ".json"
                    jsonRes = os.popen(cmd2).readlines()

                    # 解析JSON文件
                    if jsonRes != None:
                        jsonRes = os.path.join(path, "{0}.json".format(fileName))
                        with open(jsonRes, 'r') as f:
                            data1 = f.read()
                            data2 = json.loads(data1)

                            tags = data2['tags']
                            descStr = data2['descStr']
                            likes = data2['likes']

                            # 将各项获取到的数据添加到后台接口对应的数据库中，提交生成的帖子
                            postId = Voila.PostPost(auth, imgId, tags, "Like:{0} test".format(likes), descStr, likes)

                            # 添加flag到后台接口对应的数据库中
                            flags = []
                            for tag in tags:
                                if tag in KeepFlags:
                                    flags.append(tag)

                            print postId

                            if postId:
                                for flag in flags:
                                    # 对生成的帖子添加flag
                                    Voila.AddFlagToPost(postId, flag)

            # 将已经拼接的字符串持久化到已经上传的文件的文件中
            with open(uploadFileNamePath, 'w') as f:
                f.write(alreadyUploadFileName)

        else:
            # 若存在已经上传的文件名的文件
            alreadyUploadFileNameStr = open(uploadFileNamePath, 'r').read()
            alreadyUploadFileNameStrArr = alreadyUploadFileNameStr.split(",")

            for f in os.listdir(path):

                refresh_token = loginInfo.get("refresh_token")
                loginInfo = Voila.refresh_token(refresh_token)
                auth = loginInfo.get("token")


                if f.endswith('.jpg'):
                    fileName = os.path.splitext(f)[0]

                    if fileName in alreadyUploadFileNameStrArr:
                        print("file already upload!")

                    else:
                        alreadyUploadFileNameStr = alreadyUploadFileNameStr + "," + fileName

                        imgFile = os.path.join(path, "{0}.jpg".format(fileName))
                        imgId = Voila.PostImage(auth, imgFile)

                        cmd = "find " + path + " -name " + fileName + ".mp4"
                        mp4Res = os.popen(cmd).readlines()

                        if mp4Res != None:
                            # mp4 = str(mp4Res[0].split("/")[-1])
                            mp4File = os.path.join(path, "{0}.mp4".format(fileName))
                            VoilaGo.PostVideo(imgId, mp4File)


                        cmd2 = "find " + path + " -name " + fileName + ".json"
                        jsonRes = os.popen(cmd2).readlines()

                        if jsonRes != None:
                            jsonRes = os.path.join(path, "{0}.json".format(fileName))
                            with open(jsonRes, 'r') as f:
                                data1 = f.read()
                                data2 = json.loads(data1)

                                tags = data2['tags']
                                descStr = data2['descStr']
                                likes = data2['likes']

                                # 将各项获取到的数据添加到后台接口对应的数据库中
                                postId = Voila.PostPost(auth, imgId, tags, "Like:{0} test".format(likes), descStr, likes)

                                # 添加flag到后台接口对应的数据库中
                                flags = []
                                for tag in tags:
                                    if tag in KeepFlags:
                                        flags.append(tag)

                                print postId

                                if postId:
                                    for flag in flags:
                                        Voila.AddFlagToPost(postId, flag)

            with open(uploadFileNamePath, 'w') as f:
                f.write(alreadyUploadFileNameStr)



    def tiktokUser(self):
        for root, dirs, files in os.walk(self.rootDir):
            for f in dirs:

                if not f in Fresh:
                    continue

                email = userEmails.get(f) or None

                if not email:
                    continue

                self.tiktokUpLoad(self.rootDir, f, email)


if __name__ == "__main__":
    tu = TikTokUpLoadUpdate()
    tu.tiktokUser()
