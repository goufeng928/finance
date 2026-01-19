/*
 * GF_MYSQL_SCRIPT_PROC_Loop_Mark_Duplicate_Records.sql
 * Create by GF 2024-10-14 17:46
 */

/* ################################################## */

/*
 * #######################################################################################
 * ##                                                                                   ##
 * ## Due to configuration reasons, MySQL does not distinguish between Upper and Lower. ##
 * ##                                                                                   ##
 * ## Beware of the parameter names of functions being the same as table field names.   ##
 * ##                                                                                   ##
 * #######################################################################################
 */

/* ################################################## */

/* 结束符修改 */
DELIMITER //

/* ################################################## */

/* Delete Procedure: Max Number Duplicate Records */
DROP PROCEDURE IF EXISTS PROC_MAX_NUMBER_DUPLICATE_RECORDS//

/* Delete Procedure: Max Number Duplicate Records */
CREATE PROCEDURE PROC_MAX_NUMBER_DUPLICATE_RECORDS(IN iTable_Name VARCHAR(80), OUT oMax_Number_Duplicates BIGINT(12))
BEGIN

    /* Prepare SQL Syntax : Max Number Duplicate Records */
    SET @Session_Var_Query_Max_Number_Duplicate_Records = CONCAT(
       "WITH Drive_Counting_Duplicate_Records as (
            SELECT
                f_memo,
                f_source,
                f_site,
                f_time_gl,
                f_adjusted,
                f_date,
                f_code,
                COUNT(*) AS f_repetitions
            FROM
              ",iTable_Name,"
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
       )

       SELECT
           MAX(f_repetitions)
       INTO
           @Session_Var_Max_Number_Duplicates
       FROM
           Drive_Counting_Duplicate_Records;");

    /* Prepared Statements */
    PREPARE Stmt_Max_Number_Duplicate_Records FROM @Session_Var_Query_Max_Number_Duplicate_Records;
    EXECUTE Stmt_Max_Number_Duplicate_Records;
    DEALLOCATE PREPARE Stmt_Max_Number_Duplicate_Records;
    
    /* Outgoing Value */
    SET oMax_Number_Duplicates = @Session_Var_Max_Number_Duplicates;
    
END//

/* ################################################## */

/* Delete Procedure: Mark Duplicate Records */
DROP PROCEDURE IF EXISTS PROC_MARK_DUPLICATE_RECORDS//

/* Create Procedure: Mark Duplicate Records */
CREATE PROCEDURE PROC_MARK_DUPLICATE_RECORDS(IN iTable_Name VARCHAR(80))
BEGIN

    /* Prepare SQL Syntax : Mark Duplicate Records */
    SET @Session_Var_Query_Mark_Duplicate_Records = CONCAT(
       "WITH Drive_Filter_Duplicate_Records as (
            SELECT
                f_memo,
                f_source,
                f_site,
                f_time_gl,
                f_adjusted,
                f_date,
                f_code,
                COUNT(*) as f_repetitions,
                MAX(f_id) as f_target_id
            FROM
              ",iTable_Name,"
            WHERE
                f_memo IS NULL OR f_memo != 'Delete'
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
         ",iTable_Name,"
       SET
           f_memo = 'Delete'
       WHERE
           f_id in (SELECT f_target_id FROM Drive_Filter_f_target_id);");

    /* Prepared Statements */
    PREPARE Stmt_Mark_Duplicate_Records FROM @Session_Var_Query_Mark_Duplicate_Records;
    EXECUTE Stmt_Mark_Duplicate_Records;
    DEALLOCATE PREPARE Stmt_Mark_Duplicate_Records;
    
END//

/* ################################################## */

/* Delete Procedure: Loop Mark Duplicate Record */
DROP PROCEDURE IF EXISTS PROC_LOOP_MARK_DUPLICATE_RECORDS//

/* Delete Procedure: Loop Mark Duplicate Record */
CREATE PROCEDURE PROC_LOOP_MARK_DUPLICATE_RECORDS(IN iTable_Name VARCHAR(80))
BEGIN

    DECLARE Times BIGINT(12);
    DECLARE Max_Number_Duplicates BIGINT(12);
    
    /* Calling Other Store Procedure */
    CALL PROC_MAX_NUMBER_DUPLICATE_RECORDS(iTable_Name, Max_Number_Duplicates);

    SET Times = 1;
    WHILE Times <= Max_Number_Duplicates DO
        /* Calling Other Store Procedure */
        CALL PROC_MARK_DUPLICATE_RECORDS(iTable_Name);
        /* ------------------------------------------ */
        SET Times = (Times + 1);
    END WHILE;
    
END//

/* ################################################## */

/* 改回默认结束符 */
DELIMITER ;
