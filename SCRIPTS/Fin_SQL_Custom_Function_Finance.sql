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

/*
 * Requirement : Fin_SQL_Procedure_Container.sql
 */

/* -------------------------------------------------- */
-- ERROR 1418 (HY000): This function has none of DETERMINISTIC, NO SQL, or READS SQL DATA in its declaration and binary logging is enabled
--                     (you might want to use the less safe log_bin_trust_function_creators variable)

-- SET GLOBAL log_bin_trust_function_creators=TRUE;

/* -------------------------------------------------- */

/* 修改语句结束符为 "//" */
DELIMITER //

/* -------------------------------------------------- */
/* Finance Technical Analysis Function */

/* 删除函数: 简单移动平均 (Finance - Simple Moving Average) */
DROP FUNCTION IF EXISTS FUNC_FIN_SMA//

/* 创建函数: 简单移动平均 (Finance - Simple Moving Average) */
CREATE FUNCTION FUNC_FIN_SMA(In_Index INT(8), In_Period INT(4), In_Close DOUBLE(16,4)) RETURNS DOUBLE(16,4)
BEGIN

    DECLARE Inner_Bgn_Idx INT(8); /* Declare Local Variable: Begin Index */
    DECLARE Out_SMA_Result DOUBLE(16,4); /* Declare Local Variable: Return Value */
    
    /* **************************************** */

    REPLACE INTO container(cntr_index, cntr_class, cntr_name, cntr_double_value) VALUES (In_Index, "Func_Calc", "Copy_Close", In_Close);

    /* **************************************** */

    IF In_Index < In_Period THEN
        RETURN NULL; /* Return Value */
    ELSEIF In_Index >= In_Period THEN
        SET Inner_Bgn_Idx = (In_Index - In_Period + 1); /* 计算 Container 取值的起始索引(Begin Index) */
        /* ************************************ */
        SET Out_SMA_Result =
            (SELECT AVG(cntr_double_value) FROM container WHERE Inner_Bgn_Idx <= cntr_index AND cntr_index <= In_Index AND cntr_class = "Func_Calc" AND cntr_name = "Copy_Close");
        /* ************************************ */
        RETURN Out_SMA_Result; /* Return Value */
    END IF;
    
END//

/* 删除函数: 指数移动平均 (Finance - Exponential Moving Average) */
DROP FUNCTION IF EXISTS FUNC_FIN_EMA//

/* 创建函数: 指数移动平均 (Finance - Exponential Moving Average) */
CREATE FUNCTION FUNC_FIN_EMA(In_Index INT(8), In_Period INT(4), In_Close DOUBLE(16,4)) RETURNS DOUBLE(16,4)
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

    DECLARE Inner_EMA_CNTR_Name CHAR(80);
    DECLARE Inner_Previous_EMA DOUBLE(16,4); /* Declare Local Variable: 前1日 EMA 值 */
    DECLARE Out_EMA_Result DOUBLE(16,4) DEFAULT 0.0; /* Declare Local Variable: Return Value */

    /* **************************************** */
    
    SET Inner_EMA_CNTR_Name = CONCAT("EMA_", CONVERT(In_Period, CHAR));

    /* **************************************** */

    CASE In_Index
    WHEN 1 THEN
        REPLACE INTO container(cntr_index, cntr_class, cntr_name, cntr_double_value) VALUES (In_Index, "Func_Calc", Inner_EMA_CNTR_Name, In_Close);
        /* ************************************ */
        RETURN In_Close; /* Return Value */
    ELSE
        SET Inner_Previous_EMA =
            (SELECT cntr_double_value FROM container WHERE cntr_index = (In_Index - 1) AND cntr_class = "Func_Calc" AND cntr_name = Inner_EMA_CNTR_Name);
        /* ************************************ */
        SET Out_EMA_Result = (2 / (In_Period + 1) * In_Close + (In_Period + 1 - 2) / (In_Period + 1) * Inner_Previous_EMA);
        /* ************************************ */
        REPLACE INTO container(cntr_index, cntr_class, cntr_name, cntr_double_value) VALUES (In_Index, "Func_Calc", Inner_EMA_CNTR_Name, Out_EMA_Result);
        /* ************************************ */
        RETURN Out_EMA_Result; /* Return Value */
    END CASE;
    
