#!/usr/bin/env python
# -*- coding: utf-8 -*-

from backend import *
from api import *

class IndexProductId:
    def indexProductId(self):
        bk = Backend()

        productIds = bk.getProductId()
        bk.deleteProductId()

        for value in productIds:
            productId = value.get("productId")
            VoilaGo.IndexEs(productId)

if __name__ == '__main__':
    ip = IndexProductId()

    ip.indexProductId()