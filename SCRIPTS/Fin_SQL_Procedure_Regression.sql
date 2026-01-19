-- Fin_SQL_Procedure_Regression.sql

-- Create By GF 2023-10-10 22:43

/* -------------------------------------------------- */

/*
 * #######################################################################################
 * ##                                                                                   ##
 * ## Due to configuration reasons, MySQL does not distinguish between Upper and Lower. ##
 * ##                                                                                   ##
 * ## Beware of the parameter names of functions being the same as table field names.   ##
 * ##                                                                                   ##
 * #######################################################################################
 */

/* -------------------------------------------------- */

/*
 * Requirement : Fin_SQL_Custom_Function_Mathematics.sql
 * Requirement : Fin_SQL_Procedure_Container.sql
 */

/* -------------------------------------------------- */

/* Drop Table: Staging (Temporarily Storing Mathematics Data for Calculation) */
DROP TABLE IF EXISTS staging_slrg;

/* Create Table: Staging (Temporarily Storing Mathematics Data for Calculation) */
CREATE TABLE IF NOT EXISTS staging_slrg(st_index BIGINT(12) AUTO_INCREMENT PRIMARY KEY,
                                        st_feature_bigint BIGINT(12),
                                        st_feature_double DOUBLE(36,12),
                                        st_slrg_x DOUBLE(36,12),
                                        st_slrg_y DOUBLE(36,12),
                                        st_slrg_fitting_y DOUBLE(36,12),
                                        st_slrg_predict_y DOUBLE(36,12),
                                        st_slrg_train_x DOUBLE(36,12),
                                        st_slrg_train_y DOUBLE(36,12));

/* -------------------------------------------------- */

/* 结束符修改 */
DELIMITER //

/* -------------------------------------------------- */
/* Simple Linear Regression Procedure */

/* 删除存储过程: 简单线性回归 - 拷贝XY (Simple Linear Regression - Copy X and Y) */
DROP PROCEDURE IF EXISTS PROC_SLRG_COPY_XY//

/* 创建存储过程: 简单线性回归 - 拷贝XY (Simple Linear Regression - Copy X and Y) */
CREATE PROCEDURE PROC_SLRG_COPY_XY(IN In_Table_Name VARCHAR(80),
                                   IN In_Index_Field_Name VARCHAR(80),
                                   IN In_X_Field_Name VARCHAR(80),
                                   IN In_Y_Field_Name VARCHAR(80))
BEGIN

    UPDATE staging_slrg SET st_slrg_x = NULL;
    UPDATE staging_slrg SET st_slrg_y = NULL;

    /* **************************************** */

    /*
     * Prepare SQL Syntax : Simple Linear Regression Copy X Field.
     *
     * INSERT INTO staging_slrg(st_index, st_slrg_x) (SELECT Index_Field_Name, X_Field_Name FROM Table_Name) ON DUPLICATE KEY UPDATE st_slrg_x = X_Field_Name;
     */
    SET @Session_Copy_X_Field = CONCAT(
        "INSERT INTO staging_slrg(st_index, st_slrg_x) (SELECT ",In_Index_Field_Name,", ",In_X_Field_Name," FROM ",In_Table_Name,") ON DUPLICATE KEY UPDATE st_slrg_x = ",In_X_Field_Name,";");
    /* Prepared Statements */
    PREPARE Stmt_Copy_X_Field FROM @Session_Copy_X_Field;
    EXECUTE Stmt_Copy_X_Field;
    DEALLOCATE PREPARE Stmt_Copy_X_Field;

    /* **************************************** */

    /*
     * Prepare SQL Syntax : Simple Linear Regression Copy Y Field.
     *
     * INSERT INTO staging_slrg(st_index, st_slrg_y) (SELECT Index_Field_Name, Y_Field_Name FROM Table_Name) ON DUPLICATE KEY UPDATE st_slrg_y = Y_Field_Name;
     */
    SET @Session_Copy_Y_Field = CONCAT(
        "INSERT INTO staging_slrg(st_index, st_slrg_y) (SELECT ",In_Index_Field_Name,", ",In_Y_Field_Name," FROM ",In_Table_Name,") ON DUPLICATE KEY UPDATE st_slrg_y = ",In_Y_Field_Name,";");
    /* Prepared Statements */
    PREPARE Stmt_Copy_Y_Field FROM @Session_Copy_Y_Field;
    EXECUTE Stmt_Copy_Y_Field;
    DEALLOCATE PREPARE Stmt_Copy_Y_Field;
    
END//

/* 删除存储过程: 简单线性回归 - 生成特征 - 整数 (Simple Linear Regression - Generate Feature - Integer) */
DROP PROCEDURE IF EXISTS PROC_SLRG_GENERATE_FEATURE_INT//

