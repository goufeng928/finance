/* Fin_SQL_Custom_Function_Mathematics.sql */

/* Create By GF 2023-09-21 19:46 */

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

/* Drop Table: Staging (Temporarily Storing Mathematics Data for Calculation) */
DROP TABLE IF EXISTS staging_math;

/* Create Table: Staging (Temporarily Storing Mathematics Data for Calculation) */
CREATE TABLE IF NOT EXISTS staging_math(st_index BIGINT(12) AUTO_INCREMENT PRIMARY KEY,
                                        st_base_acc_avg DOUBLE(16,4), /* Base Value of Accumulate Average */
                                        st_base_mov_sum_offset DOUBLE(16,4), /* Base Value of Moving Sum - Offset */
                                        st_base_mov_var DOUBLE(16,4), /* Base Value of Moving Variance */
                                        st_base_mov_cov_x DOUBLE(16,4), /* Base Value of Moving X of Covariance */
                                        st_base_mov_cov_y DOUBLE(16,4)); /* Base Value of Moving Y of Covariance */

/* -------------------------------------------------- */
/* ERROR 1418 (HY000): This function has none of DETERMINISTIC, NO SQL, or READS SQL DATA in its declaration and binary logging is enabled
 *                     (you might want to use the less safe log_bin_trust_function_creators variable)
 */

/* SET GLOBAL log_bin_trust_function_creators=TRUE; */

/* -------------------------------------------------- */

/* 修改语句结束符为 "//" */
DELIMITER //

/* -------------------------------------------------- */
/* Math Function */

/* 删除函数: 累计平均 (Math - Accumulate Average) */
DROP FUNCTION IF EXISTS FUNC_MATH_ACC_AVG//

/* 创建函数: 累计平均 (Math - Accumulate Average) */
CREATE FUNCTION FUNC_MATH_ACC_AVG(In_Index INT(8), In_Value DOUBLE(16,4)) RETURNS DOUBLE(16,4)
BEGIN

    /*
     * 累计平均。
     * 又叫累加平均, 当连续不断地得到测定值 X1, X2, ... 时, 则 (X1 + X2) / 2, (X1 + X2 + X3) / 3, ... 等。
     * 分别称为第一次, 第二次, 第三次, ... 的累计平均数。
     */
    
    /* **************************************** */

    DECLARE Out_ACC_Avg_Result DOUBLE(16,4) DEFAULT 0.0; /* Declare Local Variable: Return Value */
    
    /* **************************************** */

    INSERT INTO staging_math(st_index, st_base_acc_avg)
        VALUES (In_Index, In_Value) ON DUPLICATE KEY UPDATE st_base_acc_avg = In_Value;

    /* **************************************** */

    SET Out_ACC_Avg_Result =
        (SELECT AVG(st_base_acc_avg) FROM staging_math WHERE st_index <= In_Index);

    /* **************************************** */

    RETURN Out_ACC_Avg_Result; /* Return Value */
    
END//

/* 删除函数: 移动合计 - 带偏移量 (Math - Moving Sum - Offset) */
DROP FUNCTION IF EXISTS FUNC_MATH_MOV_SUM_OFFSET//

