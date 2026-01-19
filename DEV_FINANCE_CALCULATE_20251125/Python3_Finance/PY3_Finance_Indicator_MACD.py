# GF_PY3_CLASS/Python3_Finance/PY3_Finance_Indicator_MACD.py
# Create By GF 2024-01-22 18:16

class PY3_Finance_Indicator_MACD(object):

    def __init__(self):

        self.JSON_Digit_of_Previous_MACD_DEA:float = None

    def MACD_DIF(self, EMA12:float, EMA26:float) -> float:

        # 异同移动平均线 - DIF (Moving Average Convergence / Divergence - DIF)
        #
        # 公式: MACD_DIF = 当日 EMA(12) - 当日 EMA(26)
        # 12 日 EMA 和 26 日 EMA 通常是 MACD 的常用值, 如要修改 MACD 的观测参数, 则修改对应的 EMA 数值。

        MACD_DIF_Value = EMA12 - EMA26
        # ..........................................
        return round(MACD_DIF_Value, 4)

    def MACD_DEA(self, Seq:int, MACD_DIF:float) -> float:

        # 异同移动平均线 - DEA (Moving Average Convergence / Divergence - DEA)
        #
        # 注意: 首日 DEA 直接使用 0 值。
        # ..........................................
        # DEA 又叫: 计算 DIF 的 9 日EMA。
        # 根据离差值计算其 9 日的 EMA, 即离差平均值, 是所求的 MACD 值。为了不与指标原名相混淆, 此值又名 DEA。
        # 公式: 当日 DEA = 2 / (9 + 1) * 当日 DIF + (9 + 1 - 2) / (9 + 1) * 前日 DEA。
        # 首日 DEA 由于没有昨日 DEA 数据, 所以首日 DEA 直接使用 0 值。

        if (Seq == 1):

            self.JSON_Digit_of_Previous_MACD_DEA = None  # 从第 1 行开始执行函数时先重置公共变量。
            # ......................................
            MACD_DEA_Value:float = 0.0
            # ......................................
            # 将 Current MACD DEA Value 赋值到 Previous MACD DEA Value, 以备下 1 行使用。
            self.JSON_Digit_of_Previous_MACD_DEA = MACD_DEA_Value
            # ......................................
            return round(MACD_DEA_Value, 4)

        if (Seq >= 2):

            MACD_DEA_Value:float = 2 / (9 + 1) * MACD_DIF + (9 + 1 - 2) / (9 + 1) * self.JSON_Digit_of_Previous_MACD_DEA
            # ......................................
            # 将 Current MACD DEA Value 赋值到 Previous MACD DEA Value, 以备下 1 行使用。
            self.JSON_Digit_of_Previous_MACD_DEA = MACD_DEA_Value
            # ......................................
            return round(MACD_DEA_Value, 4)

    def MACD_STICK(self, MACD_DIF:float, MACD_DEA:float) -> float:

        # 异同移动平均线 - STICK (Moving Average Convergence / Divergence - STICK)
        #
        # 用 (DIF - DEA) x 2 即为 MACD 柱状图, 一般称作 MACD 或 STICK。
        # 公式: MACD_STICK(MACD) = (MACD_DIF - MACD_DEA) * 2

        MACD_STICK_Value = (MACD_DIF - MACD_DEA) * 2
        # ..........................................
        return round(MACD_STICK_Value, 4)

# EOF Signed by GF.
