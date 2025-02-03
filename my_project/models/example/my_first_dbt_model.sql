{{ config(materialized='table') }}

WITH source_data AS (
    SELECT
        ROW_NUMBER() OVER () AS id,  -- Generate a unique ID for each row
        channel_name,
        message_text,
        media_link,
        media_type,
        timestamp_utc
    FROM {{ ref('standardized_data') }}
)
SELECT * FROM source_data
