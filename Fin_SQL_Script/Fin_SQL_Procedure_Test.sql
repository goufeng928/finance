/* Fin_SQL_Procedure_Test.sql */

/* Create By GF 2023-09-21 23:13 */

/* -------------------------------------------------- */

-- 结束符修改。
DELIMITER //

/* -------------------------------------------------- */
/* Test Procedure */

-- 删除存储过程: 测试计算视图 (Test Calculate View).
DROP PROCEDURE IF EXISTS TEST_CALCULATE_VIEW//

-- 创建存储过程: 测试计算视图 (Test Calculate View).
CREATE PROCEDURE TEST_CALCULATE_VIEW(IN In_Table_Name CHAR(80))
BEGIN

    /*
     * Requirement : MySQL 8.0+ (OLAP : Online Anallytical Processing).
     */
    
    /* **************************************** */
    
    -- 声明局部变量 : 保存视图(View)名称的变量.
    DECLARE Inner_View_Name CHAR(80);
    
    /* **************************************** */
    
    -- 拼接字符串 : View + 表名.
    SET Inner_View_Name = CONCAT("view_test_",In_Table_Name);

    /* **************************************** */

    -- 创建视图语句 - 以字符串的形式保存到会话变量.
    SET @Inner_Prepare_SQL = CONCAT("
    CREATE OR REPLACE VIEW ",Inner_View_Name," as
    SELECT
        _index,
        _date,
        _close,
        _volume,
        MATH_ACC_AVG(_index, _close) as MATH_ACC_AVG,
        MATH_MOV_VAR(60, _index, _close) as MATH_MOV_VAR_60
    FROM
        (SELECT
             -- 为原表添加行号.
             ROW_NUMBER() OVER(ORDER BY _date ASC) as _index,
             _date,
             _close,
             _volume
         FROM
             ",In_Table_Name,"
         WHERE
             _volume <> 0.0) as _Temp;");
    
    /* **************************************** */
    
    -- 预处理语句.
    PREPARE stmt FROM @Inner_Prepare_SQL;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

END//  

-- 改回默认结束符。
DELIMITER ;

/* -------------------------------------------------- */
/* EOF */
