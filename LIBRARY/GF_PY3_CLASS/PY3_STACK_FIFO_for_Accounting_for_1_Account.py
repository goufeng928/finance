# GF_PY3_CLASS/PY3_STACK_FIFO_for_Accounting_for_1_Account.py
# Create by GF 2025-08-15 10:46

import pandas  # Pandas 2.0.3
# ..................................................
import PY3_STACK_FIFO_for_Accounting

# ##################################################

class PY3_STACK_FIFO_for_Accounting_for_1_Account(object):

    # Examples:
    # >>> # 示例数据 (输入数据):
    # >>> Records = [{"ROW_NUM": 1, "ID":  5, "时间": "2022-12-31", "借方":    0, "贷方": 200, "借贷标志": "贷", "发生额": -200},
    # ...            {"ROW_NUM": 2, "ID":  6, "时间": "2023-12-31", "借方":    0, "贷方": 300, "借贷标志": "贷", "发生额": -300},
    # ...            {"ROW_NUM": 3, "ID":  7, "时间": "2024-06-30", "借方": 1000, "贷方":   0, "借贷标志": "借", "发生额": 1000},
    # ...            {"ROW_NUM": 4, "ID":  8, "时间": "2024-12-31", "借方":    0, "贷方": 600, "借贷标志": "贷", "发生额": -600},
    # ...            {"ROW_NUM": 5, "ID":  9, "时间": "2025-04-30", "借方":  300, "贷方":   0, "借贷标志": "借", "发生额":  300},
    # ...            {"ROW_NUM": 6, "ID": 10, "时间": "2025-05-31", "借方":    0, "贷方": 400, "借贷标志": "贷", "发生额": -400},
    # ...            {"ROW_NUM": 7, "ID": 11, "时间": "2025-06-30", "借方":  300, "贷方":   0, "借贷标志": "借", "发生额":  300},
    # ...            {"ROW_NUM": 8, "ID": 12, "时间": "2025-07-31", "借方":  400, "贷方":   0, "借贷标志": "借", "发生额":  400}]
    # >>>
    # >>> import pandas
    # >>>
    # >>> df = pandas.DataFrame(Records)
    # >>> df["发生额剩余数"] = df["发生额"]  # 初始化 "发生额剩余数"
    # >>> print(df)
    #    ROW_NUM  ID        时间  借方  贷方  借贷标志  发生额  发生额剩余数
    # 0        1   5  2022-12-31     0   200        贷    -200          -200
    # 1        2   6  2023-12-31     0   300        贷    -300          -300
    # 2        3   7  2024-06-30  1000     0        借    1000          1000
    # 3        4   8  2024-12-31     0   600        贷    -600          -600
    # 4        5   9  2025-04-30   300     0        借     300           300
    # 5        6  10  2025-05-31     0   400        贷    -400          -400
    # 6        7  11  2025-06-30   300     0        借     300           300
    # 7        8  12  2025-07-31   400     0        借     400           400
    # >>>
    # >>> # 初始化类 (Class)
    # >>> STACK_FIFO_1_Account = PY3_STACK_FIFO_for_Accounting_for_1_Account()
    # >>>
    # >>> # 传入示例数据: 用例 (1), 计算所有 "被多次冲抵之后的发生额" 的剩余数
    # >>> Result = STACK_FIFO_1_Account.Run(Pandas_DataFrame = df, return_value = "remaining")
    # >>> print(Result)
    #    ROW_NUM  ID         时间  借方  贷方  借贷标志  发生额  发生额剩余数
    # 0        1   5   2022-12-31     0   200        贷    -200             0
    # 1        2   6   2023-12-31     0   300        贷    -300             0
    # 2        3   7   2024-06-30  1000     0        借    1000             0
    # 3        4   8   2024-12-31     0   600        贷    -600             0
    # 4        5   9   2025-04-30   300     0        借     300             0
    # 5        6  10   2025-05-31     0   400        贷    -400             0
    # 6        7  11   2025-06-30   300     0        借     300           100
    # 7        8  12   2025-07-31   400     0        借     400           400
    # >>>
    # >>> # 传入示例数据: 用例 (2), 计算所有 "用于冲抵发生额的消耗数" 的被消耗明细
    # >>> Result = STACK_FIFO_1_Account.Run(Pandas_DataFrame = df, return_value = "discarded")
    # >>> print(Result)
    #    ROW_NUM  ID  Direction  Occurrence  Remaining  Consumed  Consumer
    # 0        1   5        OUT         200          0       200         7
    # 1        2   6        OUT         300          0       300         7
    # 2        3   7         IN        1000          0       500         8
    # 3        4   8        OUT         600          0       100         9
    # 4        5   9         IN         300          0       200        10
    # 5        6  10        OUT         400          0       200        11

    def Run(self, Pandas_DataFrame, return_value:str = "remaining") -> dict:

        TEMP = Pandas_DataFrame.copy()
        # ..........................................
        Head_Symbol:str  = "资产" if (TEMP.loc[0, "借贷标志"] == "借") else "负债"  # 初始化首行借贷标志
        TAIL_ROWNUM:int  = TEMP["ROW_NUM"].max()  # 停止条件 (保险)
        List_DISUSE:list = []
        List_PROCES:list = []

        STACKAccounting = PY3_STACK_FIFO_for_Accounting.PY3_STACK_FIFO_for_Accounting()

        DEBUG_COUNTER = 30  # 防止陷入无限循环 (保险)
        while (TEMP.empty != True and 0 < DEBUG_COUNTER):

            if (Head_Symbol == "资产"):

                for i, ROW in TEMP.iterrows():

                    if (ROW["借贷标志"] == "贷"):  # 与首行借贷标志相反 (开始消耗)

                        Occurrence_Remaining = STACKAccounting.Comsuming_for_IN(ID = ROW["ID"], Occurrence = ROW["发生额剩余数"] * (-1))

                        if (Occurrence_Remaining == 0):

                            TEMP.loc[i, "发生额剩余数"] = 0
                            List_PROCES.append(TEMP.loc[i, :].to_dict())
                            TEMP = TEMP[i < TEMP.index]  # 推进到下一行 (下次迭代从 "当前行 + 1" 开始)
                            break

                        if (Occurrence_Remaining != 0):  # 合同资产性质改变 (从 "资产" 转为 "负债")

                            TEMP.loc[i, "发生额剩余数"] = Occurrence_Remaining * (-1)
                            List_PROCES.append(TEMP.loc[i, :].to_dict())
                            TEMP = TEMP[i <= TEMP.index]  # 下次迭代从 "当前行" 开始)
                            Head_Symbol = "负债"
                            break

                    if (ROW["借贷标志"] == "借"):

                        Record = {
                            "ROW_NUM":    ROW["ROW_NUM"],
                            "ID":         ROW["ID"],
                            "Direction":  "IN",
                            "Occurrence": ROW["发生额"],
                            "Remaining":  ROW["发生额剩余数"]
                        }
                        STACKAccounting.IN.append(Record)

                    if (ROW["ROW_NUM"] == TAIL_ROWNUM):

                        TEMP = pandas.DataFrame()
                        break

            if (Head_Symbol == "负债"):

                for i, ROW in TEMP.iterrows():

                    if (ROW["借贷标志"] == "借"):  # 与首行借贷标志相反 (开始消耗)

                        Occurrence_Remaining = STACKAccounting.Comsuming_for_OUT(ID = ROW["ID"], Occurrence = ROW["发生额剩余数"])

                        if (Occurrence_Remaining == 0):

                            TEMP.loc[i, "发生额剩余数"] = 0
                            List_PROCES.append(TEMP.loc[i, :].to_dict())
                            TEMP = TEMP[i < TEMP.index]  # 推进到下一行 (下次迭代从 "当前行 + 1" 开始)
                            break

                        if (Occurrence_Remaining != 0):  # 合同资产性质改变 (从 "负债" 转为 "资产")

                            TEMP.loc[i, "发生额剩余数"] = Occurrence_Remaining
                            List_PROCES.append(TEMP.loc[i, :].to_dict())
                            TEMP = TEMP[i <= TEMP.index]  # 下次迭代从 "当前行" 开始)
                            Head_Symbol = "资产"
                            break

                    if (ROW["借贷标志"] == "贷"):

                        Record = {
                            "ROW_NUM":    ROW["ROW_NUM"],
                            "ID":         ROW["ID"],
                            "Direction":  "OUT",
                            "Occurrence": ROW["发生额"] * (-1),  # 转换为正数
                            "Remaining":  ROW["发生额剩余数"] * (-1)   # 转换为正数
                        }
                        STACKAccounting.OUT.append(Record)

                    if (ROW["ROW_NUM"] == TAIL_ROWNUM):

                        TEMP = pandas.DataFrame()
                        break

            #DEBUG_COUNTER = DEBUG_COUNTER - 1

        RESULT = Pandas_DataFrame[["ROW_NUM", "ID", "时间", "借方", "贷方", "借贷标志", "发生额"]].copy()
        # ..........................................
        PROCES = pandas.DataFrame(List_PROCES)  # 过程中的发生额 "剩余数"
        # >>> print(PROCES)
        #    ROW_NUM  ID          时间  借方  贷方  借贷标志  发生额  发生额剩余数
        # 0        3   7    2024-06-30  1000     0        借    1000           500
        # 1        4   8    2024-12-31     0   600        贷    -600          -100
        # 2        5   9    2025-04-30   300     0        借     300           200
        # 3        6  10    2025-05-31     0   400        贷    -400          -200
        # 4        7  11    2025-06-30   300     0        借     300           100
        if (PROCES.empty != True):
            PROCES = PROCES[["ID", "发生额剩余数"]].groupby("ID", as_index = False).agg({"发生额剩余数": "last"})
            # >>> print(PROCES)
            #    ID  发生额剩余数
            # 0   7           500
            # 1   8          -100
            # 2   9           200
            # 3  10          -200
            # 4  11           100
        # ..........................................
        # ########## 提取 "栈 (Stack)" 队列: "尚处在队列中" (剩余数可能已经发生变化) ##########
        IN_OUT = pandas.concat([pandas.DataFrame(STACKAccounting.IN), pandas.DataFrame(STACKAccounting.OUT)])
        # >>> print(IN_OUT)
        #    ROW_NUM  ID  Direction  Occurrence  Remaining
        # 0        7  11         IN         300        100
        # 1        8  12         IN         400        400
        if (IN_OUT.empty != True):
            IN_OUT["Remaining"] = IN_OUT.apply(lambda ROW: ROW["Remaining"] * (-1) if (ROW["Direction"] == "OUT") else ROW["Remaining"], axis = 1)  # 添加符号
        # ..........................................
        # ########## 提取 "栈 (Stack)" 队列: "消耗数 / 剩余数" 最终明细 ##########
        DISUSE = pandas.DataFrame(STACKAccounting.DISUSE)
        # >>> print(DISUSE)
        #    ROW_NUM  ID  Direction  Occurrence  Remaining  Consumed  Consumer
        # 0        1   5        OUT         200          0       200         7
        # 1        2   6        OUT         300          0       300         7
        # 2        3   7         IN        1000          0       500         8
        # 3        4   8        OUT         600          0       100         9
        # 4        5   9         IN         300          0       200        10
        # 5        6  10        OUT         400          0       200        11
        if (DISUSE.empty != True):
            DISUSE["Consumed"] = DISUSE.apply(lambda ROW: ROW["Consumed"] * (-1) if (ROW["Direction"] == "OUT") else ROW["Consumed"], axis = 1)  # 添加符号
            # 数据聚合: "消耗数 -> 合计消耗数", "剩余数 -> 最后剩余数"
            DISUSE = DISUSE[["ID", "Consumed", "Remaining"]].groupby("ID", as_index = False).agg({"Consumed": "sum", "Remaining": "last"})
            # >>> print(DISUSE)
            #    ID  Consumed  Remaining
            # 0   5      -200          0
            # 1   6      -300          0
            # 2   7       500          0
            # 3   8      -100          0
            # 4   9       200          0
            # 5  10      -200          0
        # ..........................................
        RESULT["发生额剩余数"] = None
        # ..........................................
        if (PROCES.empty != True):
            for _ID_ in PROCES["ID"].drop_duplicates().values.tolist():
                RESULT_Index = RESULT[RESULT["ID"] == _ID_].index
                PROCES_Value = PROCES[PROCES["ID"] == _ID_]["发生额剩余数"].values[0]
                RESULT.loc[RESULT_Index, "发生额剩余数"] = PROCES_Value
        # ..........................................
        if (DISUSE.empty != True):
            for _ID_ in DISUSE["ID"].drop_duplicates().values.tolist():
                RESULT_Index = RESULT[RESULT["ID"] == _ID_].index
                DISUSE_Value = DISUSE[DISUSE["ID"] == _ID_]["Remaining"].values[0]
                RESULT.loc[RESULT_Index, "发生额剩余数"] = DISUSE_Value
        # ..........................................
        if (IN_OUT.empty != True):
            for _ID_ in IN_OUT["ID"].drop_duplicates().values.tolist():
                RESULT_Index = RESULT[RESULT["ID"] == _ID_].index
                IN_OUT_Value = IN_OUT[IN_OUT["ID"] == _ID_]["Remaining"].values[0]
                RESULT.loc[RESULT_Index, "发生额剩余数"] = IN_OUT_Value

        # ------------- #
        # Return Result #
        # ------------- #

        if (return_value.lower() == "remaining"):  # 结果包含 "被多次冲抵之后的发生额" 的剩余数
            return RESULT
        # ..........................................
        if (return_value.lower() == "discarded"):  # 结果包含 "用于冲抵发生额的消耗数" 的被消耗明细
            return pandas.DataFrame(STACKAccounting.DISUSE)

# Signed by GF.
