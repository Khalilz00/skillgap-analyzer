with source as (
    select * from {{ source('raw', 'offers') }}
),

renamed as (
    select
        offer_id,
        title,
        created_at,
        scrape_date,
        location,
        seniority,
        contract_type,
        rome_code,
        tech_stack,
        company_name
    from source
)

select * from renamed
