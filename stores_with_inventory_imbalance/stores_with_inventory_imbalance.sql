with store_metrics as (
    SELECT
        store_id,
        first_value(quantity) over (partition by store_id order by price desc) as quantity_max_price,
        first_value(product_name) over (partition by store_id order by price desc) as name_max_price,
        last_value(quantity) over (partition by store_id order by price desc rows between unbounded preceding and unbounded following) as quantity_min_price,
        last_value(product_name) over (partition by store_id order by price desc rows between unbounded preceding and unbounded following) as name_min_price,
        count(*) over (partition by store_id) count_products
    from inventory
),
 deduplicated_stores as(
    select
        store_id,
        max(name_max_price) as name_max_price,
        max(name_min_price) as name_min_price,
        (max(quantity_min_price)::numeric / max(quantity_max_price)) as imbalance_ratio
    from store_metrics
    where 
        quantity_max_price < quantity_min_price
        and count_products >= 3
    group by 
        store_id
)
select 
   d.store_id,
   s.store_name,
   s.location,
   d.name_max_price as most_exp_product,
   d.name_min_price as cheapest_product,
   round(d.imbalance_ratio, 2) as imbalance_ratio
from deduplicated_stores d
join stores s
on d.store_id = s.store_id
order by 
    d.imbalance_ratio desc,
    s.store_name asc