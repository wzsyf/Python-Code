
在根据帖子的flags匹配帖子之前首先要保证对应分配下面的博主已经打上分类的flags,若没有打上则执行打flags的程序，然后再执行帖子的匹配程序




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





select 
id, 
post_image_id,
flags, 
enabled
from 
mukhin_sylius_blogging_post 
where
(flags
like
'%datenightoutfit%'
or
flags
like
'%dateoutfit%'
or
flags
like
'%dateoutfits%'
or
flags
like
'%date-outfits%')
and
LOCATE("blocked-post",flags)=0
and
enabled = 0
and 
id
not in 
(select post_id from mukhin_sylius_blogging_post_product_relation) 
and 
not 
(short_description like '%%LTK%%' OR short_description like '%%LIKEtoKNOW%%' OR short_description like '%%liketk%%' OR short_description like '%%liketoknow%%') 
order by 
created_at
desc;



select 
id, 
post_image_id,
flags, 
enabled
from 
mukhin_sylius_blogging_post 
where
(flags
like
'%datenightoutfit%'
or
flags
like
'%dateoutfit%'
or
flags
like
'%dateoutfits%'
or
flags
like
'%date-outfits%')
and
LOCATE("blocked-post",flags)=0
and
enabled = 0
and 
id
not in 
(select post_id from mukhin_sylius_blogging_post_product_relation)
and 
not 
(short_description like '%%LTK%%' OR short_description like '%%LIKEtoKNOW%%' OR short_description like '%%liketk%%' OR short_description like '%%liketoknow%%') 
order by 
created_at
desc;


 


select 
id, 
post_image_id,
flags, 
enabled
from 
mukhin_sylius_blogging_post 
where 
(flags
like
'%momstyle%'
or
flags
like
'%momstylelife%'
or
flags
like
'%momstyleblogger%'
)
and
LOCATE("blocked-post",flags)=0
and
enabled = 0
and 
id
not in 
(select post_id from mukhin_sylius_blogging_post_product_relation) 
and 
not 
(short_description like '%%LTK%%' OR short_description like '%%LIKEtoKNOW%%' OR short_description like '%%liketk%%' OR short_description like '%%liketoknow%%') 
order by 
created_at
desc;



select 
id, 
post_image_id,
flags, 
enabled 
from 
mukhin_sylius_blogging_post 
where 
enabled = 0
and
(flags
like
'%maternityfashion%'
or
flags
like
'%maternity%'
or
flags
like
'%maternitydresses%'
or
flags
like
'%bumpstyle%'
or
flags
like
'%bumplife%'
or
flags
like
'%bumpdate%'
or
flags
like
'%maternitystyle%'
or
flags
like
'%pregnantstyle%'
or
flags
like
'%pregnantfashion%'
or
flags
like
'%pregnantlife%')
and 
id
not in 
(select post_id from mukhin_sylius_blogging_post_product_relation) 
and 
not 
(short_description like '%%LTK%%' OR short_description like '%%LIKEtoKNOW%%' OR short_description like '%%liketk%%' OR short_description like '%%liketoknow%%') 
order by 
created_at
desc;




LOCATE("vintagestyle",flags)>0 
or LOCATE("vintage",flags)>0 

flags
like
'%vintagestyle%'
or
flags
like
'%vintage%'


LOCATE("streetstyle",flags)>0 
or LOCATE("streetwear",flags)>0 
or LOCATE("street-style",flags)>0 

flags
like
'%streetstyle%'
or
flags
like
'%streetwear%'
or
flags
like
'%street-style%' 

LOCATE("travelstyle",flags)>0 
or LOCATE("travelfashion",flags)>0 
or LOCATE("travel-style",flags)>0 

flags
like
'%travel-style%'
or
flags
like
'%travelstyle%'
or
flags
like
'%travelfashion%' 


LOCATE("loungewear",hash)>0 
or LOCATE("sleep-wear",hash)>0
or LOCATE("loungeunder-wear",hash)>0 
or LOCATE("pajamas",hash)>0 
or LOCATE("home-wear",hash)>0 
or LOCATE("lounge-set",hash)>0 
or LOCATE("pajamaset",hash)>0 
or LOCATE("mylounge-life",hash)>0


LOCATE("swimsuit",hash)>0 
or LOCATE("swimwear",hash)>0 
or LOCATE("bikini",hash)>0 
or LOCATE("beach-wear",hash)>0






select
id,flags
from
(select 
id, 
post_image_id,
flags, 
created_at 
from 
mukhin_sylius_blogging_post 
where
enabled = 0
and 
(flags
like
'%vintage%'
or
flags
like
'%vintagestyle%'
)
and 
id
not in 
(select post_id from mukhin_sylius_blogging_post_product_relation) 
and 
not 
(short_description like '%%LTK%%' OR short_description like '%%LIKEtoKNOW%%' OR short_description like '%%liketk%%' OR short_description like '%%liketoknow%%') 
order by 
created_at
desc) a
where
flags
like
'%month-may%' 
or
flags
like
'%month-jun%'
or
flags
like
'%month-jul%'
or
flags
like
'%month-aug%'
or
flags
like
'%month-sept%';








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

select id,post_image_id, flags from mukhin_sylius_blogging_post where id not in (select post_id from mukhin_sylius_blogging_post_product_relation) and not (short_description like '%%LTK%%' OR short_description like '%%LIKEtoKNOW%%' OR short_description like '%%liketk%%' OR short_description like '%%liketoknow%%') and updated_at > '2020-07-31 00:00:00' and enabled = 0;



