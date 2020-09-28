# -*- coding: utf-8 -*-

import pymysqlpool


class AnalysisNewPostAndNewUser:

    # 数据库连接池
    def connectionpool(self):
        config = {'host': '172.31.20.34', 'user': 'mysqldev', 'password': 'mysqlpwd', 'database': 'odesk_visual_chameleon_sylius',
                  'autocommit': True}
        connPool = pymysqlpool.ConnectionPool(size=5, name='connPool', **config)
        conn = connPool.get_connection()
        cur = conn.cursor()

        return connPool, conn, cur

    # 持久化
    def persistFile(self, processWay, content, downloadPath):
        with open(downloadPath, processWay) as dataFile:
            dataFile.write(content)


    def analysisNewPostAndNewUser(self):

        # 获取数据库连接池
        connPool, conn, cur = self.connectionpool()

        newPostNumSQL = """
                        select 
                        d.userId,d.userName,d.newPostNum,e.totalPostNum
                        from
                        ((select 
                        blog_id userId,count(blog_id) totalPostNum
                        from
                        mukhin_sylius_blogging_post
                        group by
                        blog_id) e
                        inner join
                        (select 
                        c.blog_id userId,c.first_name userName,count(c.blog_id) newPostNum
                        from
                        (select 
                        blog_id,b.first_name,created_at
                        from 
                        mukhin_sylius_blogging_post
                        inner join 
                        (select mukhin_sylius_blogging_blog.id,a.first_name from mukhin_sylius_blogging_blog inner join (select id,first_name from sylius_customer where LOCATE('@a.com',email)=0) a on mukhin_sylius_blogging_blog.customer_id = a.id) b
                        on
                        mukhin_sylius_blogging_post.blog_id = b.id) c
                        where
                        DATE_FORMAT(created_at,'%Y-%m-%d') = DATE_FORMAT(date_sub(curdate(),interval 1 day),'%Y-%m-%d')
                        group by
                        c.blog_id) d
                        on
                        d.userId = e.userId);"""

        cur.execute(newPostNumSQL)
        conn.commit()

        newPostNumResults = cur.fetchall()
        if len(newPostNumResults) == 0:
            self.persistFile('w', '无新帖子!', "D:\aaaaa\newPostNum.csv")
        else:
            print newPostNumResults


