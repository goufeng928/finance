# GF_PY3_CLASS/Python3_Finance/PY3_Finance_Indicator_EMA.py
# Create By GF 2024-01-22 18:16

class PY3_Finance_Indicator_EMA(object):

    def __init__(self):

        self.JSON_Digit_of_Previous_EMA:float = None

    def EMA(self, Seq:int, Period:int, Close:float) -> float:

        # 指数移动平均 (Exponential Moving Average)
        #
        # 注意: 首日EMA直接使用当日收盘价。
        # ..........................................
        # 公式: EMA = 当日收盘价 * 2 / (N + 1) + 前一日 EMA * (N - 1) / (N + 1)
        # ..........................................
        # 以计算 12 日 EMA 举例:
        # 其中 [i] 代表当日日期。
        # EMA12 = 2 / (12 + 1) * Close[i] + (12 + 1 - 2) / (12 + 1) * EMA12[i - 1]
        # 首日 EMA 由于没有昨日 EMA 数据, 所以首日 EMA 直接使用当日收盘价。

        if (Seq == 1):

            self.JSON_Digit_of_Previous_EMA = None  # 从第 1 行开始执行函数时先重置公共变量。
            # ......................................
            EMA_Value:float = Close
            # ......................................
            # 将 Current EMA Value 赋值到 Previous EMA Value, 以备下 1 行使用。
            self.JSON_Digit_of_Previous_EMA = EMA_Value
            # ......................................
            return round(EMA_Value, 4)

        if (Seq >= 2):

            EMA_Value:float = 2 / (Period + 1) * Close + (Period + 1 - 2) / (Period + 1) * self.JSON_Digit_of_Previous_EMA
            # ......................................
            # 将 Current EMA Value 赋值到 Previous EMA Value, 以备下 1 行使用。
            self.JSON_Digit_of_Previous_EMA = EMA_Value
            # ......................................
            return round(EMA_Value, 4)

# EOF Signed by GF.