/* 创建存储过程: 简单线性回归 - 生成特征 - 整数 (Simple Linear Regression - Generate Feature - Integer) */
CREATE PROCEDURE PROC_SLRG_GENERATE_FEATURE_INT(IN In_Table_Name VARCHAR(80))
BEGIN

    UPDATE staging_slrg SET st_feature_bigint = NULL;

    /* **************************************** */

    /*
     * Prepare SQL Syntax : Simple Linear Regression Generate Feature.
     *
     * INSERT INTO staging_slrg(st_index, st_feature_bigint)
     *     (SELECT _index, _Feature FROM (SELECT _index, CONV(CONCAT(str1, str2, ...), 2, 10) as _Feature FROM Table_Name) as _Temp)
     *         ON DUPLICATE KEY UPDATE st_feature_bigint = _Feature;
     */
    SET @Session_Generate_Feature_Sql = CONCAT(
        "INSERT INTO
             staging_slrg(st_index, st_feature_bigint)
         (SELECT
              _index,
              _Feature
          FROM
          ( /* Drive_1 : Generate Feature */
          SELECT
              _index,
              CONV(CONCAT(SMA5_CU_SMA10, SMA5_CU_SMA20, SMA10_CU_SMA20,
                          SMA5_CD_SMA10, SMA5_CD_SMA20, SMA10_CD_SMA20,
                          SMA5_A_SMA10, SMA5_A_SMA20, SMA10_A_SMA20,
                          SMA5_B_SMA10, SMA5_B_SMA20, SMA10_B_SMA20,
                          
                          MACD_DIF_CU_DEA, MACD_DIF_CD_DEA,
                          MACD_DIF_A_DEA, MACD_DIF_B_DEA,
                          MACD_DIF_A_0, MACD_DEA_A_0,
                          MACD_DIF_B_0, MACD_DEA_B_0,
                          
                          RSI1_CU_RSI2, RSI1_CD_RSI2,
                          RSI1_A_RSI2, RSI1_B_RSI2,
                          RSI1_A_50, RSI2_A_50, RSI1_B_50, RSI2_B_50,
                          RSI1_A_70, RSI2_A_70, RSI1_B_70, RSI2_B_70,
                          RSI1_A_30, RSI2_A_30, RSI1_B_30, RSI2_B_30), 2, 10) as _Feature
          FROM
              ",In_Table_Name,"
          ) as Drive_1
          ) ON DUPLICATE KEY UPDATE st_feature_bigint = _Feature;");
    /* Prepared Statements */
    PREPARE Stmt_Generate_Feature FROM @Session_Generate_Feature_Sql;
    EXECUTE Stmt_Generate_Feature;
    DEALLOCATE PREPARE Stmt_Generate_Feature;
    
END//

/* 删除存储过程: 简单线性回归 - X或Y的行数 (Simple Linear Regression - The Number of Rows for X or Y) */
DROP PROCEDURE IF EXISTS PROC_SLRG_NUM_OF_ROWS_X_OR_Y//

/* 创建存储过程: 简单线性回归 - X或Y的行数 (Simple Linear Regression - The Number of Rows for X or Y) */
CREATE PROCEDURE PROC_SLRG_NUM_OF_ROWS_X_OR_Y(IN In_Table_Name VARCHAR(80),
                                              IN In_X_Or_Y_Field_Name VARCHAR(80),
                                              OUT Out_Result DOUBLE(36,12))
BEGIN

    /* Calculation Example :
     *
     * Row 1 : [X(1) or Y(1)] {+1}
     * Row 2 : [X(2) or Y(2)] {+1}
     * Row 3 : [X(3) or Y(3)] {+1}
     * ...
     * Row N : [X(N) or Y(N)] {+1}
     *
     * The Number of Rows for X or Y = 1 + 1 + 1 + ... + 1
     *                                {-------- N --------}
     */

    /* **************************************** */

    /* Prepare SQL Syntax : Calculate The Number of Rows for X or Y
     *
     * SELECT COUNT(In_X_Or_Y_Field) INTO @Session_Result FROM In_Table_Name;
     */
    SET @Session_Calculate_Num_Of_Rows_X_Or_Y = CONCAT("SELECT COUNT(",In_X_Or_Y_Field_Name,") INTO @Session_Result FROM ",In_Table_Name,";");
    
    /* Prepared Statements */
    PREPARE Stmt FROM @Session_Calculate_Num_Of_Rows_X_Or_Y;
    EXECUTE Stmt;
    DEALLOCATE PREPARE Stmt;

    /* **************************************** */
    
    /* Outgoing Value */
    SET Out_Result = @Session_Result;
    
END//

/* 删除存储过程: 简单线性回归 - 所有X的和 (Simple Linear Regression - The Sum of All X) */
DROP PROCEDURE IF EXISTS PROC_SLRG_SUM_ALL_X//

/* 创建存储过程: 简单线性回归 - 所有X的和 (Simple Linear Regression - The Sum of All X) */
CREATE PROCEDURE PROC_SLRG_SUM_ALL_X(IN In_Table_Name VARCHAR(80),
                                     IN In_X_Field_Name VARCHAR(80),
                                     OUT Out_Result DOUBLE(36,12))
BEGIN

    /* Calculation Example :
     *
     * Row 1 : X(1)
     * Row 2 : X(2)
     * Row 3 : X(3)
     * ...
     * Row N : X(N)
     *
     * The Sum of All X = X(1) + X(2) + X(3) + ... + X(N)
     */

    /* **************************************** */

    /* Prepare SQL Syntax : Calculate The Sum of All X
     *
     * SELECT SUM(In_X_Field_Name) INTO @Session_Result FROM In_Table_Name;
     */
    SET @Session_Calculate_Sum_All_X = CONCAT("SELECT SUM(",In_X_Field_Name,") INTO @Session_Result FROM ",In_Table_Name,";");
    
    /* Prepared Statements */
    PREPARE Stmt FROM @Session_Calculate_Sum_All_X;
    EXECUTE Stmt;
    DEALLOCATE PREPARE Stmt;

    /* **************************************** */
    
    /* Outgoing Value */
    SET Out_Result = @Session_Result;
    
END//

/* 删除存储过程: 简单线性回归 - 所有Y的和 (Simple Linear Regression - The Sum of All Y) */
DROP PROCEDURE IF EXISTS PROC_SLRG_SUM_ALL_Y//

/* 创建存储过程: 简单线性回归 - 所有Y的和 (Simple Linear Regression - The Sum of All Y) */
CREATE PROCEDURE PROC_SLRG_SUM_ALL_Y(IN In_Table_Name VARCHAR(80),
                                     IN In_Y_Field_Name VARCHAR(80),
                                     OUT Out_Result DOUBLE(36,12))
BEGIN

    /* Calculation Example :
     *
     * Row 1 : Y(1)
     * Row 2 : Y(2)
     * Row 3 : Y(3)
     * ...
     * Row N : Y(N)
     *
     * The Sum of All Y = Y(1) + Y(2) + Y(3) + ... + Y(N)
     */

    /* **************************************** */

    /* Prepare SQL Syntax : Calculate The Sum of All Y
     *
     * SELECT SUM(In_Y_Field_Name) INTO @Session_Result FROM In_Table_Name;
     */
    SET @Session_Calculate_Sum_All_Y = CONCAT("SELECT SUM(",In_Y_Field_Name,") INTO @Session_Result FROM ",In_Table_Name,";");
    
    /* Prepared Statements */
    PREPARE Stmt FROM @Session_Calculate_Sum_All_Y;
    EXECUTE Stmt;
    DEALLOCATE PREPARE Stmt;

    /* **************************************** */
    
    /* Outgoing Value */
    SET Out_Result = @Session_Result;
    
END//

/* 删除存储过程: 简单线性回归 - 所有X平方的和 (Simple Linear Regression - The Sum of All X Squares) */
DROP PROCEDURE IF EXISTS PROC_SLRG_SUM_ALL_X_SQUARE//

/* 创建存储过程: 简单线性回归 - 所有X平方的和 (Simple Linear Regression - The Sum of All X Squares) */
CREATE PROCEDURE PROC_SLRG_SUM_ALL_X_SQUARE(IN In_Table_Name VARCHAR(80),
                                            IN In_X_Field_Name VARCHAR(80),
                                            OUT Out_Result DOUBLE(36,12))
BEGIN

    /* Calculation Example :
     *
     * Row 1 : X_Sqr(1) = X(1) * X(1)
     * Row 2 : X_Sqr(2) = X(2) * X(2)
     * Row 3 : X_Sqr(3) = X(3) * X(3)
     * ...
     * Row N : X_Sqr(N) = X(N) * X(N)
     *
     * The Sum of All X Squares = X_Sqr(1) + X_Sqr(2) + X_Sqr(3) + ... + X_Sqr(N)
     */

    /* **************************************** */

    /* Prepare SQL Syntax : Calculate The Sum of All X Squares
     *
     * SELECT SUM(_X_Sqr) INTO @Session_Result FROM (SELECT (In_X_Field_Name * In_X_Field_Name) as _X_Sqr FROM In_Table_Name) as _Temp;
     */
    SET @Session_Calculate_Sum_All_X_Square =
        CONCAT("SELECT SUM(_X_Sqr) INTO @Session_Result FROM (SELECT (",In_X_Field_Name," * ",In_X_Field_Name,") as _X_Sqr FROM ",In_Table_Name,") as _Temp;");
    
    /* Prepared Statements */
    PREPARE Stmt FROM @Session_Calculate_Sum_All_X_Square;
    EXECUTE Stmt;
    DEALLOCATE PREPARE Stmt;

    /* **************************************** */
    
    /* Outgoing Value */
    SET Out_Result = @Session_Result;
    
END//

/* 删除存储过程: 简单线性回归 - 所有XY乘积的和 (Simple Linear Regression - The Sum of All XY Products) */
DROP PROCEDURE IF EXISTS PROC_SLRG_SUM_ALL_XY_PRODUCT//

/* 创建存储过程: 简单线性回归 - 所有XY乘积的和 (Simple Linear Regression - The Sum of All XY Products) */
CREATE PROCEDURE PROC_SLRG_SUM_ALL_XY_PRODUCT(IN In_Table_Name VARCHAR(80),
                                              IN In_X_Field_Name VARCHAR(80),
                                              IN In_Y_Field_Name VARCHAR(80),
                                              OUT Out_Result DOUBLE(36,12))
BEGIN

    /* Calculation Example :
     *
     * Row 1 : XY(1) = X(1) * Y(1)
     * Row 2 : XY(2) = X(2) * Y(2)
     * Row 3 : XY(3) = X(3) * Y(3)
     * ...
     * Row N : XY(N) = X(N) * Y(N)
     *
     * The Sum of All XY Products = XY(1) + XY(2) + XY(3) + ... + XY(N)
     */

    /* **************************************** */

    /* Prepare SQL Syntax : Calculate The Sum of All XY Products
     *
     * SELECT SUM(_XY) INTO @Session_Result FROM (SELECT (In_X_Field_Name * In_Y_Field_Name) as _XY FROM In_Table_Name) as _Temp;
     */
    SET @Session_Calculate_Sum_All_XY_Product =
        CONCAT("SELECT SUM(_XY) INTO @Session_Result FROM (SELECT (",In_X_Field_Name," * ",In_Y_Field_Name,") as _XY FROM ",In_Table_Name,") as _Temp;");
    
    /* Prepared Statements */
    PREPARE Stmt FROM @Session_Calculate_Sum_All_XY_Product;
    EXECUTE Stmt;
    DEALLOCATE PREPARE Stmt;

    /* **************************************** */
    
    /* Outgoing Value */
    SET Out_Result = @Session_Result;
    
END//

/* 删除存储过程: 简单线性回归 - 斜率 (Simple Linear Regression - Slope) */
DROP PROCEDURE IF EXISTS PROC_SLRG_SLOPE//

/* 创建存储过程: 简单线性回归 - 斜率 (Simple Linear Regression - Slope) */
CREATE PROCEDURE PROC_SLRG_SLOPE(IN In_Table_Name VARCHAR(80),
                                 IN In_X_Field_Name VARCHAR(80),
                                 IN In_Y_Field_Name VARCHAR(80),
                                 OUT Out_Result DOUBLE(36,12))
BEGIN

    /* Slope Calculation Example :
     *
     * ( n(∑xy)-(∑x)(∑y) ) / ( n(∑x²)-(∑x)² )
     *
     * Slope =
     *    [PROC_SLRG_NUM_OF_ROWS_X_OR_Y] * [PROC_SLRG_SUM_ALL_XY_PRODUCT] - [PROC_SLRG_SUM_ALL_X] * [PROC_SLRG_SUM_ALL_Y]
     *    ---------------------------------------------------------------------------------------------------------------
     *            [PROC_SLRG_NUM_OF_ROWS_X_OR_Y] * [PROC_SLRG_SUM_ALL_X_SQUARE] - POWER([PROC_SLRG_SUM_ALL_X], 2)
     */

    /* **************************************** */
    
    DECLARE Inner_Slrg_Num_Of_Rows_X_Or_Y DOUBLE(36,12);
    DECLARE Inner_Slrg_Sum_All_X DOUBLE(36,12);
    DECLARE Inner_Slrg_Sum_All_Y DOUBLE(36,12);
    DECLARE Inner_Slrg_Sum_All_X_Square DOUBLE(36,12);
    DECLARE Inner_Slrg_Sum_All_XY_Product DOUBLE(36,12);
    DECLARE Inner_Numerator DOUBLE(36,12); /* 分子(Numerator) */
    DECLARE Inner_Denominator DOUBLE(36,12); /* 分母(Denominator) */

    /* **************************************** */

    /* Calling Other Store Procedure */
    CALL PROC_SLRG_NUM_OF_ROWS_X_OR_Y(In_Table_Name, In_X_Field_Name, Inner_Slrg_Num_Of_Rows_X_Or_Y); /* Calculate Only The Number of Rows for X */
    CALL PROC_SLRG_SUM_ALL_X(In_Table_Name, In_X_Field_Name, Inner_Slrg_Sum_All_X);
    CALL PROC_SLRG_SUM_ALL_Y(In_Table_Name, In_Y_Field_Name, Inner_Slrg_Sum_All_Y);
    CALL PROC_SLRG_SUM_ALL_X_SQUARE(In_Table_Name, In_X_Field_Name, Inner_Slrg_Sum_All_X_Square);
    CALL PROC_SLRG_SUM_ALL_XY_PRODUCT(In_Table_Name, In_X_Field_Name, In_Y_Field_Name, Inner_Slrg_Sum_All_XY_Product);

    /* **************************************** */
    
    /* Calculation and Outgoing Value */
    SET Inner_Numerator = (Inner_Slrg_Num_Of_Rows_X_Or_Y * Inner_Slrg_Sum_All_XY_Product - Inner_Slrg_Sum_All_X * Inner_Slrg_Sum_All_Y);
    SET Inner_Denominator = (Inner_Slrg_Num_Of_Rows_X_Or_Y * Inner_Slrg_Sum_All_X_Square - POWER(Inner_Slrg_Sum_All_X, 2));
    SET Out_Result = (Inner_Numerator / Inner_Denominator);
    
END//

/* 删除存储过程: 简单线性回归 - 截距 (Simple Linear Regression - Intercept) */
DROP PROCEDURE IF EXISTS PROC_SLRG_INTERCEPT//

/* 创建存储过程: 简单线性回归 - 截距 (Simple Linear Regression - Intercept) */
CREATE PROCEDURE PROC_SLRG_INTERCEPT(IN In_Table_Name VARCHAR(80),
                                     IN In_X_Field_Name VARCHAR(80),
                                     IN In_Y_Field_Name VARCHAR(80),
                                     OUT Out_Result DOUBLE(36,12))
BEGIN

    /* Intercept Calculation Example :
     *
     * ( (∑y)(∑x²)-(∑x)(∑xy) ) / ( n(∑x²)-(∑x)² )
     *
     * Intercept =
     *    [PROC_SLRG_SUM_ALL_Y] * [PROC_SLRG_SUM_ALL_X_SQUARE] - [PROC_SLRG_SUM_ALL_X] * [PROC_SLRG_SUM_ALL_XY_PRODUCT]
     *    ---------------------------------------------------------------------------------------------------------------
     *            [PROC_SLRG_NUM_OF_ROWS_X_OR_Y] * [PROC_SLRG_SUM_ALL_X_SQUARE] - POWER([PROC_SLRG_SUM_ALL_X], 2)
     */

    /* **************************************** */
    
    DECLARE Inner_Slrg_Num_Of_Rows_X_Or_Y DOUBLE(36,12);
    DECLARE Inner_Slrg_Sum_All_X DOUBLE(36,12);
    DECLARE Inner_Slrg_Sum_All_Y DOUBLE(36,12);
    DECLARE Inner_Slrg_Sum_All_X_Square DOUBLE(36,12);
    DECLARE Inner_Slrg_Sum_All_XY_Product DOUBLE(36,12);
    DECLARE Inner_Numerator DOUBLE(36,12); /* 分子(Numerator) */
    DECLARE Inner_Denominator DOUBLE(36,12); /* 分母(Denominator) */

    /* **************************************** */

    /* Calling Other Store Procedure */
    CALL PROC_SLRG_NUM_OF_ROWS_X_OR_Y(In_Table_Name, In_X_Field_Name, Inner_Slrg_Num_Of_Rows_X_Or_Y); /* Calculate Only The Number of Rows for X */
    CALL PROC_SLRG_SUM_ALL_X(In_Table_Name, In_X_Field_Name, Inner_Slrg_Sum_All_X);
    CALL PROC_SLRG_SUM_ALL_Y(In_Table_Name, In_Y_Field_Name, Inner_Slrg_Sum_All_Y);
    CALL PROC_SLRG_SUM_ALL_X_SQUARE(In_Table_Name, In_X_Field_Name, Inner_Slrg_Sum_All_X_Square);
    CALL PROC_SLRG_SUM_ALL_XY_PRODUCT(In_Table_Name, In_X_Field_Name, In_Y_Field_Name, Inner_Slrg_Sum_All_XY_Product);

    /* **************************************** */
    
    /* Calculation and Outgoing Value */
    SET Inner_Numerator = (Inner_Slrg_Sum_All_Y * Inner_Slrg_Sum_All_X_Square - Inner_Slrg_Sum_All_X * Inner_Slrg_Sum_All_XY_Product);
    SET Inner_Denominator = (Inner_Slrg_Num_Of_Rows_X_Or_Y * Inner_Slrg_Sum_All_X_Square - POWER(Inner_Slrg_Sum_All_X, 2));
    SET Out_Result = (Inner_Numerator / Inner_Denominator);
    
END//

/* 删除存储过程: 简单线性回归 - 预测Y值 (Simple Linear Regression - Predict Y) */
DROP PROCEDURE IF EXISTS PROC_SLRG_PREDICT_Y//

/* 创建存储过程: 简单线性回归 - 预测Y值 (Simple Linear Regression - Predict Y) */
CREATE PROCEDURE PROC_SLRG_PREDICT_Y(IN In_Slope_Value DOUBLE(36,12),
                                     IN In_X_Value DOUBLE(36,12),
                                     IN In_Intercept_Value DOUBLE(36,12),
                                     OUT Out_Predict_Y_Result DOUBLE(36,12))
BEGIN

    /* Predict Y Calculation Example :
     *
     * 预测Y值(Predict) = 斜率(Slope) * 新的X值 + 截距(Intercept)
     *
     * The Predict Y = [In_Slope_Value] * [In_X_Value] + [In_Intercept_Value]
     */

    /* **************************************** */
    
    /* Calculation and Outgoing Value */
    SET Out_Predict_Y_Result = (In_Slope_Value * In_X_Value + In_Intercept_Value);
    
END//

/* 删除存储过程: 简单线性回归 - 拟合Y (Simple Linear Regression - Fitting Y) */
DROP PROCEDURE IF EXISTS PROC_SLRG_FITTING_Y//

/* 创建存储过程: 简单线性回归 - 拟合Y (Simple Linear Regression - Fitting Y) */
CREATE PROCEDURE PROC_SLRG_FITTING_Y(IN In_Table_Name VARCHAR(80),
                                     IN In_Index_Field_Name VARCHAR(80),
                                     IN In_X_Field_Name VARCHAR(80),
                                     IN In_Y_Field_Name VARCHAR(80))
BEGIN

    DECLARE Inner_SLRG_Slope DOUBLE(36,12);
    DECLARE Inner_SLRG_Intercept DOUBLE(36,12);

    /* **************************************** */

    /* Calling Other Store Procedure: Copy X and Y */
    CALL PROC_SLRG_COPY_XY(In_Table_Name, In_Index_Field_Name, In_X_Field_Name, In_Y_Field_Name);

    /* **************************************** */

    /* Calling Other Store Procedure: Calculate SLRG Slope & SLRG Intercept */
    CALL PROC_SLRG_SLOPE("staging_slrg", "st_slrg_x", "st_slrg_y", Inner_SLRG_Slope);
    CALL PROC_SLRG_INTERCEPT("staging_slrg", "st_slrg_x", "st_slrg_y", Inner_SLRG_Intercept);

    /* **************************************** */

    UPDATE staging_slrg SET st_slrg_fitting_y = FUNC_SLRG_PREDICT_Y(Inner_SLRG_Slope, st_slrg_x, Inner_SLRG_Intercept);

END//

/* 删除存储过程: 简单线性回归 - 交叉计算 (Simple Linear Regression - Cross Calculation) */
DROP PROCEDURE IF EXISTS PROC_SLRG_CROSS_CALCULATE//

/* 创建存储过程: 简单线性回归 - 交叉计算 (Simple Linear Regression - Cross Calculation) */
CREATE PROCEDURE PROC_SLRG_CROSS_CALCULATE(IN In_Table_Name VARCHAR(80),
                                           IN In_Index_Field_Name VARCHAR(80),
                                           IN In_X_Field_Name VARCHAR(80),
                                           IN In_Y_Field_Name VARCHAR(80),
                                           IN In_Num_of_Slice BIGINT(12))
BEGIN

    DECLARE Inner_Outer_Cycle BIGINT(12);
    DECLARE Inner_Inner_Cycle BIGINT(12);
    DECLARE Inner_Data_Slice_Bgn_Index BIGINT(12);
    DECLARE Inner_Data_Slice_End_Index BIGINT(12);
    DECLARE Inner_SLRG_Slope DOUBLE(36,12);
    DECLARE Inner_SLRG_Intercept DOUBLE(36,12);

    /* **************************************** */

    /* Calling Other Store Procedure: Date Index Slice & Copy X and Y */
    CALL PROC_CNTR_MATH_DATA_INDEX_SLICE(In_Table_Name, In_Num_of_Slice);
    CALL PROC_SLRG_COPY_XY(In_Table_Name, In_Index_Field_Name, In_X_Field_Name, In_Y_Field_Name);

    /* **************************************** */

    SET Inner_Outer_Cycle = 1;
    WHILE Inner_Outer_Cycle <= In_Num_of_Slice DO
        /* ---------- Inner Loop Bgn ---------- */
        SET Inner_Inner_Cycle = 1;
        WHILE Inner_Inner_Cycle <= In_Num_of_Slice DO
            IF Inner_Inner_Cycle <> Inner_Outer_Cycle THEN
                SET Inner_Data_Slice_Bgn_Index =
                    (SELECT cntr_bigint_value FROM container WHERE cntr_class = "Data_Slice_Bgn_Idx" AND cntr_name = In_Table_Name AND cntr_purpose = "Begin_Index" AND cntr_number = Inner_Inner_Cycle);
                SET Inner_Data_Slice_End_Index =
                    (SELECT cntr_bigint_value FROM container WHERE cntr_class = "Data_Slice_End_Idx" AND cntr_name = In_Table_Name AND cntr_purpose = "Ends_Index" AND cntr_number = Inner_Inner_Cycle);
                /* **************************** */
                /* Extract Training Data: SLRG X Field & SLRG Y Field */
                UPDATE staging_slrg SET st_slrg_train_x = st_slrg_x WHERE Inner_Data_Slice_Bgn_Index <= st_index AND st_index <= Inner_Data_Slice_End_Index;
                UPDATE staging_slrg SET st_slrg_train_y = st_slrg_y WHERE Inner_Data_Slice_Bgn_Index <= st_index AND st_index <= Inner_Data_Slice_End_Index;
            END IF;
            /* ******************************** */
            SET Inner_Inner_Cycle = (Inner_Inner_Cycle + 1);
        END WHILE;
        /* ---------- Inner Loop End ---------- */
        /* Calling Other Store Procedure: Calculate SLRG Slope & SLRG Intercept */
        CALL PROC_SLRG_SLOPE("staging_slrg", "st_slrg_train_x", "st_slrg_train_y", Inner_SLRG_Slope);
        CALL PROC_SLRG_INTERCEPT("staging_slrg", "st_slrg_train_x", "st_slrg_train_y", Inner_SLRG_Intercept);
        /* ************************************ */
        UPDATE staging_slrg SET st_slrg_train_x = NULL;
        UPDATE staging_slrg SET st_slrg_train_y = NULL;
        /* ************************************ */
        DELETE FROM container WHERE cntr_class = "SLRG_Slope" AND cntr_name = In_Table_Name AND cntr_number = Inner_Outer_Cycle;
        DELETE FROM container WHERE cntr_class = "SLRG_Intercept" AND cntr_name = In_Table_Name AND cntr_number = Inner_Outer_Cycle;
        /* ************************************ */
        INSERT INTO container(cntr_class, cntr_name, cntr_number, cntr_double_value) VALUES ("SLRG_Slope", In_Table_Name, Inner_Outer_Cycle, Inner_SLRG_Slope);
        INSERT INTO container(cntr_class, cntr_name, cntr_number, cntr_double_value) VALUES ("SLRG_Intercept", In_Table_Name, Inner_Outer_Cycle, Inner_SLRG_Intercept);
        /* ************************************ */
        SET Inner_Outer_Cycle = (Inner_Outer_Cycle + 1);
    END WHILE;
    
END//

/* 删除存储过程: 简单线性回归 - 交叉预测Y (Simple Linear Regression - Cross Predict Y) */
DROP PROCEDURE IF EXISTS PROC_SLRG_CROSS_PREDICT_Y//

/* 创建存储过程: 简单线性回归 - 交叉预测Y (Simple Linear Regression - Cross Predict Y) */
CREATE PROCEDURE PROC_SLRG_CROSS_PREDICT_Y(IN In_Table_Name VARCHAR(80),
                                           IN In_Index_Field_Name VARCHAR(80),
                                           IN In_X_Field_Name VARCHAR(80),
                                           IN In_Y_Field_Name VARCHAR(80),
                                           IN In_Num_of_Slice BIGINT(12))
BEGIN

    DECLARE Inner_Cycle BIGINT(12);
    DECLARE Inner_Data_Slice_Bgn_Index BIGINT(12);
    DECLARE Inner_Data_Slice_End_Index BIGINT(12);
    DECLARE Inner_SLRG_Slope DOUBLE(36,12);
    DECLARE Inner_SLRG_Intercept DOUBLE(36,12);

    /* **************************************** */

    /* Calling Other Store Procedure: SLRG Cross Calculate */
    CALL PROC_SLRG_CROSS_CALCULATE(In_Table_Name, In_Index_Field_Name, In_X_Field_Name, In_Y_Field_Name, In_Num_of_Slice);

    /* **************************************** */

    SET Inner_Cycle = 1;
    WHILE Inner_Cycle <= In_Num_of_Slice DO
        SET Inner_Data_Slice_Bgn_Index =
            (SELECT cntr_bigint_value FROM container WHERE cntr_class = "Data_Slice_Bgn_Idx" AND cntr_name = In_Table_Name AND cntr_purpose = "Begin_Index" AND cntr_number = Inner_Cycle);
        SET Inner_Data_Slice_End_Index =
            (SELECT cntr_bigint_value FROM container WHERE cntr_class = "Data_Slice_End_Idx" AND cntr_name = In_Table_Name AND cntr_purpose = "Ends_Index" AND cntr_number = Inner_Cycle);
        SET Inner_SLRG_Slope =
            (SELECT cntr_double_value FROM container WHERE cntr_class = "SLRG_Slope" AND cntr_name = In_Table_Name AND cntr_number = Inner_Cycle);
        SET Inner_SLRG_Intercept =
            (SELECT cntr_double_value FROM container WHERE cntr_class = "SLRG_Intercept" AND cntr_name = In_Table_Name AND cntr_number = Inner_Cycle);
        /* ************************************ */
        UPDATE staging_slrg SET st_slrg_predict_y =
            FUNC_SLRG_PREDICT_Y(Inner_SLRG_Slope, st_slrg_x, Inner_SLRG_Intercept) WHERE Inner_Data_Slice_Bgn_Index <= st_index AND st_index <= Inner_Data_Slice_End_Index;
        /* ************************************ */
        SET Inner_Cycle = (Inner_Cycle + 1);
    END WHILE;

END//

/* 删除存储过程: 简单线性回归 - 交叉验证 (Simple Linear Regression - Cross Validation) */
DROP PROCEDURE IF EXISTS PROC_SLRG_CROSS_VALIDATE//

/* 创建存储过程: 简单线性回归 - 交叉验证 (Simple Linear Regression - Cross Validation) */
CREATE PROCEDURE PROC_SLRG_CROSS_VALIDATE(IN In_Table_Name VARCHAR(80),
                                          IN In_Index_Field_Name VARCHAR(80),
                                          IN In_X_Field_Name VARCHAR(80),
                                          IN In_Y_Field_Name VARCHAR(80),
                                          IN In_Num_of_Slice BIGINT(12))
BEGIN

    DECLARE Inner_Cycle BIGINT(12);
    DECLARE Inner_Data_Slice_Bgn_Index BIGINT(12);
    DECLARE Inner_Data_Slice_End_Index BIGINT(12);
    DECLARE Inner_SLRG_Est_Accuracy_Sum DOUBLE(36,12);
    DECLARE Inner_SLRG_Est_Accuracy_Rate DOUBLE(36,12);

    /* **************************************** */

    DELETE FROM container WHERE cntr_class = "SLRG_Accuracy" AND cntr_name = In_Table_Name;

    /* **************************************** */

    /* Calling Other Store Procedure: SLRG Cross Predict Y */
    CALL PROC_SLRG_CROSS_PREDICT_Y(In_Table_Name, In_Index_Field_Name, In_X_Field_Name, In_Y_Field_Name, In_Num_of_Slice);

    /* **************************************** */

    SET Inner_Cycle = 1;
    WHILE Inner_Cycle <= In_Num_of_Slice DO
        SET Inner_Data_Slice_Bgn_Index =
            (SELECT cntr_bigint_value FROM container WHERE cntr_class = "Data_Slice_Bgn_Idx" AND cntr_name = In_Table_Name AND cntr_purpose = "Begin_Index" AND cntr_number = Inner_Cycle);
        SET Inner_Data_Slice_End_Index =
            (SELECT cntr_bigint_value FROM container WHERE cntr_class = "Data_Slice_End_Idx" AND cntr_name = In_Table_Name AND cntr_purpose = "Ends_Index" AND cntr_number = Inner_Cycle);
        /* ************************************ */
        SET Inner_SLRG_Est_Accuracy_Sum =
            (SELECT SUM(FUNC_SLRG_EST_ACCURACY(st_slrg_y, st_slrg_predict_y, 0.05)) FROM staging_slrg WHERE Inner_Data_Slice_Bgn_Index <= st_index AND st_index <= Inner_Data_Slice_End_Index);
        /* ************************************ */
        SET Inner_SLRG_Est_Accuracy_Rate = (Inner_SLRG_Est_Accuracy_Sum / (Inner_Data_Slice_End_Index - Inner_Data_Slice_Bgn_Index + 1));
        /* ************************************ */
        INSERT INTO container(cntr_class, cntr_name, cntr_number, cntr_double_value) VALUES ("SLRG_Accuracy", In_Table_Name, Inner_Cycle, Inner_SLRG_Est_Accuracy_Rate);
        /* ************************************ */
        SET Inner_Cycle = (Inner_Cycle + 1);
    END WHILE;

END//

/* 改回默认结束符 */
DELIMITER ;

/* -------------------------------------------------- */
/* EOF */
