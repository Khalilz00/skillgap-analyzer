{{ config(materialized='table') }}

with exploded as (
    select * from {{ ref('int_offers_tech_exploded') }}
),

aggregated as (
    select
        tech,
        min(scrape_date) as first_seen,
        max(scrape_date) as last_seen,
        count(distinct offer_id) as total_mentions
    from exploded
    group by tech
)

select * from aggregated
