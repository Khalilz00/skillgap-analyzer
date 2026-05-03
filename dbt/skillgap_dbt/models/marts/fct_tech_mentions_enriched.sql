{{ config(
    materialized='table',
    partition_by={'field': 'scrape_date', 'data_type': 'date'},
    cluster_by=['tech']
) }}

with exploded as (
    select * from {{ ref('int_offers_tech_exploded') }}
)

select
    scrape_date,
    tech,
    rome_code,
    seniority,
    location,
    count(distinct offer_id) as mention_count
from exploded
group by scrape_date, tech, rome_code, seniority, location
