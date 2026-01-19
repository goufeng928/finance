/*
 * GF_MYSQL_SCRIPT_Mark_Duplicate_Records.sql
 * Create by GF 2024-10-14 17:46
 */

WITH Drive_Filter_Duplicate_Records as (
    SELECT
        f_memo,
        f_source,
        f_site,
        f_time_gl,
        f_adjusted,
        f_date,
        f_code,
        COUNT(*) AS f_repetitions,
        MAX(f_id) AS f_target_id
    FROM
        dataset_stocks
    GROUP BY
        f_memo,
        f_source,
        f_site,
        f_time_gl,
        f_adjusted,
        f_date,
        f_code,
        f_open,
        f_high,
        f_low,
        f_close
    HAVING
        f_repetitions > 1
)

, Drive_Filter_f_target_id as (
    SELECT
        f_target_id
    FROM
        Drive_Filter_Duplicate_Records
)

UPDATE
    dataset_stocks
SET
    f_memo = "Delete"
WHERE
    f_id in (SELECT f_target_id FROM Drive_Filter_f_target_id)
;
