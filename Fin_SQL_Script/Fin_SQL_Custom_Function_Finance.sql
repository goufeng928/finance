/* Fin_SQL_Custom_Function_Finance.sql */

/* Create By GF 2023-09-05 15:21 */

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
DROP TABLE IF EXISTS container_fin;

/* 创建表: 容器表 (计算用) */
CREATE TABLE IF NOT EXISTS container_fin(_index BIGINT(12) AUTO_INCREMENT PRIMARY KEY,
                                         _temp_close DOUBLE(16,4),
                                         _temp_ema DOUBLE(16,4),
                                         _temp_macd_dea DOUBLE(16,4),
                                         _temp_2_line_cross_base DOUBLE(16,4));

/* -------------------------------------------------- */
-- ERROR 1418 (HY000): This function has none of DETERMINISTIC, NO SQL, or READS SQL DATA in its declaration and binary logging is enabled
--                     (you might want to use the less safe log_bin_trust_function_creators variable)

-- SET GLOBAL log_bin_trust_function_creators=TRUE;

/* -------------------------------------------------- */

-- 修改语句结束符为 "//".
DELIMITER //

/* -------------------------------------------------- */
/* Technical Analysis Function */

/* 删除函数: 简单移动平均 (Simple Moving Average) */
DROP FUNCTION IF EXISTS FIN_SMA//

/* 创建函数: 简单移动平均 (Simple Moving Average) */
CREATE FUNCTION FIN_SMA(In_Period INT(4), In_Index INT(8), In_Close DOUBLE(16,4)) RETURNS DOUBLE(16,4)
BEGIN

    /* 声明局部变量: 起始索引 */
    DECLARE Inner_Bgn_Idx INT(8) DEFAULT 0;
    /* 声明传出变量: 要返回的值 */
    DECLARE Out_SMA_Result DOUBLE(16,4) DEFAULT 0.0;
    
    /* **************************************** */
    
    /* 将收盘价插入到容器(Container_Fin) */
    INSERT INTO container_fin(_index, _temp_close)
        VALUES (In_Index, In_Close) ON DUPLICATE KEY UPDATE _temp_close = In_Close;

    /* **************************************** */

    /* 条件判断: 如果索引小于周期数 */
    IF In_Index < In_Period THEN
        /* 返回值 */
        RETURN NULL;
    
    /* 条件判断: 如果索引大于或等于周期数 */
    ELSEIF In_Index >= In_Period THEN
        /* 计算查询取值的起始索引(Begin Index) */
        SET Inner_Bgn_Idx = In_Index - In_Period + 1;
        /* 查询取值并计算平均值 */
        SET Out_SMA_Result = 
            (SELECT AVG(_temp_close) FROM container_fin WHERE Inner_Bgn_Idx <= _index AND _index <= In_Index);
        /* 返回值 */
        RETURN Out_SMA_Result;

    END IF;
    
END//

/* 删除函数: 指数移动平均 (Exponential Moving Average) */
DROP FUNCTION IF EXISTS FIN_EMA//

