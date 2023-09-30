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

/* 删除表: 容器表 (计算用) */
DROP TABLE IF EXISTS container_math;

/* 创建表: 容器表 (计算用) */
CREATE TABLE IF NOT EXISTS container_math(_index BIGINT(12) AUTO_INCREMENT PRIMARY KEY,
                                          _temp_acc_avg_base DOUBLE(16,4),
                                          _temp_mov_sum_offset_base DOUBLE(16,4),
                                          _temp_mov_var_base DOUBLE(16,4),
                                          _temp_mov_cov_x_base DOUBLE(16,4),
                                          _temp_mov_cov_y_base DOUBLE(16,4));

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

/* 删除函数: 累计平均 (Accumulate Average) */
DROP FUNCTION IF EXISTS MATH_ACC_AVG//

/* 创建函数: 累计平均 (Accumulate Average) */
CREATE FUNCTION MATH_ACC_AVG(In_Index INT(8), In_Value DOUBLE(16,4)) RETURNS DOUBLE(16,4)
BEGIN

    /*
     * 累计平均。
     * 又叫累加平均, 当连续不断地得到测定值 X1, X2, ... 时, 则 (X1 + X2) / 2, (X1 + X2 + X3) / 3, ... 等。
     * 分别称为第一次, 第二次, 第三次, ... 的累计平均数。
     */
    
    /* **************************************** */

    /* 声明传出变量 : 要返回的值 */
    DECLARE Out_ACC_Avg_Result DOUBLE(16,4) DEFAULT 0.0;
    
    /* **************************************** */
    
    /* 将传入基数值插入到容器(Container_Math) */
    INSERT INTO container_math(_index, _temp_acc_avg_base)
        VALUES (In_Index, In_Value) ON DUPLICATE KEY UPDATE _temp_acc_avg_base = In_Value;

    /* **************************************** */

    /* 从容器(Container_Math)取出截止当前索引临时存放的基数值, 计算其平均值 */
    SET Out_ACC_Avg_Result =
        (SELECT AVG(_temp_acc_avg_base) FROM container_math WHERE _index <= In_Index);
    /* 返回值 */
    RETURN Out_ACC_Avg_Result;
    
END//

/* 删除函数: 移动合计 - 带偏移量 (Moving Sum - Offset) */
DROP FUNCTION IF EXISTS MATH_MOV_SUM_OFFSET//

/* 创建函数: 移动合计 - 带偏移量 (Moving Sum - Offset) */
CREATE FUNCTION MATH_MOV_SUM_OFFSET(In_Sample_Size INT(4), In_Offset INT(2), In_Index INT(8), In_Value DOUBLE(16,4)) RETURNS DOUBLE(16,4)
BEGIN

    /* 声明局部变量 : 查询的起始索引(Begin Index) */
    DECLARE Inner_Bgn_Qry_Idx INT(8) DEFAULT 0;
    /* 声明局部变量 : 查询的截止索引(End Index) */
    DECLARE Inner_End_Qry_Idx INT(8) DEFAULT 0;
    /* 声明传出变量 : 要返回的值 */
    DECLARE Out_Mov_Sum_offset_Result DOUBLE(16,4) DEFAULT 0.0;

    /* **************************************** */

    /* 将传入基数值插入到容器(Container_Math) */
    INSERT INTO container_math(_index, _temp_mov_sum_offset_base)
        VALUES(In_Index, In_Value) ON DUPLICATE KEY UPDATE _temp_mov_sum_offset_base = In_Value;

    /* **************************************** */

    /*
     * 计算查询的起始索引(Begin Index)。
     * 查询的起始索引(Begin Index) = 当前索引(In Index) - 偏移量(In Offset) - 样本量(In Sample Size) + 1。
     */
    SET Inner_Bgn_Qry_Idx = In_Index - In_Offset - In_N + 1;


    /*
     * 计算查询的截止索引(End Index)。
     * 查询的截止索引(End Index) = 当前索引(In Index) - 偏移量(In Offset)。
     */
    SET Inner_End_Qry_Idx = In_Index - In_Offset;

    /* **************************************** */

    /*
     * 查询合计起始索引(Begin Index)和截止索引(End Index)之间的所有值。
     */
    IF In_Index >= (In_N + In_Offset) THEN
        SET Out_Mov_Sum_offset_Result =
            (SELECT SUM(_temp_mov_sum_offset_base) FROM container_math WHERE Inner_Bgn_Qry_Idx <= _index AND _index <= Inner_End_Qry_Idx);
        /* 返回值 */
        RETURN Out_Mov_Sum_offset_Result;
    
    ELSE
        /* 返回值 */
        RETURN NULL;

    END IF;
    
END//

/* 删除函数: 移动方差 (Moving Variance) */
DROP FUNCTION IF EXISTS MATH_MOV_VAR//

/* 创建函数: 移动方差 (Moving Variance) */
CREATE FUNCTION MATH_MOV_VAR(In_Sample_Size INT(4), In_Index INT(8), In_Value DOUBLE(16,4)) RETURNS DOUBLE(16,4)
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
    INSERT INTO container_math(_index, _temp_mov_var_base)
        VALUES (In_Index, In_Value) ON DUPLICATE KEY UPDATE _temp_mov_var_base = In_Value;
        
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
                (SELECT _temp_mov_var_base FROM container_math WHERE _index = (Inner_Bgn_Qry_Idx + Inner_Cyc_Cnt));
            /* 从容器(Container_Math)查询截止当前索引临时存放的基数值, 计算平均值 */
            SET Inner_Mov_Var_Avg =
                (SELECT AVG(_temp_mov_var_base) FROM container_math WHERE Inner_Bgn_Qry_Idx <= _index AND _index <= Inner_End_Qry_Idx);
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

