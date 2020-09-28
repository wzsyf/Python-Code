# -*- coding: utf-8 -*-

import csv
import threading

import requests
import thread

class MatchProductAnalysis:

    def __init__(self):

        self.headers = {
            "Accpet":"application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36",
            "Accpet-Encoding": "gzip"
        }


    def matchProductResponse(self, pageNum):
        url =  "http://backend.voila.fashion/shop-api/blog/post?flags[popular-post]=1&channel=US_WEB&locale=en_US&page=" + str(pageNum)

        # 请求URL
        resp = requests.get(url, headers=self.headers, verify=False)
        items = resp.json()['items']

        if items is None:
            return None

        return items

    def matchProductAnalysis(self):
        pageCount = 133

        categoryNumDic = {}
        brandNumDic = {}
        storeNumDic = {}



        for pageNum in range(1, pageCount + 1):
            items = self.matchProductResponse(pageNum)

            for item in items:
                if 'productRelations' in item.keys():
                    productRelations = item['productRelations']

                    for productRelation in productRelations:
                        taxons1 = productRelation['originalProduct']['taxons']
                        taxons1Main = taxons1['main']
                        taxons1Others = taxons1['others']

                        if taxons1Main.startswith('category'):

                            category = categoryNumDic.get(taxons1Main)
                            if category is None:
                                categoryNumDic[taxons1Main] = 1
                            else:
                                categoryNumDic[taxons1Main] = category + 1

                        elif taxons1Main.startswith('brand'):
                            # brandArr.append(taxons1Main)
                            brand = brandNumDic.get(taxons1Main)
                            if brand is None:
                                brandNumDic[taxons1Main] = 1
                            else:
                                brandNumDic[taxons1Main] = brand + 1
                        else:
                            # storeArr.append(taxons1Main)
                            store = storeNumDic.get(taxons1Main)
                            if store is None:
                                storeNumDic[taxons1Main] = 1
                            else:
                                storeNumDic[taxons1Main] = store + 1

                        for taxons1Other in taxons1Others:
                            if taxons1Other.startswith('category'):
                                # categoryArr.append(taxons1Main)
                                category = categoryNumDic.get(taxons1Other)
                                if category is None:
                                    categoryNumDic[taxons1Other] = 1
                                else:
                                    categoryNumDic[taxons1Other] = category + 1

                            elif taxons1Other.startswith('brand'):
                                # brandArr.append(taxons1Main)
                                brand = brandNumDic.get(taxons1Other)
                                if brand is None:
                                    brandNumDic[taxons1Other] = 1
                                else:
                                    brandNumDic[taxons1Other] = brand + 1

                            else:
                                # storeArr.append(taxons1Main)
                                store = storeNumDic.get(taxons1Other)
                                if store is None:
                                    storeNumDic[taxons1Other] = 1
                                else:
                                    storeNumDic[taxons1Other] = store + 1



                        alternativeProducts = productRelation['alternativeProducts']
                        for alternativeProduct in alternativeProducts:
                            taxons2 = alternativeProduct['taxons']
                            taxons2Main = taxons2['main']
                            taxons2Others = taxons2['others']

                            if taxons2Main.startswith('category'):
                                category = categoryNumDic.get(taxons2Main)
                                if category is None:
                                    categoryNumDic[taxons2Main] = 1
                                else:
                                    categoryNumDic[taxons2Main] = category + 1

                            elif taxons2Main.startswith('brand'):

                                brand = brandNumDic.get(taxons2Main)
                                if brand is None:
                                    brandNumDic[taxons2Main] = 1
                                else:
                                    brandNumDic[taxons2Main] = brand + 1

                            else:
                                store = storeNumDic.get(taxons2Main)
                                if store is None:
                                    storeNumDic[taxons2Main] = 1
                                else:
                                    storeNumDic[taxons2Main] = store + 1


                            for taxons2Other in taxons2Others:
                                if taxons2Other.startswith('category'):

                                    category = categoryNumDic.get(taxons2Other)
                                    if category is None:
                                        categoryNumDic[taxons2Other] = 1
                                    else:
                                        categoryNumDic[taxons2Other] = category + 1

                                elif taxons2Other.startswith('brand'):

                                    brand = brandNumDic.get(taxons2Other)
                                    if brand is None:
                                        brandNumDic[taxons2Other] = 1
                                    else:
                                        brandNumDic[taxons2Other] = brand + 1

                                else:
                                    store = storeNumDic.get(taxons2Other)
                                    if store is None:
                                        storeNumDic[taxons2Other] = 1
                                    else:
                                        storeNumDic[taxons2Other] = store + 1

                else:
                    print("productRelations not exsist!")

        # categoryCount =
        # brandCount =
        # storeCount =

        return categoryNumDic, brandNumDic, storeNumDic


    def persist(self):

        categoryDownloadPath = "D://aaaaa/category.csv"
        brandDownloadPath = "D://aaaaa/brand.csv"
        storeDownloadPath = "D://aaaaa/store.csv"

        categoryNumDic, brandNumDic, storeNumDic = self.matchProductAnalysis()

        categoryThread = threading.Thread(target = self.write2File, args = (categoryDownloadPath, categoryNumDic))
        brandThread = threading.Thread(target = self.write2File, args = (brandDownloadPath, brandNumDic))
        storeThread = threading.Thread(target = self.write2File, args = (storeDownloadPath, storeNumDic))

        categoryThread.start()
        brandThread.start()
        storeThread.start()

        # self.write2File(categoryDownloadPath, categoryNumDic)
        # self.write2File(brandDownloadPath, brandNumDic)
        # self.write2File(storeDownloadPath, storeNumDic)



    def write2File(self, downpath, typeDic):
        with open(downpath, 'w') as csvFile:
            data = []
            writer = csv.writer(csvFile)

            writer.writerow(['productType', 'count'])

            for key, value in typeDic.items():
                arr = [key, value]
                data.append(arr)

            writer.writerows(data)


if __name__ == "__main__":
    mpa = MatchProductAnalysis()
    mpa.persist()
