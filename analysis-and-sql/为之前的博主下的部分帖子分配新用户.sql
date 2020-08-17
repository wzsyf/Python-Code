update
mukhin_sylius_blogging_blog
set
customer_id = ''
where
id
in
(select
blog_id
from
mukhin_sylius_blogging_post
where
id
in
(select 
id 
from 
mukhin_sylius_blogging_post 
where 
enabled = 0 
and 
blog_id 
in 
(select id from mukhin_sylius_blogging_blog where customer_id in (select id from sylius_customer where email = '268@a.com'))))






update
mukhin_sylius_blogging_post
set
blog_id = 644
where
id
in
(select
postId
from
(select
blog_id,b.postId
from
mukhin_sylius_blogging_post
inner join
(select 
mukhin_sylius_blogging_post.id postId
from 
mukhin_sylius_blogging_post 
inner join  
(select mukhin_sylius_blogging_blog.id blodId from mukhin_sylius_blogging_blog inner join (select sylius_customer.id from sylius_customer where email = '268@a.com') customer on mukhin_sylius_blogging_blog.customer_id = customer.id) a
on
mukhin_sylius_blogging_post.blog_id = a.blodId
where 
enabled = 0 ) b
on
mukhin_sylius_blogging_post.id = b.postId
limit 0,1000) c)



select id,email,first_name from sylius_customer where email = '306@a.com';
select id,customer_id,code,name from mukhin_sylius_blogging_blog where customer_id = 666;

