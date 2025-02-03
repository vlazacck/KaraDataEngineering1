{{ config(materialized='table') }}

SELECT
    "channel_name",
    "message_id",
    TRIM("message_text") AS "message_text",
    "media_link",
    COALESCE("media_type", 'unknown') AS "media_type",
    "timestamp" AT TIME ZONE 'UTC' AS "timestamp_utc"
FROM {{ source('public', 'raw_telegram_data') }}