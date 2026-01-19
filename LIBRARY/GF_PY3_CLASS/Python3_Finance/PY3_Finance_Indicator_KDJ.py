# GF_PY3_CLASS/Python3_Finance/PY3_Finance_Indicator_KDJ.py
# Create By GF 2024-01-22 18:16

class PY3_Finance_Indicator_KDJ(object):

    def __init__(self):

        self.JSON_Queue_of_High:list = []
        self.JSON_Queue_of_Low:list = []
        self.JSON_Queue_of_Close:list = []
        self.JSON_Queue_of_KDJ_K:list = []
        self.JSON_Queue_of_KDJ_D:list = []

    def KDJ_RSV(self, Seq:int, Period:int, High:float, Low:float, Close:float) -> float:

        # KDJ 随机指标 - RSV (KDJ Stochastic Oscillator - RSV)
        #
        # RSV 是指当日收盘价与过去一段时间的最低价和最高价之间的比值。
        # 计算条件: 股票在过去 9 个交易日的收盘价数据已知。
        # RSV 是衡量最近 N 天内 (例如 9 天) 收盘价相对于这 N 天最高价和最低价的位置的指标。其计算方法大致可以理解为:
        # RSV = (最近 N 天的收盘价 - 最近 N 天的最低价) / (最近 N 天的最高价 - 最近 N 天的最低价) * 100
        # 注意: 这里的乘 100 是为了将结果从 0 - 1 的数值转换为 0 - 100 的数值，方便观察。

        if (Seq == 1):

            self.JSON_Queue_of_High.clear()
            self.JSON_Queue_of_Low.clear()
            self.JSON_Queue_of_Close.clear()
            # ......................................
            self.JSON_Queue_of_High.append(High)
            self.JSON_Queue_of_Low.append(Low)
            self.JSON_Queue_of_Close.append(Close)
            # ......................................
            return None

        elif (1 < Seq and Seq < Period):

            self.JSON_Queue_of_High.append(High)
            self.JSON_Queue_of_Low.append(Low)
            self.JSON_Queue_of_Close.append(Close)
            # ......................................
            return None

        else:

            self.JSON_Queue_of_High.append(High)
            self.JSON_Queue_of_Low.append(Low)
            self.JSON_Queue_of_Close.append(Close)
            # ......................................
            Python_Subscript = (Seq - 1) # -> 由于行号索引是从 1 开始, 但 Python 列表索引是从 0 开始, 所以需要减去 1。
            # ......................................
            Min_Within_Period = min(self.JSON_Queue_of_Low[(Python_Subscript + 1 - Period):(Python_Subscript + 1)]) # -> 周期内(例如 9 日)最小值。
            Max_Within_Period = max(self.JSON_Queue_of_High[(Python_Subscript + 1 - Period):(Python_Subscript + 1)]) # -> 周期内(例如 9 日)最大值。
            # ......................................
            RSV:float = (Close - Min_Within_Period) / (Max_Within_Period - Min_Within_Period) * 100
            # ......................................
            return round(RSV, 4)

    def KDJ_K(self, Seq:int, RSV_Prd:int, K_Prd:int, High:float, Low:float, Close:float) -> float:

        # KDJ 随机指标 - K (KDJ Stochastic Oscillator - K)
        #
        # K 值是 RSV 的平滑值, 通常使用前一天的 K 值和当天的 RSV 值来计算。一个简化的计算方法是:
        # 当天 K 值 = 前一天的 K 值 * 2/3 + 当天的 RSV 值 * 1/3
        # 注意: 这里的 2/3 和 1/3 是平滑系数, 实际计算中可能会有所不同。
        # 在实际计算中, 如果没有前一日的 K 值数据, 通常会使用初始值, 如 50%。

        # Calling Other Function.
        RSV = self.KDJ_RSV(Seq = Seq, Period = RSV_Prd, High = High, Low = Low, Close = Close)
        
        if (Seq == 1):

            self.JSON_Queue_of_KDJ_K.clear()
            # ......................................
            self.JSON_Queue_of_KDJ_K.append(50)
            # ......................................
            return 50

        elif (1 < Seq and Seq < RSV_Prd): # -> RSV 值为空的时候均不计算, 因为 K 值计算依赖于 RSV 值。

            self.JSON_Queue_of_KDJ_K.append(50)
            # ......................................
            return 50

        else:

            Python_Subscript = (Seq - 1) # -> 由于行号索引是从 1 开始, 但 Python 列表索引是从 0 开始, 所以需要减去 1。
            # ......................................
            Smoothing_Factor:float = (1 / K_Prd) # 计算平滑系数(Smoothing Factor)。
            # ......................................
            K_Val = Smoothing_Factor * RSV + (1 - Smoothing_Factor) * self.JSON_Queue_of_KDJ_K[Python_Subscript - 1]
            # ......................................
            self.JSON_Queue_of_KDJ_K.append(K_Val)
            # ......................................
            return round(K_Val, 4)

    def KDJ_D(self, Seq:int, RSV_Prd:int, D_Prd:int, K_Val:float) -> float:

        # KDJ 随机指标 - D (KDJ Stochastic Oscillator - D)
        #
        # D 值是 K 值的进一步平滑, 用于减缓 K 值的波动。其计算方法类似于 K 值, 但通常使用更长的平滑周期:
        # 当天 D 值 = 前一天的 D 值 * 2/3 + 当天的 K 值 * 1/3
        # 注意: 这里的 2/3 和 1/3 是平滑系数, 实际计算中可能会有所不同。
        # 在实际计算中, 如果没有前一日的 D 值数据, 通常会使用初始值, 如 50%。

        if (Seq == 1):

            self.JSON_Queue_of_KDJ_D.clear()
            # ......................................
            self.JSON_Queue_of_KDJ_D.append(50)
            # ......................................
            return 50

        elif (1 < Seq and Seq < RSV_Prd): # -> RSV 值为空的时候均不计算, 因为 K 值计算依赖于 RSV, 而 D 值计算依赖于 K 值。

            self.JSON_Queue_of_KDJ_D.append(50)
            # ......................................
            return 50

        else:

            Python_Subscript = (Seq - 1) # -> 由于行号索引是从 1 开始, 但 Python 列表索引是从 0 开始, 所以需要减去 1。
            # ......................................
            Smoothing_Factor:float = (1 / D_Prd) # 计算平滑系数 (Smoothing Factor)。
            # ......................................
            D_Val = Smoothing_Factor * K_Val + (1 - Smoothing_Factor) * self.JSON_Queue_of_KDJ_D[Python_Subscript - 1]
            # ......................................
            self.JSON_Queue_of_KDJ_D.append(D_Val)
            # ......................................
            return round(D_Val, 4)

    def KDJ_J(self, K_Val:float, D_Val:float) -> float:

        # KDJ 随机指标 - J (KDJ Stochastic Oscillator - J)
        #
        # J 值是 KDJ 指标中的方向敏感线, 用于反映市场趋势的强弱。它通常是通过 K 值和 D 值的某种组合来计算的, 例如:
        # 当天 J 值 = 3 * 当天 K 值 - 2 * 当天 D 值

        # ......................................----
        J_Val = 3 * K_Val - 2 * D_Val
        # ......................................
        return round(J_Val, 4)

# EOF Signed by GF.
