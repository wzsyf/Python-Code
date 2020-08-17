#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

class GetMaxCommonSubStr:
    def getMaxCommonSubstr(self, s1, s2):
        # 求两个字符串的最长公共子串
        # 思想：建立一个二维数组，保存连续位相同与否的状态

        len_s1 = len(s1)
        len_s2 = len(s2)

        # 生成0矩阵，为方便后续计算，多加了1行1列
        # 行: (len_s1+1)
        # 列: (len_s2+1)
        record = [[0 for i in range(len_s2 + 1)] for j in range(len_s1 + 1)]

        maxNum = 0  # 最长匹配长度
        p = 0  # 字符串匹配的终止下标

        for i in range(len_s1):
            for j in range(len_s2):
                if s1[i] == s2[j]:
                    # 相同则累加
                    record[i + 1][j + 1] = record[i][j] + 1

                    if record[i + 1][j + 1] > maxNum:
                        maxNum = record[i + 1][j + 1]
                        p = i  # 匹配到下标i

        # 返回 子串长度，子串
        return maxNum, s1[p + 1 - maxNum: p + 1]



    def getColumn(self, filePath):
        column = {}
        with open(filePath, 'r') as csvfile:
            reader = csv.reader(csvfile)

            for row in reader:
                column[row[0]] = row[1]
            # column = [row[0] for row in reader]

        return column



    def calMaxSubStr(self):

        filePath = 'D:/brands.csv'

        column = self.getColumn(filePath)
        del column['Name']

        columnKeys = column.keys()
        columnLen = len(columnKeys)

        allCommonSubstr = {}

        for i in range(0, columnLen - 1):
            for j in range(i + 1, columnLen):

                subStrLen, subStr = self.getMaxCommonSubstr(columnKeys[i], columnKeys[j])

                if subStrLen >= 6:
                    subStrValue = allCommonSubstr.get(subStr)
                    if subStrValue is None:
                        commonSubStr = {}
                        commonSubStr[columnKeys[i]] = column.get(columnKeys[i])
                        commonSubStr[columnKeys[j]] = column.get(columnKeys[j])

                        allCommonSubstr[subStr] = commonSubStr
                    else:
                        subStrValue[columnKeys[j]] = column.get(columnKeys[j])
                        allCommonSubstr[subStr] = subStrValue


        return allCommonSubstr



    def calSubStrLen(self, dic):

        subStrKeys = dic.keys()
        subStrLenDic = {}

        for subStrKey in subStrKeys:
            subStrKeyLen = len(subStrKey)
            subStrLenDic[subStrKey] = subStrKeyLen

        dics = sorted(subStrLenDic.items(), key=lambda item: item[1], reverse=True)
        return dics



    def persist2File(self, downpath, dic):
        with open(downpath, 'w') as csvFile:
            data = []
            writer = csv.writer(csvFile, lineterminator='\n')

            subStrLenSortedDic = self.calSubStrLen(dic)
            for key, value in subStrLenSortedDic:
                val = dic.get(key)
                data.append([key, ""])
                for name, brand in val.items():
                    arr = []
                    arr.append(name)
                    arr.append(brand)

                    data.append(arr)


            writer.writerows(data)


if __name__ == "__main__":

    gmcss = GetMaxCommonSubStr()
    column = gmcss.calMaxSubStr()
    # haveNotRepeat = gmcss.removeRepeat(column)

    downpath = 'D:\substr/result.csv'
    gmcss.persist2File(downpath, column)

