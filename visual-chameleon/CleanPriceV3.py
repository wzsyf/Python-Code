#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta
from backend import *

class CleanPriceV3:


    def getAllDic(self, flags):
        bk = Backend()
        allDic = {}

        items = bk.getProductIdAndCode(flags)

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



    def getVariantOfAfterDel(self, flags):
        bk = Backend()
        afterDelVariantDic = {}

        items = bk.getProductIdAndCode(flags)

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
    cp = CleanPriceV3()

    flags = ["f_20200826_hoodies", "f_20200906_cropcardigans", "f_20200906_sneakerunder100", "f_20200906_nike",
             "f_20200906_oversizetee", "f_20200906_backpacks", "f_20200902_new", "f_20200902_sleepwear",
             "f_20200904_mask", "f_20200902_under25", "f_20200902_gold", "f_20200902_shorts", "f_20200826_heels",
             "f_20200826_luxury", "f_20200820_denim"]

    allDic = cp.getAllDic(flags)

    if len(allDic) != 0:
        deleteDic = cp.getDeleteDic(allDic)
        if len(deleteDic) != 0:
            cp.cleanPrice(deleteDic)

        variantOfAfterDel = cp.getVariantOfAfterDel(flags)
        cp.delVariantOfNeedDeleted(variantOfAfterDel)