/* 创建函数: 指数移动平均 (Exponential Moving Average) */
CREATE FUNCTION FIN_EMA(In_Period INT(4), In_Index INT(8), In_Close DOUBLE(16,4)) RETURNS DOUBLE(16,4)
BEGIN

    /*
     * ########## 首日EMA直接使用当日收盘价 #############
     * --------------------------------------------------
     * 公式：EMA = 当日收盘价 x 2/(N+1) + 前1日EMA x (N-1)/(N+1)
     * --------------------------------------------------
     * 以计算12日EMA举例：
     * EMA12 = 2/(12+1) * Close[当日] + (12+1-2)/(12+1) * EMA12[前1日]
     * 首日EMA由于没有昨日EMA数据，所以首日EMA直接使用当日收盘价。
     * --------------------------------------------------
     */

    /* **************************************** */

    -- 声明局部变量: 存储索引.
    DECLARE Inner_Storage_Index INT(8) DEFAULT 0;
    -- 声明局部变量: 前1日 "EMA值".
    DECLARE Inner_Previous_EMA DOUBLE(16,4) DEFAULT 0.0;
    -- 声明传出变量: 要返回的值.
    DECLARE Out_EMA_Result DOUBLE(16,4) DEFAULT 0.0;

    /* **************************************** */

    /* 计算不同周期 EMA 值在容器中存放的位置索引号 */
    SET Inner_Storage_Index = In_Period * 10000000 + In_Index;

    /* **************************************** */

    CASE In_Index
    /* 条件判断: 如果索引等于1 */
    WHEN 1 THEN
        -- 将收盘价插入到 "容器".
        REPLACE INTO container_fin(_index, _temp_ema) VALUES(Inner_Storage_Index, In_Close);
        /* 返回值 */
        RETURN In_Close;
    
    /* 条件判断: 如果索引不等于1 */
    ELSE
        /* 查询取值前1日的 EMA 值 */
        SET Inner_Previous_EMA =
            (SELECT _temp_ema FROM container_fin WHERE _index = (Inner_Storage_Index - 1));
        /* 计算当前 EMA 值 */
        SET Out_EMA_Result = (2 / (In_Period + 1) * In_Close + (In_Period + 1 - 2) / (In_Period + 1) * Inner_Previous_EMA);
        /* 将当前 EMA 值插入到容器(Container_Fin) */
        REPLACE INTO container_fin(_index, _temp_ema) VALUES(Inner_Storage_Index, Out_EMA_Result);
        -- 返回值.
        RETURN Out_EMA_Result;

    END CASE;
    
END//

/* 删除函数: 异同移动平均线 - DIF (Moving Average Convergence / Divergence - DIF) */
DROP FUNCTION IF EXISTS FIN_MACD_DIF//

/* 创建函数: 异同移动平均线 - DIF (Moving Average Convergence / Divergence - DIF) */
CREATE FUNCTION FIN_MACD_DIF(In_Short_EMA_Period INT(4), In_Long_EMA_Period INT(4), In_Index INT(8), In_Close DOUBLE(16,4)) RETURNS DOUBLE(16,4)
BEGIN

    /*
     * 公式：MACD_DIF = 当日EMA(12) - 当日EMA(26)
     * 12日EMA和26日EMA通常是MACD的常用值，如要修改MACD的观测参数，则修改对应的EMA数值。
     */

    /* **************************************** */

    /* 声明局部变量: 当前索引短期 EMA 的值 */
    DECLARE Inner_Current_Short_EMA DOUBLE(16,4) DEFAULT 0.0;
    /* 声明局部变量: 当前索引长期 EMA 的值 */
    DECLARE Inner_Current_Long_EMA DOUBLE(16,4) DEFAULT 0.0;
    /* 声明传出变量: 要返回的值 */
    DECLARE Out_MACD_DIF_Result DOUBLE(16,4) DEFAULT 0.0;

    /* **************************************** */

    /* 调用其它函数: 计算当前索引短期 EMA 的值 */
    SET Inner_Current_Short_EMA = FIN_EMA(In_Short_EMA_Period, In_Index, In_Close);
    /* 调用其它函数: 计算当前索引长期 EMA 的值 */
    SET Inner_Current_Long_EMA = FIN_EMA(In_Long_EMA_Period, In_Index, In_Close);

    /* **************************************** */

    CASE In_Index
    /* 条件判断: 如果索引等于1 */
    WHEN 1 THEN
        /* 返回值 */
        RETURN 0.0;
    
    /* 条件判断: 如果索引不等于1 */
    ELSE
        /* 计算当前 MACD_DIF 值 */
        SET Out_MACD_DIF_Result = (Inner_Current_Short_EMA - Inner_Current_Long_EMA);
        /* 返回值 */
        RETURN Out_MACD_DIF_Result;

    END CASE;
    
END//

/* 删除函数: 异同移动平均线 - DEA (Moving Average Convergence / Divergence - DEA) */
DROP FUNCTION IF EXISTS FIN_MACD_DEA//

