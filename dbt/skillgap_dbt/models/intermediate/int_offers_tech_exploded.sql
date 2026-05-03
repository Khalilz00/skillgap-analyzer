with stg as (
    select * from {{ ref('stg_offers') }}
),

exploded as (
    select
        offer_id,
        scrape_date,
        rome_code,
        seniority,
        location,
        tech
    from stg, unnest(tech_stack) as tech
    where tech is not null
      and tech != ''
)

select * from exploded
