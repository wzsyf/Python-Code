select
original_store,
brand_name
from
sylius_product
where
enabled = 1
and
brand_name
like
'%nike%'
and
last_imported_at > '2020-07-31 00:00:00'
and
last_imported_at < '2020-07-31 23:59:59'
and
original_store = 'NORDSTROM RACK'
and
id
in
(select
product_id
from
sylius_product_variant
where
id
in
(select
a.product_variant_id
from
(select
product_variant_id,
price/msrp rate
from
sylius_channel_pricing) a
where
rate >= 0.3 and rate <= 0.7))
and
id
in
(select
product_id
from
sylius_product_taxon
where
taxon_id
in
(select
id
from
sylius_taxon
where
code = 'category-women-clothing'
or
code = 'category-women-shoes'
or
code = 'category-women-bags'));



活动数据-不用限制这个导入导出时间,客户端只按照折扣，store、分类限定的
select
original_store,
brand_name
from
sylius_product
where
enabled = 1
and
brand_name
like
'%nike%'
and
original_store = 'NORDSTROM RACK'
and
id
in
(select
product_id
from
sylius_product_variant
where
id
in
(select
a.product_variant_id
from
(select
product_variant_id,
price/msrp rate
from
sylius_channel_pricing) a
where
rate >= 0.3 and rate <= 0.7))
and
id
in
(select
product_id
from
sylius_product_taxon
where
taxon_id
in
(select
id
from
sylius_taxon
where
code = 'category-women-clothing'
or
code = 'category-women-shoes'
or
code = 'category-women-bags'));














select
product_id
from
sylius_product_taxon
where
taxon_id
in
(select
id
from
sylius_taxon
where
code = 'category-women-clothing'
or
code = 'category-women-shoes'
or
code = 'category-women-bags')



select
a.product_variant_id,
a.rate rate
from
(select
product_variant_id,
price/msrp rate
from
sylius_channel_pricing) a
where
rate > 0.3 and rate < 0.7