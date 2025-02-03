{{ config(materialized='table') }}

WITH cleaned_data AS (
    SELECT
        channel_name,
        message_id,
        COALESCE(message_text, '') AS message_text,
        CASE 
            WHEN media_link ~ '^https://.*$' THEN media_link
            ELSE NULL
        END AS media_link,
        media_type,
        timestamp AT TIME ZONE 'UTC' AS timestamp_utc
    FROM {{ source('raw', 'raw_telegram_data') }}
)

SELECT * FROM cleaned_data;DBT_LOGS = {{
    config(materialized='table')
}}

WITH cleaned_data AS (
    SELECT
        channel_name,
        message_id,
        COALESCE(message_text, '') AS message_text,
        CASE 
            WHEN media_link ~ '^https://.*$' THEN media_link
            ELSE NULL
        END AS media_link,
        media_type,
        timestamp AT TIME ZONE 'UTC' AS timestamp_utc
    FROM {{ source('raw', 'raw_telegram_data') }}
)

SELECT * FROM cleaned_data;