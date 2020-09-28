#!/usr/bin/env python
#-*- coding:utf-8

from api import *
from backend import *
import threading

def list_split(items, n):
    return [items[i:i+n] for i in range(0, len(items), n)]

def indexProducts(products):
    for product in products:
        id = product.get("id")
        VoilaGo.IndexEs(id)

if __name__ == "__main__":
    bk = Backend()
    CPUS = 8
    #products = bk.all_enabled_products()
    products = bk.all_enabled_products_in_taxon(11099)
    productArrayList = list_split(products, len(products) / CPUS)
    threads = []
    for productArray in productArrayList:
        t1 = threading.Thread(target=indexProducts,args=(productArray,))
        threads.append(t1)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

