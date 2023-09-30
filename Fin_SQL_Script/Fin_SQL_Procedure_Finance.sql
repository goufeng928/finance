-- Fin_SQL_Procedure_Finance.sql

-- Create By GF 2023-09-05 15:21

/* -------------------------------------------------- */

-- 结束符修改。
DELIMITER //

/* -------------------------------------------------- */
/* Finance Calculate Procedure */

-- 删除存储过程: 金融计算数据视图 (Finance Calculate View).
DROP PROCEDURE IF EXISTS FIN_CALCULATE_VIEW//

-- 创建存储过程: 金融计算数据视图 (Finance Calculate View).
CREATE PROCEDURE FIN_CALCULATE_VIEW(IN In_Table_Name CHAR(80))
BEGIN

    /*
     * Requirement : MySQL 8.0+ (OLAP : Online Anallytical Processing).
     */
    
    /* 声明局部变量 : 保存视图(View)名称的变量 */
    DECLARE Inner_View_Name CHAR(80);

    /* **************************************** */

    /* 拼接字符串 : View + 表名 */
    SET Inner_View_Name = CONCAT("view_",In_Table_Name);

    /* 创建视图语句 - 以字符串的形式保存到会话变量 */
    SET @Inner_View_Prepare_SQL = CONCAT("
        CREATE OR REPLACE VIEW ",Inner_View_Name," as
        SELECT
            _index,
            _date,
            _close,
            _volume,
            FIN_SMA(5, _index, _close) as SMA5,
            FIN_SMA(10, _index, _close) as SMA10,
            FIN_EMA(12, _index, _close) as EMA12,
            FIN_EMA(26, _index, _close) as EMA26,
            FIN_MACD_DIF(12, 26, _index, _close) as MACD_DIF,
            FIN_MACD_DEA(12, 26, _index, _close) as MACD_DEA,
            FIN_MACD_STICK(12, 26, _index, _close) as MACD_STICK,
            SUM_FUTURE_20_RISE_FALL,
            FIN_EST_2_LINE_CROSS(\"Up\", _index, FIN_SMA(5, _index, _close), FIN_SMA(10, _index, _close)) as SMA_CROSS_UP,
            FIN_EST_2_LINE_CROSS(\"Down\", _index, FIN_SMA(5, _index, _close), FIN_SMA(10, _index, _close)) as SMA_CROSS_DOWN,
            FIN_EST_2_VALUE_COMPARE_SIZE(\"Larger\", FIN_SMA(5, _index, _close), FIN_SMA(10, _index, _close)) as SMA_BULLISH,
            FIN_EST_2_VALUE_COMPARE_SIZE(\"Larger\", FIN_MACD_DIF(12, 26, _index, _close), FIN_MACD_DEA(12, 26, _index, _close)) as MACD_BULLISH
        FROM
            (SELECT
                 -- 为原表添加行号.
                 ROW_NUMBER() OVER(ORDER BY _date ASC) as _index,
                 SUM(_rise_fall_rate) OVER(ORDER BY _date ASC ROWS BETWEEN 1 FOLLOWING AND 20 FOLLOWING) as SUM_FUTURE_20_RISE_FALL,
                 _date,
                 _close,
                 _volume
             FROM
                 ",In_Table_Name,"
             WHERE
                 _volume <> 0.0) as _Temp;");
    
    /* 预处理语句 - 创建视图语句 */
    PREPARE View_Stmt FROM @Inner_View_Prepare_SQL;
    EXECUTE View_Stmt;
    DEALLOCATE PREPARE View_Stmt;

END//  

-- 改回默认结束符。
DELIMITER ;

/* -------------------------------------------------- */
/* EOF */