END//

/* 删除函数: 异同移动平均线 - DIF (Finance - Moving Average Convergence / Divergence - DIF) */
DROP FUNCTION IF EXISTS FUNC_FIN_MACD_DIF//

/* 创建函数: 异同移动平均线 - DIF (Finance - Moving Average Convergence / Divergence - DIF) */
CREATE FUNCTION FUNC_FIN_MACD_DIF(In_Index INT(8), In_Short_EMA_Period INT(4), In_Long_EMA_Period INT(4), In_Close DOUBLE(16,4)) RETURNS DOUBLE(16,4)
BEGIN

    /*
     * 公式：MACD_DIF = 当日EMA(12) - 当日EMA(26)
     * 12日EMA和26日EMA通常是MACD的常用值，如要修改MACD的观测参数，则修改对应的EMA数值。
     */

    /* **************************************** */

    DECLARE Inner_Current_Short_EMA DOUBLE(16,4); /* Declare Local Variable: 当前索引短期 EMA 值 */
    DECLARE Inner_Current_Long_EMA DOUBLE(16,4); /* Declare Local Variable: 当前索引长期 EMA 值 */
    DECLARE Out_MACD_DIF_Result DOUBLE(16,4) DEFAULT 0.0; /* Declare Local Variable: Return Value */

    /* **************************************** */

    /* Calling Other Function: Calculate Current Short / Long EMA */
    SET Inner_Current_Short_EMA = FUNC_FIN_EMA(In_Index, In_Short_EMA_Period, In_Close);
    SET Inner_Current_Long_EMA = FUNC_FIN_EMA(In_Index, In_Long_EMA_Period, In_Close);

    /* **************************************** */

    CASE In_Index
    WHEN 1 THEN
        RETURN 0.0; /* Return Value */
    ELSE
        SET Out_MACD_DIF_Result = (Inner_Current_Short_EMA - Inner_Current_Long_EMA);
        /* ************************************ */
        RETURN Out_MACD_DIF_Result; /* Return Value */
    END CASE;
    
END//

/* 删除函数: 异同移动平均线 - DEA (Finance - Moving Average Convergence / Divergence - DEA) */
DROP FUNCTION IF EXISTS FUNC_FIN_MACD_DEA//