/* 创建函数: 移动合计 - 带偏移量 (Math - Moving Sum - Offset) */
CREATE FUNCTION FUNC_MATH_MOV_SUM_OFFSET(In_Index INT(8), In_Sample_Size INT(4), In_Offset INT(2), In_Value DOUBLE(16,4)) RETURNS DOUBLE(16,4)
BEGIN

    DECLARE Inner_Bgn_Qry_Idx INT(8); /* Declare Local Variable: Begin Index */
    DECLARE Inner_End_Qry_Idx INT(8); /* Declare Local Variable: Ends Index */
    DECLARE Out_Mov_Sum_offset_Result DOUBLE(16,4) DEFAULT 0.0; /* Declare Local Variable: Return Value */

    /* **************************************** */

    INSERT INTO staging_math(st_index, st_base_mov_sum_offset)
        VALUES(In_Index, In_Value) ON DUPLICATE KEY UPDATE st_base_mov_sum_offset = In_Value;

    /* **************************************** */

    /* 查询的起始索引(Begin Index) = 当前索引(In Index) - 偏移量(In Offset) - 样本量(In Sample Size) + 1 */
    SET Inner_Bgn_Qry_Idx = (In_Index - In_Offset - In_Sample_Size + 1);
    /* 查询的截止索引(Ends Index) = 当前索引(In Index) - 偏移量(In Offset) */
    SET Inner_End_Qry_Idx = (In_Index - In_Offset);

    /* **************************************** */

    /* 查询合计起始索引(Begin Index)和截止索引(Ends Index)之间的所有值 */
    IF In_Index >= (In_Sample_Size + In_Offset) THEN
        SET Out_Mov_Sum_offset_Result =
            (SELECT SUM(st_base_mov_sum_offset) FROM staging_math WHERE Inner_Bgn_Qry_Idx <= st_index AND st_index <= Inner_End_Qry_Idx);
        /* ************************************ */
        RETURN Out_Mov_Sum_offset_Result; /* Return Value */
    ELSE
        RETURN NULL; /* Return Value */
    END IF;
    
END//

/* 删除函数: 移动方差 (Math - Moving Variance) */
DROP FUNCTION IF EXISTS FUNC_MATH_MOV_VAR//

/* 创建函数: 移动方差 (Math - Moving Variance) */
CREATE FUNCTION FUNC_MATH_MOV_VAR(In_Index INT(8), In_Sample_Size INT(4), In_Value DOUBLE(16,4)) RETURNS DOUBLE(16,4)
BEGIN

    /*
     * 在概率分布中, 数学期望值和方差或标准差是一种分布的重要特征.
     *
     * 样本方差:
     * 也叫无偏估计, 无偏方差(Unbiased Variance), 对于一组随机变量, 从中随机抽取N个样本的方差.
     * 这组样本的方差就是[(X1 - X均值)的平方 + (X2 - X均值)的平方 + (X3 - X均值)的平方 + ... + (Xn - X均值)的平方]除以(n - 1).
     *
     * 总体方差:
     * 也叫做有偏估计, 其实就是初高中就学到的那个标准定义的方差.
     * 总体方差就是[(X1 - X均值)的平方 + (X2 - X均值)的平方 + (X3 - X均值)的平方 + ... + (Xn - X均值)的平方]除以n.
     *
     * 一般在实际应用中使用的都是样本方差.
     */

    /* **************************************** */

    /* 声明局部变量 : 循环计数(Cycles Count) */
    DECLARE Inner_Cyc_Cnt INT(8) DEFAULT 0;
    /* 声明局部变量 : 查询的起始索引(Begin Index) */
    DECLARE Inner_Bgn_Qry_Idx INT(8) DEFAULT 0;
    /* 声明局部变量 : 查询的截止索引(End Index) */
    DECLARE Inner_End_Qry_Idx INT(8) DEFAULT 0;
    /* 声明局部变量 : 移动方差基数值 */
    DECLARE Inner_Mov_Var_Base DOUBLE(16,4) DEFAULT 0.0;
    /* 声明局部变量 : 移动方差(中间Step)均值 */
    DECLARE Inner_Mov_Var_Avg DOUBLE(16,4) DEFAULT 0.0;
    /* 声明局部变量 : 移动方差(中间Step)归一化值的平方的和 */
    DECLARE Inner_Mov_Var_Normalized_Square_Sum DOUBLE(16,4) DEFAULT 0.0;
    /* 声明传出变量 : 要返回的值 */
    DECLARE Out_Mov_Var_Result DOUBLE(16,4) DEFAULT 0.0;
    
    /* **************************************** */
    
    /* 将传入基数值插入到容器(Container_Math) */
    INSERT INTO staging_math(_index, st_base_mov_var)
        VALUES (In_Index, In_Value) ON DUPLICATE KEY UPDATE st_base_mov_var = In_Value;
        
    /* **************************************** */
    
    IF In_Index < In_Sample_Size THEN
        /* 返回值 */
        RETURN NULL;

    /* 计算移动方差 */
    ELSEIF In_Index >= In_Sample_Size THEN
        /* 计算起始索引(Begin Index) */
        SET Inner_Bgn_Qry_Idx = In_Index - In_Sample_Size + 1;
        /* 计算截止索引(End Index) */
        SET Inner_End_Qry_Idx = In_Index;
        /* 设定循环起始值 */
        SET Inner_Cyc_Cnt = 0;
        WHILE Inner_Cyc_Cnt < In_Sample_Size DO
            /* 从容器(Container_Math)查询截止当前索引临时存放的基数值 */
            SET Inner_Mov_Var_Base =
                (SELECT st_base_mov_var FROM staging_math WHERE _index = (Inner_Bgn_Qry_Idx + Inner_Cyc_Cnt));
            /* 从容器(Container_Math)查询截止当前索引临时存放的基数值, 计算平均值 */
            SET Inner_Mov_Var_Avg =
                (SELECT AVG(st_base_mov_var) FROM staging_math WHERE Inner_Bgn_Qry_Idx <= _index AND _index <= Inner_End_Qry_Idx);
            /* 累加移动方差(中间Step)归一化值的平方的和 */
            SET Inner_Mov_Var_Normalized_Square_Sum = 
                (Inner_Mov_Var_Normalized_Square_Sum + POW((Inner_Mov_Var_Base - Inner_Mov_Var_Avg), 2));
            /* 循环次数 +1 */
            SET Inner_Cyc_Cnt = Inner_Cyc_Cnt + 1;
        END WHILE;
        /* 计算移动N日方差的值 */
        SET Out_Mov_Var_Result = Inner_Mov_Var_Normalized_Square_Sum / (In_Sample_Size - 1);
        /* 返回值 */
        RETURN Out_Mov_Var_Result;
    
    ELSE
        /* 返回值 */
        RETURN NULL;
    
    END IF;

