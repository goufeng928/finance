-- Fin_SQL_Procedure_DML.sql

-- Create By GF 2023-09-05 15:21

/* -------------------------------------------------- */

-- 结束符修改。
DELIMITER //

/* -------------------------------------------------- */
/* Data Manipulation Language Procedure */

/* 删除存储过程: DML - 插入转更新 - Double类型值 (DML - Insert or Update - Double Type Value) */
DROP PROCEDURE IF EXISTS PROC_DML_INSERT_OR_UPDATE_DOUBLE//

/* 创建存储过程: DML - 插入转更新 - Double类型值 (DML - Insert or Update - Double Type Value) */
CREATE PROCEDURE PROC_DML_INSERT_OR_UPDATE_DOUBLE(IN In_Table_Name VARCHAR(80),
                                                  IN In_Index_Field_Name VARCHAR(80),
                                                  IN In_Index_Value BIGINT(12),
                                                  IN In_Double_Field_Name VARCHAR(80),
                                                  IN In_Double_Value DOUBLE(16,4))
BEGIN

    /* Similar SQL Statements:
     *
     * INSERT INTO table_name(index, double_value) VALUES (1, 3.14) ON DUPLICATE KEY UPDATE double_value = 3.14;
     */

    /* Prepare SQL语句 : 判断是否存在某条记录，如果存在则返回 1 */
    SET @Session_Check_Exists_Sql =
        CONCAT("SELECT ",
               "IF(EXISTS (SELECT ",In_Double_Field_Name," FROM ",In_Table_Name," WHERE ",In_Index_Field_Name," = ",In_Index_Value,"), 1, 0) ",
               "INTO @Session_Check_Exists_Result;");
    /* Prepared Statements */
    PREPARE Stmt_Check_Exists FROM @Session_Check_Exists_Sql;
    EXECUTE Stmt_Check_Exists;
    DEALLOCATE PREPARE Stmt_Check_Exists;

    /* **************************************** */

    /*
     * 条件判断。
     * 如果要插入的记录行存在 : 更新记录。
     * 如果要插入的记录行不存在 : 插入记录。
     */
    IF @Session_Check_Exists_Result = 1 THEN
        SET @Session_Update_Sql =
            CONCAT("UPDATE ",In_Table_Name," SET ",In_Double_Field_Name," = ",In_Double_Value," WHERE ",In_Index_Field_Name," = ",In_Index_Value,";");
        /* Prepared Statements */
        PREPARE Stmt_Update FROM @Session_Update_Sql;
        EXECUTE Stmt_Update;
        DEALLOCATE PREPARE Stmt_Update;
    
    ELSE
        SET @Session_Insert_Sql =
            CONCAT("INSERT INTO ",In_Table_Name,"(",In_Index_Field_Name,", ",In_Double_Field_Name,") VALUES (",In_Index_Value,", ",In_Double_Value,");");
        /* Prepared Statements */
        PREPARE Stmt_Insert FROM @Session_Insert_Sql;
        EXECUTE Stmt_Insert;
        DEALLOCATE PREPARE Stmt_Insert;
    END IF;
    
END//

/* 删除存储过程: DML - 删除再插入 - Double类型值 (DML - Delete and Insert - Double Type Value) */
DROP PROCEDURE IF EXISTS PROC_DML_DELETE_AND_INSERT_DOUBLE//

/* 创建存储过程: DML - 删除再插入 - Double类型值 (DML - Delete and Insert - Double Type Value) */
CREATE PROCEDURE PROC_DML_DELETE_AND_INSERT_DOUBLE(IN In_Table_Name VARCHAR(80),
                                                   IN In_Index_Field_Name VARCHAR(80),
                                                   IN In_Index_Value BIGINT(12),
                                                   IN In_Double_Field_Name VARCHAR(80),
                                                   IN In_Double_Value DOUBLE(16,4))
BEGIN

    /* Similar SQL Statements:
     *
     * REPLACE INTO table_name(index, double_value) VALUES (1, 3.14);
     */

    /* Prepare SQL语句 : 判断是否存在某条记录，如果存在则返回 1 */
    SET @Session_Check_Exists_Sql =
        CONCAT("SELECT ",
               "IF(EXISTS (SELECT ",In_Double_Field_Name," FROM ",In_Table_Name," WHERE ",In_Index_Field_Name," = ",In_Index_Value,"), 1, 0) ",
               "INTO @Session_Check_Exists_Result;");
    /* Prepared Statements */
    PREPARE Stmt_Check_Exists FROM @Session_Check_Exists_Sql;
    EXECUTE Stmt_Check_Exists;
    DEALLOCATE PREPARE Stmt_Check_Exists;

    /* **************************************** */

    /*
     * 条件判断。
     * 如果要插入的记录行存在 : 先删除再插入。
     * 如果要插入的记录行不存在 : 直接插入记录。
     */
    IF @Session_Check_Exists_Result = 1 THEN
        SET @Session_Delete_and_Insert_Sql =
            CONCAT("DELETE FROM ",In_Table_Name," WHERE ",In_Index_Field_Name," = ",In_Index_Value,";",
                   "INSERT INTO ",In_Table_Name,"(",In_Index_Field_Name,", ",In_Double_Field_Name,") VALUES (",In_Index_Value,", ",In_Double_Value,");");
        /* Prepared Statements */
        PREPARE Stmt_Delete_and_Insert FROM @Session_Delete_and_Insert_Sql;
        EXECUTE Stmt_Delete_and_Insert;
        DEALLOCATE PREPARE Stmt_Delete_and_Insert;
    
    ELSE
        SET @Session_Insert_Sql =
            CONCAT("INSERT INTO ",In_Table_Name,"(",In_Index_Field_Name,", ",In_Double_Field_Name,") VALUES (",In_Index_Value,", ",In_Double_Value,");");
        /* Prepared Statements */
        PREPARE Stmt_Insert FROM @Session_Insert_Sql;
        EXECUTE Stmt_Insert;
        DEALLOCATE PREPARE Stmt_Insert;
    END IF;
    
END//

-- 改回默认结束符。
DELIMITER ;

/* -------------------------------------------------- */
/* EOF */
