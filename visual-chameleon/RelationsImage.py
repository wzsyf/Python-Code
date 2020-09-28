#!/usr/bin/env python
# -*- coding: utf-8 -*-

from backend import *


class RelationsImage:

    def matchProduct(self, flags=[], minScore=0.4):
        bk = Backend()

        haveNotMatcProduct = bk.haveNotMatchProduct(flags)

        for post in haveNotMatcProduct:

            postId = post.get("id")
            image = post.get("image") or None
            if not image:
                continue

            email = bk.queryEmailByPostId(postId)

            loginInfo = Voila.login(email, "demo")
            auth = loginInfo.get("token")

            print(postId, email)

            productsSimilar = VoilaGo.SearchSimilarProducts(image, minScore)
            if len(productsSimilar) > 0:
                print postId, email
                Voila.PostRelations(auth, postId, productsSimilar)

                Voila.EnablePost(auth, postId)

if __name__ == "__main__":

    ri = RelationsImage()

    monthFlags = ["month-apr", "month-may", "month-jun", "month-jul", "month-aug", "month-sept", "month-oct"]
    ri.matchProduct(monthFlags, 0.51)



