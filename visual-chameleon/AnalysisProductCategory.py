#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from backendV3 import *

class AnalysisProductCategory:

    def analysis(self, categorys):
        bk = Backend()
        items = []

        for val in categorys:
            map = bk.analysisProductCategory(val)
            items.append(map)

        return items


    def persistFile(self, downpath, rowData, contents):

        with open(downpath, 'w') as csvFile:
            data = []

            writer = csv.writer(csvFile, lineterminator='\n')
            writer.writerow(rowData)

            for content in contents:
                arr = []
                for key,value in content.items():
                    arr.append(key)
                    arr.append(value)

                data.append(arr)

            writer.writerows(data)



if __name__ == "__main__":
    categorys = ["category-women-clothing", "category-women-shoes", "category-women-bags", "category-women-accessories",
                 "category-women-jewelry", "category-men-clothing", "category-men-shoes", "category-men-bags",
                 "category-men-accessories", "category-men-jewelry", "category-men-cologne-grooming",
                 "category-beauty-skin-care", "category-beauty-makeup", "category-beauty-hair-care",
                 "category-beauty-body-care", "category-beauty-tools-accessories", "category-beauty-nail-polish-care",
                 "category-beauty-fragrances"]

    download = "/home/ubuntu/scripts/result.csv"
    rowData = ["category", "num"]

    apc = AnalysisProductCategory()
    items = apc.analysis(categorys)

    apc.persistFile(download, rowData, items)


