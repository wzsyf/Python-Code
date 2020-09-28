#!/usr/bin/env
# -*- coding: utf-8 -*-

import sqlalchemy as sa
import json
import random
import time
import itertools
import requests
import datetime
from visearch import client
from api import *
from slugify import slugify
from bitly import *
#from user_map import *

source = 'mysql://mysqldev:mysqlpwd@localhost/odesk_visual_chameleon_sylius'
source_import = 'mysql://mysqldev:mysqlpwd@localhost/odesk_visual_chameleon_sylius_import'

access_key = "bfdd1db783b2bd0e75279919af83bf04"
secret_key = "d85f7ef4d829ed9a5ed703901b037abc"

def list_split(items, n):
    return [items[i:i+n] for i in range(0, len(items), n)]

def get_visense_api():
    api = client.ViSearchAPI(access_key, secret_key)
    return api

def get_pg_conn(source):
    ng = sa.create_engine(source, encoding='utf8', echo = False)
    conn = ng.connect()
    return conn

class Backend:

    def __init__(self):
        self.conn = get_pg_conn(source)
        self.conn_import = get_pg_conn(source_import)
        self.visense_api = get_visense_api()

    def short_url_for_blogs(self):
        sql = "select id, code from mukhin_sylius_blogging_blog where short_url is null or short_url ='' order by id desc"
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            blogId = row["id"]
            blogCode = row["code"]
            blogCode = slugify(blogCode)
            print blogId, blogCode
            #shortUrl = Bitly.CustomizeBlogUrl(blogCode)

    def post_updated_recently_time(self):
        sql = "select max(updated_at) as updated_at from mukhin_sylius_blogging_post"
        res = self.conn.execute(sql)
        if res:
            row = res.fetchone()
            updatedAt = row["updated_at"]
            return updatedAt

        return None

    def resolve_avatar(self):
        sql = "select * from app_customer_image order by id desc limit 100"
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            path = row["path"]
            resolve_path = "https://backend.voila.fashion/media/cache/resolve/app_customer_image_avatar{0}".format(path)
            requests.get(resolve_path)

    def export_brand(self):
        sql = "select code, id from sylius_taxon where code like 'brand-%%' order by code desc"
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            code = row["code"]
            brandId = row["id"]
            sql = "select name from sylius_taxon_translation where translatable_id = {0} and locale = 'en_US'".format(brandId)
            res = self.conn.execute(sql)
            _row =res.fetchone()
            if _row:
                name = _row["name"]
                print '"{0}",{1},{2}'.format(name, code, "")

    def all_stores(self):
        result = []
        sql = "select * from sylius_taxon where code like 'store-%%'"
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            taxonId = row["id"]
            sql = "select * from sylius_taxon_translation where locale = 'en_US' and translatable_id = {0}".format(taxonId)
            res = self.conn.execute(sql)
            _row = res.fetchone()
            if _row:
                result.append(_row["name"])
        return result


    def hack_farfetch(self):
        sql = "select id from sylius_product where original_store = 'Farfetch' and created_at > '2020-08-05 00:00:00';"
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            productId = row["id"]
            sql = "delete from sylius_product where id = {0}".format(productId)
            self.conn.execute(sql)
            uri = "http://localhost:19200/product_v1/product/{0}".format(productId)
            print uri
            requests.delete(uri)

    def deactivate(self):
        sql = "select distinct(store) as store from productdata"
        res = self.conn_import.execute(sql)
        rows = res.fetchall()
        stores = []
        for row in rows:
            store = row["store"]
            #store = store.replace("'", "\\\'")
            if store == "Macy's":
                store = "Macy\\'s"
            stores.append("'{0}'".format(store))


        clause = "original_store in ({0})".format(",".join(stores))

        today = datetime.datetime.now()
        yestoday = today + datetime.timedelta(days = -1)
        today = "{0}-{1:0>2}-{2:0>2} 00:00:00".format(today.year, today.month, today.day)
        yestoday = "{0}-{1:0>2}-{2:0>2} 00:00:00".format(yestoday.year, yestoday.month, yestoday.day)

        sql = "update sylius_product_image set visearch_indexed=0 where owner_id in (select id from sylius_product where enabled=0 and last_imported_at >= '{0}' and {1})".format(yestoday, clause)
        self.conn.execute(sql)

        sql = "update sylius_product set enabled=1 where enabled=0 and last_imported_at >= '{0}' and {1}".format(yestoday, clause)
        print sql
        self.conn.execute(sql)

        sql = "select id from sylius_product where {0} and enabled=1".format(clause)
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            productId = row["id"]
            sql = "select count(*) as total from sylius_product_image where owner_id = {0}".format(productId)
            res = self.conn.execute(sql)
            _row = res.fetchone()
            imageCount = _row["total"]

            sql = "select count(*) as total from sylius_product_variant where product_id = {0}".format(productId)
            res = self.conn.execute(sql)
            _row = res.fetchone()
            varCount = _row["total"]

            if imageCount == 0 or varCount == 0 :
                sql = "update sylius_product set enabled=0 where id = {0}".format(productId)
                sql = "delete from sylius_product where id = {0}".format(productId)
                print sql
                self.conn.execute(sql)

    def AddFlagToProduct(self, code, flag):
        sql = "select * from sylius_product where code = '{0}'".format(code)
        res = self.conn.execute(sql)
        row = res.fetchone()
        if row:
            code = row["code"]
            id = row["id"]
            flags = row["flags"] or "[]"
            flags = json.loads(flags)
            if not flag in flags:
                flags.append(flag)
                flags = json.dumps(flags)
                sql = "update sylius_product set flags='{0}' where id = {1}".format(flags, id)
                print sql
                self.conn.execute(sql)
                VoilaGo.IndexEs(id)

    def ClearProductsWithFlag(self, flag, store=None):
        storeClause = ""
        if store:
            store = store.replace("'", "\\'")
            storeClause = " and original_store = '{0}'".format(store)

        sql = "select * from sylius_product where flags like '%%{0}%%'{1}".format(flag, storeClause)
        print sql
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            code = row["code"]
            id = row["id"]
            flags = row["flags"] or "[]"
            flags = json.loads(flags)
            if flag in flags:
                flags.remove(flag)
                flags = json.dumps(flags)
                sql = "update sylius_product set flags='{0}' where id = {1}".format(flags, id)
                self.conn.execute(sql)
                VoilaGo.IndexEs(id)

    def FixJsonTaxon(self):
        sql = "select * from sylius_taxon_translation where name like '%%{%%' and locale = 'en_US'"
        res = self.conn.execute(sql)
        rows = res.fetchall()
        idx = 0
        for row in rows:
            taxonId = row["translatable_id"]
            name = row["name"]
            name = json.loads(name)
            name = name.get("name") or name.get("title")
            name = slugify(name)
            code = "brand-{0}".format(name)
            sql = "select id from sylius_taxon where code = '{0}'".format(code)
            res = self.conn.execute(sql)
            _row = res.fetchone()
            if _row: 
                id = _row["id"]
                print id, taxonId, code
                sql = "select count(*) as total from sylius_product_taxon where taxon_id = {0}".format(taxonId)
                res = self.conn.execute(sql)
                row = res.fetchone()
                print row["total"]
                sql = "select product_id, taxon_id from sylius_product_taxon where taxon_id = {0}".format(taxonId)
                print sql
                res = self.conn.execute(sql)
                products = []
                _rows = res.fetchall()
                for r in _rows:
                    products.append(r["product_id"])

                if len(products) > 0:
                    sql = "update sylius_product_taxon set taxon_id = {0} where taxon_id = {1}".format((id), taxonId)
                    self.conn.execute(sql)
                    print sql
                    for product in products:
                        VoilaGo.IndexEs(product)
            sql = "delete from sylius_taxon where id = {0}".format(taxonId)
            print sql
            self.conn.execute(sql)

    def PostsHaveNoRelationsHot(self, flags=None):
        flagClause = ""
        if flags:
            clauses = []
            for flag in flags:
                clause = "flags like '%%{0}%%'".format(flag)
                clauses.append(clause)

            flagClause = "and ({0})".format(" OR ".join(clauses))

        sql = "select id, post_image_id, flags from mukhin_sylius_blogging_post where id not in (select post_id from mukhin_sylius_blogging_post_product_relation) {0} and not ( short_description like '%%LTK%%' OR short_description like '%%LIKEtoKNOW%%' OR short_description like '%%liketk%%' OR short_description like '%%liketoknow%%') order by base_like desc".format(flagClause)
        print sql
        res = self.conn.execute(sql)
        rows = res.fetchall()
        items = []
        for row in rows:
            postId = row["id"]
            postImageId = row["post_image_id"]
            sql = "select * from mukhin_sylius_blogging_post_image where id = {0}".format(postImageId)
            res = self.conn.execute(sql)
            row = res.fetchone()
            if row:
                cdnUrl = row["cdn_url"] or None
                if cdnUrl and cdnUrl != "" and cdnUrl != "None":
                    item = {}
                    item["id"] = postId
                    item["image"] = cdnUrl
                    items.append(item)

        return items

    def PostsHaveNoRelations(self, email, flags):
        items = []
        sql = "select id, post_image_id, flags from mukhin_sylius_blogging_post where enabled = 0 and LOCATE('blocked-post',flags) = 0 and blog_id in (select id from mukhin_sylius_blogging_blog where customer_id in (select id from sylius_customer where email = '{0}')) and id not in (select post_id from mukhin_sylius_blogging_post_product_relation) and not ( short_description like '%%LTK%%' OR short_description like '%%LIKEtoKNOW%%' OR short_description like '%%liketk%%' OR short_description like '%%liketoknow%%') order by base_like desc".format(email)
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            postId = row["id"]
            postImageId = row["post_image_id"]
            _flags = row["flags"]
            _flags = json.loads(_flags) or []
            hasFlags = True
            if len(flags) == 0:
                hasFlags = True
            else:
                hasFlags = len(set(flags) & set(_flags)) > 0
            if hasFlags:
                sql = "select * from mukhin_sylius_blogging_post_image where id = {0}".format(postImageId)
                res = self.conn.execute(sql)
                row = res.fetchone()
                if row:
                    cdnUrl = row["cdn_url"] or None
                    if cdnUrl and cdnUrl != "" and cdnUrl != "None":
                        item = {}
                        item["id"] = postId
                        item["image"] = cdnUrl
                        item["flags"] = _flags
                        items.append(item)

        return items

	
    def PostsTypeHaveNoRelations(self, flags):


        vintageStyleSql = """select id, post_image_id,flags, created_at from mukhin_sylius_blogging_post where (flags 
							like '%%vintage%%' or flags like '%%vintagestyle%%') and LOCATE("blocked-post",flags) = 0 
                            and enabled = 0 and id not in (select post_id from 
							mukhin_sylius_blogging_post_product_relation) and not (short_description like '%%LTK%%' 
							OR short_description like '%%LIKEtoKNOW%%' OR short_description like '%%liketk%%' OR short_description 
							like '%%liketoknow%%') order by created_at desc; """ 
        streetStyleSql = """select id, post_image_id,flags, created_at from mukhin_sylius_blogging_post where (flags 
                            like '%%streetstyle%%' or flags like '%%streetwear%%' or flags like '%%street-style%%') 
                            and LOCATE("blocked-post",flags) = 0 and enabled = 0 and 
                            id not in (select post_id from mukhin_sylius_blogging_post_product_relation) and not (short_description 
                            like '%%LTK%%' OR short_description like '%%LIKEtoKNOW%%' OR short_description like '%%liketk%%' 
                            OR short_description like '%%liketoknow%%') order by created_at desc;"""

        travelStyleSql = """select id, post_image_id,flags, created_at from mukhin_sylius_blogging_post where (flags 
							like '%%travel-style%%' or flags like '%%travelstyle%%' or flags like '%%travelfashion%%') 
                            and LOCATE("blocked-post",flags) = 0 and enabled = 0 
                            and id not in (select post_id from mukhin_sylius_blogging_post_product_relation) and not (short_description 
							like '%%LTK%%' OR short_description like '%%LIKEtoKNOW%%' OR short_description like '%%liketk%%' 
							OR short_description like '%%liketoknow%%') order by created_at desc;""" 

        res1 = self.conn.execute(vintageStyleSql)
        rows1 = res1.fetchall()
        vintageStyleArr = self.matchProductCode(rows1, flags)

        res2 = self.conn.execute(streetStyleSql)
        rows2 = res2.fetchall()
        streetStyleArr = self.matchProductCode(rows2, flags)

        res3 = self.conn.execute(travelStyleSql)
        rows3 = res3.fetchall()
        travelStyleArr = self.matchProductCode(rows3, flags)


        return vintageStyleArr, streetStyleArr, travelStyleArr


    def matchProductCode(self, rows, flags):
        items = []

        for row in rows:
            postId = row["id"]
            postImageId = row["post_image_id"]
            _flags = row["flags"]
            _flags = json.loads(_flags) or []
            hasFlags = True
            if len(flags) == 0:
                hasFlags = True
            else:
                hasFlags = len(set(flags) & set(_flags)) > 0
            if hasFlags:
                sql = "select * from mukhin_sylius_blogging_post_image where id = {0};".format(postImageId)
                res = self.conn.execute(sql)
                row = res.fetchone()
                if row:
                    cdnUrl = row["cdn_url"] or None
                    if cdnUrl and cdnUrl != "" and cdnUrl != "None":
                        item = {}
                        item["id"] = postId
                        item["image"] = cdnUrl
                        item["flags"] = _flags
                        items.append(item)
        return items
    
    
    def judgePostIsMatchProduct(self, postId):
        sql = "select post_id from mukhin_sylius_blogging_post_product_relation where post_id = {0};".format(postId)
        res = self.conn.execute(sql)
        
        result = res.fetchall()

        return result


    def queryEmailByPostId(self, postId):
        sql = "select email from sylius_customer where id in (select customer_id from mukhin_sylius_blogging_blog where id in (select blog_id from mukhin_sylius_blogging_post where id = {0}));".format(postId)
        
        res = self.conn.execute(sql)
        rows = res.fetchall()

        return rows[0]['email']


    def updateFlagsToPost(self, postId, oldTag, newTag):
        sql = "update mukhin_sylius_blogging_post set flags = replace(flags,'{0}','{1}') where id = {2};".format(oldTag, newTag, postId)
        self.conn.execute(sql)
    

    def getEmailOfPostId(self, postId):
        sql = "select email from sylius_customer where id in (select customer_id from mukhin_sylius_blogging_blog where id in (select blog_id from mukhin_sylius_blogging_post where id = {0}));".format(postId)
        res = self.conn.execute(sql)
        rows = res.fetchall()

        email = rows[0]['email']

        return email

    def getEnabledPost(self, email):
        items = []
        sql = "select id from mukhin_sylius_blogging_post where enabled = 1 and blog_id in (select id from mukhin_sylius_blogging_blog where customer_id in (select id from sylius_customer where email = '{0}'));".format(email)
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            postId = row["id"]
            item = {}
            item['postId'] = postId
            items.append(item)

        return items
    
    
    def getNoFlagProductId(self):
        items = []
        sql = """select id from sylius_product where flags like '%%""%%' and original_store = 'finish line';"""
        res = self.conn.execute(sql)
        rows = res.fetchall()
        print len(rows)
        for row in rows:
            productId = row["id"]
            item = {}
            item['productId'] = productId
            items.append(item)

        return items



    def getProductIdAndCode(self, flags):
        items = []

        if len(flags) != 0:
            for flag in flags:
                sql = "select product_id,code,last_imported_at from sylius_product_variant inner join (select id from sylius_product where flags like '%%{0}%%') a on sylius_product_variant.product_id = a.id;".format(flag)
                res = self.conn.execute(sql)
                rows = res.fetchall()

                for row in rows:
                    item = {}
                    item["productId"] = row["product_id"]
                    item["code"] = row["code"]
                    item["lastImportedTime"] = row["last_imported_at"]

                    items.append(item)

        return items


    def cleanPrice(self, productId, codePre):
        sql = "delete from sylius_product_variant where product_id = {0} and code like '%%{1}%%';".format(productId, codePre)
        self.conn.execute(sql)

    def cleanPriceAfterDelVariant(self, productId, importTime):
        sql = "delete from sylius_product_variant where product_id = {0} and last_imported_at = '{1}';".format(productId, importTime)
        self.conn.execute(sql)



    def PostVedio(self, email):
        items = []
        sql = "select id, post_image_id, flags from mukhin_sylius_blogging_post where enabled = 0 and LOCATE('blocked-post',flags) = 0 and blog_id in (select id from mukhin_sylius_blogging_blog where customer_id in (select id from sylius_customer where email = '{0}'));".format(email)
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            postId = row["id"]
            postVideoId = row["post_image_id"]
            flags = row["flags"]

            item = {}
            item['postId'] = postId
            item['videoId'] = postVideoId
            item['flags'] = flags

            items.append(item)

        return items

    def haveNotMatchProduct(self, flags):
        sql = "select id,post_image_id, flags from mukhin_sylius_blogging_post where id not in (select post_id from mukhin_sylius_blogging_post_product_relation) and not (short_description like '%%LTK%%' OR short_description like '%%LIKEtoKNOW%%' OR short_description like '%%liketk%%' OR short_description like '%%liketoknow%%') and updated_at > '2020-07-31 00:00:00' and enabled = 0;"
        res = self.conn.execute(sql)
        rows = res.fetchall()

        haveNotMatchProduct = self.matchProductCode(rows, flags)

        return haveNotMatchProduct

    
    def updateTime(self, postId):
        sql = "update mukhin_sylius_blogging_post set updated_at = CURRENT_TIME where id = {0};".format(postId)        
        self.conn.execute(sql)

    def videoPostUpdateTimeRandom(self):
        updateTime = []
        
        sql = """select updated_at from mukhin_sylius_blogging_post where flags like '%%popular-post%%' and enabled=1 
                and updated_at > '2020-07-31 00:00:00' 
                order by updated_at desc;"""
        res = self.conn.execute(sql)
        rows = res.fetchall()

        for row in rows:
            updateTime.append(row["updated_at"])

        return updateTime


    def randomVideoUpdateTime(self, videoPostId):
        randomPostUpdateTime = self.videoPostUpdateTimeRandom()

        randomNum = random.randint(0, len(randomPostUpdateTime) - 1)
        randomTime = randomPostUpdateTime[randomNum]

        sql = "update mukhin_sylius_blogging_post set  updated_at = '{0}' where id = {1}".format(randomTime, videoPostId)
        self.conn.execute(sql)



    def check_taxon_conflict(self,gender="women"):
        taxonList = {
            "women":[
                "category-women-clothing",
                "category-women-shoes",
                "category-women-bags"
            ],
            "men": [
                "category-men-clothing",
                "category-men-shoes",
                "category-men-bags"
            ]
        }
        taxons = taxonList[gender]

        cms = itertools.combinations(taxons,2)
        for cm in cms:
            codes = []
            for c in cm:
                taxonCode = self.GetTaxonId(c)
                codes.append(taxonCode)

            if len(codes) == 2:
                sql = "select product_id from sylius_product_taxon where taxon_id = {0} and product_id in (select product_id from sylius_product_taxon where taxon_id = {1})".format(codes[0], codes[1])
                res = self.conn.execute(sql)
                rows = res.fetchall()
                print len(rows), cms[0], cms[1]

    def blogs_updated_yestoday(self):
        # 2020-04-27 07:38:05
        today = datetime.datetime.now()
        yestoday = today + datetime.timedelta(days = -1)
        today = "{0}-{1:0>2}-{2:0>2} 00:00:00".format(today.year, today.month, today.day)
        yestoday = "{0}-{1:0>2}-{2:0>2} 00:00:00".format(yestoday.year, yestoday.month, yestoday.day)

        sql = "select blog_id, created_at, updated_at from mukhin_sylius_blogging_post where (updated_at >= '{0}' and updated_at <'{1}') or (created_at >= '{0}' and created_at <'{1}') and enabled=1".format(yestoday, today)

        items = []
        res = self.conn.execute(sql)
        rows = res.fetchall()
        blogMap = {}
        for row in rows:
            item = {}
            blogId = row["blog_id"]
            if not blogMap.get("{0}".format(blogId)):
                item["blog_id"] = row["blog_id"]
                items.append(item)
                blogMap["{0}".format(blogId)]= True

        return items

    def dedup_post(self):
        idmaps = [
            [77, 135],
            [8, 138],
            [81, 163],
            [84, 160],
            [86, 167]
        ]

        for idmap in idmaps:
            keep_id = idmap[0]
            keep_email = "{0}@a.com".format(keep_id)
            keep_customer_id = self.customer_id_of_user(keep_id)
            keep_blog_id = self.blog_id_of_customer(keep_customer_id)

            dup_id = idmap[1]
            dup_email = "{0}@a.com".format(dup_id)

            keep_images = []

            sql = "select cdn_url from mukhin_sylius_blogging_post_image where id in (select post_image_id from mukhin_sylius_blogging_post where blog_id in (select id from mukhin_sylius_blogging_blog where customer_id in (select customer_id from sylius_shop_user where username = '{0}')))".format(keep_email)
            res = self.conn.execute(sql)
            rows = res.fetchall()

            existed_images = []

            for row in rows:
                existed_images.append(row["cdn_url"])

            sql = "select * from mukhin_sylius_blogging_post where blog_id in (select id from mukhin_sylius_blogging_blog where customer_id in (select customer_id from sylius_shop_user where username = '{0}'))".format(dup_email)
            print sql
            res = self.conn.execute(sql)
            rows = res.fetchall()
            print len(rows)
            for row in rows:
                postId = row["id"]
                postImageId = row["post_image_id"]
                _sql = "select * from mukhin_sylius_blogging_post_image where id = {0}".format(postImageId)
                res = self.conn.execute(_sql)
                _row = res.fetchone()
                cdnUrl = _row["cdn_url"]
                if cdnUrl in existed_images:

                    sql = "delete from mukhin_sylius_blogging_post where id = {0}".format(postId)
                    self.conn.execute(sql)
                    sql = "delete from mukhin_sylius_blogging_post_image where id = {0}".format(postImageId)
                    self.conn.execute(sql)
                else:
                    sql = "update mukhin_sylius_blogging_post set blog_id={0} where id = {1}".format(keep_blog_id, postId)
                    print sql
                    self.conn.execute(sql)
                    sql = "update mukhin_sylius_blogging_post_image set customer_id={0} where id = {1}".format(keep_customer_id, postImageId)
                    print sql
                    self.conn.execute(sql)

            #print keep_id, dup_id

    def stats_blogger_post(self):
        for user in users:
            index = userMapOld.get(user) or None
            if not index:
                index = userMap.get(user) or None
            if not index:
                print "no", user
                continue
            email = "{0}@a.com".format(index)

            sql = "select count(*) as total from mukhin_sylius_blogging_post where blog_id in (select id from mukhin_sylius_blogging_blog where customer_id in (select customer_id from sylius_shop_user where username = '{0}'))".format(email)
            res = self.conn.execute(sql)
            total = 0
            row = res.fetchone()
            if row:
                total = row["total"]

            print  "{0},{1},{2}".format(user, email, total)

    def fix_jcrew_data(self):
        sql = "select * from sylius_product where original_store = 'J.Crew' order by id desc"
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            original_url = row["original_url"]
            product_id = row["id"]
            original_url = original_url.replace("//at", "")
            print product_id, original_url

            sql = "update sylius_product set original_url='{0}' where id = {1}".format(original_url, product_id)
            self.conn.execute(sql)

    def productsNewArrival(self):
        sql = "select product_id, gender, newest, newest_order from productdata where newest is not null and newest_order is not null"
        items = []

        utc = int(time.time())
        try:
            res = self.conn_import.execute(sql)
            rows = res.fetchall()

            for row in rows:
                productId = row["product_id"]
                gender = row["gender"]
                newest = row["newest"]
                newest = newest.strip("|")
                newestOrder = row["newest_order"]
                newestOrder = newestOrder.strip("|")

                newestArray = newest.split("|")
                newestOrderArray = newestOrder.split("|")

                index = 0
                for tag in newestArray:

                    try:
                        cats = tag.split("/")
                        taxonName = buildTaxonName(gender, cats)

                        item = {}
                        item["product_id"] = productId
                        item["taxon_code"] = taxonName
                        item["new_position"] = int(newest) - utc
                        items.append(item)
                    except Exception, ex:
                        continue
        except Exception, ex:
            print ex

        return items

    def allStores(self):
        sql = "select distinct(store) as store from productdata"
        res = self.conn_import.execute(sql)
        rows = res.fetchall()
        stores = []
        for row in rows:
            store = row["store"]
            store = store.replace("'", "\\'")
            stores.append(store)

        return stores

    def products_need_disable(self):
        sql = "select distinct(store) as store from productdata"
        res = self.conn_import.execute(sql)
        rows = res.fetchall()
        stores = []
        for row in rows:
            store = row["store"]
            #store = store.replace("'", "\\\'")
            if store == "Macy's":
                store = "Macy\\'s"
            stores.append("'{0}'".format(store))


        clause = "original_store in ({0})".format(",".join(stores))

        sql = "select original_id from sylius_product where {0} and enabled=1".format(clause)
        print sql
        res = self.conn.execute(sql)
        rows = res.fetchall()
        ids = []
        for row in rows:
            _id = row["original_id"]
            _id = _id.decode("utf-8")
            ids.append(slugify(_id))



        idsn = []
        sql = "select product_id from productdata"
        res = self.conn_import.execute(sql)
        rows = res.fetchall()
        for row in rows:
            _id = row["product_id"]
            try:
                _id = _id.replace("J.Crew", "J-Crew")
                _id = _id.replace("_", "-")
                _id = _id.decode("utf-8")
                idsn.append(slugify(_id))
            except:
                pass

        # ids = ids[0:10]
        # idsn = idsn[0:10]
        # print ids, idsn


        ids = set(ids)
        idsn = set(idsn)

        diff = ids - idsn
        diff = list(diff)

        if len(diff) == len(ids):
            return []

        return diff

    def ShuffleProductByFlag(self, flags=[]):
        for flag in flags:
            ids = []
            ranks = []
            sql = "select id, pretty_rank from sylius_product where flags like '%%{0}%%' order by pretty_rank asc".format(flag)
            res = self.conn.execute(sql)
            rows = res.fetchall()
            for row in rows:
                productId = row["id"]
                prettyRank = row["pretty_rank"]
                ids.append(productId)
                ranks.append(prettyRank)

            if len(ids) > 10:
                ids = ids[10:]
                random.shuffle(ids)
                minRank = ranks[9]
                for productId in ids:
                    minRank += 1
                    sql = "update sylius_product set pretty_rank = {0} where id = {1}".format(minRank, productId)
                    self.conn.execute(sql)
                    VoilaGo.IndexEs(productId)

    def ClearPomotionFlag(self):
        flags = []
        stores = []
        sql = "select distinct(flag) as flag from productdata"
        res = self.conn_import.execute(sql)
        rows = res.fetchall()
        for row in rows:
            flag = row["flag"]
            flags.append(flag)

        sql = "select distinct(store) as store from productdata"
        res = self.conn_import.execute(sql)
        rows = res.fetchall()
        for row in rows:
            store = row["store"]
            stores.append(store)

        for flag in flags:
            for store in stores:
                self.ClearProductsWithFlag(flag, store)


    def products_need_update(self):
        products = []
        sql = "select product_id, current_price, msrp from productdata order by id asc"
        res = self.conn_import.execute(sql)
        rows = res.fetchall()
        for row in rows:
            try:
                pid = row["product_id"]
                price = row["current_price"]
                msrp = row["msrp"]
                if not( price and msrp):
                    continue
                price = price.encode("utf-8")
                msrp = msrp.encode("utf-8")

                price = price.replace(",", "")
                prices = price.split(" ")
                price = prices[0]

                msrp = msrp.replace(",", "")
                msrps = msrp.split(" ")
                msrp = msrps[0]

                if not( price and msrp):
                    continue
                price = int(float(price) * 100.0)
                msrp = int(float(msrp) * 100.0)

                if price > msrp:
                    tmp = msrp
                    msrp = price
                    price = tmp

                if price and msrp :
                    try:
                        product = {}
                        pid = pid.replace("URBAN_OUTFITTERS", "urban-outfitters")
                        pid = pid.replace("J.Crew", "j-crew")
                        pid = pid.decode("utf-8")
                        pid = slugify(pid)
                        product["product_id"] = pid
                        product["price"] = price
                        product["msrp"] = msrp
                        products.append(product)
                    except:
                        pass

            except Exception, ex:
                print ex

        return products

    def rename_voila_in_post(self):
        sql = "select * from mukhin_sylius_blogging_post where enabled = 1 order by id desc"
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            pid = row["id"]
            desc = row["short_description"]
            desc = desc.replace("@voila.love", "@voila")
            desc = desc.replace("@voilasummer", "#voilasummer")
            desc = desc.replace("@voila", "@voila.love")
            desc = desc.replace("'", "\\'")
            desc = desc.replace("%", "%%")
            print pid, desc
            sql = "update mukhin_sylius_blogging_post set short_description='{0}' where id = {1}".format(desc, pid)
            print sql
            self.conn.execute(sql)

    def clear_images(self, store):
        sql = "select im_name from img_data order by id desc"
        res = self.conn_import.execute(sql)
        rows = res.fetchall()

        imgDict = {}
        for row in rows:
            code = row["im_name"]
            code = code.lower()
            imgDict[code] = True

        sql = "select id, code, original_url from sylius_product_image where owner_id in (select id from sylius_product where enabled=1 and original_store = '{0}')".format(store)
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            code = row["code"]
            imgUrl = row["original_url"]
            imgId = row["id"]
            if not imgDict.has_key(code):
                self.visense_api.remove([code])
                sql = "delete from sylius_product_image where id = {0}".format(imgId)
                print sql, code, imgUrl
                self.conn.execute(sql)


    def addBlock(self):
        sql = "insert into mukhin_sylius_cms_blocks_block(code, name, type, header, subheader, request, created_at, position, enabled,updated_at,list_type, style) values('under-20-dollar', 'under $20', 'product', 'Under $20', '', '/shop-api/product?flags[under-20]=1&channel=US_WEB&locale=en_US&sort[prettyRank]=asc', '2019-03-01 12:25:14', 9, 0, '2019-06-13 06:26:18', 0, '0101001')"
        self.conn.execute(sql)

        sql = "insert into mukhin_sylius_cms_blocks_block(code, name, type, header, subheader, request, created_at, position, enabled,updated_at,list_type, style) values('under-50-dollar', 'under $50', 'product', 'Under $50', '', '/shop-api/product?flags[under-50]=1&channel=US_WEB&locale=en_US&sort[prettyRank]=asc', '2019-03-01 12:25:14', 10, 0, '2019-06-13 06:26:18', 0, '0101001')"
        self.conn.execute(sql)

    def GetTaxonId(self, code):
        sql = "select id from sylius_taxon where code = '{0}'".format(code)
        res = self.conn.execute(sql)
        row = res.fetchone()
        if row:
            return row["id"]

        return None

    def merge_taxon(self):
        taxons = [
            "category-men-cologne-grooming",
            "category-men-cologne-grooming-cologne-perfume",
            "category-men-cologne-grooming-hair-care",
            "category-men-cologne-grooming-skin-care",
            "category-men-cologne-grooming-shaving-beard-care",
            "category-men-cologne-grooming-gifts-sets"
        ]
        for taxon in taxons:
            fakeTaxon = taxon.replace("category-men", "category-men-s")
            print taxon, fakeTaxon
            taxonId = self.GetTaxonId(taxon)
            fakeTaxonId = self.GetTaxonId(fakeTaxon)

            sql = "update sylius_product_taxon set taxon_id = {0} where taxon_id={1}".format(taxonId, fakeTaxonId)
            print sql
            self.conn.execute(sql)

            sql = "update sylius_product set main_taxon_id = {0} where main_taxon_id={1}".format(taxonId, fakeTaxonId)
            print sql
            self.conn.execute(sql)

            sql = "delete from sylius_taxon where id = {0}".format(fakeTaxonId)
            sql = "update sylius_taxon set parent_id=3082 where id = 226;"
            print sql
            self.conn.execute(sql)

    def export_size(self, taxon):
        sizes = {}

        taxonId = self.GetTaxonId(taxon)
        sql = "select * from sylius_product_taxon where taxon_id = {0}".format(taxonId)
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            productId = row["id"]
            sql = "select * from sylius_product_variant where product_id = {0}".format(productId)
            _res = self.conn.execute(sql)
            _rows = _res.fetchall()
            for _row in _rows:
                variantId = _row["id"]
                sql = "select * from sylius_product_variant_option_value where variant_id={0}".format(variantId)
                __res = self.conn.execute(sql)
                __rows = __res.fetchall()
                for __row in __rows:
                    optionValueId = __row["option_value_id"]
                    sql = "select * from sylius_product_option_value_translation where translatable_id = {0} and locale='en_US'".format(optionValueId)
                    ___res = self.conn.execute(sql)
                    ___rows = ___res.fetchall()
                    for ___row in ___rows:
                        value = ___row["value"]
                        if not sizes.has_key(value):
                            print value
                            sizes[value] = 1

    def replace_flag(self):
        sql = "select * from sylius_product where flags like '%%f_20200810_s5osneakers%%' or flags like '%%f_20200810_ncsneakers%%'"
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            productId = row["id"]
            flags = row["flags"]
            oldFlags = flags
            flags = flags.replace("f_20200810_s5osneakers", "f_20200810_topsneakers")
            flags = flags.replace("f_20200810_ncsneakers", "f_20200810_topsneakers")
            flags = json.loads(flags)
            flags = list(set(flags))
            flags = json.dumps(flags)
            print productId, flags, oldFlags
            sql = "update sylius_product set flags = '{0}' where id = {1}".format(flags, productId)
            print sql
            self.conn.execute(sql)
            VoilaGo.IndexEs(productId)


    def clear_flags(self):
        sql = "select * from sylius_product where flags != '[]'"
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            productId = row["id"]
            sql = "update sylius_product set flags='[]' where id = {0}".format(productId)
            self.conn.execute(sql)
            VoilaGo.IndexEs(productId)

    def import_flagged_products(self):
        #self.clear_flags()
        _file = "flags.out"
        with open(_file) as f:
            line = f.readline()
            while line:
                line = line.strip()

                lines = line.split("###")
                productId, flags, prettyRank = lines[0], lines[1], lines[2]
                flags = flags.replace("%", "%%")

                flags = json.loads(flags)

                sql = "select flags from sylius_product where id = {0}".format(productId)
                res = self.conn.execute(sql)
                if res:
                    row = res.fetchone()
                    if row:
                        _flags = row["flags"] or '[]'
                        _flags = json.loads(_flags)
                        flags.extend(_flags)
                        flags = list(set(flags))

                flags = json.dumps(flags)

                sql = "update sylius_product set flags='{0}', pretty_rank={1} where id = {2}".format(flags, prettyRank, productId)
                print sql
                self.conn.execute(sql)
                oldData = Elastic.getProduct(productId)
                if oldData:
                    oldData["prettyRank"] = int(prettyRank)
                    oldData["raw_prettyRank"] = int(prettyRank)
                    oldData["flags"] = json.loads(flags)
                    print oldData["prettyRank"], oldData["raw_prettyRank"]
                    #Elastic.putProduct(productId, oldData)

                VoilaGo.IndexEs(productId)

                line = f.readline()

    def export_some_flagged_products(self):
        sql = "select id, flags, pretty_rank from sylius_product where flags like '%%50%%off-bag%%' order by id desc"
        res = self.conn.execute(sql)
        rows = res.fetchall()
        with open("f.out", "w") as f:
            for row in rows:
                id = row["id"]
                flags = row["flags"]
                prettyRank = row["pretty_rank"]
                f.write("{0}###{1}###{2}\n".format(id, flags, prettyRank))

    def export_flagged_products(self):
        sql = "select id, flags, pretty_rank from sylius_product where flags != '[]' order by id desc"
        res = self.conn.execute(sql)
        rows = res.fetchall()
        with open("flags.out", "w") as f:
            for row in rows:
                id = row["id"]
                flags = row["flags"] or "[]"
                flags = json.loads(flags) or []
                for flag in flags:
                    if flag.find("f_2020") == 0 :
                        flags.remove(flag)
                flags = json.dumps(flags)
                prettyRank = row["pretty_rank"]
                f.write("{0}###{1}###{2}\n".format(id, flags, prettyRank))

            # esInfo = Elastic.getProduct(id)
            # print esInfo.get("prettyRank")
            # if esInfo.get("prettyRank") != prettyRank:
            #     sql = "update sylius_product set pretty_rank={0} where id = {1}".format(esInfo.get("prettyRank"), id)
            #     self.conn.execute(sql)
            #     print sql

    def new_flaged_products(self):
        products = []
        sql = "select id from sylius_product where pretty_rank < -1000 order by id desc"
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            products.append(row["id"])

        return products

    def posted_products(self):
        products = []
        conn = get_pg_conn(source)
        sql = "select original_product_id from mukhin_sylius_blogging_post_product_relation order by id desc"
        res = conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            pid = row["original_product_id"]
            products.append(pid)

        sql = "select product_id from mukhin_sylius_blogging_post_product_relation_alternative"
        res = conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            pid = row["product_id"]
            products.append(pid)

	    return products

    def get_taxon_by_name(self, taxonName):
        taxonName  = slugify(taxonName)
        sql = "select * from sylius_taxon where code = '{0}'".format(taxonName)
        res = self.conn.execute(sql)
        row = res.fetchone()
        if row:
            result = {}
            result["id"] = row["id"]
            result["code"] = row["code"]

            return result

        return None

    def all_enabled_products_by_rank(self, storeName):
        storeName = storeName.replace("'", "\\'")
        print storeName
        sql = "select id, code, base_rating, base_favorite, base_review from sylius_product where enabled=1 and original_store = '{0}' order by base_rating desc, base_favorite desc, base_review desc".format(storeName)
        res = self.conn.execute(sql)
        rows = res.fetchall()
        index = 0
        for row in rows:
            code = row["code"]
            productId = row["id"]
            baseRating = row["base_rating"]
            baseFavorite = row["base_favorite"]
            baseReview = row["base_review"]
            print productId, baseRating, baseFavorite, baseReview
            index += 1
            data = {}
            data["rank"] = index
            VoilaGo.UpdateProduct(code, data)

    def all_enabled_products_in_taxon(self, taxon=None):
        ps = []
        sql = "select product_id from sylius_product_taxon where taxon_id = {0}".format(taxon)
        sql = "select id from sylius_product where flags != '[]' and flags is not null"
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            item = {}
            #item["id"] = row["product_id"]
            item["id"] = row["id"]
            ps.append(item)

        return ps

    def clear_newest_rank(self, productId):
        sql = "select id, new_position from sylius_product_taxon where product_id = {0}".format(productId)
        res = self.conn.execute(sql)
        rows =  res.fetchall()
        needClear = False
        for row in rows:
            ptId = row["id"]
            newPosition = row["new_position"] or 1000
            if newPosition < 1000:
                needClear = True

        if needClear:
            sql = "update sylius_product_taxon set new_position = 1000 where product_id = {0}".format(productId)
            self.conn.execute(sql)
            VoilaGo.IndexEs(productId)

    def all_products(self, stores=None):
        ps = []
        sql = "select * from sylius_product where enabled=1 order by id asc"
        if stores:
            stores = "','".join(stores)
            stores = "'{0}'".format(stores)
            sql = "select * from sylius_product where original_store in ({0}) order by id desc".format(stores)
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            item = {}
            item["id"] = row["id"]
            ps.append(item)

        return ps

    def all_enabled_products(self, stores=None):
        ps = []
        sql = "select * from sylius_product where enabled=1 order by id asc"
        if stores:
            stores = "','".join(stores)
            stores = "'{0}'".format(stores)
            sql = "select * from sylius_product where DATE_FORMAT(last_imported_at,'%%Y-%%m-%%d') >= DATE_FORMAT(date_sub(curdate(),interval 3 day),'%%Y-%%m-%%d') and DATE_FORMAT(updated_at,'%%Y-%%m-%%d') >= DATE_FORMAT(date_sub(curdate(),interval 3 day),'%%Y-%%m-%%d') and original_store in ({0}) order by id asc".format(stores)
            # sql = "select * from sylius_product where original_store in ({0}) order by id desc".format(stores)
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            item = {}
            item["id"] = row["id"]
            ps.append(item)

        return ps

    def all_enabled_posts(self):
        ps = []
        sql = "select * from mukhin_sylius_blogging_post order by updated_at desc limit 1000"
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            item = {}
            item["id"] = row["id"]
            ps.append(item)

        return ps

    def all_updated_posts(self):
        ps = []
        sql = "select * from mukhin_sylius_blogging_post order by updated_at desc limit 200"
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            item = {}
            item["id"] = row["id"]
            ps.append(item)

        return ps


    def fix_price(self):
        offset = 0
        while True:
            sql = "select * from sylius_channel_pricing where id <=12713943 order by id desc limit 50000 offset {0}".format(offset)
            res = self.conn.execute(sql)
            rows = res.fetchall()
            for row in rows:
                id = row["id"]
                original_price = row["original_price"]
                sql = "update sylius_channel_pricing set price={0} where id = {1}".format(original_price, id)
                self.conn.execute(sql)
            if len(rows) <= 0:
                break
            offset += 50000
            print offset

            time.sleep(0.5)

    def clean(self):
        sql = "select * from sylius_product where enabled=0 order by id asc"
        res = self.conn.execute(sql)
        rows = res.fetchall()
        postedProducts = self.posted_products()
        count = 0
        for row in rows:
            pid = row["id"]
            print pid
            if pid in postedProducts:
                continue

            sql = "select * from sylius_product_image where owner_id = {0}".format(pid)
            _res = self.conn.execute(sql)
            _rows = _res.fetchall()
            im_ids = []
            for _row in _rows:
                code = _row["code"]
                im_ids.append(code)

            self.visense_api.remove(im_ids)

            sql = "delete from sylius_product where id = {0}".format(pid)
            self.conn.execute(sql)
            count += 1
            if count >=10000:
                time.sleep(0.5)
                count = 0

    def all_orders(self):
        result = []
        sql = "select * from sylius_affiliate_orders order by id asc"
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            item = {}
            item["post_id"] = row["post_id"]
            item["customer_id"] = row["customer_id"]
            item["product_id"] = row["product_id"]
            createdAt = row["created_at"]
            item["created_at"] = "{0:0>4}-{1:0>2}-{2:0>2} {3:0>2}:{4:0>2}:{5:0>2}".format(createdAt.year, createdAt.month, createdAt.day, createdAt.hour, createdAt.minute, createdAt.second)
            item["id"] = row["id"]
            result.append(item)

        return result

    def getOriginalId(self, productId):
        if not productId:
            return None
        sql = "select * from sylius_product where id = {0}".format(productId)
        _res = self.conn.execute(sql)
        _row = _res.fetchone()
        if _row:
            originalId =  _row["original_id"]
            originalId = originalId.replace("neimanmarcus", "neiman-marcus")
            originalId = originalId.replace("theoutnet", "the-outnets")
            return originalId
        return None

    def all_alternatives(self, relationId):
        result = []
        sql = "select * from mukhin_sylius_blogging_post_product_relation_alternative where post_product_relation_id = {0}".format(relationId)
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            productId = row["product_id"]
            position = row["position"]
            if productId:
                originalId = self.getOriginalId(productId)
                result.append("{0}@{1}".format(originalId, position))

        return result

    def all_post_product(self):
        sql = "select * from mukhin_sylius_blogging_post_product_relation order by id asc"
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            relationId = row["id"]
            postId = row["post_id"]
            productId = row["original_product_id"]
            position = row["position"]
            if productId:
                sql = "select * from sylius_product where id = {0}".format(productId)
                _res = self.conn.execute(sql)
                _row = _res.fetchone()
                if _row:
                    originalId =  _row["original_id"]
                    originalId = originalId.replace("neimanmarcus", "neiman-marcus")
                    originalId = originalId.replace("theoutnet", "the-outnets")
                    alternatives = self.all_alternatives(relationId)
                    print "{0},{1},{2},{3},{4}".format(postId, productId, position, originalId, "|".join(alternatives))

    def getProductIdByOriginalId(self, originalId):
        sql = "select * from sylius_product where original_id = '{0}'".format(originalId)
        res = self.conn.execute(sql)
        row = res.fetchone()
        if row:
            return row["id"]

        return None

    def getProductByCode(self, code):
        data = {}
        sql = "select * from sylius_product where code = '{0}'".format(code)
        res = self.conn.execute(sql)
        row = res.fetchone()
        if row:
            data["pretty_rank"] = row["pretty_rank"]
            data["id"] = row["id"]

        return data


    def import_csv(self, csv):
        with open(csv) as f:
            line = f.readline()
            while line:
                line = line.strip()
                lines = line.split(",")
                print len(lines)
                if len(lines) < 5:
                    continue
                postId, productId, position, originalId, alters = lines[0], lines[1], lines[2], lines[3], lines[4]

                productId = self.getProductIdByOriginalId(originalId)

                if productId:
                    sql = "insert into mukhin_sylius_blogging_post_product_relation(post_id, original_product_id, position) values({0}, {1}, 0)".format(postId, productId)
                    self.conn.execute(sql)

                    sql = "select id from mukhin_sylius_blogging_post_product_relation where post_id = {0} and original_product_id = {1}".format(postId, productId)
                    res = self.conn.execute(sql)
                    row = res.fetchone()

                    if row:
                        reid = row["id"]
                        alternatives = alters.split("|")
                        for alternative in alternatives:
                            alternative = alternative.split("@")
                            print alternative
                            if len(alternative) <2:
                                continue
                            _original_product_id, _position = alternative[0], alternative[1]
                            _productId = self.getProductIdByOriginalId(_original_product_id)
                            if _position == "None":
                                _position = 0
                            if not _position:
                                _position = 0

                            if _productId:
                                sql = "insert into mukhin_sylius_blogging_post_product_relation_alternative(post_product_relation_id, product_id, position) values({0}, {1}, {2})".format(reid, _productId, _position)
                                self.conn.execute(sql)

                line = f.readline()

    def products_with_flag(self, flag):
        products = []
        sql = "select code from sylius_product where flags like '%%{0}%%'".format(flag)
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            product_code = row["code"]
            products.append(product_code)

        return products

    def wishlist_products(self, listName):
        products = []
        pscore = {}
        sql = "select * from webburza_wishlist_item where wishlist_id in (select id from webburza_wishlist where slug = '{0}' and user_id != 281) order by id asc".format(listName)
        res = self.conn.execute(sql)
        rows = res.fetchall()
        index = 0
        for row in rows:
            index += 1
            product_variant_id = row["product_variant_id"]
            wid = row["id"]
            sql = "select * from sylius_product where id in (select product_id from sylius_product_variant where id = {0})".format(product_variant_id)
            _res = self.conn.execute(sql)
            _rows = _res.fetchall()
            for _row in _rows:
                product_id = _row["id"]
                product_code = _row["code"]
                products.append(product_code)
                pscore[product_code] = 0 - index

        return (products, pscore)


    def like_post_number(self):
        result = []
        sql = "select * from mukhin_sylius_blogging_post where base_like > 0 and enabled=0"
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            postId = row["id"]
            title = row["title"]
            baseLike = row["base_like"]
            title = "Like:{0} {1}".format(baseLike, title)
            sql = "update mukhin_sylius_blogging_post set title = '{0}' where id = {1}".format(title, postId)
            #print sql
            self.conn.execute(sql)

    def add_flag2post(self):
        result = []
        sql = "select * from mukhin_sylius_blogging_post where enabled=1 order by id desc"
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            postId = row["id"]
            flags = row["flags"] or "[]"
            flags = json.loads(flags) or []
            if "popular-post" in flags or "blocked-post" in flags:
                print "continue"
                continue
            flags.append("popular-post")
            flags = json.dumps(flags)
            sql = "update mukhin_sylius_blogging_post set flags = '{0}' where id = {1}".format(flags, postId)
            print sql
            self.conn.execute(sql)
            VoilaGo.IndexPost(postId)

    def first_page_blocks(self):
        sqls = []
        sql = "update mukhin_sylius_cms_blocks_block set code = 'featured-designer', header='Featured Designer', request='/shop-api/product?flags[featured-designer]=1&channel=US_WEB&locale=en_US', style ='0101001' where id = 5"
        sqls.append(sql)
        sql = "update mukhin_sylius_cms_blocks_block set code = 'fashionable-steals', header='Fashionalble Steals', request='/shop-api/product?flags[fashionable-steals]=1&channel=US_WEB&locale=en_US', style ='0101001' where id = 6"
        sqls.append(sql)
        sql = "update mukhin_sylius_cms_blocks_block set code = 'fashion-must-haves', header='Fashion Must Haves', request='/shop-api/product?flags[fashion-must-haves]=1&channel=US_WEB&locale=en_US', style ='0101001' where id = 9"
        sqls.append(sql)
        for sql in sqls:
            self.conn.execute(sql)

    def customer_id_of_user(self, userId):
        sql = "select customer_id from sylius_shop_user where id = {0}".format(userId)
        res = self.conn.execute(sql)
        row = res.fetchone()
        if row:
            return row["customer_id"]

        return None


    def blog_id_of_customer(self, customerId):
        sql = "select id from mukhin_sylius_blogging_blog where customer_id={0}".format(customerId)
        res = self.conn.execute(sql)
        row = res.fetchone()
        if row:
            return row["id"]

        return None

    def self_customer_ids(self):
        ids = self.robot_customer_ids()
        ids.append(404)

        return ids

    def robot_customer_ids(self):
        ids = []
        sql = "select customer_id from sylius_shop_user where username like '%%@a.com%%'"
        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            ids.append(row["customer_id"])

        return ids

    def post_count_of_customer(self, customerId):
        sql = "select count(*) as total from mukhin_sylius_blogging_post where enabled=1 and blog_id in (select id from mukhin_sylius_blogging_blog where customer_id={0})".format(customerId)
        res = self.conn.execute(sql)
        row = res.fetchone()
        if row:
            return row["total"]

        return 0

    def customer_followers(self, customerId):
        sql = "select customer_id from sylius_customer_following_blogs where blog_id in (select id from mukhin_sylius_blogging_blog where customer_id = {0})".format(customerId)
        ids = []

        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            ids.append(row["customer_id"])

        return ids

    def blog_followers(self, blogId):
        #sql = "select customer_id from sylius_customer_following_blogs where blog_id in (select id from mukhin_sylius_blogging_blog where customer_id = {0})".format(customerId)
        ids = []
        sql = "select customer_id from sylius_customer_following_blogs where blog_id = {0}".format(blogId)

        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            ids.append(row["customer_id"])

        return ids

    def followed_by_customer(self, customerId):
        ids = []
        sql = "select blog_id from sylius_customer_following_blogs where customer_id = {0}".format(customerId)

        res = self.conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            ids.append(row["blog_id"])

        return ids

    def follow_blog(self, customer_id, blog_id):
        sql = "insert into sylius_customer_following_blogs(customer_id, blog_id) values({0}, {1})".format(customer_id, blog_id)
        #print sql
        self.conn.execute(sql)

    def unfollow_blog(self, customer_id, blog_id):
        sql = "delete from sylius_customer_following_blogs where customer_id={0} and blog_id={1}".format(customer_id, blog_id)
        #print sql
        self.conn.execute(sql)