/* 创建函数: 异同移动平均线 - DEA (Finance - Moving Average Convergence / Divergence - DEA) */
CREATE FUNCTION FUNC_FIN_MACD_DEA(In_Index INT(8), In_Short_EMA_Period INT(4), In_Long_EMA_Period INT(4), In_Close DOUBLE(16,4)) RETURNS DOUBLE(16,4)
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

    DECLARE Inner_Current_MACD_DIF DOUBLE(16,4); /* Declare Local Variable: 当前索引 MACD - DIF 值 */
    DECLARE Inner_Previous_MACD_DEA DOUBLE(16,4); /* Declare Local Variable: 前1日 MACD - DEA 值 */
    DECLARE Inner_MACD_DEA_CNTR_Name CHAR(80);
    DECLARE Out_MACD_DEA_Result DOUBLE(16,4) DEFAULT 0.0; /* Declare Local Variable: Return Value */

    /* **************************************** */

    /* Calling Other Function: Calculate Current MACD - DIF */
    SET Inner_Current_MACD_DIF = FUNC_FIN_MACD_DIF(In_Index, In_Short_EMA_Period, In_Long_EMA_Period, In_Close);

    /* **************************************** */

    SET Inner_MACD_DEA_CNTR_Name = CONCAT("MACD_DEA_", CONVERT(In_Short_EMA_Period, CHAR), "_", CONVERT(In_Long_EMA_Period, CHAR));

    /* **************************************** */

    CASE In_Index
    WHEN 1 THEN
        REPLACE INTO container(cntr_index, cntr_class, cntr_name, cntr_double_value) VALUES (In_Index, "Func_Calc", Inner_MACD_DEA_CNTR_Name, 0.0);
        /* ************************************ */
        RETURN 0.0; /* Return Value */
    ELSE
        SET Inner_Previous_MACD_DEA =
            (SELECT cntr_double_value FROM container WHERE cntr_index = (In_Index - 1) AND cntr_class = "Func_Calc" AND cntr_name = Inner_MACD_DEA_CNTR_Name);
        /* ************************************ */
        SET Out_MACD_DEA_Result = (2 / (9 + 1) * Inner_Current_MACD_DIF + (9 + 1 - 2) / (9 + 1) * Inner_Previous_MACD_DEA);
        /* ************************************ */
        REPLACE INTO container(cntr_index, cntr_class, cntr_name, cntr_double_value) VALUES (In_Index, "Func_Calc", Inner_MACD_DEA_CNTR_Name, Out_MACD_DEA_Result);
        /* ************************************ */
        RETURN Out_MACD_DEA_Result; /* Return Value */
    END CASE;
    
END//

/* 删除函数: 异同移动平均线 - STICK (Finance - Moving Average Convergence / Divergence - STICK) */
DROP FUNCTION IF EXISTS FUNC_FIN_MACD_STICK//

/* 创建函数: 异同移动平均线 - STICK (Finance - Moving Average Convergence / Divergence - STICK) */
CREATE FUNCTION FUNC_FIN_MACD_STICK(In_Index INT(8), In_Short_EMA_Period INT(4), In_Long_EMA_Period INT(4), In_Close DOUBLE(16,4)) RETURNS DOUBLE(16,4)
BEGIN

    /*
     * 用 (DIF - DEA ) x 2 即为MACD柱状图，一般称作MACD或STICK。
     * 公式：MACD_STICK(MACD) = (MACD_DIF - MACD_DEA) * 2
     */

    /* **************************************** */

    DECLARE Inner_Current_MACD_DIF DOUBLE(16,4); /* Declare Local Variable: 当前索引 MACD - DIF 值 */
    DECLARE Inner_Current_MACD_DEA DOUBLE(16,4); /* Declare Local Variable: 当前索引 MACD - DEA 值 */
    DECLARE Out_MACD_STICK_Result DOUBLE(16,4) DEFAULT 0.0; /* Declare Local Variable: Return Value */

    /* **************************************** */

    /* Calling Other Function: Calculate Current MACD - DIF / MACD - DEA */
    SET Inner_Current_MACD_DIF = FUNC_FIN_MACD_DIF(In_Index, In_Short_EMA_Period, In_Long_EMA_Period, In_Close);
    SET Inner_Current_MACD_DEA = FUNC_FIN_MACD_DEA(In_Index, In_Short_EMA_Period, In_Long_EMA_Period, In_Close);

    /* **************************************** */
    
    CASE In_Index
    WHEN 1 THEN
        RETURN 0.0; /* Return Value */
    ELSE
        SET Out_MACD_STICK_Result = ((Inner_Current_MACD_DIF - Inner_Current_MACD_DEA) * 2);
        /* ************************************ */
        RETURN Out_MACD_STICK_Result; /* Return Value */
    END CASE;
    
END//

/* 删除函数: 相对强弱指标 (Finance - Relative Strength Index) */
DROP FUNCTION IF EXISTS FUNC_FIN_RSI//

