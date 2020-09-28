#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from slugify import slugify


class VoilaStats:
    host = "http://localhost:3010"

    @staticmethod
    def recordOrder(postId, customerId, productId, orderId, createdAt):
        route = "/v1/order/action?post_id={0}&customer_id={1}&product_id={2}&order_id={3}&created_at={4}".format(postId,
                                                                                                                 customerId,
                                                                                                                 productId,
                                                                                                                 orderId,
                                                                                                                 createdAt)
        uri = VoilaStats.host + route
        resp = requests.get(uri)
        data = resp.text
        data = json.loads(data)


class VoilaGo:
    host = "http://localhost:3000"
    host = "http://backend.voila.fashion"
    host = "http://i.voila.fashion"
    host = "http://localhost:3000"

    @staticmethod
    def PostPostNoAuth(customerId, im_id, tags, title, desc, base_like):
        route = "/shop-api/account/blog/post-noAuth"
        uri = VoilaGo.host + route

        headers = {}
        headers["Content-Type"] = "application/json"
        # headers["Authorization"] = "Bearer {0}".format(auth)

        data = {}
        data["customerId"] = customerId
        data["hashtags"] = tags
        data["postImageId"] = im_id
        data["title"] = title
        data["slug"] = slugify(title)
        data["shortDescription"] = desc
        data["base_like"] = base_like

        data = json.dumps(data)

        resp = requests.post(uri, data=data, headers=headers)

        data = resp.text
        data = json.loads(data)

        return data.get("id") or None


    @staticmethod
    def PostImageNoAuth(customerId, img_path):
        headers = {}
        #headers["Content-Type"] = "multipart/form-data; boundary=--------voila"
        headers["Authorization"] = "{0}".format(customerId)
        img = open(img_path, 'rb')
        files = {}
        files["file"] = (img_path, img)
        route = "/shop-api/account/blog/post/image/noAuth"
        uri = VoilaGo.host + route
        resp = requests.post(uri, data={}, files=files, headers=headers)
        data = resp.text
        print data
        resp.close()
        data = json.loads(data)
        return data.get("id") or None


    @staticmethod
    def DeleteIndexById(productId):
        route = "/shop-api/delete-index/{0}".format(productId)
        uri = VoilaGo.host + route

        resp = requests.delete(uri)

        respData = resp.text
        respData = json.loads(respData)

        return respData


    @staticmethod
    def DeleteProductClick(productId):
        route = "/shop-api/delete-productClick/{0}".format(productId)
        uri = VoilaGo.host + route

        resp = requests.delete(uri)

        respData = resp.text
        respData = json.loads(respData)

        return respData


    @staticmethod
    def GetSearchResult():
        route = "/shop-api/getclick-list?customerId=280"
        uri = VoilaGo.host + route

        resp = requests.get(uri)

        respData = resp.text
        respData = json.loads(respData)

        return respData




    @staticmethod
    def PostProductClick(dataDic):
        route = "/shop-api/productclick"
        uri = VoilaGo.host + route

        headers = {}
        headers["Content-Type"] = "application/json"
        headers["Connection"] = "Keep-Alive"

        data = json.dumps(dataDic)
        resp = requests.post(uri, data=data, headers=headers)

        respData = resp.text
        respData = json.loads(respData)

        return respData


    @staticmethod
    def AddFlagToPost(postId, flag):

        route = "/shop-api/account/blog/post/{0}/flag/{1}".format(postId, flag)
        uri = VoilaGo.host + route

        data = {}

        resp = requests.put(uri, data=data)
        data = resp.text
        data = json.loads(data)
        return data

    @staticmethod
    def GetPostsByImage(imageUrl):
        route = "/api/blog/posts/post-by-img-url?image_url={0}".format(imageUrl)
        uri = VoilaGo.host + route
        resp = requests.get(uri)
        data = resp.text
        data = json.loads(data)
        return data.get("items") or []

    @staticmethod
    def PostVideo(postImageId, f):
        route = "/shop-api/account/blog/post/video"
        uri = VoilaGo.host + route

        files = {"file": open(f, "rb")}

        data = {}
        data["postImageId"] = postImageId
        resp = requests.post(uri, data=data, files=files)
        data = resp.text
        print data

    @staticmethod
    def IndexEs(productId):
        route = "/index/product/{0}".format(productId)
        uri = VoilaGo.host + route
        resp = requests.get(uri)
        data = resp.text
        print data

    @staticmethod
    def UpdateProduct(data):
        route = "/shop-api/update/product"
        uri = VoilaGo.host + route

        headers = {}
        headers["Content-Type"] = "application/json"

        data = json.dumps(data)
        resp = requests.put(uri, data=data, headers=headers)
        data = resp.text
        print data

    @staticmethod
    def UpdatePrice(data):
        route = "/shop-api/price/product"
        uri = VoilaGo.host + route

        resp = requests.put(uri, data=data)
        data = resp.text
        print data

    @staticmethod
    def Search():
        route = "/shop-api/product?locale=en_US&channel=US_WEB"
        uri = VoilaGo.host + route

        headers = {}
        headers["Content-Type"] = "application/json"

        data = {}
        data["genderTaxonCodes"] = ["category-women"]
        data["storeTaxonCodes"] = ["store-asos"]
        data["storeTaxonCodes"] = ["store-6pm-com", "store-asos"]
        data["storeTaxonCodes"] = ["store-asos", "store-6pm-com"]
        data["storeTaxonCodes"] = ["store-asos"]
        data = json.dumps(data)
        resp = requests.put(uri, data=data, headers=headers)
        data = resp.text
        print data

    @staticmethod
    def SimilarRecommend():
        route = "/api/similar/recommend"
        uri = VoilaGo.host + route
        data = []
        data.append({"product_code": "a0313e4ed87fe33d5f0453929a7eb77b", "price": 19470})
        data.append({"product_code": "d5c5d02e0efbec72c5e5eba223b08965", "price": 1350})
        data = json.dumps(data)

        resp = requests.post(uri, data=data)
        data = resp.text
        print data.encode("utf-8")

    @staticmethod
    def uploadS3(path):
        route = "/shop-api/upload/aws?path={0}".format(path)
        uri = VoilaGo.host + route
        resp = requests.get(uri)
        data = resp.text
        data = json.loads(data)
        print data
        return data.get("url") or None

    @staticmethod
    def PostsNeedUpdateRelations(email):
        host = "http://i.voila.fashion"
        route = "/shop-api/no-relation/post?email={0}".format(email)
        uri = host + route
        resp = requests.get(uri)
        data = resp.text
        data = json.loads(data)
        if data.get("items"):
            return data.get("items")

        return []

    @staticmethod
    def SearchSimilarProducts(imgUrl, minScore=0.4, limit=20):
        host = "http://i.voila.fashion"

        result = []
        route = "/shop-api/products/discover-similar/by-img-url?img_url={0}&limit=100".format(imgUrl)
        uri = host + route

        headers = {}
        headers["Content-Type"] = "application/json"

        # data = {}
        # data["storeTaxonCodes"] = ["store-farfetch", "store-macy-s"]
        # data["categoryTaxonCodes"] = ["category-women-clothing"]
        # data = json.dumps(data)
        resp = requests.post(uri, headers=headers)
        data = resp.text
        data = json.loads(data)
        productListArray = data.get("items")
        for productList in productListArray:
            codes = []
            for item in productList:
                if item.get("score") >= minScore:
                    codes.append(item.get("code"))

            if len(codes) > limit:
                codes = codes[0:limit]

            if len(codes) > 0:
                result.append(codes)

        return result


