#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import *
from api import *


class LogAnalysis:

    def getLogFilePath(self):

        fileRootPath = "/home/ubuntu/scripts"

        rootPath = "/home/ubuntu/projects/go/src/VoilaStats/logs/2020/"
        yesterday = (date.today() + timedelta(days=-1)).strftime("%Y%m%d")
        month = yesterday[4:6]

        cmd = "tar -zxvf " + rootPath + month + "/access.log." + yesterday + ".tar.gz"
        os.system(cmd)

        filePath = fileRootPath + "/access.log." + yesterday

        return filePath


    def analysisLogFile(self):

        filePath = self.getLogFilePath()

        productClickArr = []

        with open(filePath, 'r') as f:
            while True:
                lines = f.readlines()
                if not lines:
                    break
                for line in lines:

                    productClickDic = {}

                    splitLineArr = line.split(" ")

                    dateStr = splitLineArr[3]
                    ymdhms = self.processDateFormat(dateStr)

                    link = splitLineArr[6]

                    linkSplitArr = link.split("?")
                    preString = linkSplitArr[0]

                    if "/v1/action" != preString:
                        continue

                    if len(linkSplitArr) != 0:
                        continue


                    sufString = linkSplitArr[1]
                    sufStringSplitArr = sufString.split("&")

                    if "action=clicks" != sufStringSplitArr[-1]:
                        continue

                    subSufStringSplitArr = sufStringSplitArr[:3]

                    print ymdhms

                    index = 1
                    for value in subSufStringSplitArr:
                        subStr = value.split("=")

                        if index == 1:
                            if subStr[1] == "":
                                productClickDic["productId"] = 0
                                index += 1
                                continue

                            id = int(subStr[1])
                            productClickDic["productId"] = id
                            print id

                        if index == 2:
                            if subStr[1] == "":
                                productClickDic["postId"] = 0
                                index += 1
                                continue

                            id = int(subStr[1])
                            productClickDic["postId"] = id
                            print id

                        if index == 3:
                            if subStr[1] == "":
                                productClickDic["customerId"] = 0
                                index += 1
                                continue

                            id = int(subStr[1])
                            productClickDic["customerId"] = id
                            print id

                        index += 1

                    productClickDic["clickTime"] = ymdhms
                    productClickArr.append(productClickDic)

        rmCmd = "rm -rf " + filePath
        os.system(rmCmd)

        return productClickArr



    def processDateFormat(self,dateStr):
        monthMap = {}

        monthMap["Jan"] = "01"
        monthMap["Feb"] = "02"
        monthMap["Mar"] = "03"
        monthMap["Apr"] = "04"
        monthMap["May"] = "05"
        monthMap["Jun"] = "06"
        monthMap["Jul"] = "07"
        monthMap["Aug"] = "08"
        monthMap["Sep"] = "09"
        monthMap["Oct"] = "10"
        monthMap["Nov"] = "11"
        monthMap["Dec"] = "12"

        subDateStr = dateStr.split("[")[1]
        subDateStr = subDateStr.replace(":", " ", 1)
        subDateStr = subDateStr.replace("/", "-")

        ymdhmsArr = subDateStr.split(" ")
        yearMonthDate = ymdhmsArr[0]
        yearMonthDateArr = yearMonthDate.split("-")
        yearMonthDateStr = yearMonthDateArr[2] + "-" + monthMap[yearMonthDateArr[1]] + "-" + yearMonthDateArr[0]

        ymdhms = yearMonthDateStr + " " + ymdhmsArr[1]

        return ymdhms


    def postProductClick(self):
        productClickArr = self.analysisLogFile()

        for value in productClickArr:

            data = VoilaGo.PostProductClick(value)
            print data

            productClickId = data.get("id")
            VoilaGo.GetProductClickByIdAndIndex(productClickId)


if __name__ == "__main__":

    la = LogAnalysis()
    la.postProductClick()

    # filePath = "D:\\access.log"
    #
    # la = LogAnalysis()
    # productClickArr = la.analysisLogFile()
    # for value in productClickArr:
    #     print value