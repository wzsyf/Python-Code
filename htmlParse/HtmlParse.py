#!/usr/bin/env python
# -*- coding: utf-8 -*-

from backendV3 import *

class HtmlParse:

    def htmlParse(self):
        bk = Backend()
        bk.htmlParser()

if __name__ == "__main__":
    hp = HtmlParse()
    hp.htmlParse()