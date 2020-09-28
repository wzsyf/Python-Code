#!/usr/bin/env python
# -*- coding: utf-8 -*-


from api import *

class SearchTest:
    def search(self):
        data = VoilaGo.GetSearchResult
        print data

if __name__ == "__main__":
    st = SearchTest()
    st.search()