END//

/* 删除函数: 移动协方差 (Math - Moving Covariance) */
DROP FUNCTION IF EXISTS FUNC_MATH_MOV_COV//

/* 创建函数: 移动协方差 (Math - Moving Covariance) */
CREATE FUNCTION FUNC_MATH_MOV_COV(In_Index INT(8), In_Sample_Size INT(4), In_X_Value DOUBLE(16,4), In_Y_Value DOUBLE(16,4)) RETURNS DOUBLE(16,4)
BEGIN

    /*
     * 协方差:
     * 方差是协方差的一种特殊情况, 即当两个变量是相同的情况.
     * 协方差表示的是两个变量的总体的误差, 这与只表示一个变量误差的方差不同.
     * 如果两个变量的变化趋势一致, 如果其中一个大于自身的期望值, 另外一个也大于自身的期望值, 那么两个变量之间的协方差就是正值.
     * 如果两个变量的变化趋势相反, 如果其中一个大于自身的期望值, 另外一个却小于自身的期望值, 那么两个变量之间的协方差就是负值.
     *
     * 期望值:
     * 在统计学中, 想要估算变量的期望值时, 经常用到的方法是重复测量此变量的值, 然后用所得数据的平均值来作为此变量的期望值的估计.
     *
     * 协方差中, 方差的公式为: Cov(X, X) = E{[X - E(X)][X - E(X)]}
     * 协方差中, 协方差的公式为: Cov(X, Y) = E{[X - E(X)][Y - E(Y)]}
     */

    /* **************************************** */

    DECLARE Inner_Cyc_Cnt INT(8); /* Declare Local Variable: Cycles Count */
    DECLARE Inner_Bgn_Qry_Idx INT(8) DEFAULT 0; /* Declare Local Variable: Begin Query Index */
    DECLARE Inner_End_Qry_Idx INT(8) DEFAULT 0; /* Declare Local Variable: Ends Query Index */
    DECLARE Inner_Mov_Cov_X_Base DOUBLE(16,4); /* Declare Local Variable: X基数值 */
    DECLARE Inner_Mov_Cov_Y_Base DOUBLE(16,4); /* Declare Local Variable: Y基数值 */
    DECLARE Inner_Mov_Cov_X_Avg DOUBLE(16,4); /* Declare Local Variable: X均值 */
    DECLARE Inner_Mov_Cov_Y_Avg DOUBLE(16,4); /* Declare Local Variable: Y均值 */
    DECLARE Inner_Mov_Cov_Normalized_Product_Sum DOUBLE(16,4); /* Declare Local Variable: 归一化值的平方的和 */
    DECLARE Out_Mov_Cov_Result DOUBLE(16,4) DEFAULT 0.0; /* Declare Local Variable: Return Value */
    
    /* **************************************** */
    
    /* 拷贝将传入X/Y基数值的副本 */
    INSERT INTO staging_math(_index, st_base_mov_cov_x)
        VALUES (In_Index, In_X_Value) ON DUPLICATE KEY UPDATE st_base_mov_cov_x = In_X_Value;
    INSERT INTO staging_math(_index, st_base_mov_cov_y)
        VALUES (In_Index, In_Y_Value) ON DUPLICATE KEY UPDATE st_base_mov_cov_y = In_Y_Value;
        
    /* **************************************** */
    
    IF In_Index < In_Sample_Size THEN
        RETURN NULL; /* Return Value */
    ELSEIF In_Index >= In_Sample_Size THEN
        SET Inner_Bgn_Qry_Idx = In_Index - In_Sample_Size + 1; /* 计算起始索引(Begin Index) */
        SET Inner_End_Qry_Idx = In_Index; /* 计算截止索引(Ends Index) */
        /* ************************************ */
        SET Inner_Cyc_Cnt = 0;
        WHILE Inner_Cyc_Cnt < In_Sample_Size DO
            SET Inner_Mov_Cov_X_Base = /* 查询提取当前索引临时存放的X基数值 */
                (SELECT st_base_mov_cov_x FROM staging_math WHERE _index = (Inner_Bgn_Qry_Idx + Inner_Cyc_Cnt));
            SET Inner_Mov_Cov_Y_Base = /* 查询提取当前索引临时存放的Y基数值 */
                (SELECT st_base_mov_cov_y FROM staging_math WHERE _index = (Inner_Bgn_Qry_Idx + Inner_Cyc_Cnt));
            /* ******************************** */
            SET Inner_Mov_Cov_X_Avg = /* 查询提取截至当前索引临时存放的X基数值的平均值 */
                (SELECT AVG(st_base_mov_cov_x) FROM staging_math WHERE Inner_Bgn_Qry_Idx <= _index AND _index <= Inner_End_Qry_Idx);
            SET Inner_Mov_Cov_Y_Avg = /* 查询提取截至当前索引临时存放的Y基数值的平均值 */
                (SELECT AVG(st_base_mov_cov_y) FROM staging_math WHERE Inner_Bgn_Qry_Idx <= _index AND _index <= Inner_End_Qry_Idx);
            /* ******************************** */
            SET Inner_Mov_Cov_Normalized_Product_Sum = /* 累加移动协方差(中间Step)归一化值的平方的和 */
                (Inner_Mov_Cov_Normalized_Product_Sum + (Inner_Mov_Cov_X_Base - Inner_Mov_Cov_X_Avg) * (Inner_Mov_Cov_Y_Base - Inner_Mov_Cov_Y_Avg));
            /* ******************************** */
            SET Inner_Cyc_Cnt = Inner_Cyc_Cnt + 1; /* 循环次数 +1 */
        END WHILE;
        /* ************************************ */
        SET Out_Mov_Cov_Result = Inner_Mov_Cov_Normalized_Product_Sum / (In_Sample_Size - 1); /* 计算移动N日方差的值 */
        /* ************************************ */
        RETURN Out_Mov_Var_Result; /* Return Value */
    ELSE
        RETURN NULL; /* Return Value */
    END IF;
    