/* 创建函数: 异同移动平均线 - DEA (Moving Average Convergence / Divergence - DEA) */
CREATE FUNCTION FIN_MACD_DEA(In_Short_EMA_Period INT(4), In_Long_EMA_Period INT(4), In_Index INT(8), In_Close DOUBLE(16,4)) RETURNS DOUBLE(16,4)
BEGIN

    /*
     * ############### 首日DEA直接使用0值 ################
     *  --------------------------------------------------
     *  DEA又叫：计算DIF的9日EMA。
     *  根据离差值计算其9日的EMA，即离差平均值，是所求的MACD值。为了不与指标原名相混淆，此值又名DEA。
     *  公式：当日DEA = 2/(9+1) * 当日DIF + (9+1-2)/(9+1) * 前日DEA
     *  首日DEA由于没有昨日DEA数据，所以首日DEA直接使用0值。
     */

    /* **************************************** */

    /* 声明局部变量: 当前索引 MACD_DIF 的值 */
    DECLARE Inner_Current_MACD_DIF DOUBLE(16,4) DEFAULT 0.0;
    /* 声明局部变量: 前1日 MACD_DEA 的值 */
    DECLARE Inner_Previous_MACD_DEA DOUBLE(16,4) DEFAULT 0.0;
    /* 声明传出变量: 要返回的值 */
    DECLARE Out_MACD_DEA_Result DOUBLE(16,4) DEFAULT 0.0;

    /* **************************************** */

    /* 调用其它函数: 计算当前索引 MACD_DIF 的值 */
    SET Inner_Current_MACD_DIF = FIN_MACD_DIF(In_Short_EMA_Period, In_Long_EMA_Period, In_Index, In_Close);

    /* **************************************** */

    CASE In_Index
    /* 条件判断: 如果索引等于1 */
    WHEN 1 THEN
        /* 首日 MACD_DEA 直接使用0值, 并将 0.0 插入到容器(Container_Fin) */
        INSERT INTO container_fin(_index, _temp_macd_dea)
            VALUES (In_Index, 0.0) ON DUPLICATE KEY UPDATE _temp_macd_dea = 0.0;
        /* 返回值 */
        RETURN 0.0;
    
    /* 条件判断: 如果索引不等于1 */
    ELSE
        /* 查询取值前1日的 MACD_DEA 值 */
        SET Inner_Previous_MACD_DEA =
            (SELECT _temp_macd_dea FROM container_fin WHERE _index = (In_Index - 1));
        /* 计算当前 MACD_DEA 值 */
        SET Out_MACD_DEA_Result = (2 / (9 + 1) * Inner_Current_MACD_DIF + (9 + 1 - 2) / (9 + 1) * Inner_Previous_MACD_DEA);
        /* 将当前 MACD_DEA 值插入到容器(Container_Fin) */
        INSERT INTO container_fin(_index, _temp_macd_dea)
            VALUES (In_Index, Out_MACD_DEA_Result) ON DUPLICATE KEY UPDATE _temp_macd_dea = Out_MACD_DEA_Result;
        /* 返回值 */
        RETURN Out_MACD_DEA_Result;

    END CASE;
    
END//

/* 删除函数: 异同移动平均线 - STICK (Moving Average Convergence / Divergence - STICK) */
DROP FUNCTION IF EXISTS FIN_MACD_STICK//

/* 创建函数: 异同移动平均线 - STICK (Moving Average Convergence / Divergence - STICK) */
CREATE FUNCTION FIN_MACD_STICK(In_Short_EMA_Period INT(4), In_Long_EMA_Period INT(4), In_Index INT(8), In_Close DOUBLE(16,4)) RETURNS DOUBLE(16,4)
BEGIN

    /*
     * 用 (DIF - DEA ) x 2 即为MACD柱状图，一般称作MACD或STICK。
     * 公式：MACD_STICK(MACD) = (MACD_DIF - MACD_DEA) * 2
     */

    /* **************************************** */

    /* 声明局部变量: 当前索引 MACD_DIF 的值 */
    DECLARE Inner_Current_MACD_DIF DOUBLE(16,4) DEFAULT 0.0;
    /* 声明局部变量: 当前索引 MACD_DEA 的值 */
    DECLARE Inner_Current_MACD_DEA DOUBLE(16,4) DEFAULT 0.0;
    /* 声明传出变量: 要返回的值 */
    DECLARE Out_MACD_STICK_Result DOUBLE(16,4) DEFAULT 0.0;

    /* **************************************** */

    /* 调用其它函数: 计算当前 MACD_DIF 的值 */
    SET Inner_Current_MACD_DIF = FIN_MACD_DIF(In_Short_EMA_Period, In_Long_EMA_Period, In_Index, In_Close);
    /* 调用其它函数: 计算当前 MACD_DEA 的值 */
    SET Inner_Current_MACD_DEA = FIN_MACD_DEA(In_Short_EMA_Period, In_Long_EMA_Period, In_Index, In_Close);

    /* **************************************** */

    /* 计算当前 MACD_STICK 值 */
    SET Out_MACD_STICK_Result = ((Inner_Current_MACD_DIF - Inner_Current_MACD_DEA) * 2);
    /* 返回值 */
    RETURN Out_MACD_STICK_Result;
    