/* 创建函数: 相对强弱指标 (Finance - Relative Strength Index) */
CREATE FUNCTION FUNC_FIN_RSI(In_Index INT(8), In_Period INT(4), In_Close DOUBLE(16,4)) RETURNS DOUBLE(16,4)
BEGIN

    /*
     * 相对强弱指标 RSI 是用以计测市场供需关系和买卖力道的方法及指标。
     *
     * 公式一:
     * RSI(N) = A ÷ ( A + B ) × 100
     * A = N 日内收盘价所有上涨额度之和
     * B = N 日内收盘价所有下跌额度之和(取正数, 即乘以(-1))
     *
     * 公式二:
     * RS(相对强度) = N日内收盘价所有上涨额度之和的平均值 ÷ N日内收盘价所有下跌额度之和的平均值(取绝对值)
     * RSI(相对强弱指标) = 100 - 100 ÷ ( 1 + RS )
     *
     * 这两个公式虽然有些不同, 但计算的结果一样。
     *
     * 股票 RSI 三条线分别为 RSI1, RSI2, RSI3。
     * RSI1 是白线，一般指 6 日相对强弱指标;
     * RSI2 是黄线，一般指 12 日相对强弱指标;
     * RSI3 是紫线，一般指 24 日相对强弱指标;
     */

    /* **************************************** */

    DECLARE Inner_RSI_UD_SMA_CNTR_Name CHAR(80);
    DECLARE Inner_Previous_Close DOUBLE(16,4); /* Declare Local Variable: 前1日收盘价 */
    DECLARE Inner_Cur_Rise_Fall_Amt DOUBLE(16,4); /* Declare Local Variable: 当前索引的涨跌额度 */
    DECLARE Inner_Bgn_Idx INT(8) DEFAULT 0; /* Declare Local Variable: Begin Index */
    DECLARE Inner_N_Rise_Amt_Sum DOUBLE(16,4); /* Declare Local Variable: N日上涨额度之和 */
    DECLARE Inner_N_Fall_Amt_Sum DOUBLE(16,4); /* Declare Local Variable: N日下跌额度之和 */
    DECLARE Inner_RS DOUBLE(16,4); /* Declare Local Variable: Relative Strength */
    DECLARE Inner_RSI DOUBLE(16,4); /* Declare Local Variable: Relative Strength Index */

    /* **************************************** */

    SET Inner_RSI_UD_SMA_CNTR_Name = CONCAT("RSI_", In_Period, "_UD_SMA");

    /* **************************************** */

    REPLACE INTO container(cntr_index, cntr_class, cntr_name, cntr_double_value) VALUES (In_Index, "Func_Calc", "Copy_Close", In_Close);

    /* **************************************** */

    IF In_Index >= 1 THEN
        SET Inner_Previous_Close =
            (SELECT cntr_double_value FROM container WHERE cntr_index = (In_Index - 1) AND cntr_class = "Func_Calc" AND cntr_name = "Copy_Close");
        /* ************************************ */
        SET Inner_Cur_Rise_Fall_Amt = (In_Close - Inner_Previous_Close);
        /* ************************************ */
        REPLACE INTO container(cntr_index, cntr_class, cntr_name, cntr_double_value) VALUES (In_Index, "Func_Calc", Inner_RSI_UD_SMA_CNTR_Name, Inner_Cur_Rise_Fall_Amt);
    ELSE
        REPLACE INTO container(cntr_index, cntr_class, cntr_name, cntr_double_value) VALUES (In_Index, "Func_Calc", Inner_RSI_UD_SMA_CNTR_Name, 0.0);
    END IF;

    /* **************************************** */

    IF In_Index >= In_Period THEN
        SET Inner_Bgn_Idx = (In_Index - In_Period + 1); /* 计算 Container 取值的起始索引(Begin Index) */
        /* ************************************ */
        SET Inner_N_Rise_Amt_Sum =
            (SELECT SUM(cntr_double_value) FROM container WHERE cntr_class = "Func_Calc" AND cntr_name = Inner_RSI_UD_SMA_CNTR_Name
                 AND Inner_Bgn_Idx <= cntr_index AND cntr_index <= In_Index AND cntr_double_value >= 0);
        SET Inner_N_Fall_Amt_Sum =
            (SELECT SUM(cntr_double_value) * (-1) FROM container WHERE cntr_class = "Func_Calc" AND cntr_name = Inner_RSI_UD_SMA_CNTR_Name
                 AND Inner_Bgn_Idx <= cntr_index AND cntr_index <= In_Index AND cntr_double_value < 0);
        /* ************************************ */
        /* 每天都是下跌, 这将导致没有Up Move的日期, 最近N天的所有的Up Move之和是0, Down Move会是某个正数,0 除以某个正数是0, 所以这种特殊情况会定义RSI为0 */
        IF Inner_N_Rise_Amt_Sum IS NULL THEN RETURN 0; /* Return Value */ END IF;
        /* 每天都是上涨, 这将导致没有Down Move的日期, 最近N天的所有的Down Move之和是0, RS会是某个正数除以0, 数学上这是非法的, 所以这种特殊情况会定义RSI为100 */
        IF Inner_N_Fall_Amt_Sum IS NULL THEN RETURN 100; /* Return Value */ END IF;
        /* ************************************ */
        SET Inner_RS = (Inner_N_Rise_Amt_Sum / In_Period) / (Inner_N_Fall_Amt_Sum / In_Period);
        /* ************************************ */
        SET Inner_RSI = (100 - 100 / (1 + Inner_RS));
        /* ************************************ */
        RETURN Inner_RSI; /* Return Value */
    ELSE
        RETURN NULL; /* Return Value */
    END IF;
    
