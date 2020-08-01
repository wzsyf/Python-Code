
select 
id, post_image_id, flags, created_at
from 
mukhin_sylius_blogging_post
inner join
(select
post_id,hashtag_id,a.hash
from
mukhin_sylius_blogging_hashtag__tagged_posts
inner join
(select
id,hash
from
mukhin_sylius_blogging_hashtag
where
hash = "loungewear"
or
hash = "sleepwear"
or
hash = "loungeunderwear"
or
hash = "pajamas"
or
hash = "homewear"
or
hash = "loungeset"
or
hash = "pajamaset"
or
hash = "myloungelife"
) a
on
mukhin_sylius_blogging_hashtag__tagged_posts.hashtag_id = a.id) c
on
mukhin_sylius_blogging_post.id = c.post_id
and 
id 
not in (select post_id from mukhin_sylius_blogging_post_product_relation) 
and not 
(short_description like '%%LTK%%' OR short_description like '%%LIKEtoKNOW%%' OR short_description like '%%liketk%%' OR short_description like '%%liketoknow%%') 
order by 
created_at
desc;

base_like 
and





update mukhin_sylius_blogging_post set enabled = 0 where id
in
(select 
id,post_image_id, flags
from 
mukhin_sylius_blogging_post
where 
id 
not in (select post_id from mukhin_sylius_blogging_post_product_relation) 
and 
(short_description like '%%LTK%%' OR short_description like '%%LIKEtoKNOW%%' OR short_description like '%%liketk%%' OR short_description like '%%liketoknow%%') 
and
updated_at > '2020-07-31 00:00:00'
and
enabled = 1);



select id,updated_at from mukhin_sylius_blogging_post where flags like '%popular-post%' and enabled=1 and updated_at > '2020-07-31 00:00:00' and id not in (206498,207025,207207,207218,207263,207383,207836,208131) order by updated_at desc ;
select id,updated_at from mukhin_sylius_blogging_post where flags like '%popular-post%' and enabled=1 and updated_at > '2020-07-31 00:00:00' order by updated_at desc;
206498,207025,207207,207218,207263,207383,207836,208131
215082,214719,214575,213808,212032,210841,210129,194353,192265,191584,190932,187160,180748,174551,184784,60855,58642,165502,186348,202724,186858,66731,217254,104174,214758,57216,213168,180247,175798,187910,195138


186858,165502,214575,213808,
206498,
212032,210841,175798,194353,
207025,
104174,191584,213168,187160,
207207,
180748,174551,192265,60855,
207218,
217254,195138,186348,202724,
207263,
215082,66731,58642,184784,
207383,
214758,57216,190932,180247,
207836,208131,
210129,187910,214719
select id,post_image_id, flags from mukhin_sylius_blogging_post where id not in (select post_id from mukhin_sylius_blogging_post_product_relation) and not (short_description like '%%LTK%%' OR short_description like '%%LIKEtoKNOW%%' OR short_description like '%%liketk%%' OR short_description like '%%liketoknow%%') and updated_at > '2020-07-31 00:00:00' and enabled = 0;



LOCATE("workwear",hash)>0
or
LOCATE("workoutfits",hash)>0
or
LOCATE("workfashion",hash)>0
or
LOCATE("workstyle",hash)>0
or
LOCATE("businesswear",hash)>0
or
LOCATE("officestyle",hash)>0

hash = "workwear"
or
hash = "workoutfits"
or
hash = "workfashion"
or
hash = "workstyle"
or
hash = "businesswear"
or
hash = "officestyle"


hash = "workwear" or hash = "workoutfits" or hash = "workfashion" or hash = "workstyle" or hash = "businesswear" or hash = "officestyle"



Lounge Wear:
LOCATE("loungewear",hash)>0
or
LOCATE("sleepwear",hash)>0
or
LOCATE("loungeunderwear",hash)>0
or
LOCATE("pajamas",hash)>0
or
LOCATE("homewear",hash)>0
or
LOCATE("loungeset",hash)>0
or
LOCATE("pajamaset",hash)>0
or
LOCATE("myloungelife",hash)>0


hash = "loungewear"
or
hash = "sleepwear"
or
hash = "loungeunderwear"
or
hash = "pajamas"
or
hash = "homewear"
or
hash = "loungeset"
or
hash = "pajamaset"
or
hash = "myloungelife"



hash = "loungewear" or hash = "sleepwear" or hash = "loungeunderwear" or hash = "pajamas" or hash = "homewear" or hash = "loungeset" or hash = "pajamaset" or hash = "myloungelife"




