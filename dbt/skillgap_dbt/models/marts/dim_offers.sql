{{ config(materialized='table') }}

select
    offer_id,
    title,
    created_at,
    scrape_date,
    location,
    seniority,
    contract_type,
    rome_code,
    company_name,
    array_length(tech_stack) as tech_count
from {{ ref('stg_offers') }}
