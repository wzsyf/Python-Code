# -*- coding: utf-8 -*-

import csv
import requests

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
        categoryArr = []
        brandArr = []
        storeArr = []

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
                            categoryArr.append(taxons1Main)
                        elif taxons1Main.startswith('brand'):
                            brandArr.append(taxons1Main)
                        else:
                            storeArr.append(taxons1Main)

                        for taxons1Other in taxons1Others:
                            if taxons1Other.startswith('category'):
                                categoryArr.append(taxons1Other)
                            elif taxons1Other.startswith('brand'):
                                brandArr.append(taxons1Other)
                            else:
                                storeArr.append(taxons1Main)

                        alternativeProducts = productRelation['alternativeProducts']
                        for alternativeProduct in alternativeProducts:
                            taxons2 = alternativeProduct['taxons']
                            taxons2Main = taxons2['main']
                            taxons2Others = taxons2['others']

                            if taxons2Main.startswith('category'):
                                categoryArr.append(taxons2Main)
                            elif taxons2Main.startswith('brand'):
                                brandArr.append(taxons2Main)
                            else:
                                storeArr.append(taxons2Main)

                            for taxons2Other in taxons2Others:
                                if taxons2Other.startswith('category'):
                                    categoryArr.append(taxons2Other)
                                elif taxons2Other.startswith('brand'):
                                    brandArr.append(taxons2Other)
                                else:
                                    storeArr.append(taxons2Main)

                else:
                    print("productRelations not exsist!")

        categoryCount = len(categoryArr)
        brandCount = len(brandArr)
        storeCount = len(storeArr)

        return categoryCount, brandCount, storeCount


    def persist(self):

        downloadPath = "D://aaaaa/productType.csv"
        categoryCount, brandCount, storeCount = self.matchProductAnalysis()

        with open(downloadPath, 'w') as csvFile:
            writer = csv.writer(csvFile)

            writer.writerow(['productType', 'count'])

            data = [
                ['category', categoryCount],
                ['brand', brandCount],
                ['store', storeCount]
            ]

            writer.writerows(data)


if __name__ == "__main__":
    mpa = MatchProductAnalysis()
    mpa.persist()