Beach Wear:
LOCATE("swimsuit",hash)>0
or
LOCATE("swimwear",hash)>0
or
LOCATE("bikini",hash)>0
or
LOCATE("beachwear",hash)>0

hash = "swimsuit"
or
hash = "swimwear"
or
hash = "bikini"
or
hash = "beachwear"


hash = "swimsuit" or hash = "swimwear" or hash = "bikini" or hash = "beachwear"



根据帖子找到email用户简单版本

select 
email
from 
sylius_customer
where id in
(select customer_id from mukhin_sylius_blogging_blog 
where id in 
(select blog_id from mukhin_sylius_blogging_post
where
id = 214758))


根据帖子找到email用户复杂版本
select 
email
from 
sylius_customer
where id in
(select customer_id from mukhin_sylius_blogging_blog 
where id in 
(select blog_id from mukhin_sylius_blogging_post
where
id
in
(select 
id
from 
mukhin_sylius_blogging_post
inner join
(select
post_id,hashtag_id,a.hash
from
mukhin_sylius_blogging_hashtag__tagged_posts
inner join
(select
id,hash
from
mukhin_sylius_blogging_hashtag
where
hash = "loungewear"
or
hash = "sleepwear"
or
hash = "loungeunderwear"
or
hash = "pajamas"
or
hash = "homewear"
or
hash = "loungeset"
or
hash = "pajamaset"
or
hash = "myloungelife"
) a
on
mukhin_sylius_blogging_hashtag__tagged_posts.hashtag_id = a.id) c
on
mukhin_sylius_blogging_post.id = c.post_id
and 
id 
not in (select post_id from mukhin_sylius_blogging_post_product_relation) 
and not 
( short_description like '%%LTK%%' OR short_description like '%%LIKEtoKNOW%%' OR short_description like '%%liketk%%' OR short_description like '%%liketoknow%%') 
order by 
base_like 
desc)));



根据用户找帖子
select 
id, post_image_id, flags 
from 
mukhin_sylius_blogging_post
where 
enabled = 0 
and 
blog_id 
in 
(select 
id 
from
mukhin_sylius_blogging_blog 
where 
customer_id 
in (select id from sylius_customer where email = '{0}'));





select email from sylius_customer where id in (select customer_id from mukhin_sylius_blogging_blog where id in (select blog_id from mukhin_sylius_blogging_post where id = postId));

select email from sylius_customer where id in (select customer_id from mukhin_sylius_blogging_blog where id in (select blog_id from mukhin_sylius_blogging_post where id = 216003));






select
id,post_image_id,flags
from
((select 
id, post_image_id, flags 
from 
mukhin_sylius_blogging_post 
where 
blog_id 
in 
(select id from mukhin_sylius_blogging_blog where customer_id in (select id from sylius_customer where email = '199@a.com')) 
and 
id 
not in (select post_id from mukhin_sylius_blogging_post_product_relation) 
and not 
( short_description like '%%LTK%%' OR short_description like '%%LIKEtoKNOW%%' OR short_description like '%%liketk%%' OR short_description like '%%liketoknow%%') 
order by 
base_like 
desc) c
inner join
(select
post_id,hashtag_id,a.hash
from
mukhin_sylius_blogging_hashtag__tagged_posts
inner join
(select
id,hash
from
mukhin_sylius_blogging_hashtag
where
LOCATE("workwear",hash)>0
or
LOCATE("workoutfits",hash)>0
or
LOCATE("workfashion",hash)>0
or
LOCATE("workstyle",hash)>0
or
LOCATE("businesswear",hash)>0
or
LOCATE("officestyle",hash)>0
) a
on
mukhin_sylius_blogging_hashtag__tagged_posts.hashtag_id = a.id) b
on
c.id = b.post_id);















select cdn_url from mukhin_sylius_blogging_post_image where id in
(select post_image_id from mukhin_sylius_blogging_post inner join (select post_id,hashtag_id,a.hash from mukhin_sylius_blogging_hashtag__tagged_posts inner join (select id,hash from mukhin_sylius_blogging_hashtag where hash = 'loungewear' or hash = 'sleepwear' or hash = 'loungeunderwear' or hash = 'pajamas' or hash = 'homewear' or hash = 'loungeset' or hash = 'pajamaset' or hash = 'myloungelife') a on mukhin_sylius_blogging_hashtag__tagged_posts.hashtag_id = a.id) c on mukhin_sylius_blogging_post.id = c.post_id and id not in (select post_id from mukhin_sylius_blogging_post_product_relation) and not ( short_description like '%%LTK%%' OR short_description like '%%LIKEtoKNOW%%' OR short_description like '%%liketk%%' OR short_description like '%%liketoknow%%') order by base_like desc;)