END//

/* 删除函数: 相对强弱指标 - EMA方法 (Finance - Relative Strength Index - EMA Method) */
DROP FUNCTION IF EXISTS FUNC_FIN_RSI_EMA_METHOD//

/* 创建函数: 相对强弱指标 - EMA方法 (Finance - Relative Strength Index - EMA Method) */
CREATE FUNCTION FUNC_FIN_RSI_EMA_METHOD(In_Index INT(8), In_Period INT(4), In_Close DOUBLE(16,4)) RETURNS DOUBLE(16,4)
BEGIN

    /*
     * 相对强弱指标 RSI - EMA Method 是用以计测市场供需关系和买卖力道的方法及指标。
     *
     * RS(相对强度) = N日内收盘价所有上涨额度之和的指数平均(EMA) / N日内收盘价所有下跌额度的绝对值之和的指数平均(EMA)
     * RSI(相对强弱指标) = 100 - 100 ÷ ( 1 + RS )
     */

    /* **************************************** */

    DECLARE Inner_RSI_U_EMA_CNTR_Name CHAR(80);
    DECLARE Inner_RSI_D_EMA_CNTR_Name CHAR(80);
    DECLARE Inner_Previous_Close DOUBLE(16,4); /* Declare Local Variable: 前1日收盘价 */
    DECLARE Inner_Previous_RSI_U_EMA DOUBLE(16,4); /* Declare Local Variable: 前1日上涨额度EMA */
    DECLARE Inner_Previous_RSI_D_EMA DOUBLE(16,4); /* Declare Local Variable: 前1日下跌额度EMA */
    DECLARE Inner_RSI_U_EMA DOUBLE(16,4); /* Declare Local Variable: 上涨额度EMA值 */
    DECLARE Inner_RSI_D_EMA DOUBLE(16,4); /* Declare Local Variable: 下跌额度EMA值 */
    DECLARE Inner_Cur_Rise_Fall_Amt DOUBLE(16,4); /* Declare Local Variable: 当前索引的涨跌额度 */
    DECLARE Inner_RS DOUBLE(16,4); /* Declare Local Variable: Relative Strength */
    DECLARE Inner_RSI DOUBLE(16,4); /* Declare Local Variable: Relative Strength Index */

    /* **************************************** */

    SET Inner_RSI_U_EMA_CNTR_Name = CONCAT("RSI_", In_Period, "_U_EMA");
    SET Inner_RSI_D_EMA_CNTR_Name = CONCAT("RSI_", In_Period, "_D_EMA");

    /* **************************************** */

    REPLACE INTO container(cntr_index, cntr_class, cntr_name, cntr_double_value) VALUES (In_Index, "Func_Calc", "Copy_Close", In_Close);

    /* **************************************** */

    IF In_Index >= 1 THEN
        SET Inner_Previous_Close =
            (SELECT cntr_double_value FROM container WHERE cntr_index = (In_Index - 1) AND cntr_class = "Func_Calc" AND cntr_name = "Copy_Close");
        /* ************************************ */
        SET Inner_Previous_RSI_U_EMA =
            (SELECT cntr_double_value FROM container WHERE cntr_index = (In_Index - 1) AND cntr_class = "Func_Calc" AND cntr_name = Inner_RSI_U_EMA_CNTR_Name);
        SET Inner_Previous_RSI_D_EMA =
            (SELECT cntr_double_value FROM container WHERE cntr_index = (In_Index - 1) AND cntr_class = "Func_Calc" AND cntr_name = Inner_RSI_D_EMA_CNTR_Name);
        /* ************************************ */
        SET Inner_Cur_Rise_Fall_Amt = (In_Close - Inner_Previous_Close);
        /* ----------- INNER IF Bgn ----------- */
        IF Inner_Cur_Rise_Fall_Amt < 0 THEN
            SET Inner_Cur_Rise_Fall_Amt = (Inner_Cur_Rise_Fall_Amt * (-1));
            /* ******************************** */
            SET Inner_RSI_D_EMA = (2 / (In_Period + 1) * Inner_Cur_Rise_Fall_Amt + (In_Period + 1 - 2) / (In_Period + 1) * Inner_Previous_RSI_D_EMA);
        ELSE
            SET Inner_RSI_D_EMA = (2 / (In_Period + 1) * Inner_Cur_Rise_Fall_Amt + (In_Period + 1 - 2) / (In_Period + 1) * Inner_Previous_RSI_D_EMA);
        END IF;
        /* ----------- INNER IF End ----------- */
        SET Inner_RSI_U_EMA = (2 / (In_Period + 1) * Inner_Cur_Rise_Fall_Amt + (In_Period + 1 - 2) / (In_Period + 1) * Inner_Previous_RSI_U_EMA);
        /* ************************************ */
        REPLACE INTO container(cntr_index, cntr_class, cntr_name, cntr_double_value) VALUES (In_Index, "Func_Calc", Inner_RSI_U_EMA_CNTR_Name, Inner_RSI_U_EMA);
        REPLACE INTO container(cntr_index, cntr_class, cntr_name, cntr_double_value) VALUES (In_Index, "Func_Calc", Inner_RSI_D_EMA_CNTR_Name, Inner_RSI_D_EMA);
        /* ************************************ */
        IF Inner_RSI_U_EMA = 0 THEN RETURN 0; /* Return Value */ END IF;
        IF Inner_RSI_D_EMA = 0 THEN RETURN 100; /* Return Value */ END IF;
        /* ************************************ */
        SET Inner_RS = (Inner_RSI_U_EMA / Inner_RSI_D_EMA);
        SET Inner_RSI = (100 - 100 / (1 + Inner_RS));
        /* ************************************ */
        RETURN Inner_RSI; /* Return Value */
    ELSE
        REPLACE INTO container(cntr_index, cntr_class, cntr_name, cntr_double_value) VALUES (In_Index, "Func_Calc", Inner_RSI_U_EMA_CNTR_Name, 0.0);
        REPLACE INTO container(cntr_index, cntr_class, cntr_name, cntr_double_value) VALUES (In_Index, "Func_Calc", Inner_RSI_D_EMA_CNTR_Name, 0.0);
        /* ************************************ */
        RETURN 0.0; /* Return Value */
    END IF;
    
