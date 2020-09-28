#!/usr/bin/env python
# -*- coding: utf-8 -*-

from api import *

class DeleteProductClick:
    def deleteProductClick(self, productId):

        data = VoilaGo.DeleteProductClick(productId)
        print data

if __name__ == "__main__":
    productId = 741483
    dpc = DeleteProductClick()

    dpc.deleteProductClick(productId)