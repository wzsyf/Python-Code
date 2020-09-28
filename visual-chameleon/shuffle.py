#!/usr/bin/env python
# -*- coding: utf-8 -*-

from backend import *

if __name__ == "__main__":
    bk = Backend()

    flags = ["f_20200902_sleepwear", "f_20200902_new", "f_20200902_under25", "f_20200902_gold",
             "f_20200902_topbags", "f_20200902_shorts", "f_20200826_hoodies", "f_20200826_heels",
             "f_20200826_nike", "f_20200826_sneakers", "f_20200826_luxury", "f_20200820_sunglasses",
             "f_20200807_nikeshoes", "f_20200820_activewear", "f_20200820_denim"]

    bk.ShuffleProductByFlag(flags)