END//

/* 删除函数: 评估2线穿越 (Finance - Estimate 2 Line Cross) */
DROP FUNCTION IF EXISTS FUNC_FIN_EST_2_LINE_CROSS//

/* 创建函数: 评估2线穿越 (Finance - Estimate 2 Line Cross) */
CREATE FUNCTION FUNC_FIN_EST_2_LINE_CROSS(In_Index BIGINT(12), In_Orientation CHAR(10), In_Purpose CHAR(20), In_Crossing DOUBLE(16,4), In_Crossed DOUBLE(16,4)) RETURNS INT(1)
BEGIN

    /*
     * Calculate Examples:
     *
     * Active Value:
     * A1 = Crossing[-2]; 即2天前的Crossing值。
     * A2 = Crossing[-1]; 即1天前的Crossing值。
     * A3 = Crossing; 即当天的Crossing值。
     *
     * Passive Value:
     * P1 = Crossed[-2]; 即2天前的Crossed值。
     * P2 = Crossed[-1]; 即1天前的Crossed值。
     * P3 = Crossed; 即当天的Crossed值。
     *
     * 判断上穿示例:
     * A1 <  P1 ----- 2天前的穿越值小于被穿越值。
     * A2 =< P2 ----- 1天前的穿越值小于或等于被穿越值。
     * A3 >  P3 ----- 当天的穿越值大于被穿越值。
     */

    DECLARE Inner_A1 DOUBLE(16,4);
    DECLARE Inner_A2 DOUBLE(16,4);
    DECLARE Inner_A3 DOUBLE(16,4);
    DECLARE Inner_P1 DOUBLE(16,4);
    DECLARE Inner_P2 DOUBLE(16,4);
    DECLARE Inner_P3 DOUBLE(16,4);
    DECLARE Inner_Crossing_CNTR_Name CHAR(80);
    DECLARE Inner_Crossed_CNTR_Name CHAR(80);

    /* **************************************** */

    SET Inner_Crossing_CNTR_Name = CONCAT(In_Purpose, "_Crossing");
    SET Inner_Crossed_CNTR_Name = CONCAT(In_Purpose, "_Crossed");

    /* **************************************** */

    REPLACE INTO container(cntr_index, cntr_class, cntr_name, cntr_double_value) VALUES (In_Index, "Func_Calc", Inner_Crossing_CNTR_Name, In_Crossing);
    REPLACE INTO container(cntr_index, cntr_class, cntr_name, cntr_double_value) VALUES (In_Index, "Func_Calc", Inner_Crossed_CNTR_Name, In_Crossed);

    /* **************************************** */

    IF In_Index >= 3 THEN
        SET Inner_A1 =
            (SELECT cntr_double_value FROM container WHERE cntr_index = (In_Index - 2) AND cntr_class = "Func_Calc" AND cntr_name = Inner_Crossing_CNTR_Name);
        SET Inner_A2 =
            (SELECT cntr_double_value FROM container WHERE cntr_index = (In_Index - 1) AND cntr_class = "Func_Calc" AND cntr_name = Inner_Crossing_CNTR_Name);
        SET Inner_A3 = In_Crossing;
        /* ************************************ */
        SET Inner_P1 =
            (SELECT cntr_double_value FROM container WHERE cntr_index = (In_Index - 2) AND cntr_class = "Func_Calc" AND cntr_name = Inner_Crossed_CNTR_Name);
        SET Inner_P2 =
            (SELECT cntr_double_value FROM container WHERE cntr_index = (In_Index - 1) AND cntr_class = "Func_Calc" AND cntr_name = Inner_Crossed_CNTR_Name);
        SET Inner_P3 = In_Crossed;
    ELSE
        RETURN 0; /* Return Value */
    END IF;

    /* **************************************** */

    IF In_Orientation = "Down" AND Inner_A1 IS NOT NULL THEN /* NULL 的判断需要用 IS 或者 IS NOT */
        /* ----------- INNER IF Bgn ----------- */
        IF Inner_A1 > Inner_P1 AND Inner_A2 >= Inner_P2 AND Inner_A3 < Inner_P3 THEN
            RETURN 1; /* Return Value */
        ELSE
            RETURN 0; /* Return Value */
        END IF;
        /* ----------- INNER IF End ----------- */  
    ELSEIF In_Orientation = "Up" AND Inner_A1 IS NOT NULL THEN /* NULL 的判断需要用 IS 或者 IS NOT */
        /* ----------- INNER IF Bgn ----------- */
        IF Inner_A1 < Inner_P1 AND Inner_A2 <= Inner_P2 AND Inner_A3 > Inner_P3 THEN
            RETURN 1; /* Return Value */
        ELSE
            RETURN 0; /* Return Value */
        
        END IF;
        /* ----------- INNER IF End ----------- */
    ELSE
        RETURN 0; /* Return Value */
    END IF;
    
