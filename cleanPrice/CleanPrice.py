#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta
from backend import *

class CleanPrice:


    def getAllDic(self):
        bk = Backend()
        allDic = {}

        items = bk.getProductIdAndCode()

        if len(items) != 0:

            for item in items:

                productId = item.get("productId")
                codePre = item.get("code").split("-")[0]
                lastImportTime = item.get("lastImportedTime")
                importTime = lastImportTime

                codeTimeDic = allDic.get(productId)
                if codeTimeDic is None:
                    codeTime = {}
                    codeTime[codePre] = importTime

                    allDic[productId] = codeTime
                else:
                    codeTimeDic[codePre] = importTime

                    allDic[productId] = codeTimeDic

        return allDic



    def getDeleteDic(self, allDic):

        deleteDic = {}

        for key, value in allDic.items():
            codeArr = []

            dics = sorted(value.items(), key=lambda item: item[1], reverse=True)
            dicsLen = len(dics)
            if dicsLen > 1:
                dics = dics[1:]
                for val in dics:
                    code = val[0]
                    codeArr.append(code)

                deleteDic[key] = codeArr

        return deleteDic



    def getVariantOfAfterDel(self):
        bk = Backend()
        afterDelVariantDic = {}

        items = bk.getProductIdAndCode()

        if len(items) != 0:

            for item in items:
                productId = item.get("productId")
                codePre = item.get("code").split("-")[0]
                lastImportTime = item.get("lastImportedTime")

                codeTimeDic = afterDelVariantDic.get(productId)
                if codeTimeDic is None:
                    codeTime = {}
                    timeArr = []
                    timeArr.append(lastImportTime)

                    codeTime[codePre] = timeArr

                    afterDelVariantDic[productId] = codeTime
                else:
                    timeArr = codeTimeDic.get(codePre)
                    timeArr.append(lastImportTime)

                    codeTimeDic[codePre] = timeArr

                    afterDelVariantDic[productId] = codeTimeDic

        return afterDelVariantDic


    def delVariantOfNeedDeleted(self, afterDelVariantDic):
        bk = Backend()

        for key, value in afterDelVariantDic.items():
            for code, timeArr in value.items():
                timeArr = sorted(timeArr, reverse = True)
                firstTime = timeArr[0]
                prehours = (firstTime + timedelta(hours=-1)).strftime("%Y-%m-%d %H:%M:%S")

                for val in timeArr:

                    if str(val) < prehours:
                        print(key, str(val))
                        bk.cleanPriceAfterDelVariant(key, val)




    def cleanPrice(self, deleteDic):
        bk = Backend()

        for key, value in deleteDic.items():
            print(key, value)
            for val in value:
                bk.cleanPrice(key, val)


if __name__ == "__main__":
    cp = CleanPrice()

    allDic = cp.getAllDic()

    if len(allDic) != 0:
        deleteDic = cp.getDeleteDic(allDic)
        if len(deleteDic) != 0:
            cp.cleanPrice(deleteDic)

        variantOfAfterDel = cp.getVariantOfAfterDel()
        cp.delVariantOfNeedDeleted(variantOfAfterDel)
