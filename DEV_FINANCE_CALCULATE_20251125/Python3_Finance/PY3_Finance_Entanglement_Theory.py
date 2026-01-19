# GF_PY3_CLASS/Python3_Finance/PY3_Finance_Entanglement_Theory.py
# Create By GF 2024-01-22 18:16

class PY3_Finance_Entanglement_Theory(object):

    def __init__(self):

        self.TRS_Left_Exists:int = 0
        self.TRS_Top_Exists:int = 0
        # ..........................................
        self.BRS_Left_Exists:int = 0
        self.BRS_Bottom_Exists:int = 0
        # ..........................................
        self.TRS_Left_UpperEdge:float = None
        self.TRS_Left_LowerEdge:float = None
        # ..........................................
        self.BRS_Left_UpperEdge:float = None
        self.BRS_Left_LowerEdge:float = None
        # ..........................................
        self.TRS_Top_UpperEdge:float = None
        self.TRS_Top_LowerEdge:float = None
        # ..........................................
        self.BRS_Bottom_UpperEdge:float = None
        self.BRS_Bottom_LowerEdge:float = None
        # ..........................................
        self.TRS_Group_Top = 1
        self.BRS_Group_Top = 1

    def Top_Reversal_Shape(self, Seq:int, UpperEdge:float, LowerEdge:float) -> int:

        # 顶分型 (Top Reversal Shape)
        #
        # Example:
        #
        # >>> print(df)
        #    seq        date       code   open   high    low  close  mark
        # 0    1  2024-04-25  001696.SZ  11.71  11.88  11.25  11.40  None
        # 1    2  2024-04-26  001696.SZ  12.05  12.54  12.05  12.54  None
        # 2    3  2024-04-29  001696.SZ  12.94  13.29  12.20  13.03   TRS
        # 3    4  2024-04-30  001696.SZ  12.40  12.50  11.73  11.73  None
        # 4    5  2024-05-06  001696.SZ  10.99  11.84  10.99  11.46  None
        # 5    6  2024-05-07  001696.SZ  11.80  12.61  11.65  12.61  None
        # 6    7  2024-05-08  001696.SZ  12.00  13.01  11.89  12.73   TRS
        # 7    8  2024-05-09  001696.SZ  12.75  12.80  11.81  12.31  None
        # 8    9  2024-05-10  001696.SZ  12.10  12.20  11.43  11.57  None
        #
        # >>> df["TRS"] = df.apply(
        # ...     lambda x: Top_Reversal_Shape(x["seq"], x["high"], x["low"]),
        # ...     axis=1
        # ... )
        # ... print(df)
        #    seq        date       code   open   high    low  close  mark  TRS
        # 0    1  2024-04-25  001696.SZ  11.71  11.88  11.25  11.40  None    0
        # 1    2  2024-04-26  001696.SZ  12.05  12.54  12.05  12.54  None    0
        # 2    3  2024-04-29  001696.SZ  12.94  13.29  12.20  13.03   TRS    1
        # 3    4  2024-04-30  001696.SZ  12.40  12.50  11.73  11.73  None    0
        # 4    5  2024-05-06  001696.SZ  10.99  11.84  10.99  11.46  None    0
        # 5    6  2024-05-07  001696.SZ  11.80  12.61  11.65  12.61  None    0
        # 6    7  2024-05-08  001696.SZ  12.00  13.01  11.89  12.73   TRS    1
        # 7    8  2024-05-09  001696.SZ  12.75  12.80  11.81  12.31  None    0
        # 8    9  2024-05-10  001696.SZ  12.10  12.20  11.43  11.57  None    0

        if ((Seq == 1) or (self.TRS_Left_Exists == 0)):

            # 当前为第 1 根 K 线, 或者 [顶分型左侧] 不存在。

            CURR_UpperEdge:float = UpperEdge # -> 可能多余的步骤(仅用于表达传递关系)。
            CURR_LowerEdge:float = LowerEdge # -> 可能多余的步骤(仅用于表达传递关系)。

            self.TRS_Left_UpperEdge = CURR_UpperEdge
            self.TRS_Left_LowerEdge = CURR_LowerEdge

            self.TRS_Left_Exists = 1
            self.TRS_Top_Exists = 0

            return 0

        if ((Seq == 2) or ((self.TRS_Left_Exists == 1) and (self.TRS_Top_Exists == 0))):

            # 当前为第 2 根 K 线, 或者 [分型左侧] 存在 并且 [分型顶部] 不存在。

            CURR_UpperEdge:float = UpperEdge
            CURR_LowerEdge:float = LowerEdge

            if (CURR_UpperEdge  > self.TRS_Left_UpperEdge):

                # [当前 K 线 (CURR) 上沿] 大于 [顶分型左侧上沿]。

                if (CURR_LowerEdge  > self.TRS_Left_LowerEdge):

                    # 分型顶部成立。

                    self.TRS_Top_UpperEdge = CURR_UpperEdge
                    self.TRS_Top_LowerEdge = CURR_LowerEdge
                    self.TRS_Top_Exists = 1

                    return 0

                if (CURR_LowerEdge <= self.TRS_Left_LowerEdge):

                    # [当前 K 线 (CURR)] 包含 [顶分型左侧], 包含关系。

                    self.TRS_Left_UpperEdge = CURR_UpperEdge
                    self.TRS_Left_LowerEdge = CURR_LowerEdge

                    return 0

            if (CURR_UpperEdge == self.TRS_Left_UpperEdge):

                # [当前 K 线 (CURR) 上沿] 等于 [顶分型左侧上沿]。

                if (CURR_LowerEdge >= self.TRS_Left_LowerEdge):

                    # [当前 K 线 (CURR)] 被 [顶分型左侧] 包含, 被包含关系。

                    return 0

                if (CURR_LowerEdge  < self.TRS_Left_LowerEdge):

                    # [当前 K 线 (CURR)] 包含 [顶分型左侧], 包含关系。

                    self.TRS_Left_UpperEdge = CURR_UpperEdge # -> 可能多余的步骤(仅用于表达逻辑关系)。
                    self.TRS_Left_LowerEdge = CURR_LowerEdge

                    return 0

            if (CURR_UpperEdge  < self.TRS_Left_UpperEdge):

                # [当前 K 线 (CURR) 上沿] 小于 [顶分型左侧上沿]。

                if (CURR_LowerEdge >= self.TRS_Left_LowerEdge):

                    # [当前 K 线 (CURR)] 被 [顶分型左侧] 包含, 被包含关系。

                    return 0

                if (CURR_LowerEdge  < self.TRS_Left_LowerEdge):

                    # [分型底部] 成立, 重置分型左侧。
                    # 在判断顶分型的函数中, 排除底分型相关结论, 重置 [分型左侧] 上下沿。

                    self.TRS_Left_UpperEdge = CURR_UpperEdge
                    self.TRS_Left_LowerEdge = CURR_LowerEdge

                    return 0

        if ((Seq >= 3) and ((self.TRS_Left_Exists == 1) and (self.TRS_Top_Exists == 1))):

            # 当前为第 3 根或之后的 K 线, 并且 [分型左侧] 和 [分型顶部] 都存在。

            CURR_UpperEdge:float = UpperEdge
            CURR_LowerEdge:float = LowerEdge

            if (CURR_UpperEdge  > self.TRS_Top_UpperEdge):

                # [当前 K 线 (CURR) 上沿] 大于 [顶分型顶部上沿]。

                if (CURR_LowerEdge  > self.TRS_Top_LowerEdge) and (CURR_LowerEdge  > self.TRS_Left_LowerEdge):

                    # 新的 [分型顶部上边沿] 和 [分型顶部下边沿] 以及 新的 [分型左侧上边沿] 和 [分型左侧下边沿]。

                    self.TRS_Left_UpperEdge = self.TRS_Top_UpperEdge
                    self.TRS_Left_LowerEdge = self.TRS_Top_LowerEdge
                    # ..............................
                    self.TRS_Top_UpperEdge = CURR_UpperEdge
                    self.TRS_Top_LowerEdge = CURR_LowerEdge

                    return 0

                if (CURR_LowerEdge == self.TRS_Top_LowerEdge) and (CURR_LowerEdge  > self.TRS_Left_LowerEdge):

                    # 新的 [分型顶部上边沿]。

                    self.TRS_Top_UpperEdge = CURR_UpperEdge

                    return 0

                if (CURR_LowerEdge  < self.TRS_Top_LowerEdge) and (CURR_LowerEdge >= self.TRS_Left_LowerEdge):

                    # [当前 K 线 (CURR)] 包含 [顶分型顶部], 包含关系。

                    self.TRS_Top_UpperEdge = CURR_UpperEdge
                    self.TRS_Top_LowerEdge = CURR_LowerEdge

                    return 0

                if (CURR_LowerEdge  < self.TRS_Top_LowerEdge) and (CURR_LowerEdge  < self.TRS_Left_LowerEdge):

                    # [顶分型] 成立。

                    self.TRS_Left_Exists = 0
                    self.TRS_Top_Exists = 0 # -> 可能多余的步骤(仅用于表达逻辑关系)。

                    return 1

            if (CURR_UpperEdge == self.TRS_Top_UpperEdge):

                # [当前 K 线 (CURR) 上沿] 等于 [顶分型顶部上沿]。

                if (CURR_LowerEdge >= self.TRS_Top_LowerEdge) and (CURR_LowerEdge  > self.TRS_Left_LowerEdge):

                    # [当前 K 线 (CURR)] 被 [顶分型顶部] 包含, 被包含关系。

                    return 0

                if (CURR_LowerEdge  < self.TRS_Top_LowerEdge) and (CURR_LowerEdge >= self.TRS_Left_LowerEdge):

                    # [当前 K 线 (CURR)] 包含 [顶分型顶部], 包含关系。

                    self.TRS_Top_UpperEdge = CURR_UpperEdge # -> 可能多余的步骤(仅用于表达逻辑关系)。
                    self.TRS_Top_LowerEdge = CURR_LowerEdge

                    return 0

                if (CURR_LowerEdge  < self.TRS_Top_LowerEdge) and (CURR_LowerEdge  < self.TRS_Left_LowerEdge):

                    # [顶分型] 成立。

                    self.TRS_Left_Exists = 0
                    self.TRS_Top_Exists = 0 # -> 可能多余的步骤(仅用于表达逻辑关系)。

                    return 1

            if (CURR_UpperEdge  < self.TRS_Top_UpperEdge):

                # [当前 K 线 (CURR) 上沿] 小于 [顶分型顶部上沿]。

                if (CURR_LowerEdge >= self.TRS_Top_LowerEdge) and (CURR_LowerEdge  > self.TRS_Left_LowerEdge):

                    # [当前 K 线 (CURR)] 被 [顶分型顶部] 包含, 被包含关系。

                    return 0

                if (CURR_LowerEdge  < self.TRS_Top_LowerEdge) and (CURR_LowerEdge >= self.TRS_Left_LowerEdge):

                    # 新的 [分型顶部下边沿]。

                    self.TRS_Top_LowerEdge = CURR_LowerEdge

                    return 0

                if (CURR_LowerEdge  < self.TRS_Top_LowerEdge) and (CURR_LowerEdge  < self.TRS_Left_LowerEdge):

                    # [顶分型] 成立。

                    self.TRS_Left_Exists = 0
                    self.TRS_Top_Exists = 0 # -> 可能多余的步骤(仅用于表达逻辑关系)。

                    return 1

    def Bottom_Reversal_Shape(self, Seq:int, UpperEdge:float, LowerEdge:float) -> int:

        # 底分型 (Bottom Reversal Shape)
        #
        # Example:
        #
        # >>> print(df)
        #     seq        date       code   open   high    low  close  mark
        #  0    1  2024-04-30  001696.SZ  12.40  12.50  11.73  11.73  None
        #  1    2  2024-05-06  001696.SZ  10.99  11.84  10.99  11.46  None
        #  2    3  2024-05-07  001696.SZ  11.80  12.61  11.65  12.61   BRS
        #  3    4  2024-05-08  001696.SZ  12.00  13.01  11.89  12.73  None
        #  4    5  2024-05-09  001696.SZ  12.75  12.80  11.81  12.31  None
        #  5    6  2024-05-10  001696.SZ  12.10  12.20  11.43  11.57  None
        #  6    7  2024-05-13  001696.SZ  11.20  11.74  11.00  11.71  None
        #  7    8  2024-05-14  001696.SZ  11.84  11.87  11.38  11.44  None
        #  8    9  2024-05-15  001696.SZ  11.31  11.87  11.21  11.47  None
        #  9   10  2024-05-16  001696.SZ  11.45  11.97  11.41  11.75  None
        # 10   11  2024-05-17  001696.SZ  12.02  12.93  11.44  12.93   BRS
        #
        # >>> df["BRS"] = df.apply(
        # ...     lambda x: Bottom_Reversal_Shape(x["seq"], x["high"], x["low"]),
        # ...     axis=1
        # ...  )
        # >>> print(df)
        #     seq        date       code   open   high    low  close  mark  BRS
        #  0    1  2024-04-30  001696.SZ  12.40  12.50  11.73  11.73  None    0
        #  1    2  2024-05-06  001696.SZ  10.99  11.84  10.99  11.46  None    0
        #  2    3  2024-05-07  001696.SZ  11.80  12.61  11.65  12.61   BRS    1
        #  3    4  2024-05-08  001696.SZ  12.00  13.01  11.89  12.73  None    0
        #  4    5  2024-05-09  001696.SZ  12.75  12.80  11.81  12.31  None    0
        #  5    6  2024-05-10  001696.SZ  12.10  12.20  11.43  11.57  None    0
        #  6    7  2024-05-13  001696.SZ  11.20  11.74  11.00  11.71  None    0
        #  7    8  2024-05-14  001696.SZ  11.84  11.87  11.38  11.44  None    0
        #  8    9  2024-05-15  001696.SZ  11.31  11.87  11.21  11.47  None    0
        #  9   10  2024-05-16  001696.SZ  11.45  11.97  11.41  11.75  None    0
        # 10   11  2024-05-17  001696.SZ  12.02  12.93  11.44  12.93   BRS    1

        if ((Seq == 1) or (self.BRS_Left_Exists == 0)):

            # 当前为第 1 根 K 线, 或者 [顶分型左侧] 不存在。

            CURR_UpperEdge:float = UpperEdge # -> 可能多余的步骤(仅用于表达传递关系)。
            CURR_LowerEdge:float = LowerEdge # -> 可能多余的步骤(仅用于表达传递关系)。

            self.BRS_Left_UpperEdge = CURR_UpperEdge
            self.BRS_Left_LowerEdge = CURR_LowerEdge

            self.BRS_Left_Exists = 1
            self.BRS_Bottom_Exists = 0

            return 0

        if ((Seq == 2) or ((self.BRS_Left_Exists == 1) and (self.BRS_Bottom_Exists == 0))):

            # 当前为第 2 根 K 线, 或者 [分型左侧] 存在 并且 [分型底部] 不存在。

            CURR_UpperEdge:float = UpperEdge
            CURR_LowerEdge:float = LowerEdge

            if (CURR_LowerEdge  > self.BRS_Left_LowerEdge):

                # [当前 K 线 (CURR) 下沿] 大于 [底分型左侧下沿]。

                if (CURR_UpperEdge <= self.BRS_Left_UpperEdge):

                    # [当前 K 线 (CURR)] 被 [底分型左侧] 包含, 被包含关系。

                    return 0

                if (CURR_UpperEdge  > self.BRS_Left_UpperEdge):

                    # [分型顶部] 成立, 重置分型左侧。
                    # 在判断底分型的函数中, 排除顶分型相关结论, 重置 [分型左侧] 上下沿。

                    self.BRS_Left_UpperEdge = CURR_UpperEdge
                    self.BRS_Left_LowerEdge = CURR_LowerEdge

                    return 0

            if (CURR_LowerEdge == self.BRS_Left_LowerEdge):

                # [当前 K 线 (CURR) 下沿] 等于 [底分型左侧下沿]。

                if (CURR_UpperEdge <= self.BRS_Left_UpperEdge):

                    # [当前 K 线 (CURR)] 被 [底分型左侧] 包含, 被包含关系。

                    return 0

                if (CURR_UpperEdge  > self.BRS_Left_UpperEdge):

                    # [当前 K 线 (CURR)] 包含 [底分型左侧], 包含关系。

                    self.BRS_Left_UpperEdge = CURR_UpperEdge
                    self.BRS_Left_LowerEdge = CURR_LowerEdge # -> 可能多余的步骤(仅用于表达逻辑关系)。

                    return 0

            if (CURR_LowerEdge  < self.BRS_Left_LowerEdge):

                # [当前 K 线 (CURR) 下沿] 小于 [底分型左侧下沿]。

                if (CURR_UpperEdge  < self.BRS_Left_UpperEdge):

                    # 分型底部成立。

                    self.BRS_Bottom_UpperEdge = CURR_UpperEdge
                    self.BRS_Bottom_LowerEdge = CURR_LowerEdge
                    self.BRS_Bottom_Exists = 1

                    return 0

                if (CURR_UpperEdge >= self.BRS_Left_UpperEdge):

                    # [当前 K 线 (CURR)] 包含 [底分型左侧], 包含关系。

                    self.BRS_Left_UpperEdge = CURR_UpperEdge
                    self.BRS_Left_LowerEdge = CURR_LowerEdge

                    return 0

        if ((Seq >= 3) and ((self.BRS_Left_Exists == 1) and (self.BRS_Bottom_Exists == 1))):

            # 当前为第 3 根或之后的 K 线, 并且 [分型左侧] 和 [分型底部] 都存在。

            CURR_UpperEdge:float = UpperEdge
            CURR_LowerEdge:float = LowerEdge

            if (CURR_LowerEdge  > self.BRS_Bottom_LowerEdge):

                # [当前 K 线 (CURR) 下沿] 大于 [底分型底部下沿]。

                if (CURR_UpperEdge <= self.BRS_Bottom_UpperEdge) and (CURR_UpperEdge  < self.BRS_Left_UpperEdge):

                    # [当前 K 线 (CURR)] 被 [底分型底部] 包含, 被包含关系。

                    return 0

                if (CURR_UpperEdge  > self.BRS_Bottom_UpperEdge) and (CURR_UpperEdge <= self.BRS_Left_UpperEdge):

                    # 新的 [底分型底部上边沿]。

                    self.BRS_Bottom_UpperEdge = CURR_UpperEdge

                    return 0

                if (CURR_UpperEdge  > self.BRS_Bottom_UpperEdge) and (CURR_UpperEdge  > self.BRS_Left_UpperEdge):

                    # [底分型] 成立。

                    self.BRS_Left_Exists = 0
                    self.BRS_Bottom_Exists = 0 # -> 可能多余的步骤(仅用于表达逻辑关系)。

                    return 1

            if (CURR_LowerEdge == self.BRS_Bottom_LowerEdge):

                # [当前 K 线 (CURR) 下沿] 等于 [底分型底部下沿]。

                if (CURR_UpperEdge <= self.BRS_Bottom_UpperEdge) and (CURR_UpperEdge  < self.BRS_Left_UpperEdge):

                    # [当前 K 线 (CURR)] 被 [底分型底部] 包含, 被包含关系。

                    return 0

                if (CURR_UpperEdge  > self.BRS_Bottom_UpperEdge) and (CURR_UpperEdge <= self.BRS_Left_UpperEdge):

                    # [当前 K 线 (CURR)] 包含 [底分型底部], 包含关系。

                    self.BRS_Bottom_UpperEdge = CURR_UpperEdge
                    self.BRS_Bottom_LowerEdge = CURR_LowerEdge # -> 可能多余的步骤(仅用于表达逻辑关系)。

                    return 0

                if (CURR_UpperEdge  > self.BRS_Bottom_UpperEdge) and (CURR_UpperEdge  > self.BRS_Left_UpperEdge):

                    # [底分型] 成立。

                    self.BRS_Left_Exists = 0
                    self.BRS_Bottom_Exists = 0 # -> 可能多余的步骤(仅用于表达逻辑关系)。

                    return 1

            if (CURR_LowerEdge  < self.BRS_Bottom_LowerEdge):

                # [当前 K 线 (CURR) 下沿] 小于 [底分型底部下沿]。

                if (CURR_UpperEdge  < self.BRS_Bottom_UpperEdge) and (CURR_UpperEdge  < self.BRS_Left_UpperEdge):

                    # 新的 [分型底部上边沿] 和 [分型底部下边沿] 以及 新的 [分型左侧上边沿] 和 [分型左侧下边沿]。

                    self.BRS_Left_UpperEdge = self.BRS_Bottom_UpperEdge
                    self.BRS_Left_LowerEdge = self.BRS_Bottom_LowerEdge
                    # ..............................
                    self.BRS_Bottom_UpperEdge = CURR_UpperEdge
                    self.BRS_Bottom_LowerEdge = CURR_LowerEdge

                    return 0

                if (CURR_UpperEdge == self.BRS_Bottom_UpperEdge) and (CURR_UpperEdge  < self.BRS_Left_UpperEdge):

                    # 新的 [底分型底部下边沿]。

                    self.BRS_Bottom_LowerEdge = CURR_LowerEdge

                    return 0

                if (CURR_UpperEdge  > self.BRS_Bottom_UpperEdge) and (CURR_UpperEdge <= self.BRS_Left_UpperEdge):

                    # [当前 K 线 (CURR)] 包含 [底分型底部], 包含关系。

                    self.BRS_Bottom_UpperEdge = CURR_UpperEdge
                    self.BRS_Bottom_LowerEdge = CURR_LowerEdge

                    return 0

                if (CURR_UpperEdge  > self.BRS_Bottom_UpperEdge) and (CURR_UpperEdge  > self.BRS_Left_UpperEdge):

                    # [底分型] 成立。

                    self.BRS_Left_Exists = 0
                    self.BRS_Bottom_Exists = 0 # -> 可能多余的步骤(仅用于表达逻辑关系)。

                    return 1

    def Top_Reversal_Shape_s_Group_Top(self, Seq:int, UpperEdge:float, LowerEdge:float) -> int:

        # 顶分型 - 分组 Top (Top Reversal Shape - Group Top)
        #
        # Example:
        #
        # >>> print(df)
        #     seq        date       code   open   high    low  close   Top
        # 1         1  2024-04-25  001696.SZ  11.71  11.88  11.25  11.40   NaN
        # 2         2  2024-04-26  001696.SZ  12.05  12.54  12.05  12.54   NaN
        # 3         3  2024-04-29  001696.SZ  12.94  13.29  12.20  13.03  true
        # 4         4  2024-04-30  001696.SZ  12.40  12.50  11.73  11.73   NaN
        # 5         5  2024-05-06  001696.SZ  10.99  11.84  10.99  11.46   NaN
        # 6         6  2024-05-07  001696.SZ  11.80  12.61  11.65  12.61   NaN
        # 7         7  2024-05-08  001696.SZ  12.00  13.01  11.89  12.73  true
        # 8         8  2024-05-09  001696.SZ  12.75  12.80  11.81  12.31   NaN
        # 9         9  2024-05-10  001696.SZ  12.10  12.20  11.43  11.57   NaN
        #
        # >>> df["group_top"] = df.apply(
        # ...     lambda x: Top_Reversal_Shape_s_Group_Top(x["seq"], x["high"], x["low"]),
        # ...     axis=1
        # ... )
        # >>> print(df)
        #    seq        date       code   open   high    low  close   Top  group_top
        # 1        1  2024-04-25  001696.SZ  11.71  11.88  11.25  11.40   NaN          0
        # 2        2  2024-04-26  001696.SZ  12.05  12.54  12.05  12.54   NaN          1
        # 3        3  2024-04-29  001696.SZ  12.94  13.29  12.20  13.03  true          1
        # 4        4  2024-04-30  001696.SZ  12.40  12.50  11.73  11.73   NaN          0
        # 5        5  2024-05-06  001696.SZ  10.99  11.84  10.99  11.46   NaN          0
        # 6        6  2024-05-07  001696.SZ  11.80  12.61  11.65  12.61   NaN          2
        # 7        7  2024-05-08  001696.SZ  12.00  13.01  11.89  12.73  true          2
        # 8        8  2024-05-09  001696.SZ  12.75  12.80  11.81  12.31   NaN          2
        # 9        9  2024-05-10  001696.SZ  12.10  12.20  11.43  11.57   NaN          0

        if (Seq == 1):

            # 由于条件 (Seq == 1) 与 # ((Seq == 1) or (self.TRS_Left_Exists == 0)) 条件重合。
            # 如果条件 (Seq == 1) 满足时, 执行返回 (return) 值,
            # 此时条件 ((Seq == 1) or (self.TRS_Left_Exists == 0)) 中初始化 [分型左侧上下沿] 将不会在第 1 行执行。
            # 因此条件 (Seq == 1) 满足时, 不返回 (return) 任何值, 仅初始化 顶部 K 线 组号。

            self.TRS_Group_Top = 1

        if ((Seq == 1) or (self.TRS_Left_Exists == 0)):

            # 当前为第 1 根 K 线, 或者 [顶分型左侧] 不存在。

            CURR_UpperEdge:float = UpperEdge # -> 可能多余的步骤(仅用于表达传递关系)。
            CURR_LowerEdge:float = LowerEdge # -> 可能多余的步骤(仅用于表达传递关系)。

            self.TRS_Left_UpperEdge = CURR_UpperEdge
            self.TRS_Left_LowerEdge = CURR_LowerEdge

            self.TRS_Left_Exists = 1
            self.TRS_Top_Exists = 0

            return 0

        if ((Seq == 2) or ((self.TRS_Left_Exists == 1) and (self.TRS_Top_Exists == 0))):

            # 当前为第 2 根 K 线, 或者 [分型左侧] 存在 并且 [分型顶部] 不存在。

            CURR_UpperEdge:float = UpperEdge
            CURR_LowerEdge:float = LowerEdge

            if (CURR_UpperEdge  > self.TRS_Left_UpperEdge):

                # [当前 K 线 (CURR) 上沿] 大于 [顶分型左侧上沿]。

                if (CURR_LowerEdge  > self.TRS_Left_LowerEdge):

                    # 分型顶部成立。
                    # 开始为 顶部 K 线 分组 (标示当前组号)。

                    self.TRS_Top_UpperEdge = CURR_UpperEdge
                    self.TRS_Top_LowerEdge = CURR_LowerEdge
                    self.TRS_Top_Exists = 1
                    # ..............................
                    Group_Top = self.TRS_Group_Top

                    return Group_Top

                if (CURR_LowerEdge <= self.TRS_Left_LowerEdge):

                    # [当前 K 线 (CURR)] 包含 [顶分型左侧] 包含关系。
                    # 继续查找 [分型顶部]。

                    self.TRS_Left_UpperEdge = CURR_UpperEdge
                    self.TRS_Left_LowerEdge = CURR_LowerEdge

                    return 0

            if (CURR_UpperEdge == self.TRS_Left_UpperEdge):

                # [当前 K 线 (CURR) 上沿] 等于 [顶分型左侧上沿]。

                if (CURR_LowerEdge >= self.TRS_Left_LowerEdge):

                    # [当前 K 线 (CURR)] 被 [顶分型左侧] 包含, 被包含关系。
                    # 继续查找 [分型顶部]。

                    return 0

                if (CURR_LowerEdge  < self.TRS_Left_LowerEdge):

                    # [当前 K 线 (CURR)] 包含 [顶分型左侧], 包含关系。
                    # 继续查找 [分型顶部]。

                    self.TRS_Left_UpperEdge = CURR_UpperEdge # -> 可能多余的步骤(仅用于表达逻辑关系)。
                    self.TRS_Left_LowerEdge = CURR_LowerEdge

                    return 0

            if (CURR_UpperEdge  < self.TRS_Left_UpperEdge):

                # [当前 K 线 (CURR) 上沿] 小于 [顶分型左侧上沿]。

                if (CURR_LowerEdge >= self.TRS_Left_LowerEdge):

                    # [当前 K 线 (CURR)] 被 [顶分型左侧] 包含, 被包含关系。
                    # 继续查找 [分型顶部]。

                    return 0

                if (CURR_LowerEdge  < self.TRS_Left_LowerEdge):

                    # [分型底部] 成立, 重置分型左侧。
                    # 在判断顶分型的函数中, 排除底分型相关结论, 重置 [分型左侧] 上下沿。

                    self.TRS_Left_UpperEdge = CURR_UpperEdge
                    self.TRS_Left_LowerEdge = CURR_LowerEdge

                    return 0

        if ((Seq >= 3) and ((self.TRS_Left_Exists == 1) and (self.TRS_Top_Exists == 1))):

            # 当前为第 3 根或之后的 K 线, 并且 [分型左侧] 和 [分型顶部] 都存在。

            CURR_UpperEdge:float = UpperEdge
            CURR_LowerEdge:float = LowerEdge

            if (CURR_UpperEdge  > self.TRS_Top_UpperEdge):

                # [当前 K 线 (CURR) 上沿] 大于 [顶分型顶部上沿]。

                if (CURR_LowerEdge  > self.TRS_Top_LowerEdge) and (CURR_LowerEdge  > self.TRS_Left_LowerEdge):

                    # 新的 [分型顶部上边沿] 和 [分型顶部下边沿] 以及 新的 [分型左侧上边沿] 和 [分型左侧下边沿]。
                    # 继续为 顶部 K 线 分组 (标示当前组号)。

                    self.TRS_Left_UpperEdge = self.TRS_Top_UpperEdge
                    self.TRS_Left_LowerEdge = self.TRS_Top_LowerEdge
                    # ..............................
                    self.TRS_Top_UpperEdge = CURR_UpperEdge
                    self.TRS_Top_LowerEdge = CURR_LowerEdge
                    # ..............................
                    Group_Top = self.TRS_Group_Top

                    return Group_Top

                if (CURR_LowerEdge == self.TRS_Top_LowerEdge) and (CURR_LowerEdge  > self.TRS_Left_LowerEdge):

                    # 新的 [分型顶部上边沿]。
                    # 继续为 顶部 K 线 分组 (标示当前组号)。

                    self.TRS_Top_UpperEdge = CURR_UpperEdge
                    # ..............................
                    Group_Top = self.TRS_Group_Top

                    return Group_Top

                if (CURR_LowerEdge  < self.TRS_Top_LowerEdge) and (CURR_LowerEdge >= self.TRS_Left_LowerEdge):

                    # [当前 K 线 (CURR)] 包含 [顶分型顶部], 包含关系。
                    # 继续为 顶部 K 线 分组 (标示当前组号)。

                    self.TRS_Top_UpperEdge = CURR_UpperEdge
                    self.TRS_Top_LowerEdge = CURR_LowerEdge
                    # ..............................
                    Group_Top = self.TRS_Group_Top

                    return Group_Top

                if (CURR_LowerEdge  < self.TRS_Top_LowerEdge) and (CURR_LowerEdge  < self.TRS_Left_LowerEdge):

                    # [顶分型] 成立。
                    # 终止为 顶部 K 线 分组 (标示当前组号), 并将 顶部 K 线 组号 + 1。

                    self.TRS_Left_Exists = 0
                    self.TRS_Top_Exists = 0 # -> 可能多余的步骤(仅用于表达逻辑关系)。
                    # ..............................
                    self.TRS_Group_Top = self.TRS_Group_Top + 1

                    return 0

            if (CURR_UpperEdge == self.TRS_Top_UpperEdge):

                # [当前 K 线 (CURR) 上沿] 等于 [顶分型顶部上沿]。

                if (CURR_LowerEdge >= self.TRS_Top_LowerEdge) and (CURR_LowerEdge  > self.TRS_Left_LowerEdge):

                    # [当前 K 线 (CURR)] 被 [顶分型顶部] 包含, 被包含关系。
                    # 继续为 顶部 K 线 分组 (标示当前组号)。

                    Group_Top = self.TRS_Group_Top

                    return Group_Top

                if (CURR_LowerEdge  < self.TRS_Top_LowerEdge) and (CURR_LowerEdge >= self.TRS_Left_LowerEdge):

                    # [当前 K 线 (CURR)] 包含 [顶分型顶部], 包含关系。
                    # 继续为 顶部 K 线 分组 (标示当前组号)。

                    self.TRS_Top_UpperEdge = CURR_UpperEdge # -> 可能多余的步骤(仅用于表达逻辑关系)。
                    self.TRS_Top_LowerEdge = CURR_LowerEdge
                    # ..............................
                    Group_Top = self.TRS_Group_Top

                    return Group_Top

                if (CURR_LowerEdge  < self.TRS_Top_LowerEdge) and (CURR_LowerEdge  < self.TRS_Left_LowerEdge):

                    # [顶分型] 成立。
                    # 终止为 顶部 K 线 分组 (标示当前组号), 并将 顶部 K 线 组号 + 1。

                    self.TRS_Left_Exists = 0
                    self.TRS_Top_Exists = 0 # -> 可能多余的步骤(仅用于表达逻辑关系)。
                    # ..............................
                    self.TRS_Group_Top = self.TRS_Group_Top + 1

                    return 0

            if (CURR_UpperEdge  < self.TRS_Top_UpperEdge):

                # [当前 K 线 (CURR) 上沿] 小于 [顶分型顶部上沿]。

                if (CURR_LowerEdge >= self.TRS_Top_LowerEdge) and (CURR_LowerEdge  > self.TRS_Left_LowerEdge):

                    # [当前 K 线 (CURR)] 被 [顶分型顶部] 包含, 被包含关系。
                    # 继续为 顶部 K 线 分组 (标示当前组号)。

                    Group_Top = self.TRS_Group_Top

                    return Group_Top

                if (CURR_LowerEdge  < self.TRS_Top_LowerEdge) and (CURR_LowerEdge >= self.TRS_Left_LowerEdge):

                    # 新的 [分型顶部下边沿]。
                    # 继续为 顶部 K 线 分组 (标示当前组号)。

                    self.TRS_Top_LowerEdge = CURR_LowerEdge
                    # ..............................
                    Group_Top = self.TRS_Group_Top

                    return Group_Top

                if (CURR_LowerEdge  < self.TRS_Top_LowerEdge) and (CURR_LowerEdge  < self.TRS_Left_LowerEdge):

                    # [顶分型] 成立。
                    # 终止为 顶部 K 线 分组 (标示当前组号), 并将 顶部 K 线 组号 + 1。

                    self.TRS_Left_Exists = 0
                    self.TRS_Top_Exists = 0 # -> 可能多余的步骤(仅用于表达逻辑关系)。
                    # ..............................
                    self.TRS_Group_Top = self.TRS_Group_Top + 1

                    return 0

    def Bottom_Reversal_Shape_s_Group_Bottom(self, Seq:int, UpperEdge:float, LowerEdge:float) -> int:

        # 底分型 - 分组 Bottom (Bottom Reversal Shape - Group Bottom)
        #
        # Example:
        #
        # >>> print(df)
        #     seq        date       code   open   high    low  close  bottom
        #  0    1  2024-04-30  001696.SZ  12.40  12.50  11.73  11.73     NaN
        #  1    2  2024-05-06  001696.SZ  10.99  11.84  10.99  11.46    true
        #  2    3  2024-05-07  001696.SZ  11.80  12.61  11.65  12.61     NaN
        #  3    4  2024-05-08  001696.SZ  12.00  13.01  11.89  12.73     NaN
        #  4    5  2024-05-09  001696.SZ  12.75  12.80  11.81  12.31     NaN
        #  5    6  2024-05-10  001696.SZ  12.10  12.20  11.43  11.57     NaN
        #  6    7  2024-05-13  001696.SZ  11.20  11.74  11.00  11.71    true
        #  7    8  2024-05-14  001696.SZ  11.84  11.87  11.38  11.44     NaN
        #  8    9  2024-05-15  001696.SZ  11.31  11.87  11.21  11.47     NaN
        #  9   10  2024-05-16  001696.SZ  11.45  11.97  11.41  11.75     NaN
        # 10   11  2024-05-17  001696.SZ  12.02  12.93  11.44  12.93     NaN
        #
        # >>> df["group_bottom"] = df.apply(
        # ...     lambda x: Bottom_Reversal_Shape_s_Group_Bottom(x["seq"], x["high"], x["low"]),
        # ...     axis=1
        # ... )
        # >>> print(df)
        #     seq        date       code   open   high    low  close  bottom  group_bottom
        #  0    1  2024-04-30  001696.SZ  12.40  12.50  11.73  11.73     NaN             0
        #  1    2  2024-05-06  001696.SZ  10.99  11.84  10.99  11.46    true             1
        #  2    3  2024-05-07  001696.SZ  11.80  12.61  11.65  12.61     NaN             0
        #  3    4  2024-05-08  001696.SZ  12.00  13.01  11.89  12.73     NaN             0
        #  4    5  2024-05-09  001696.SZ  12.75  12.80  11.81  12.31     NaN             2
        #  5    6  2024-05-10  001696.SZ  12.10  12.20  11.43  11.57     NaN             2
        #  6    7  2024-05-13  001696.SZ  11.20  11.74  11.00  11.71    true             2
        #  7    8  2024-05-14  001696.SZ  11.84  11.87  11.38  11.44     NaN             2
        #  8    9  2024-05-15  001696.SZ  11.31  11.87  11.21  11.47     NaN             2
        #  9   10  2024-05-16  001696.SZ  11.45  11.97  11.41  11.75     NaN             2
        # 10   11  2024-05-17  001696.SZ  12.02  12.93  11.44  12.93     NaN             0

        if (Seq == 1):

            # 由于条件 (Seq == 1) 与 # ((Seq == 1) or (self.BRS_Left_Exists == 0)) 条件重合。
            # 如果条件 (Seq == 1) 满足时, 执行返回 (return) 值,
            # 此时条件 ((Seq == 1) or (self.BRS_Left_Exists == 0)) 中初始化 [分型左侧上下沿] 将不会在第 1 行执行。
            # 因此条件 (Seq == 1) 满足时, 不返回 (return) 任何值, 仅初始化 底部 K 线 组号。

            self.BRS_Group_Bottom = 1

        if ((Seq == 1) or (self.BRS_Left_Exists == 0)):

            # 当前为第 1 根 K 线, 或者 [底分型左侧] 不存在。

            CURR_UpperEdge:float = UpperEdge # -> 可能多余的步骤(仅用于表达传递关系)。
            CURR_LowerEdge:float = LowerEdge # -> 可能多余的步骤(仅用于表达传递关系)。

            self.BRS_Left_UpperEdge = CURR_UpperEdge
            self.BRS_Left_LowerEdge = CURR_LowerEdge

            self.BRS_Left_Exists = 1
            self.BRS_Bottom_Exists = 0

            return 0

        if ((Seq == 2) or ((self.BRS_Left_Exists == 1) and (self.BRS_Bottom_Exists == 0))):

            # 当前为第 2 根 K 线, 或者 [分型左侧] 存在 并且 [分型底部] 不存在。

            CURR_UpperEdge:float = UpperEdge
            CURR_LowerEdge:float = LowerEdge

            if (CURR_LowerEdge  > self.BRS_Left_LowerEdge):

                # [当前 K 线 (CURR) 下沿] 大于 [底分型左侧下沿]。

                if (CURR_UpperEdge <= self.BRS_Left_UpperEdge):

                    # [当前 K 线 (CURR)] 被 [底分型左侧] 包含, 被包含关系。
                    # 继续查找 [分型底部]。

                    return 0

                if (CURR_UpperEdge  > self.BRS_Left_UpperEdge):

                    # [分型顶部] 成立, 重置分型左侧。
                    # 在判断底分型的函数中, 排除顶分型相关结论, 重置 [分型左侧] 上下沿。

                    self.BRS_Left_UpperEdge = CURR_UpperEdge
                    self.BRS_Left_LowerEdge = CURR_LowerEdge

                    return 0

            if (CURR_LowerEdge == self.BRS_Left_LowerEdge):

                # [当前 K 线 (CURR) 下沿] 等于 [底分型左侧下沿]。

                if (CURR_UpperEdge <= self.BRS_Left_UpperEdge):

                    # [当前 K 线 (CURR)] 被 [底分型左侧] 包含, 被包含关系。
                    # 继续查找 [分型底部]。

                    return 0

                if (CURR_UpperEdge  > self.BRS_Left_UpperEdge):

                    # [当前 K 线 (CURR)] 包含 [底分型左侧], 包含关系。
                    # 继续查找 [分型底部]。

                    self.BRS_Left_UpperEdge = CURR_UpperEdge
                    self.BRS_Left_LowerEdge = CURR_LowerEdge # -> 可能多余的步骤(仅用于表达逻辑关系)。

                    return 0

            if (CURR_LowerEdge  < self.BRS_Left_LowerEdge):

                # [当前 K 线 (CURR) 下沿] 小于 [底分型左侧下沿]。

                if (CURR_UpperEdge  < self.BRS_Left_UpperEdge):

                    # 分型底部成立。
                    # 开始为 底部 K 线 分组 (标示当前组号)。

                    self.BRS_Bottom_UpperEdge = CURR_UpperEdge
                    self.BRS_Bottom_LowerEdge = CURR_LowerEdge
                    self.BRS_Bottom_Exists = 1
                    # ..............................
                    Group_Bottom = self.BRS_Group_Bottom

                    return Group_Bottom

                if (CURR_UpperEdge >= self.BRS_Left_UpperEdge):

                    # [当前 K 线 (CURR)] 包含 [底分型左侧], 包含关系。
                    # 继续查找 [分型底部]。

                    self.BRS_Left_UpperEdge = CURR_UpperEdge
                    self.BRS_Left_LowerEdge = CURR_LowerEdge

                    return 0

        if ((Seq >= 3) and ((self.BRS_Left_Exists == 1) and (self.BRS_Bottom_Exists == 1))):

            # 当前为第 3 根或之后的 K 线, 并且 [分型左侧] 和 [分型底部] 都存在。

            CURR_UpperEdge:float = UpperEdge
            CURR_LowerEdge:float = LowerEdge

            if (CURR_LowerEdge  > self.BRS_Bottom_LowerEdge):

                # [当前 K 线 (CURR) 下沿] 大于 [底分型底部下沿]。

                if (CURR_UpperEdge <= self.BRS_Bottom_UpperEdge) and (CURR_UpperEdge  < self.BRS_Left_UpperEdge):

                    # [当前 K 线 (CURR)] 被 [底分型底部] 包含, 被包含关系。
                    # 继续为 底部 K 线 分组 (标示当前组号)。

                    Group_Bottom = self.BRS_Group_Bottom

                    return Group_Bottom

                if (CURR_UpperEdge  > self.BRS_Bottom_UpperEdge) and (CURR_UpperEdge <= self.BRS_Left_UpperEdge):

                    # 新的 [底分型底部上边沿]。
                    # 继续为 底部 K 线 分组 (标示当前组号)。

                    self.BRS_Bottom_UpperEdge = CURR_UpperEdge
                    # ..............................
                    Group_Bottom = self.BRS_Group_Bottom

                    return Group_Bottom

                if (CURR_UpperEdge  > self.BRS_Bottom_UpperEdge) and (CURR_UpperEdge  > self.BRS_Left_UpperEdge):

                    # [底分型] 成立。
                    # 终止为 底部 K 线 分组 (标示当前组号), 并将 底部 K 线 组号 + 1。

                    self.BRS_Left_Exists = 0
                    self.BRS_Bottom_Exists = 0 # -> 可能多余的步骤(仅用于表达逻辑关系)。
                    # ..............................
                    self.BRS_Group_Bottom = self.BRS_Group_Bottom + 1

                    return 0

            if (CURR_LowerEdge == self.BRS_Bottom_LowerEdge):

                # [当前 K 线 (CURR) 下沿] 等于 [底分型底部下沿]。

                if (CURR_UpperEdge <= self.BRS_Bottom_UpperEdge) and (CURR_UpperEdge  < self.BRS_Left_UpperEdge):

                    # [当前 K 线 (CURR)] 被 [底分型底部] 包含, 被包含关系。
                    # 继续为 底部 K 线 分组 (标示当前组号)。

                    Group_Bottom = self.BRS_Group_Bottom

                    return Group_Bottom

                if (CURR_UpperEdge  > self.BRS_Bottom_UpperEdge) and (CURR_UpperEdge <= self.BRS_Left_UpperEdge):

                    # [当前 K 线 (CURR)] 包含 [底分型底部], 包含关系。
                    # 继续为 底部 K 线 分组 (标示当前组号)。

                    self.BRS_Bottom_UpperEdge = CURR_UpperEdge
                    self.BRS_Bottom_LowerEdge = CURR_LowerEdge # -> 可能多余的步骤(仅用于表达逻辑关系)。
                    # ..............................
                    Group_Bottom = self.BRS_Group_Bottom

                    return Group_Bottom

                if (CURR_UpperEdge  > self.BRS_Bottom_UpperEdge) and (CURR_UpperEdge  > self.BRS_Left_UpperEdge):

                    # [底分型] 成立。
                    # 终止为 底部 K 线 分组 (标示当前组号), 并将 底部 K 线 组号 + 1。

                    self.BRS_Left_Exists = 0
                    self.BRS_Bottom_Exists = 0 # -> 可能多余的步骤(仅用于表达逻辑关系)。
                    # ..............................
                    self.BRS_Group_Bottom = self.BRS_Group_Bottom + 1

                    return 0

            if (CURR_LowerEdge  < self.BRS_Bottom_LowerEdge):

                # [当前 K 线 (CURR) 下沿] 小于 [底分型底部下沿]。

                if (CURR_UpperEdge  < self.BRS_Bottom_UpperEdge) and (CURR_UpperEdge  < self.BRS_Left_UpperEdge):

                    # 新的 [分型底部上边沿] 和 [分型底部下边沿] 以及 新的 [分型左侧上边沿] 和 [分型左侧下边沿]。
                    # 继续为 底部 K 线 分组 (标示当前组号)。

                    self.BRS_Left_UpperEdge = self.BRS_Bottom_UpperEdge
                    self.BRS_Left_LowerEdge = self.BRS_Bottom_LowerEdge
                    # ..............................
                    self.BRS_Bottom_UpperEdge = CURR_UpperEdge
                    self.BRS_Bottom_LowerEdge = CURR_LowerEdge
                    # ..............................
                    Group_Bottom = self.BRS_Group_Bottom

                    return Group_Bottom

                if (CURR_UpperEdge == self.BRS_Bottom_UpperEdge) and (CURR_UpperEdge  < self.BRS_Left_UpperEdge):

                    # 新的 [底分型底部下边沿]。
                    # 继续为 底部 K 线 分组 (标示当前组号)。

                    self.BRS_Bottom_LowerEdge = CURR_LowerEdge
                    # ..............................
                    Group_Bottom = self.BRS_Group_Bottom

                    return Group_Bottom

                if (CURR_UpperEdge  > self.BRS_Bottom_UpperEdge) and (CURR_UpperEdge <= self.BRS_Left_UpperEdge):

                    # [当前 K 线 (CURR)] 包含 [底分型底部], 包含关系。
                    # 继续为 底部 K 线 分组 (标示当前组号)。

                    self.BRS_Bottom_UpperEdge = CURR_UpperEdge
                    self.BRS_Bottom_LowerEdge = CURR_LowerEdge
                    # ..............................
                    Group_Bottom = self.BRS_Group_Bottom

                    return Group_Bottom

                if (CURR_UpperEdge  > self.BRS_Bottom_UpperEdge) and (CURR_UpperEdge  > self.BRS_Left_UpperEdge):

                    # [底分型] 成立。
                    # 终止为 底部 K 线 分组 (标示当前组号), 并将 底部 K 线 组号 + 1。

                    self.BRS_Left_Exists = 0
                    self.BRS_Bottom_Exists = 0 # -> 可能多余的步骤(仅用于表达逻辑关系)。
                    # ..............................
                    self.BRS_Group_Bottom = self.BRS_Group_Bottom + 1

                    return 0

    def TBRS(self, TRS:str, BRS:str) -> str:

        if ((TRS == 1) and (BRS == 0)):
            return  1
        if ((TRS == 0) and (BRS == 1)):
            return -1
        if ((TRS == 0) and (BRS == 0)):
            return  0
        if ((TRS == 1) and (BRS == 1)):
            # 前一根 K 线实体很短, 后一根实体很长, 比例差距越大, 反转信号就越强
            # 吞没形态的第二根 K 线伴随有明显放大的交易量, 信号增强
            # 特别是 "一吞九" (一根巨阳吞掉左边九根 K 线) 组合。
            # "一吞九" 组合无论是短线操作, 还是中长线威力都非常的不错, 少则 30% - 50% 涨幅, 多则涨幅翻番, 有的甚至几倍涨幅。
            return  -11  # "-1" and "1" = "-11"

# EOF Signed by GF.
