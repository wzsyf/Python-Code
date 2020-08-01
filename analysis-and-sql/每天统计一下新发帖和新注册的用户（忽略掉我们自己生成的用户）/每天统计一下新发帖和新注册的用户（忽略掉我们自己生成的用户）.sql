
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
newpost.userId = total.userId) sums);








select
sum(newPostNum) allNewPostOfUser
from
(select 
b.customer_id userId,b.first_name userName,count(mukhin_sylius_blogging_post.id) newPostNum
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
userId,userName) allnewpost;






DATE_FORMAT(created_at,'%Y-%m-%d') = DATE_FORMAT(date_sub(curdate(),interval 1 day),'%Y-%m-%d')








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
DATE_FORMAT(created_at,'%Y-%m-%d') <= DATE_FORMAT(date_sub(curdate(),interval 1 day),'%Y-%m-%d'))) total;



