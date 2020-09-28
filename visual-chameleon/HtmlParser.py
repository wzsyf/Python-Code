#!/usr/bin/env python
# -*- coding: utf-8 -*-

import HTMLParser

class HtmlParser:
    def htmlParser(self):
        parser = HTMLParser.HTMLParser()
        res = str(parser.unescape('Low-top take on the iconic Nike AF-1, with updated Nike Air technology for cushioning. Perforated vamp upper and star-studded bumper toe. Rubber outsole built on a cupsule design for traction. Streetwear staple since 1982. **Content + Care** |- Leather, Rubber |- Spot Clean |- Imported **Size + Fit** |- True to size '))
        print(res)
        print(type(res))


if __name__ == '__main__':
    hp = HtmlParser()
    hp.htmlParser()