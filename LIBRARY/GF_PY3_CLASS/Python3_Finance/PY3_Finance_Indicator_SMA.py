# GF_PY3_CLASS/Python3_Finance/PY3_Finance_Indicator_SMA.py
# Create By GF 2025-08-07 16:05

class PY3_Finance_Indicator_SMA(object):

    def __init__(self):

        self.JSON_Queue_of_Close:list = []

    def SMA(self, Seq:int, Period:int, Close:float) -> float:

        # 简单移动平均 (Simple Moving Average)
        # Example:
        # >>> OBJ = PY3_Finance_Indicator_SMA()
        # >>> print( OBJ.SMA(Seq = 1, Period = 5, Close = 1) )
        # >>> print( OBJ.SMA(Seq = 2, Period = 5, Close = 2) )
        # >>> print( OBJ.SMA(Seq = 3, Period = 5, Close = 3) )
        # >>> print( OBJ.SMA(Seq = 4, Period = 5, Close = 4) )
        # >>> print( OBJ.SMA(Seq = 5, Period = 5, Close = 5) )
        # None
        # None
        # None
        # None
        # >>> print( OBJ.SMA.JSON_Queue_of_Close )
        # 3.0
        # [1, 2, 3, 4, 5]
        # >>> print( OBJ.SMA(Seq = 1, Period = 3, Close = 6) )
        # >>> print( OBJ.SMA(Seq = 2, Period = 3, Close = 7) )
        # >>> print( OBJ.SMA(Seq = 3, Period = 3, Close = 8) )
        # None
        # None
        # 7.0
        # >>> print( OBJ.JSON_Queue_of_Close )
        # [6, 7, 8]

        if (1 == Seq):
            self.JSON_Queue_of_Close.clear()
            self.JSON_Queue_of_Close.append(Close)
            # ......................................
            return None

        if (2 <= Seq and Seq <= (Period - 1)):
            # 以 MA(Period = 5) 为例, 此条件等同于:
            # 2 =< Seq =< 4 (符号 "<=" 为程序中的 "小于等于", 符号 "=<" 为数学中的 "小于等于")
            self.JSON_Queue_of_Close.append(Close)
            # ......................................
            return None

        if (Seq == Period):
            self.JSON_Queue_of_Close.append(Close)
            SMA_Value = sum(self.JSON_Queue_of_Close) / Period
            # ......................................
            return round(SMA_Value, 4)

        if (Seq >= (Period + 1)):
            TRASH = self.JSON_Queue_of_Close.pop(0)  # 使用 list().pop(0) 弹出列表中第 1 个元素
            self.JSON_Queue_of_Close.append(Close)
            SMA_Value = sum(self.JSON_Queue_of_Close) / Period
            # ......................................
            return round(SMA_Value, 4)

# EOF Signed by GF.