END//

/* -------------------------------------------------- */
/* Simple Linear Regression Function */

/* 删除函数: 简单线性回归 - 预测Y值 (Simple Linear Regression - Predict Y) */
DROP FUNCTION IF EXISTS FUNC_SLRG_PREDICT_Y//

/* 创建函数: 简单线性回归 - 预测Y值 (Simple Linear Regression - Predict Y) */
CREATE FUNCTION FUNC_SLRG_PREDICT_Y(In_Slope_Value DOUBLE(36,12), In_X_Value DOUBLE(36,12), In_Intercept_Value DOUBLE(36,12)) RETURNS DOUBLE(36,12)
BEGIN

    /* Predict Y Calculation Example :
     *
     * 预测Y值(Predict) = 斜率(Slope) * 新的X值 + 截距(Intercept)
     *
     * The Predict Y = [Slope_Value] * [X_Value] + [Intercept_Value]
     */
    
    /* **************************************** */

    DECLARE Out_Predict_Y_Result DOUBLE(36,12) DEFAULT 0.0; /* Declare Local Variable: Return Value */
    
    /* **************************************** */

    SET Out_Predict_Y_Result = (In_Slope_Value * In_X_Value + In_Intercept_Value);

    /* **************************************** */

    RETURN Out_Predict_Y_Result; /* Return Value */
    
