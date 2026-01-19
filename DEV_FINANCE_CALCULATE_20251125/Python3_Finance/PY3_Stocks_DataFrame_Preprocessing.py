# GF_PY3_CLASS/Python3_Finance/PY3_Stocks_DataFrame_Preprocessing.py
# Create By GF 2024-01-22 18:16

import pandas

# ##################################################

class PY3_Stocks_DataFrame_Preprocessing(object):

    def __init__(self):

        self.DICT_Column_Name_Mapping:dict = {
            "ts_code": "code",
            "pct_chg": "chg_pct",
            "vol":     "volume"
        }

    def Before_Calculating_Stocks_Daily_Indicators(self, DataFrame) -> object:

        df = DataFrame.copy()
        # ..........................................
        df = df.rename(columns = self.DICT_Column_Name_Mapping)

        # ############ #
        # 数据类型调整 #
        # ############ #

        df["time0"  ] = pandas.to_datetime(df["time"], format = "mixed", errors = "coerce")  # errors = "coerce" 将无效日期转为 NaT
        # ..........................................
        df["open"   ] = df["open"   ].astype("float64")
        df["high"   ] = df["high"   ].astype("float64")
        df["low"    ] = df["low"    ].astype("float64")
        df["close"  ] = df["close"  ].astype("float64")
        df["change" ] = df["change" ].astype("float64")
        df["volume" ] = df["volume" ].astype("float64")

        # ############ #
        # 数据行号分配 #
        # ############ #

        df["row_num"] = df.groupby("code")["time0"].rank(method = "first", ascending = True)
        df["row_num"] = df["row_num"].astype("int64")

        # ############ #
        # 数据准备就绪 #
        # ############ #

        df = df.sort_values(["code", "time0"], ascending = [True, True])
        df = df.reset_index(drop = True)

        return df

    def Before_Calculating_Stocks_Weekly_Indicators(self, DataFrame) -> object:

        return self.Before_Calculating_Stocks_Daily_Indicators(DataFrame = DataFrame)

    def Before_Converting_Stocks_Daily_to_Weekly(self, DataFrame) -> object:

        df = DataFrame.copy()
        # ..........................................
        df = df.rename(columns = self.DICT_Column_Name_Mapping)

        # ############ #
        # 数据类型调整 #
        # ############ #

        df["time0"  ] = pandas.to_datetime(df["time"], format = "mixed", errors = "coerce")  # errors = "coerce" 将无效日期转为 NaT
        # ..........................................
        df["open"   ] = df["open"   ].astype("float64")
        df["high"   ] = df["high"   ].astype("float64")
        df["low"    ] = df["low"    ].astype("float64")
        df["close"  ] = df["close"  ].astype("float64")
        df["change" ] = df["change" ].astype("float64")
        df["volume" ] = df["volume" ].astype("float64")

        # ############ #
        # 基础数据计算 #
        # ############ #

        # 提取必要数据: 年份 (Year), 本年中第几周 (Week Number)
        df["year"    ] = df["time0"   ].dt.year
        df["year"    ] = df["year"    ].astype("string")
        df["week_num"] = df["time0"   ].dt.strftime("%U")  # 其中 %U 表示本年中的第几周
        df["week_num"] = df["week_num"].str.zfill(2)       # 函数 str().zfill() 用于将字符串填充 0 至指定宽度
        # ..........................................
        df["iso_8601_week"] = df["year"] + "-W" + df["week_num"]  # ISO 8601 表示周采用 YYYY-Www 格式

        # ############ #
        # 数据行号分配 #
        # ############ #

        df["row_num"] = df[["code", "iso_8601_week", "time0"]].groupby(["code", "iso_8601_week"], as_index = False).rank(method = "first", ascending = True)
        df["row_num"] = df["row_num"].astype("int64")

        # ############ #
        # 数据准备就绪 #
        # ############ #

        df = df.sort_values(["code", "time0"], ascending = [True, True])
        df = df.reset_index(drop = True)

        return df

# EOF Signed by GF.