class Elastic:
    host = "http://localhost:9200"

    @staticmethod
    def getProduct(id):
        try:
            route = "/sylius/product/{0}/_source".format(id)
            uri = Elastic.host + route
            resp = requests.get(uri)
            data = resp.text
            data = json.loads(data)
            return data
        except Exception, ex:
            return None

    @staticmethod
    def putProduct(id, data):
        try:
            data = json.dumps(data)
            route = "/sylius/product/{0}".format(id)
            uri = Elastic.host + route

            headers = {}
            headers["Content-Type"] = "application/json"

            resp = requests.put(uri, headers=headers, data=data)
            data = resp.text
            print data
            # data = json.loads(data)
            return data
        except Exception, ex:
            print ex
            return None


class Voila:
    host = "http://localhost:3000"
    host = "http://18.144.156.163"
    host = "http://13.57.246.100"
    host = "http://52.52.236.31"
    host = "http://backend.voila.fashion"

    @staticmethod
    def register(email, username, pwd):
        # route = "/shop-api/register"
        route = "/shop-api/signup"
        uri = Voila.host + route
        data = {}
        data["username"] = username
        data["email"] = email
        data["plainPassword"] = pwd
        data["birthday"] = "1995-01-01 00:00:00"
        data["channelCode"] = "US_WEB"
        resp = requests.post(uri, data)
        data = resp.text
        data = json.loads(data)
        return data

    @staticmethod
    def login(username, password):
        route = "/shop-api/login/check"
        uri = Voila.host + route
        data = {}
        data["_username"] = username
        data["_password"] = password
        resp = requests.post(uri, data)
        data = resp.text
        data = json.loads(data)
        return data

    @staticmethod
    def refresh_token(token):
        host = "http://backend.voila.fashion"
        route = "/shop-api/token/refresh"
        # uri = Voila.host + route
        uri = host + route
        data = {}
        data["refresh_token"] = token
        resp = requests.post(uri, data)
        data = resp.text
        data = json.loads(data)
        return data

    @staticmethod
    def withdraw(auth, amount):
        route = "/shop-api/account/withdraw"
        uri = Voila.host + route
        # uri = host + route
        headers = {}
        headers["Authorization"] = "Bearer {0}".format(auth)

        data = {}
        data["amount"] = amount

        resp = requests.post(uri, headers=headers, data=data)
        data = resp.text
        print data

    @staticmethod
    def wishlist(auth, channel, locale, limit):
        host = "http://backend.voila.fashion"
        route = "/shop-api/account/wishlist/default/item?channel={0}&locale={1}&limit={2}".format(channel, locale,
                                                                                                  limit)
        # uri = Voila.host + route
        uri = host + route
        headers = {}
        headers["Authorization"] = "Bearer {0}".format(auth)

        resp = requests.get(uri, headers=headers)
        data = resp.text
        print data

    @staticmethod
    def all_wishlist(auth, channel, locale, limit):
        host = "http://backend.voila.fashion"
        route = "/shop-api/account/wishlist?channel={0}&locale={1}&limit={2}".format(channel, locale, limit)
        uri = Voila.host + route
        # uri = host + route
        headers = {}
        headers["Authorization"] = "Bearer {0}".format(auth)

        resp = requests.get(uri, headers=headers)
        data = resp.text
        print data

    @staticmethod
    def getAccountInfo(auth):
        route = "/shop-api/account"
        # uri = Voila.host + route
        uri = "http://backend.voila.fashion" + route
        headers = {}
        headers["Authorization"] = "Bearer {0}".format(auth)

        resp = requests.get(uri, headers=headers)
        data = resp.text
        print data

    @staticmethod
    def PutAccount(auth, data):
        # data["lastName"] = ""
        # data["firstName"] = ""
        route = "/shop-api/account"
        uri = Voila.host + route
        headers = {}
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = "Bearer {0}".format(auth)

        data = json.dumps(data)

        resp = requests.put(uri, headers=headers, data=data)
        data = resp.text

    @staticmethod
    def statistics(auth):
        route = "/shop-api/account/statistics?interval=last-7days"
        uri = Voila.host + route
        headers = {}
        headers["Authorization"] = "Bearer {0}".format(auth)

        resp = requests.get(uri, headers=headers)
        data = resp.text
        print data

    @staticmethod
    def disable(id, auth):
        route = "/shop-api/account/blog/post/{0}/disable".format(id)
        uri = Voila.host + route
        headers = {}
        headers["Authorization"] = "Bearer {0}".format(auth)

        resp = requests.request("PATCH", uri, headers=headers)
        data = resp.text
        print data

    @staticmethod
    def searchSimilarUpload(img_path):
        headers = {}
        headers["Content-Type"] = "image/jpg"
        data = open(img_path, 'rb').read()
        route = "/shop-api/product/search-similar/upload"
        uri = Voila.host + route
        # uri = "http://stage.voila.fashion" + route
        print uri
        resp = requests.post(uri, data=data, headers=headers)
        data = resp.text
        resp.close()
        print data
        data = json.loads(data)
        return data.get("id") or None

    @staticmethod
    def searchSimilarByImage(im_id, detect="bottom"):
        host = "http://stage.voila.fashion"
        uri = "{0}/shop-api/product/search-similar/by-image/{1}?channel=US_WEB&page=1&limit=25&box=391,888,503,1021&score_min=0&detection={2}".format(
            Voila.host, im_id, detect)
        uri = "{0}/shop-api/product/search-similar/by-image/{1}?channel=US_WEB&page=1&limit=25&score_min=0&detection={2}&score=true".format(
            Voila.host, im_id, detect)

        headers = {}
        headers["Content-Type"] = "application/json"

        data = {}
        # data["genderTaxonCodes"] = ["category-women"]
        # data["storeTaxonCodes"] = ["store-asos"]
        # data["storeTaxonCodes"] = ["store-6pm-com", "store-asos"]
        # data["storeTaxonCodes"] = ["store-asos", "store-6pm-com"]
        # data["storeTaxonCodes"] = ["store-zappos"]
        data = json.dumps(data)
        resp = requests.put(uri, data=data)
        data = resp.text
        resp.close()
        print data
        data = json.loads(data)

    @staticmethod
    def searchSimilarByProduct(product_id):
        uri = "{0}/shop-api/product/search-similar/by-product/{1}?channel=US_WEB&locale=en_US&limit=18&page=1&fq[gender]=".format(
            Voila.host, product_id)

        headers = {}
        headers["Content-Type"] = "application/json"

        data = {}
        data["genderTaxonCodes"] = ["category-women"]
        data["categoryTaxonCodes"] = ["category-women"]
        data = json.dumps(data)

        resp = requests.put(uri, data=data, headers=headers)
        data = resp.text
        resp.close()
        data = json.loads(data)
        print data

    @staticmethod
    def listProductsOfCategory(cates):
        data = {}
        data["categoryTaxonCodes"] = cates
        uri = "{0}/shop-api/product?channel=US_WEB&locale=en_US&limit=18&page=1&score_min=0.4".format(Voila.host)
        print uri
        resp = requests.put(uri)
        data = resp.text
        resp.close()
        data = json.loads(data)
        print data

    @staticmethod
    def PostAvatar(auth, img_path):
        headers = {}
        headers["Content-Type"] = "image/jpg"
        headers["Authorization"] = "Bearer {0}".format(auth)
        data = open(img_path, 'rb').read()
        route = "/shop-api/account/image/avatar"
        uri = Voila.host + route
        resp = requests.post(uri, data=data, headers=headers)
        data = resp.text
        resp.close()
        data = json.loads(data)
        return data.get("id") or None

    @staticmethod
    def PostImage(auth, img_path):
        headers = {}
        headers["Content-Type"] = "image/jpg"
        headers["Authorization"] = "Bearer {0}".format(auth)
        data = open(img_path, 'rb').read()
        route = "/shop-api/account/blog/post/image"
        uri = Voila.host + route
        resp = requests.post(uri, data=data, headers=headers)
        data = resp.text
        print data
        resp.close()
        data = json.loads(data)
        return data.get("id") or None

    @staticmethod
    def PostImageByUrl(auth, img_path):
        headers = {}
        # headers["Content-Type"] = "image/jpg"
        headers["Authorization"] = "Bearer {0}".format(auth)
        data = {}
        data["img_url"] = img_path
        route = "/shop-api/account/blog/post/image"
        uri = Voila.host + route
        resp = requests.post(uri, data=data, headers=headers)
        data = resp.text
        print data
        resp.close()
        data = json.loads(data)
        return data.get("id") or None

    @staticmethod
    def PostRelations(auth, postId, productArray):
        headers = {}
        # headers["Content-Type"] = "image/jpg"
        headers["Authorization"] = "Bearer {0}".format(auth)

        relations = []
        index = 0
        for arr in productArray:
            if len(arr) <= 0:
                continue
            index += 1
            relation = {}
            relation["position"] = index
            relation["originalProductCode"] = arr[0]
            relation["alternativeProductCodes"] = arr[1:]
            relations.append(relation)

        relations = json.dumps(relations)

        route = "/shop-api/account/blog/post/{0}/relations?channel=US_WEB&locale=en_US".format(postId)
        uri = Voila.host + route
        resp = requests.post(uri, data=relations, headers=headers)
        data = resp.text

    @staticmethod
    def PostPost(auth, im_id, tags, title, desc, base_like):
        route = "/shop-api/account/blog/post"
        uri = Voila.host + route

        headers = {}
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = "Bearer {0}".format(auth)

        data = {}
        data["hashtags"] = tags
        data["postImageId"] = im_id
        data["title"] = title
        data["slug"] = slugify(title)
        data["shortDescription"] = desc
        data["base_like"] = base_like

        data = json.dumps(data)

        resp = requests.post(uri, data=data, headers=headers)

        data = resp.text
        data = json.loads(data)

        return data.get("id") or None

    @staticmethod
    def EnablePost(auth, post_id):
        route = "/shop-api/account/blog/post/{0}/enable".format(post_id)

        uri = Voila.host + route
        headers = {}
        headers["Authorization"] = "Bearer {0}".format(auth)

        resp = requests.request("PATCH", uri, headers=headers)
        data = resp.text
        print data

    @staticmethod
    def getPosts(auth):
        route = "/shop-api/account/blog/post?channel=US_WEB&locale=en_US&page=1&limit=4"

        uri = Voila.host + route
        headers = {}
        headers["Authorization"] = "Bearer {0}".format(auth)

        resp = requests.request("GET", uri, headers=headers)
        data = resp.text
        print data

    @staticmethod
    def putTaxonProduct(id, data):
        route = "/api/taxonproduct/{0}".format(id)
        uri = "http://localhost:3000" + route

        resp = requests.request("PUT", uri, data=data)
        data = resp.text
        print data

    @staticmethod
    def PostBlock(auth, data):
        route = "/shop-api/account/cms/block"
        uri = Voila.host + route

        headers = {}
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = "Bearer {0}".format(auth)
        resp = requests.post(uri, data=data, headers=headers)

        data = resp.text
        data = json.loads(data)

        return data.get("id") or None

    @staticmethod
    def PubBlock(auth, data):
        route = "/shop-api/account/cms/block/{0}".format(data.get("id"))
        uri = Voila.host + route

        headers = {}
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = "Bearer {0}".format(auth)
        data = json.dumps(data)
        resp = requests.put(uri, data=data, headers=headers)

        data = resp.text
        data = json.loads(data)
        print data

        return data.get("id") or None

    @staticmethod
    def PostCover():
        host = "http://localhost:3000"
        route = "/shop-api/cover"
        uri = host + route

        data = {}
        data["header"] = "FIRST ARRIVAL"
        data["request"] = "/shop-api/product?flags[first-arrival]=1&channel=US_WEB&locale=en_US"
        data["image"] = "https://fashion-data-mining.s3.amazonaws.com/007ef2eccbca0c82a09bb75303ea3638"
        data["enabled"] = 1

        resp = requests.post(uri, data=data)

        data = resp.text
        data = json.loads(data)
        print data

        return data.get("id") or None

    @staticmethod
    def PutCover(data):
        host = "http://localhost:3000"
        route = "/shop-api/cover/{0}".format(data.get("id"))
        uri = host + route

        resp = requests.put(uri, data=data)

        data = resp.text
        data = json.loads(data)
        print data

        return data.get("id") or None

    @staticmethod
    def AddFlagToPost(postId, flag):
        loginInfo = Voila.login("jorsion@foxmail.com", "123456")
        auth = loginInfo.get("token")

        route = "/shop-api/account/blog/post/{0}/flag/{1}".format(postId, flag)
        uri = Voila.host + route

        headers = {}
        headers["Authorization"] = "Bearer {0}".format(auth)

        data = {}

        resp = requests.put(uri, headers=headers, data=data)
        data = resp.text
        print data

    @staticmethod
    def NewAddFlagToProduct(auth, productCode, flag):
        route = "/shop-api/account/product/{0}/flag/{1}".format(productCode, flag)
        uri = Voila.host + route

        headers = {}
        headers["Authorization"] = "Bearer {0}".format(auth)

        data = {}

        resp = requests.put(uri, headers=headers, data=data)
        data = resp.text
        print data

    @staticmethod
    def AddFlagToProduct(auth, productCode, flag, rank):
        route = "/shop-api/account/product/{0}/flag/{1}".format(productCode, flag)
        uri = Voila.host + route

        headers = {}
        headers["Authorization"] = "Bearer {0}".format(auth)

        data = {}
        data["pretty_rank"] = rank

        resp = requests.put(uri, headers=headers, data=data)
        data = resp.text
        print data

    @staticmethod
    def DeleteFlagFromProduct(auth, productCode, flag):
        route = "/shop-api/account/product/{0}/flag/{1}".format(productCode, flag)
        uri = Voila.host + route

        headers = {}
        headers["Authorization"] = "Bearer {0}".format(auth)

        resp = requests.delete(uri, headers=headers, data=None)
        data = resp.text
        print data
        # data = json.loads(data)
        # print data