END//

/* 删除函数: 评估2线穿越 (Estimate 2 Line Cross) */
DROP FUNCTION IF EXISTS FIN_EST_2_LINE_CROSS//

/* 创建函数: 评估2线穿越 (Estimate 2 Line Cross) */
CREATE FUNCTION FIN_EST_2_LINE_CROSS(In_Orientation VARCHAR(10), In_Index INT(8), In_Crossing_Value DOUBLE(16,4), In_Crossed_Value DOUBLE(16,4)) RETURNS INT(1)
BEGIN

    /* 声明局部变量: Crossing 基数值存储索引 */
    DECLARE Inner_Crossing_Sto_Idx INT(8) DEFAULT 0;
    /* 声明局部变量: Crossed 基数值存储索引 */
    DECLARE Inner_Crossed_Sto_Idx INT(8) DEFAULT 0;
    /* 声明局部变量: 3个 Crossing 的值中的第1个 */
    DECLARE Inner_1st_of_3_Crossing_Values DOUBLE(16,4) DEFAULT 0.0;
    /* 声明局部变量: 3个 Crossing 的值中的第2个 */
    DECLARE Inner_2st_of_3_Crossing_Values DOUBLE(16,4) DEFAULT 0.0;
    /* 声明局部变量: 3个 Crossed 的值中的第1个 */
    DECLARE Inner_1st_of_3_Crossed_Values DOUBLE(16,4) DEFAULT 0.0;
    /* 声明局部变量: 3个 Crossed 的值中的第2个 */
    DECLARE Inner_2st_of_3_Crossed_Values DOUBLE(16,4) DEFAULT 0.0;

    /* **************************************** */
    
    /* Crossing 的基数值在容器中存放的位置索引号 */
    SET Inner_Crossing_Sto_Idx = 1 * 10000000 + In_Index;

    /* Crossed 的基数值在容器中存放的位置索引号 */
    SET Inner_Crossed_Sto_Idx = 2 * 10000000 + In_Index;

    /* **************************************** */
    
    /* 将 Crossing 基数值插入到容器(Container_Fin) */
    INSERT INTO container_fin(_index, _temp_2_line_cross_base)
        VALUES (Inner_Crossing_Sto_Idx, In_Crossing_Value) ON DUPLICATE KEY UPDATE _temp_2_line_cross_base = In_Crossing_Value;
    /* 将 Crossed 基数值插入到容器(Container_Fin) */
    INSERT INTO container_fin(_index, _temp_2_line_cross_base)
        VALUES (Inner_Crossed_Sto_Idx, In_Crossed_Value) ON DUPLICATE KEY UPDATE _temp_2_line_cross_base = In_Crossed_Value;

    /* **************************************** */
    
    /* 如果当前索引 >= 3 */
    IF In_Index >= 3 THEN
    
        SET Inner_1st_of_3_Crossing_Values =
            (SELECT _temp_2_line_cross_base FROM container_fin WHERE _index = (Inner_Crossing_Sto_Idx - 2));
        SET Inner_2st_of_3_Crossing_Values =
            (SELECT _temp_2_line_cross_base FROM container_fin WHERE _index = (Inner_Crossing_Sto_Idx - 1));

        SET Inner_1st_of_3_Crossed_Values =
            (SELECT _temp_2_line_cross_base FROM container_fin WHERE _index = (Inner_Crossed_Sto_Idx - 2));
        SET Inner_2st_of_3_Crossed_Values =
            (SELECT _temp_2_line_cross_base FROM container_fin WHERE _index = (Inner_Crossed_Sto_Idx - 1));
            
    /* 如果当前索引 < 3 */
    ELSE
        /* 返回值 */
        RETURN 0;

    END IF;
    
    /* **************************************** */
    
    /* In_Orientation = "Down" 的情况(NULL 的判断需要用 IS 或者 IS NOT) */
    IF In_Orientation = "Down" AND Inner_1st_of_3_Crossing_Values IS NOT NULL THEN
            
        IF Inner_1st_of_3_Crossing_Values > Inner_1st_of_3_Crossed_Values AND
           Inner_2st_of_3_Crossing_Values >= Inner_2st_of_3_Crossed_Values AND
           In_Crossing_Value < In_Crossed_Value THEN
           
            /* 返回值 */
            RETURN 1;
        
        ELSE
            /* 返回值 */
            RETURN 0;
        
        END IF;

    /* In_Orientation = "Up" 的情况(NULL 的判断需要用 IS 或者 IS NOT)*/
    ELSEIF In_Orientation = "Up" AND Inner_1st_of_3_Crossing_Values IS NOT NULL THEN
            
        IF Inner_1st_of_3_Crossing_Values < Inner_1st_of_3_Crossed_Values AND
           Inner_2st_of_3_Crossing_Values <= Inner_2st_of_3_Crossed_Values AND
           In_Crossing_Value > In_Crossed_Value THEN
           
            /* 返回值 */
            RETURN 1;
        
        ELSE
            /* 返回值 */
            RETURN 0;
        
        END IF;

    ELSE
        /* 返回值 */
        RETURN 0;

    END IF;
    