LOCATE("work-wear",flags)>0
or
LOCATE("workoutfits",flags)>0
or
LOCATE("workfashion",flags)>0
or
LOCATE("workstyle",flags)>0
or
LOCATE("businesswear",flags)>0
or
LOCATE("officestyle",flags)>0

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


hash = "lounge-wear"
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

LOCATE("swimsuit",flags)>0
or
LOCATE("swimwear",flags)>0
or
LOCATE("bikini",flags)>0
or
LOCATE("beachwear",flags)>0




hash = "swimsuit" or hash = "swimwear" or hash = "bikini" or hash = "beachwear"


验证帖子匹配是否成功的sql,具体就是查看帖子的更新时间
select id,updated_at from mukhin_sylius_blogging_post where flags like '%popular-post%' and enabled=1 and updated_at > '2020-08-13 00:00:00' order by updated_at desc;

select updated_at from mukhin_sylius_blogging_post where flags like '%popular-post%' and enabled=1 and updated_at >= '2020-08-03 00:00:00' 
and
(flags
like
'%travel-style%'
or
flags
like
'%travelfashion%'
or
flags
like
'%travelstyle%'
)
order by updated_at desc ;


update mukhin_sylius_blogging_post set enabled=0 where id in 
(select
*
from
(select id from mukhin_sylius_blogging_post where flags like '%popular-post%' and enabled=1 and updated_at > '2020-08-10 00:00:00' order by updated_at desc) a);
DATE_FORMAT(updated_at,'%Y-%m-%d') >= DATE_FORMAT(date_sub(curdate(),interval 7 day),'%Y-%m-%d')


(flags
like
'%vintage%'
or
flags
like
'%vintagestyle%'
)
or
(flags
like
'%streetstyle%'
or
flags
like
'%streetwear%'
or
flags
like
'%street-style%')
or
(flags
like
'%travel-style%'
or
flags
like
'%travelfashion%'
or
flags
like
'%travelstyle%')


根据帖子找到email用户简单版本

select 
id,
email
from 
sylius_customer
where id in
(select customer_id from mukhin_sylius_blogging_blog 
where id in 
(select blog_id from mukhin_sylius_blogging_post
where
id = 242892))

224664 220969
根据用户找帖子
select id, post_image_id, flags,enabled from mukhin_sylius_blogging_post 
where enabled = 0 
and blog_id in 
(select id from mukhin_sylius_blogging_blog where customer_id in (select id from sylius_customer where email = '209@a.com'));


判断帖子是否已经匹配了商品
select post_id from mukhin_sylius_blogging_post_product_relation where post_id = 149675;

查询用户头像路径
select customer_id,path from app_customer_image where customer_id = 656;


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
(select 
id, post_image_id, flags, created_at
from 
mukhin_sylius_blogging_post
where
(flags
like
'%travel-style%'
or
flags
like
'%travelfashion%'
or
flags
like
'%travelstyle%')
and
id 
not in (select post_id from mukhin_sylius_blogging_post_product_relation) 
and not 
(short_description like '%%LTK%%' OR short_description like '%%LIKEtoKNOW%%' OR short_description like '%%liketk%%' OR short_description like '%%liketoknow%%') 
order by 
created_at
desc) a
where
flags
like
'%month-may%' 
or
flags
like
'%month-jun%'
or
flags
like
'%month-jul%'
or
flags
like
'%month-aug%'
or
flags
like
'%month-sept%')));



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








workWearSql = """select id, post_image_id, flags, created_at from mukhin_sylius_blogging_post where 
                          LOCATE("work-wear",flags)>0 or LOCATE("workoutfits",flags)>0 or LOCATE("workfashion",flags)>0 
                          or LOCATE("workstyle",flags)>0 or LOCATE("businesswear",flags)>0 or LOCATE("officestyle",flags)>0 
                          and id not in (select post_id from mukhin_sylius_blogging_post_product_relation) and 
                          not (short_description like '%%LTK%%' OR short_description like '%%LIKEtoKNOW%%' OR short_description 
                         like '%%liketk%%' OR short_description like '%%liketoknow%%') order by created_at desc;"""
 
          loungeWearSql = """select id, post_image_id, flags, created_at from mukhin_sylius_blogging_post where 
                          LOCATE("lounge-wear",flags)>0 or LOCATE("sleepwear",flags)>0 or LOCATE("loungeunderwear",flags)>0 
                         or LOCATE("pajamas",flags)>0 or LOCATE("homewear",flags)>0 or LOCATE("loungeset",flags)>0 
                        or LOCATE("pajamaset",flags)>0 or LOCATE("myloungelife",flags)>0 and id not 
                        in (select post_id from mukhin_sylius_blogging_post_product_relation) and 
                       not (short_description like '%%LTK%%' OR short_description like '%%LIKEtoKNOW%%' OR short_description 
                        like '%%liketk%%' OR short_description like '%%liketoknow%%') order by created_at desc;"""

        beachWearSql = """select id, post_image_id, flags, created_at from mukhin_sylius_blogging_post where 
                         LOCATE("swimsuit",flags)>0 or LOCATE("swimwear",flags)>0 or LOCATE("bikini",flags)>0 
                         or LOCATE("beach-wear",flags)>0 and id not in (select post_id from mukhin_sylius_blogging_post_product_relation) 
                        and not (short_description like '%%LTK%%' OR short_description like '%%LIKEtoKNOW%%' OR short_description 
                        like '%%liketk%%' OR short_description like '%%liketoknow%%') order by created_at desc;"""