def random_rm_follower():
    bk = Backend()
    conn = get_pg_conn(source)
    robots = bk.robot_customer_ids()
    for robot in robots:
        sql = "select id from mukhin_sylius_blogging_blog where customer_id = {0}".format(robot)
        res = conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            blogId = row["id"]
            followers = bk.blog_followers(blogId)
            print blogId, len(followers)

            if len(followers) > 90:
                lim = random.randint(5,20)

                sql = "delete from sylius_customer_following_blogs where blog_id ={0} order by customer_id desc limit {1}".format(blogId, lim)
                print sql
                #conn.execute(sql)

def rotot_follow():
    bk = Backend()
    conn = get_pg_conn(source)
    robots = bk.robot_customer_ids()
    for robot in robots:
        sql = "select id from mukhin_sylius_blogging_blog where customer_id = {0}".format(robot)
        res = conn.execute(sql)
        rows = res.fetchall()
        for row in rows:
            blogId = row["id"]
            followers = bk.blog_followers(blogId)
            followed = bk.followed_by_customer(robot)
            numFollowed = len(followed)
            num = numFollowed * 5
            rbs = bk.robot_customer_ids()
            random.shuffle(rbs)
            while num > 0:
                for _robot in rbs:
                    if _robot not in followers and _robot != robot:
                        print _robot, robot
                        try:
                            bk.follow_blog(_robot, blogId)
                            num -= 1
                        except Exception, ex:
                            num -= 1
                            print ex

