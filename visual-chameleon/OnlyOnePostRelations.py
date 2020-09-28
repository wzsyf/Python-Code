#!/usr/bin/env python

from backend import *


class RelationsImage:

    def matchProduct(self, flags=[], minScore=0.4):

        postId = 214758
        image = "https://fashion-data-mining.s3.amazonaws.com/d576bdfe4bc22a9690cd42b5bde567b7"

        email = '266@a.com'

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



