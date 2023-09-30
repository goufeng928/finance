-- Fin_SQL_Procedure_DML.sql

-- Create By GF 2023-09-05 15:21

/* -------------------------------------------------- */

-- 结束符修改。
DELIMITER //

/* -------------------------------------------------- */
/* Data Manipulation Language Procedure */

/* 删除存储过程: 插入转更新 - Double类型值 (Insert or Update - Double Type Value) */
DROP PROCEDURE IF EXISTS DML_INSERT_OR_UPDATE_DOUBLE//

/* 创建存储过程: 插入转更新 - Double类型值 (Insert or Update - Double Type Value) */
CREATE PROCEDURE DML_INSERT_OR_UPDATE_DOUBLE(IN In_Table_Name VARCHAR(80),
                                             IN In_Index_Field_Name VARCHAR(80),
                                             IN In_Index_Value BIGINT(12),
                                             IN In_Double_Field_Name VARCHAR(80),
                                             IN In_Double_Value DOUBLE(16,4))
BEGIN

    /* Prepare SQL语句 : 判断是否存在某条记录，如果存在则返回 1 */
    SET @Inner_Check_Exists_Sql = CONCAT("SELECT _Value INTO @Inner_Check_Exists_Result FROM (SELECT IF(EXISTS (SELECT ",
                                         In_Double_Field_Name," FROM ",
                                         In_Table_Name,
                                         " WHERE ",
                                         In_Index_Field_Name,
                                         " = ",
                                         In_Index_Value,
                                         "), 1, 0) as _Value) as _Temp;");
    /* 预处理语句 */
    PREPARE Stmt_Check_Exists FROM @Inner_Check_Exists_Sql;
    EXECUTE Stmt_Check_Exists;
    DEALLOCATE PREPARE Stmt_Check_Exists;

    /*
     * 条件判断。
     * 如果要插入的记录行存在 : 更新记录。
     * 如果要插入的记录行不存在 : 插入记录。
     */
    IF @Inner_Check_Exists_Result = 1 THEN
        /* Prepare SQL语句 : 更新语句 */
        SET @Inner_Update_Sql = CONCAT("UPDATE ",
                                       In_Table_Name,
                                       " SET ",
                                       In_Double_Field_Name,
                                       " = ",
                                       In_Double_Value,
                                       " WHERE ",
                                       In_Index_Field_Name,
                                       " = ",
                                       In_Index_Value,";");
        /* 预处理语句 */
        PREPARE Stmt_Update FROM @Inner_Update_Sql;
        EXECUTE Stmt_Update;
        DEALLOCATE PREPARE Stmt_Update;
    
    ELSE
        /* Prepare SQL语句 : 插入语句 */
        SET @Inner_Insert_Sql = CONCAT("INSERT INTO ",
                                       In_Table_Name,
                                       "(",
                                       In_Index_Field_Name,
                                       ", ",
                                       In_Double_Field_Name,
                                       ") VALUES (",
                                       In_Index_Value,
                                       ", ",
                                       In_Double_Value,
                                       ");");
        /* 预处理语句 */
        PREPARE Stmt_Insert FROM @Inner_Insert_Sql;
        EXECUTE Stmt_Insert;
        DEALLOCATE PREPARE Stmt_Insert;

    END IF;
    
END//

-- 改回默认结束符。
DELIMITER ;

/* -------------------------------------------------- */
/* EOF */