END//

/* 删除函数: 评估2值大小对比 (Finance - Estimate 2 Value Compare Size) */
DROP FUNCTION IF EXISTS FUNC_FIN_EST_2_VALUE_COMPARE_SIZE//

/* 创建函数: 评估2值大小对比 (Finance - Estimate 2 Value Compare Size) */
CREATE FUNCTION FUNC_FIN_EST_2_VALUE_COMPARE_SIZE(In_Larger_Or_Smaller VARCHAR(10), In_Compare DOUBLE(16,4), In_Compared DOUBLE(16,4)) RETURNS INT(1)
BEGIN

    IF In_Compare IS NULL OR In_Compared IS NULL THEN /* NULL 的判断需要用 IS 或者 IS NOT */
        RETURN 0; /* Return Value */
    END IF;
    
    /* **************************************** */

    IF In_Larger_Or_Smaller = "Larger" THEN
        /* ----------- INNER IF Bgn ----------- */
        IF In_Compare > In_Compared THEN
            RETURN 1; /* Return Value */

        ELSE
            RETURN 0; /* Return Value */
        END IF;
        /* ----------- INNER IF End ----------- */
    ELSEIF In_Larger_Or_Smaller = "Smaller" THEN
        /* ----------- INNER IF Bgn ----------- */
        IF In_Compare < In_Compared THEN
            RETURN 1; /* Return Value */
        ELSE
            RETURN 0; /* Return Value */
        END IF;
        /* ----------- INNER IF End ----------- */
    ELSE
        RETURN 0; /* Return Value */
    END IF;
    
END//

/* 删除函数: 评估值的所在区间 (Finance - Estimate Value Whithin Range) */
DROP FUNCTION IF EXISTS FUNC_FIN_EST_VALUE_WHITHIN_RANGE//

/* 创建函数: 评估值的所在区间 (Finance - Estimate Value Whithin Range) */
CREATE FUNCTION FUNC_FIN_EST_VALUE_WHITHIN_RANGE(In_Upper_Bound DOUBLE(16,4), In_Lower_Bound DOUBLE(16,4), In_Value DOUBLE(16,4)) RETURNS INT(1)
BEGIN

    IF In_Value IS NULL OR In_Compared_Value IS NULL THEN /* NULL 的判断需要用 IS 或者 IS NOT */
        RETURN 0; /* Return Value */
    END IF;
    
    /* **************************************** */

    IF In_Lower_Bound <= In_Value AND In_Value <= In_Upper_Bound THEN
        RETURN 1; /* Return Value */
    ELSE
        RETURN 0; /* Return Value */
    END IF;
    
END//

/* 改回语句结束符为 ";" */
DELIMITER ;

/* -------------------------------------------------- */
/* EOF */
