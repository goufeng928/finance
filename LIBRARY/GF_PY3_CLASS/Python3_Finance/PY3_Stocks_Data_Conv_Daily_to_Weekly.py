# GF_PY3_CLASS/Python3_Finance/PY3_Stocks_Data_Conv_Daily_to_Weekly.py
# Create By GF 2024-01-22 18:16

import datetime

# ##################################################

class PY3_Stocks_Data_Conv_Daily_to_Weekly(object):

    # Examples for "Finance Data Convert Daily to Weekly":
    # >>> import pandas
    # >>>
    # >>> df = pandas.read_csv("./example.csv")
    # >>> print(df)
    #    id        time       code  open  high   low  close  change    chg_pct    volume
    # 0   1  2015-12-25  000422.SZ  8.03  8.05  7.93   8.03    0.04   0.005006  18974000
    # 1   2  2015-12-24  000422.SZ  7.93  8.16  7.87   7.99    0.07   0.008838  23781900
    # 2   3  2015-12-23  000422.SZ  7.97  8.11  7.88   7.92    0.03   0.003802  38033600
    # 3   4  2015-12-22  000422.SZ  7.86  7.93  7.76   7.89    0.06   0.007663  24178700
    # 4   5  2015-12-21  000422.SZ  7.59  7.89  7.56   7.83    0.20   0.026212  27633600
    # 5   6  2015-12-18  000422.SZ  7.71  7.74  7.57   7.63   -0.11  -0.014212  22234900
    # 6   7  2015-12-17  000422.SZ  7.58  7.75  7.57   7.74    0.19   0.025166  25188400
    # 7   8  2015-12-16  000422.SZ  7.57  7.62  7.53   7.55    0.00   0.000000  18601600
    # 8   9  2015-12-15  000422.SZ  7.63  7.66  7.52   7.55   -0.07  -0.009186  23256600
    # 9  10  2015-12-14  000422.SZ  7.40  7.64  7.36   7.62    0.11   0.014647  18860100
    # >>>
    # >>> # 生成必要数据: 时间对象 (Time Object) -> 时间可计算, 可比较
    # >>> df["time"] = pandas.to_datetime(df["time"], format = "mixed", errors = "coerce")  # errors = "coerce" 将无效日期转为 NaT
    # >>> # 周涨跌率 = (本周最后 1 天收盘价 - 上周最后 1 天收盘价) / 本周最后 1 天收盘价 (无法通过单周数据计算得出)
    # >>> df = df[["id", "time", "code", "open", "high", "low, "close, "change, "volume"]]  # 筛除无法计算的涨跌率 (Change Percent)
    # >>>
    # >>> # 提取必要数据: 年份 (Year), 本年中第几周 (Week Number)
    # >>> df["year"    ] = df["time"    ].dt.year
    # >>> df["year"    ] = df["year"    ].astype("string")
    # >>> df["week_num"] = df["time"    ].dt.strftime("%U")  # 其中 %U 表示本年中的第几周
    # >>> df["week_num"] = df["week_num"].str.zfill(2)       # 函数 str().zfill() 用于将字符串填充 0 至指定宽度
    # >>>
    # >>> # ISO 8601 表示周采用 YYYY-Www 格式
    # >>> # - YYYY: 四位年份
    # >>> # - W: 固定字母标识
    # >>> # - ww: 两位数周编号 (01-53)
    # >>> # - 例如: 2024-W28 表示 2024 年第 28 周
    # >>> df["iso_8601_week"] = df["year"] + "-W" + df["week_num"]
    # >>>
    # >>> # 生成必要数据: 行号 (Row Number)
    # >>> df = df.sort_values("time", ascending = True)
    # >>> # Pandas DataFrame 中 rank 方法的 method 参数: 指定处理相同值时的方法
    # >>> # - first: 如果两个数值相同, 根据数值的 "大小" 和 "顺序" 进行排名
    # >>> # - average: 如果两个数值相同, 排名是它们的 "平均值"
    # >>> # - min: 如果两个数值相同, 取最小排名作为两个数的排名, 如, 第 1 个 3.14 按顺序应排第 4, 第 2 个 3.14 按顺序应排第 5, 则这两个数的排名都是 4 (最小排名)
    # >>> # - max: 如果两个数值相同, 取最大排名作为两个数的排名, 如, 第 1 个 3.14 按顺序应排第 4, 第 2 个 3.14 按顺序应排第 5, 则这两个数的排名都是 5 (最大排名)
    # >>> # - dense: 如果两个数值相同, 与 min 相同, 但不会出现跳跃排名, 如 min 方式下, 连续的两个数排名第 4, 则下个数排名是 6, 跳过了 5, 而 dense 方式则不会跳跃
    # >>> df["seq"] = df[["iso_8601_week", "time"]].groupby(["iso_8601_week"], as_index = False).rank(method = "first")
    # >>> df["seq"] = df["seq"].astype("int64")
    # >>> df = df.reset_index(drop = True)
    # >>> print(df)
    #    id        time       code  open  high   low  close  change    volume  year  week_num  iso_8601_week  seq
    # 0  10  2015-12-14  000422.SZ  7.40  7.64  7.36   7.62    0.11  18860100  2015        50       2015-W50    1
    # 1   9  2015-12-15  000422.SZ  7.63  7.66  7.52   7.55   -0.07  23256600  2015        50       2015-W50    2
    # 2   8  2015-12-16  000422.SZ  7.57  7.62  7.53   7.55    0.00  18601600  2015        50       2015-W50    3
    # 3   7  2015-12-17  000422.SZ  7.58  7.75  7.57   7.74    0.19  25188400  2015        50       2015-W50    4
    # 4   6  2015-12-18  000422.SZ  7.71  7.74  7.57   7.63   -0.11  22234900  2015        50       2015-W50    5
    # 5   5  2015-12-21  000422.SZ  7.59  7.89  7.56   7.83    0.20  27633600  2015        51       2015-W51    1
    # 6   4  2015-12-22  000422.SZ  7.86  7.93  7.76   7.89    0.06  24178700  2015        51       2015-W51    2
    # 7   3  2015-12-23  000422.SZ  7.97  8.11  7.88   7.92    0.03  38033600  2015        51       2015-W51    3
    # 8   2  2015-12-24  000422.SZ  7.93  8.16  7.87   7.99    0.07  23781900  2015        51       2015-W51    4
    # 9   1  2015-12-25  000422.SZ  8.03  8.05  7.93   8.03    0.04  18974000  2015        51       2015-W51    5
    # >>>
    # >>> # 计算目标数据: 日数据 -> 周数据 (Daily -> Weekly)
    # >>> Obj = PY3_Finance_Data_Conv_Daily_to_Weekly()
    # >>> for i in df.index:
    # ...     Seq       = df.loc[i, "seq"    ]
    # ...     DY_Time   = df.loc[i, "time"   ]
    # ...     DY_Open   = df.loc[i, "open"   ]
    # ...     DY_High   = df.loc[i, "high"   ]
    # ...     DY_Low    = df.loc[i, "low"    ]
    # ...     DY_Close  = df.loc[i, "close"  ]
    # ...     DY_Change = df.loc[i, "change" ]
    # ...     DY_Volume = df.loc[i, "volume" ]
    # ...     df.loc[i, "wk_time"  ] = Obj.WK_Time(Seq = Seq, DY_Time = DY_Time)
    # ...     df.loc[i, "wk_open"  ] = Obj.WK_Open(Seq = Seq, DY_Open = DY_Open)
    # ...     df.loc[i, "wk_high"  ] = Obj.WK_High(Seq = Seq, DY_High = DY_High)
    # ...     df.loc[i, "wk_low"   ] = Obj.WK_Low(Seq = Seq, DY_Low = DY_Low)
    # ...     df.loc[i, "wk_close" ] = Obj.WK_Close(Seq = Seq, DY_Close = DY_Close)
    # ...     df.loc[i, "wk_change"] = Obj.WK_Change(Seq = Seq, DY_Change = DY_Change)
    # ...     df.loc[i, "wk_volume"] = Obj.WK_Volume(Seq = Seq, DY_Volume = DY_Volume)
    # >>> df = df[["id", "wk_time", "code", "wk_open", "wk_high", "wk_low, "wk_close, "wk_change, "wk_volume", "year", "week_num", "iso_8601_week", "seq"]]
    # >>> print(df)
    #    id     wk_time       code  wk_open  wk_high  wk_low  wk_close  wk_change  wk_volume  year  week_num  iso_8601_week  seq
    # 0  10  2015-12-14  000422.SZ     7.40     7.64    7.36      7.62       0.11   18860100  2015        50       2015-W50    1
    # 1   9  2015-12-15  000422.SZ     7.40     7.66    7.36      7.55       0.04   42116700  2015        50       2015-W50    2
    # 2   8  2015-12-16  000422.SZ     7.40     7.66    7.36      7.55       0.04   60718300  2015        50       2015-W50    3
    # 3   7  2015-12-17  000422.SZ     7.40     7.75    7.36      7.74       0.23   85906700  2015        50       2015-W50    4
    # 4   6  2015-12-18  000422.SZ     7.40     7.75    7.36      7.63       0.12  108141600  2015        50       2015-W50    5
    # 5   5  2015-12-21  000422.SZ     7.59     7.89    7.56      7.83       0.20   27633600  2015        51       2015-W51    1
    # 6   4  2015-12-22  000422.SZ     7.59     7.93    7.56      7.89       0.26   51812300  2015        51       2015-W51    2
    # 7   3  2015-12-23  000422.SZ     7.59     8.11    7.56      7.92       0.29   89845900  2015        51       2015-W51    3
    # 8   2  2015-12-24  000422.SZ     7.59     8.16    7.56      7.99       0.36  113627800  2015        51       2015-W51    4
    # 9   1  2015-12-25  000422.SZ     7.59     8.16    7.56      8.03       0.40  132601800  2015        51       2015-W51    5
    # >>>
    # >>> # 筛选目标数据: 每组周数据中最后 1 个日期的数据
    # >>> df = df.sort_values("wk_time", ascending = False)
    # >>> df["cum_max"] = df[["iso_8601_week", "seq"]].groupby("iso_8601_week", as_index = False).cummax()["seq"]
    # >>> print(df)
    #    id     wk_time       code  wk_open  wk_high  wk_low  wk_close  wk_change  wk_volume  year  week_num  iso_8601_week  seq  cum_max
    # 9   1  2015-12-25  000422.SZ     7.59     8.16    7.56      8.03       0.40  132601800  2015        51       2015-W51    5        5
    # 8   2  2015-12-24  000422.SZ     7.59     8.16    7.56      7.99       0.36  113627800  2015        51       2015-W51    4        5
    # 7   3  2015-12-23  000422.SZ     7.59     8.11    7.56      7.92       0.29   89845900  2015        51       2015-W51    3        5
    # 6   4  2015-12-22  000422.SZ     7.59     7.93    7.56      7.89       0.26   51812300  2015        51       2015-W51    2        5
    # 5   5  2015-12-21  000422.SZ     7.59     7.89    7.56      7.83       0.20   27633600  2015        51       2015-W51    1        5
    # 4   6  2015-12-18  000422.SZ     7.40     7.75    7.36      7.63       0.12  108141600  2015        50       2015-W50    5        5
    # 3   7  2015-12-17  000422.SZ     7.40     7.75    7.36      7.74       0.23   85906700  2015        50       2015-W50    4        5
    # 2   8  2015-12-16  000422.SZ     7.40     7.66    7.36      7.55       0.04   60718300  2015        50       2015-W50    3        5
    # 1   9  2015-12-15  000422.SZ     7.40     7.66    7.36      7.55       0.04   42116700  2015        50       2015-W50    2        5
    # 0  10  2015-12-14  000422.SZ     7.40     7.64    7.36      7.62       0.11   18860100  2015        50       2015-W50    1        5
    # >>> df = df[df["seq"] == df["cum_max"]]
    # >>> print(df)
    #    id     wk_time       code  wk_open  wk_high  wk_low  wk_close  wk_change  wk_volume  year  week_num  iso_8601_week  seq  cum_max
    # 9   1  2015-12-25  000422.SZ     7.59     8.16    7.56      8.03       0.40  132601800  2015        51       2015-W51    5        5
    # 4   6  2015-12-18  000422.SZ     7.40     7.75    7.36      7.63       0.12  108141600  2015        50       2015-W50    5        5

    def __init__(self):

        self.JSON_Queue_of_DY_Time:list = []
        self.JSON_Queue_of_DY_Open:list = []
        self.JSON_Queue_of_DY_High:list = []
        self.JSON_Queue_of_DY_Low:list = []
        self.JSON_Queue_of_DY_Close:list = []
        self.JSON_Queue_of_DY_Change:list = []
        self.JSON_Queue_of_DY_Volume:list = []

    def OBJ_Time(self, Time:str) -> datetime.datetime:

        OBJ_Time:datetime.datetime = None
        # ..........................................
        STR_Time:str = str(Time)
        STR_Time     = STR_Time.replace('/', '-')
        STR_Time_Len = len(STR_Time)
        # ..........................................
        if   (STR_Time_Len ==  7):  # be Similar to: YYYYmdd
            OBJ_Time = datetime.datetime.strptime(STR_Time, "%Y%m%d")
        elif (STR_Time_Len ==  8):  # be Similar to: YYYYmmdd
            OBJ_Time = datetime.datetime.strptime(STR_Time, "%Y%m%d")
        elif (STR_Time_Len ==  9):  # be Similar to: YYYY-m-dd
            OBJ_Time = datetime.datetime.strptime(STR_Time, "%Y-%m-%d")
        elif (STR_Time_Len == 10):  # be Similar to: YYYY-mm-dd
            OBJ_Time = datetime.datetime.strptime(STR_Time, "%Y-%m-%d")
        elif (STR_Time_Len == 17):  # be Similar to: YYYYmmdd HH:MM:SS
            OBJ_Time = datetime.datetime.strptime(STR_Time, "%Y%m%d %H:%M:%S")
        elif (STR_Time_Len == 19):  # be Similar to: YYYY-mm-dd HH:MM:SS
            OBJ_Time = datetime.datetime.strptime(STR_Time, "%Y-%m-%d %H:%M:%S")
        # ..........................................
        return OBJ_Time

    def Week_Number(self, Time:str) -> int:

        OBJ_Time:datetime.datetime = self.OBJ_Time(Time = Time)
        # ..........................................
        Which_Week_of_The_Year:str = OBJ_Time.strftime("%W")
        Which_Week_of_The_Year:int = int(Which_Week_of_The_Year)
        # ..........................................
        return Which_Week_of_The_Year

    def WK_Time(self, Seq:int, DY_Time:str) -> str:

        if (Seq == 1):
            self.JSON_Queue_of_DY_Time.clear()  # 首行执行函数时先清空全局列表变量。
            # ......................................
            self.JSON_Queue_of_DY_Time.append(DY_Time)
            # ......................................
            return DY_Time

        if (Seq >= 2):
            self.JSON_Queue_of_DY_Time.append(DY_Time)
            # ......................................
            return self.JSON_Queue_of_DY_Time[-1]  # 返回日 (Day) 数据 <日期> 的末尾值

    def WK_Open(self, Seq:int, DY_Open:float) -> float:

        if (Seq == 1):
            self.JSON_Queue_of_DY_Open.clear()
            # ......................................
            self.JSON_Queue_of_DY_Open.append(DY_Open)
            # ......................................
            return DY_Open

        if (Seq >= 2):
            self.JSON_Queue_of_DY_Open.append(DY_Open)
            # ......................................
            return self.JSON_Queue_of_DY_Open[0]  # 返回日 (Day) 数据 <开盘价> 的首个值

    def WK_High(self, Seq:int, DY_High:float) -> float:

        if (Seq == 1):
            self.JSON_Queue_of_DY_High.clear()
            # ......................................
            self.JSON_Queue_of_DY_High.append(DY_High)
            # ......................................
            return DY_High

        if (Seq >= 2):
            self.JSON_Queue_of_DY_High.append(DY_High)
            # ......................................
            return max(self.JSON_Queue_of_DY_High)  # 返回日 (Day) 数据 <最高价> 的最大值

    def WK_Low(self, Seq:int, DY_Low:float) -> float:

        if (Seq == 1):
            self.JSON_Queue_of_DY_Low.clear()
            # ......................................
            self.JSON_Queue_of_DY_Low.append(DY_Low)
            # ......................................
            return DY_Low

        if (Seq >= 2):
            self.JSON_Queue_of_DY_Low.append(DY_Low)
            # ......................................
            return min(self.JSON_Queue_of_DY_Low)  # 返回日 (Day) 数据 <最低价> 的最小值

    def WK_Close(self, Seq:int, DY_Close:float) -> float:

        if (Seq == 1):
            self.JSON_Queue_of_DY_Close.clear()
            # ......................................
            self.JSON_Queue_of_DY_Close.append(DY_Close)
            # ......................................
            return DY_Close

        if (Seq >= 2):
            self.JSON_Queue_of_DY_Close.append(DY_Close)
            # ......................................
            return self.JSON_Queue_of_DY_Close[-1]  # 返回日 (Day) 数据 <收盘价> 的末尾值

    def WK_Change(self, Seq:int, DY_Change:float) -> float:

        if (Seq == 1):
            self.JSON_Queue_of_DY_Change.clear()
            # ......................................
            self.JSON_Queue_of_DY_Change.append(DY_Change)
            # ......................................
            return DY_Change

        if (Seq >= 2):
            self.JSON_Queue_of_DY_Change.append(DY_Change)
            # ......................................
            return sum(self.JSON_Queue_of_DY_Change)  # 返回日 (Day) 数据 <涨跌额> 的合计值

    def WK_Volume(self, Seq:int, DY_Volume:float) -> float:

        if (Seq == 1):
            self.JSON_Queue_of_DY_Volume.clear()
            # ......................................
            self.JSON_Queue_of_DY_Volume.append(DY_Volume)
            # ......................................
            return DY_Volume

        if (Seq >= 2):
            self.JSON_Queue_of_DY_Volume.append(DY_Volume)
            # ......................................
            return sum(self.JSON_Queue_of_DY_Volume)  # 返回日 (Day) 数据 <成交量> 的合计值

# EOF Signed by GF.