END//

/* 删除函数: 评估2值大小对比 (Estimate 2 Value Compare Size) */
DROP FUNCTION IF EXISTS FIN_EST_2_VALUE_COMPARE_SIZE//

/* 创建函数: 评估2值大小对比 (Estimate 2 Value Compare Size) */
CREATE FUNCTION FIN_EST_2_VALUE_COMPARE_SIZE(In_Larger_Or_Smaller VARCHAR(10), In_Compare_Value DOUBLE(16,4), In_Compared_Value DOUBLE(16,4)) RETURNS INT(1)
BEGIN
    
    /* 如果对比值(Compare Value)或被对比值(Compared Value)为 NULL (NULL 的判断需要用 IS 或者 IS NOT) */
    IF In_Compare_Value IS NULL OR In_Compared_Value IS NULL THEN

        /* 返回值 */
        RETURN 0;

    END IF;
    
    /* **************************************** */
    
    /* In_Larger_Or_Smaller = "Larger" 的情况 */
    IF In_Larger_Or_Smaller = "Larger" THEN
            
        IF In_Compare_Value > In_Compared_Value THEN
           
            /* 返回值 */
            RETURN 1;

        ELSE
            /* 返回值 */
            RETURN 0;
        
        END IF;

    /* In_Larger_Or_Smaller = "Smaller" 的情况 */
    ELSEIF In_Larger_Or_Smaller = "Smaller" THEN
            
        IF In_Compare_Value < In_Compared_Value THEN

            /* 返回值 */
            RETURN 1;
        
        ELSE
            /* 返回值 */
            RETURN 0;
        
        END IF;

    ELSE
        /* 返回值 */
        RETURN 0;

    END IF;
    
END//

/* 删除函数: 评估值的所在区间 (Estimate Value Whithin Range) */
DROP FUNCTION IF EXISTS FIN_EST_VALUE_WHITHIN_RANGE//

/* 创建函数: 评估值的所在区间 (Estimate Value Whithin Range) */
CREATE FUNCTION FIN_EST_VALUE_WHITHIN_RANGE(In_Upper_Bound DOUBLE(16,4), In_Lower_Bound DOUBLE(16,4), In_Value DOUBLE(16,4)) RETURNS INT(1)
BEGIN
    
    /* 如果传入值(In Value)为 NULL (NULL 的判断需要用 IS 或者 IS NOT) */
    IF In_Value IS NULL OR In_Compared_Value IS NULL THEN

        /* 返回值 */
        RETURN 0;

    END IF;
    
    /* **************************************** */

    IF In_Lower_Bound <= In_Value AND In_Value <= In_Upper_Bound THEN

        /* 返回值 */
        RETURN 1;

    ELSE
        /* 返回值 */
        RETURN 0;

    END IF;
    
END//

-- 改回语句结束符为 ";".
DELIMITER ;

/* -------------------------------------------------- */
/* EOF */