if __name__ == "__main__":
    loginInfo = Voila.login("jorsion@foxmail.com", "123456")
    auth = loginInfo.get("token")
    # Voila.AddFlagToPost(auth, 174551, "test")
    # # Voila.wishlist(auth, "CN_WEB", "zh_CN", 10)
    # # Voila.statistics(auth)
    # #Voila.disable(237, auth)
    # Voila.register()
    # #loginInfo =  Voila.login("nkwill@126.com", "123456")
    # loginInfo =  Voila.login("jorsion@foxmail.com", "123456")
    # loginInfo =  Voila.login("nkwill@gmail.com", "test")
    # loginInfo =  Voila.login("yiqifa@yiqifa.com", "123456")
    # print loginInfo
    # auth = loginInfo.get("token")
    # #Voila.wishlist(auth, "CN_WEB", "zh_CN", 10)
    # Voila.all_wishlist(auth, "CN_WEB", "zh_CN", 10)
    # Voila.withdraw(auth, 100)
    # Voila.getPosts(auth)

    # Voila.AddFlagToProduct(auth, "61d86a8e48a5cfe150abcfb7ff96c22b", "fashion-girl-picks")
    # Voila.DeleteFlagFromProduct(auth, "61d86a8e48a5cfe150abcfb7ff96c22b", "fashion-girl-picks")
    # Voila.AddFlagToProduct(auth, "61d86a8e48a5cfe150abcfb7ff96c22b", "fashion-girl-picks")

    # refresh_token = loginInfo.get("refresh_token")
    # print refresh_token
    # Voila.refresh_token(refresh_token)

    # print "get account"
    # Voila.getAccountInfo(auth)
    # Voila.statistics(auth)

    # im_id = Voila.searchSimilarUpload("couple.png")
    # print im_id

    # im_id = Voila.postImageByUrl(auth, "https://fashion-data-mining.s3.amazonaws.com/42d8f497e274fe933b4a30dda94e790e")
    # print im_id
    # Voila.searchSimilarByImage(im_id)
    # Voila.searchSimilarByProduct("6a85b3bddc299487cf04caaeb89af976")
    # Voila.listProductsOfCategory(["category-women-bags"])

    data = {}
    data["id"] = 2
    data["code"] = "fashion-girl-picks"
    data["header"] = "Fashion Girl Picks"
    data["type"] = "product"
    data["style"] = "0101001"
    data["request"] = "/shop-api/product?flags[fashion-girl-picks]=1&channel=US_WEB&locale=en_US"
    data["list_type"] = 0
    data["channels"] = ["US_WEB", "CN_WEB"]
    # Voila.PubBlock(auth, data)

    data = {}
    data["id"] = 4
    data["code"] = "the-fabulous-haggle"
    data["header"] = "THE FABULOUS HAGGLE"
    data["type"] = "product"
    data["style"] = "0101002"
    data["request"] = "/shop-api/product?flags[the-fabulous-haggle]=1&channel=US_WEB&locale=en_US"
    data["list_type"] = 0
    data["channels"] = ["US_WEB", "CN_WEB"]
    # Voila.PubBlock(auth, data)

    # Voila.PostCover()
    data = {}
    data["id"] = 1
    data["request"] = "/shop-api/product?flags[first-arrival]=1&channel=US_WEB&locale=en_US"
    # Voila.PutCover(data)

    data = {}
    data["id"] = 8
    data["code"] = "first-arrival"
    data["header"] = "FIRST-ARRIVAL"
    data["type"] = "cover"
    data["style"] = "0301001"
    data["request"] = "/shop-api/covers?channel=US_WEB&locale=en_US"
    data["list_type"] = 0
    data["position"] = 0
    data["channels"] = ["US_WEB", "CN_WEB"]
    # Voila.PubBlock(auth, data)

    # VoilaGo.SimilarRecommend()
    # VoilaGo.Search()
    # Voila.NewAddFlagToProduct(auth, "23d39dbdf94b4e912bdf99e4b01eecb9", "test")
    # Voila.DeleteFlagFromProduct(auth, "e330f03ff956bb13a26186588c9bdca8", "featured-designer")

    # VoilaGo.uploadS3("/l4.jpeg")

    data = {}
    data["product_id"] = "Zappos-9282102-14-W"
    data["product_id"] = 'asos-10000013-w'
    data["price"] = 10000
    data["msrp"] = 10000000
    # variants = []
    # variants.append({"size": "S - UK 8 - UK 10", "price": 3200, "msrp": 3200})
    # data["variants"] = variants

    # VoilaGo.UpdatePrice(data)

    # VoilaGo.PostVideo(175137, "/Users/jorsion/Documents/final.mp4")
    # VoilaGo.PostVideo(175142, "/Users/jorsion/tiktok1.mp4")
    # VoilaGo.PostVideo(175139, "/Users/jorsion/tiktok2.mp4")
    # VoilaGo.SearchSimilarProducts()
    # VoilaGo.SearchSimilarProducts("https://fashion-data-mining.s3.amazonaws.com/0b4201a7b05d8a5d08c38bc2d28cd9a4")
    # items = VoilaGo.GetPostsByImage("https://fashion-data-mining.s3.amazonaws.com/26026bacc0b024ac5b8edbb1ebed09f4")
    # print items
    VoilaGo.AddFlagToPost(174563, "tes")
