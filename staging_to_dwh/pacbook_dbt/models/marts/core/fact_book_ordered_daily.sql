WITH stg_book_order AS (
    SELECT
        order_id AS nk_order_id,
        order_date::date AS order_date,
        customer_id AS nk_customer_id
    FROM {{ source('pacbook', 'cust_order') }}
),


stg_order_line AS (
    SELECT *
    FROM  {{ source('pacbook', 'order_line') }}
),


dim_book AS (
    SELECT *
    FROM {{ ref("dim_book") }}
),


dim_date AS (
    SELECT *
    FROM {{ ref("dim_date") }}
),


dwh_book_order AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(["nk_book_id"]) }} AS sk_book_id,
        db.nk_book_id,
        dd.date_id, 
        {{ dbt_date.now() }} AS created_at,
        {{ dbt_date.now() }} AS updated_at
    FROM stg_book_order bo 
    INNER JOIN dim_date dd ON DATE(bo.order_date) = dd.date_actual 
    INNER JOIN stg_order_line ol ON bo.nk_order_id = ol.order_id 
    INNER JOIN dim_book db ON ol.book_id = db.nk_book_id

)

SELECT * FROM dwh_book_order