/* 删除函数: 移动协方差 (Moving Covariance) */
DROP FUNCTION IF EXISTS MATH_MOV_COV//

/* 创建函数: 移动协方差 (Moving Covariance) */
CREATE FUNCTION MATH_MOV_COV(In_Sample_Size INT(4), In_Index INT(8), In_X_Value DOUBLE(16,4), In_Y_Value DOUBLE(16,4)) RETURNS DOUBLE(16,4)
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
     *
     */

    /* 声明局部变量 : 循环计数(Cycles Count) */
    DECLARE Inner_Cyc_Cnt INT(8) DEFAULT 0;
    /* 声明局部变量 : 查询的起始索引(Begin Index) */
    DECLARE Inner_Bgn_Qry_Idx INT(8) DEFAULT 0;
    /* 声明局部变量 : 查询的截止索引(End Index) */
    DECLARE Inner_End_Qry_Idx INT(8) DEFAULT 0;
    /* 声明局部变量 : 移动协方差X基数值 */
    DECLARE Inner_Mov_Cov_X_Base DOUBLE(16,4) DEFAULT 0.0;
    /* 声明局部变量 : 移动协方差Y基数值 */
    DECLARE Inner_Mov_Cov_Y_Base DOUBLE(16,4) DEFAULT 0.0;
    /* 声明局部变量 : 移动协方差(中间Step)X均值 */
    DECLARE Inner_Mov_Cov_X_Avg DOUBLE(16,4) DEFAULT 0.0;
    /* 声明局部变量 : 移动协方差(中间Step)Y均值 */
    DECLARE Inner_Mov_Cov_Y_Avg DOUBLE(16,4) DEFAULT 0.0;
    /* 声明局部变量 : 移动协方差(中间Step)归一化值的平方的和 */
    DECLARE Inner_Mov_Cov_Normalized_Product_Sum DOUBLE(16,4) DEFAULT 0.0;
    /* 声明传出变量 : 要返回的值 */
    DECLARE Out_Mov_Cov_Result DOUBLE(16,4) DEFAULT 0.0;
    
    /* **************************************** */
    
    /* 将传入X基数值插入到容器(Container_Math) */
    INSERT INTO container_math(_index, _temp_mov_cov_x_base)
        VALUES (In_Index, In_X_Value) ON DUPLICATE KEY UPDATE _temp_mov_cov_x_base = In_X_Value;
    /* 将传入Y基数值插入到容器(Container_Math) */
    INSERT INTO container_math(_index, _temp_mov_cov_y_base)
        VALUES (In_Index, In_Y_Value) ON DUPLICATE KEY UPDATE _temp_mov_cov_y_base = In_Y_Value;
        
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
            /* 从容器(Container_Math)查询截止当前索引临时存放的X基数值 */
            SET Inner_Mov_Cov_X_Base =
                (SELECT _temp_mov_cov_x_base FROM container_math WHERE _index = (Inner_Bgn_Qry_Idx + Inner_Cyc_Cnt));
            /* 从容器(Container_Math)查询截止当前索引临时存放的Y基数值 */
            SET Inner_Mov_Cov_Y_Base =
                (SELECT _temp_mov_cov_y_base FROM container_math WHERE _index = (Inner_Bgn_Qry_Idx + Inner_Cyc_Cnt));
            /* 从容器(Container_Math)查询截止当前索引临时存放的X基数值, 计算平均值 */
            SET Inner_Mov_Cov_X_Avg =
                (SELECT AVG(_temp_mov_cov_x_base) FROM container_math WHERE Inner_Bgn_Qry_Idx <= _index AND _index <= Inner_End_Qry_Idx);
            /* 从容器(Container_Math)查询截止当前索引临时存放的Y基数值, 计算平均值 */
            SET Inner_Mov_Cov_Y_Avg =
                (SELECT AVG(_temp_mov_cov_y_base) FROM container_math WHERE Inner_Bgn_Qry_Idx <= _index AND _index <= Inner_End_Qry_Idx);
            /* 累加移动协方差(中间Step)归一化值的平方的和 */
            SET Inner_Mov_Cov_Normalized_Product_Sum = 
                (Inner_Mov_Cov_Normalized_Product_Sum + (Inner_Mov_Cov_X_Base - Inner_Mov_Cov_X_Avg) * (Inner_Mov_Cov_Y_Base - Inner_Mov_Cov_Y_Avg));
            /* 循环次数 +1 */
            SET Inner_Cyc_Cnt = Inner_Cyc_Cnt + 1;
        END WHILE;
        /* 计算移动N日方差的值 */
        SET Out_Mov_Cov_Result = Inner_Mov_Cov_Normalized_Product_Sum / (In_Sample_Size - 1);
        /* 返回值 */
        RETURN Out_Mov_Var_Result;
    
    ELSE
        /* 返回值 */
        RETURN NULL;
    
    END IF;
    
END//

/* 改回语句结束符为 ";" */
DELIMITER ;

/* -------------------------------------------------- */
/* EOF */