END//

/* 删除函数: 简单线性回归 - 评估准确性 (Simple Linear Regression - Estimate Accuracy) */
DROP FUNCTION IF EXISTS FUNC_SLRG_EST_ACCURACY//

/* 创建函数: 简单线性回归 - 评估准确性 (Simple Linear Regression - Estimate Accuracy) */
CREATE FUNCTION FUNC_SLRG_EST_ACCURACY(In_Actual_Y_Value DOUBLE(36,12), In_Predicted_Y_Value DOUBLE(36,12), In_Tolerance DOUBLE(36,12)) RETURNS INT(1)
BEGIN

    /*
     * Difference Calculate Examples:
     *
     * [Difference] = [Predicted_Y] - [Actual_Y]
     *
     * 求出差值的绝对值(去掉负号):
     *
     * 求平方(Square) : [Difference_Sq] = POWER([Difference], 2)
     * 求平方根(Square Root) : [Difference_Sqr] = SQRT([Difference_Sq])
     *
     * 判断差值的绝对值是否在误差范围内:
     *
     * IF [Difference_Sqr] =< [Tolerance] THEN Return 1 ELSE Return 0;
     */
    
    /* **************************************** */

    DECLARE Inner_D_Value DOUBLE(36,12); /* Declare Local Variable: 差值(Difference Value / D-Value) */
    DECLARE Inner_D_Value_Sq DOUBLE(36,12); /* Declare Local Variable: 差值的平方(Square of D-Value) */
    DECLARE Inner_D_Value_Sqr DOUBLE(36,12); /* Declare Local Variable: 差值的平方根(Square Root of D-Value) */
    
    /* **************************************** */

    SET Inner_D_Value = (In_Predicted_Y_Value - In_Actual_Y_Value);
    SET Inner_D_Value_Sq = POWER(Inner_D_Value, 2);
    SET Inner_D_Value_Sqr = SQRT(Inner_D_Value_Sq);

    /* **************************************** */

    IF Inner_D_Value_Sqr <= In_Tolerance THEN
        RETURN 1; /* Return Value */
    ELSE
        RETURN 0; /* Return Value */
    END IF;
    
END//

/* 改回语句结束符为 ";" */
DELIMITER ;

/* -------------------------------------------------- */
/* EOF */
