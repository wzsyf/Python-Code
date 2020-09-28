# -*- coding: utf-8 -*-

import os
import csv
import pymysql
from datetime import datetime, date, timedelta


class AnalysisNewPostAndNewUser:

    # 持久化
    def write2File(self, downpath, contents, rowDataArr, type):

        if type:
            with open(downpath, 'w', newline='') as csvFile:
                data = []
                writer = csv.writer(csvFile, lineterminator='\n')

                writer.writerow(rowDataArr)

                contentsLen = len(contents)

                if contentsLen == 1:
                    for content in contents:
                        arr = []

                        for num in range(0, len(content)):
                            arr.append(content[num])
                        data.append(arr)
                else:
                    for index in range(0, contentsLen):
                        if index == contentsLen - 2:
                            arr = []
                            content = contents[index]
                            contentLen = len(content)

                            for num in range(0, contentLen):
                                arr.append(content[num])
                            data.append(arr)

                            arrNull = ["", "", "", ""]
                            data.append(arrNull)
                        else:
                            arr = []
                            content = contents[index]
                            contentLen = len(content)

                            for num in range(0, contentLen):
                                arr.append(content[num])
                            data.append(arr)


                writer.writerows(data)

        else:
            with open(downpath, 'w', newline='') as csvFile:
                # data = []
                writer = csv.writer(csvFile, lineterminator='\n')

                writer.writerow(rowDataArr)

                arr = []
                arr.append(contents)
                # data.append(arr)

                writer.writerow(arr)


    def analysisNewPost(self):

        # 获取数据库连接池
        conn = pymysql.connect(host='localhost', user='mysqldev', password='mysqlpwd', database='odesk_visual_chameleon_sylius', charset='utf8')

        newPostNumSQL = """
                        select
                        newpost.userId,newpost.userName,newpost.newPostNum,total.totalPostNum
                        from
                        (select 
                        b.customer_id userId,min(b.first_name) userName,count(mukhin_sylius_blogging_post.id) newPostNum
                        from 
                        mukhin_sylius_blogging_post
                        inner join 
                        (select mukhin_sylius_blogging_blog.id,mukhin_sylius_blogging_blog.customer_id,a.first_name from mukhin_sylius_blogging_blog 
                        inner join 
                        (select 
                        sylius_customer.id,concat(first_name,'-',last_name) first_name 
                        from 
                        sylius_customer 
                        where 
                        LOCATE('@a.com',email)=0) a 
                        on 
                        mukhin_sylius_blogging_blog.customer_id = a.id) b
                        on
                        mukhin_sylius_blogging_post.blog_id = b.id
                        where
                        DATE_FORMAT(created_at,'%Y-%m-%d') >= DATE_FORMAT(date_sub(curdate(),interval 7 day),'%Y-%m-%d')
                        and
                        DATE_FORMAT(created_at,'%Y-%m-%d') <= DATE_FORMAT(date_sub(curdate(),interval 1 day),'%Y-%m-%d')
                        group by
                        userId) newpost
                        inner join
                        (select 
                        b.customer_id userId,min(b.first_name) userName,count(mukhin_sylius_blogging_post.id) totalPostNum
                        from 
                        mukhin_sylius_blogging_post
                        inner join 
                        (select mukhin_sylius_blogging_blog.id,mukhin_sylius_blogging_blog.customer_id,a.first_name from mukhin_sylius_blogging_blog 
                        inner join 
                        (select 
                        sylius_customer.id,concat(first_name,'-',last_name) first_name 
                        from 
                        sylius_customer 
                        where 
                        LOCATE('@a.com',email)=0) a 
                        on 
                        mukhin_sylius_blogging_blog.customer_id = a.id) b
                        on
                        mukhin_sylius_blogging_post.blog_id = b.id
                        group by
                        userId) total
                        on
                        newpost.userId = total.userId
                        union
                        (select
                        count(sums.userId) userId,"总数" userName,sum(sums.newPostNum) newPostNum,"总数" totalPostNum
                        from
                        (select
                        newpost.userId,newpost.userName,newpost.newPostNum,total.totalPostNum
                        from
                        (select 
                        b.customer_id userId,min(b.first_name) userName,count(mukhin_sylius_blogging_post.id) newPostNum
                        from 
                        mukhin_sylius_blogging_post
                        inner join 
                        (select mukhin_sylius_blogging_blog.id,mukhin_sylius_blogging_blog.customer_id,a.first_name from mukhin_sylius_blogging_blog 
                        inner join 
                        (select 
                        sylius_customer.id,concat(first_name,'-',last_name) first_name 
                        from 
                        sylius_customer 
                        where 
                        LOCATE('@a.com',email)=0) a 
                        on 
                        mukhin_sylius_blogging_blog.customer_id = a.id) b
                        on
                        mukhin_sylius_blogging_post.blog_id = b.id
                        where
                        DATE_FORMAT(created_at,'%Y-%m-%d') >= DATE_FORMAT(date_sub(curdate(),interval 7 day),'%Y-%m-%d')
                        and
                        DATE_FORMAT(created_at,'%Y-%m-%d') <= DATE_FORMAT(date_sub(curdate(),interval 1 day),'%Y-%m-%d')
                        group by
                        userId) newpost
                        inner join
                        (select 
                        b.customer_id userId,min(b.first_name) userName,count(mukhin_sylius_blogging_post.id) totalPostNum
                        from 
                        mukhin_sylius_blogging_post
                        inner join 
                        (select mukhin_sylius_blogging_blog.id,mukhin_sylius_blogging_blog.customer_id,a.first_name from mukhin_sylius_blogging_blog 
                        inner join 
                        (select 
                        sylius_customer.id,concat(first_name,'-',last_name) first_name 
                        from 
                        sylius_customer 
                        where 
                        LOCATE('@a.com',email)=0) a 
                        on 
                        mukhin_sylius_blogging_blog.customer_id = a.id) b
                        on
                        mukhin_sylius_blogging_post.blog_id = b.id
                        group by
                        userId) total
                        on
                        newpost.userId = total.userId) sums);"""

        cur = conn.cursor()
        cur.execute(newPostNumSQL)
        conn.commit()

        newPostNumResults = cur.fetchall()

        yesterday = (date.today() + timedelta(days=-1)).strftime("%Y%m%d")
        downloadPath = "/home/ubuntu/scripts/analysis/newPostNum_" + yesterday + ".csv"

        dayBeforeYesterday = (date.today() + timedelta(days=-2)).strftime("%Y%m%d")
        dbyDownloadPath = "/home/ubuntu/scripts/analysis/newPostNum_" + dayBeforeYesterday + ".csv"

        if os.path.exists(dbyDownloadPath):
            rmCmd = "rm -rf " + dbyDownloadPath
            os.system(rmCmd)

        if os.path.exists(downloadPath):
            rmCmd = "rm -rf " + downloadPath
            os.system(rmCmd)

            touchCmd = "sudo touch " + downloadPath
            os.system(touchCmd)

            rowDataArr = ['userId', 'userName', 'newPostNum', 'totalPostNum']

            if len(newPostNumResults) == 0:
                self.write2File(downloadPath, 'There is not have new user!', rowDataArr, False)
                print("There is not have new post!")
            else:
                print(newPostNumResults)
                self.write2File(downloadPath, newPostNumResults, rowDataArr, True)

        else:
            touchCmd = "sudo touch " + downloadPath
            os.system(touchCmd)

            rowDataArr = ['userId', 'userName', 'newPostNum', 'totalPostNum']

            if len(newPostNumResults) == 0:
                self.write2File(downloadPath, 'There is not have new user!', rowDataArr, False)
                print("There is not have new post!")
            else:
                print(newPostNumResults)
                self.write2File(downloadPath, newPostNumResults, rowDataArr, True)

        cur.close()
        conn.close()


    def analysisNewUser(self):
        conn = pymysql.connect(host='localhost', user='mysqldev', password='mysqlpwd',
                               database='odesk_visual_chameleon_sylius', charset='utf8')

        newUserNumSQL = """
                        select
                        *
                        from
                        ((select 
                        id userId,concat(first_name,'-',last_name) userName,email,created_at registerTime
                        from 
                        sylius_customer 
                        where 
                        LOCATE('@a.com',email)=0 
                        and 
                        DATE_FORMAT(created_at,'%Y-%m-%d') >= DATE_FORMAT(date_sub(curdate(),interval 7 day),'%Y-%m-%d')
                        and
                        DATE_FORMAT(created_at,'%Y-%m-%d') <= DATE_FORMAT(date_sub(curdate(),interval 1 day),'%Y-%m-%d')
                        order by
                        registerTime
                        DESC)
                        union
                        (select 
                        count(id) userId,"" userName,"" email,"" registerTime
                        from 
                        sylius_customer 
                        where 
                        LOCATE('@a.com',email)=0 
                        and 
                        DATE_FORMAT(created_at,'%Y-%m-%d') >= DATE_FORMAT(date_sub(curdate(),interval 7 day),'%Y-%m-%d')
                        and
                        DATE_FORMAT(created_at,'%Y-%m-%d') <= DATE_FORMAT(date_sub(curdate(),interval 1 day),'%Y-%m-%d'))) total;"""

        cur = conn.cursor()
        cur.execute(newUserNumSQL)
        conn.commit()

        newUserNumResults = cur.fetchall()

        yesterday = (date.today() + timedelta(days=-1)).strftime("%Y%m%d")
        downloadPath = "/home/ubuntu/scripts/analysis/newUserNum_" + yesterday + ".csv"

        dayBeforeYesterday = (date.today() + timedelta(days=-2)).strftime("%Y%m%d")
        dbyDownloadPath = "/home/ubuntu/scripts/analysis/newUserNum_" + dayBeforeYesterday + ".csv"

        if os.path.exists(dbyDownloadPath):
            rmCmd = "rm -rf " + dbyDownloadPath
            os.system(rmCmd)

        if os.path.exists(downloadPath):
            rmCmd = "rm -rf " + downloadPath
            os.system(rmCmd)

            touchCmd = "sudo touch " + downloadPath
            os.system(touchCmd)

            rowDataArr = ['userId', 'userName', 'email', 'registerTime']

            if len(newUserNumResults) == 0:
                self.write2File(downloadPath, 'There is not have new user!', rowDataArr, False)
                print("There is not have new user!")
            else:
                print(newUserNumResults)
                self.write2File(downloadPath, newUserNumResults, rowDataArr, True)

        else:
            touchCmd = "sudo touch " + downloadPath
            os.system(touchCmd)

            rowDataArr = ['userId', 'userName', 'email', 'registerTime']

            if len(newUserNumResults) == 0:
                self.write2File(downloadPath, 'There is not have new user!', rowDataArr, False)
                print("There is not have new user!")
            else:
                print(newUserNumResults)
                self.write2File(downloadPath, newUserNumResults, rowDataArr, True)

        cur.close()
        conn.close()


if __name__ == "__main__":
    anpanu = AnalysisNewPostAndNewUser()
    anpanu.analysisNewPost()
    anpanu.analysisNewUser()


