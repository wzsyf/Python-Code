#!/usr/bin/env python
# -*- coding: utf-8 -*-

from api import *
from backend import *

bk = Backend()

def clear(flag):
     global bk
     index = 0
     bk.ClearProductsWithFlag(flag)

def promote(flag, gender=None, store=None, category=None, subCategory=None, brand=None, discountRange=None, priceRange=None):
     global bk
     clear(flag)

     codes = []
     for product in VoilaGo.SearchProducts(gender, store, category, subCategory, brand, discountRange, priceRange):
         code = product.get("code")
         codes.append(code)

     print flag, len(codes)

     for code in reversed(codes):
         print flag, code
         bk.AddFlagToProduct(code, flag)

if __name__ == "__main__":
     # promote("f_20200724_sleepwear", None, ["store-shopbop"], None, ["category-women-clothing-lounge-sleepwear"], None, "40,80", None)
     # promote("f_20200724_tops", None, ["store-revolve"], None, ["category-women-clothing-tops"], None, "40,80", None)
     # promote("f_20200727_under100", None, ["store-selfridges"], ["category-women-clothing"], None, None, "50,99", "0,10000")
     # promote("f_20200727_under150", None, ["store-selfridges"], ["category-women-shoes"], None, None, "50,99", "0,15000")
     # promote("f_20200727_70off", ["category-women"], ["store-shopbop"], None, None, None, "70", None)
     # promote("f_20200727_sunglass", ["category-women"], ["store-nordstrom-rack"], None, ["category-women-accessories-sunglasses-eyewear"], No    ne, "60,90", None)
     # promote("f_20200727_nike", ["category-women"], ["store-nordstrom-rack"], ["category-women-clothing", "category-women-bags", "category-wo    men-shoes"], None, ["brand-nike"], "30,70", None)

    promote("f_20200731_handbags", None, ["store-saks-fifth-avenue-off-5th"], ["category-women-bags"], None, None, "40,80",
        None)

    promote("f_20200731_beach", None, ["store-saks-fifth-avenue-off-5th"], None,
        ["category-women-clothing-swimwear-coverups"], None, "30,90", None)

    promote("f_20200731_otherstories", None, ["store-other-stories"], ["category-women-clothing "], None, None, "20,90",
        None)