if __name__ == "__main__":
    #bk.all_post_product()
    #bk.import_csv("out.csv")
    #bk.like_post_number()
    #bk.add_flag2post()
    #bk.first_page_blocks()

    #random_rm_follower()
    bk = Backend()
    #bk.export_brand()
    bk.ShuffleProductByFlag([])
    #bk.replace_flag()
    #print bk.post_updated_recently_time()
    #bk.ClearProductsWithFlag("test", "Macy's")
    #bk.blogs_updated_yestoday()
    #bk.clear_images('URBAN OUTFITTERS')
    #bk.merge_taxon()
    #bk.clear_flags()
    #bk.fix_price()
    #bk.clean()
    #bk.export_flagged_products()
    #items = bk.PostsHaveNoRelations("1@a.com", ["month-apr", "month-may", "month-jun"])
    #print len(items)
    #bk.export_flagged_products()
    #bk.import_flagged_products()
    #bk.export_some_flagged_products()
    #stores =  bk.allStores()
    #print stores
    #items = bk.productsNewArrival()
    #print len(items)
    #bk.merge_taxon()
    #bk.export_flagged_products()
    #bk.import_flagged_products()
    #bk.export_flagged_products()
    #bk.import_flagged_products()
    #bk.export_size("category-men-clothing")
    #bk.rename_voila_in_post()
    #bk.stats_blogger_post()
    #bk.dedup_post()
    #bk.check_taxon_conflict()
    #bk.fix_jcrew_data()
    #a = bk.PostsHaveNoRelationsHot(["month-apr", "month-may", "month-jun"])
    #print len(a)
    #bk.FixJsonTaxon()
