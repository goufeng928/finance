# GF_PY3_CLASS/PY3_STACK_FIFO_for_Accounting.py
# Create by GF 2025-08-15 10:46

import jmespath  # JMESPath 1.0.1

# ##################################################

class PY3_STACK_FIFO_for_Accounting(object):

    def __init__(self):

        self.IN:list     = []  # Example: [{"ROW_NUM": 1, "ID": 25, "Direction": "IN",  "Occurrence": 125.80, "Remaining": 125.80}, ...]
        self.OUT:list    = []  # Example: [{"ROW_NUM": 6, "ID": 31, "Direction": "OUT", "Occurrence": 220.05, "Remaining": 220.05}, ...]
        self.DISUSE:list = []  # Example: [{"ROW_NUM": 1, "ID": 25, "Direction": "IN",  "Occurrence": 125.80, "Consumed": 60.00, "Consumer": 52}, ...]

    def Comsuming_for_IN(self, ID:int, Occurrence:float) -> float:

        Occurrence_Remove_Symbols:float = Occurrence

        if (Occurrence < 0):
            # 去除 "发生额 (Occurrence)" 的符号
            Occurrence_Remove_Symbols = Occurrence * (-1)

        # 本次发生额的余额 (类似于 "用 100 元去商店消费 A 商品 50 元, B 商品 20 元, 应找零 30 元")
        Occurrence_Remaining:float = Occurrence_Remove_Symbols

        Cumulative_Comsuming:float = 0
        while (Cumulative_Comsuming < Occurrence_Remove_Symbols and self.IN != []):
            # 从 "栈 (Stack)" 顶开始消耗资产
            PROPERTY = jmespath.search(f""" [0].Remaining """, self.IN)  # 筛选出第 1 条并取 Remaining 的值
            # ......................................
            Cumulative_Comsuming = Cumulative_Comsuming + PROPERTY
            # ......................................
            if (Cumulative_Comsuming > Occurrence_Remove_Symbols):
                # 如果: 累计消耗额 > 发生额 (无符号)
                # 计算 "溢出 (Overflow) 部分"
                Overflow = Cumulative_Comsuming - Occurrence_Remove_Symbols
                # 修改 "栈 (Stack)" 顶的余额为 "溢出 (Overflow)" 数
                self.IN[0]["Remaining"] = round(Overflow, 4)
                # ..................................
                Occurrence_Remaining = 0
                # ..................................
                # 将已经被消耗的部分转移到 DISUSE 队列
                FERRY = self.IN[0].copy()  # 必须 "拷贝 (Copy)" 而不是 "引用 (Quote)"
                FERRY["Consumed"] = round(FERRY["Occurrence"] - Overflow, 4)
                FERRY["Consumer"] = ID
                #TRASH = FERRY.pop("Remaining")
                # ..................................
                self.DISUSE.append(FERRY)
                # ..................................
                # "栈 (Stack)" 顶尚存在余额, 跳过 "转移到 DISUSE 队列" 的过程
                break
            if (Cumulative_Comsuming == Occurrence_Remove_Symbols):
                # 如果: 累计消耗额 == 发生额 (无符号)
                # 直至本次消耗, 刚好将 "发生额 (无符号)" 冲抵为 0, 本次消耗后 "栈 (Stack)" 顶余额为 0, 转移到 DISUSE 队列
                Occurrence_Remaining = 0
                # ..................................
                FERRY = self.IN.pop(0)
                FERRY["Consumed" ] = FERRY["Occurrence"]
                FERRY["Consumer" ] = ID
                FERRY["Remaining"] = 0
                #TRASH = FERRY.pop("Remaining")
                # ..................................
                self.DISUSE.append(FERRY)
                break
            if (Cumulative_Comsuming < Occurrence_Remove_Symbols):
                # 如果: 累计消耗额 < 发生额 (无符号)
                # 直至本次消耗, 尚未将 "发生额 (无符号)" 冲抵为 0, 本次消耗后 "栈 (Stack)" 顶余额为 0, 转移到 DISUSE 队列
                FERRY = self.IN.pop(0)
                FERRY["Consumed" ] = FERRY["Remaining"]
                FERRY["Consumer" ] = ID
                FERRY["Remaining"] = 0
                #TRASH = FERRY.pop("Remaining")
                # ..................................
                self.DISUSE.append(FERRY)

        # 如果: 队列消耗完后, "累计消耗额 < 发生额 (无符号)" 依然成立 (队列中存在的所有资产不足以抵冲本次发生额)
        if (Cumulative_Comsuming < Occurrence_Remove_Symbols):
            # 本次发生额存在余额 (Occurrence Remaining)
            Occurrence_Remaining = Occurrence_Remove_Symbols - Cumulative_Comsuming

        return round(Occurrence_Remaining, 4)

    def Comsuming_for_OUT(self, ID:int, Occurrence:float) -> float:

        Occurrence_Remove_Symbols:float = Occurrence

        if (Occurrence < 0):
            # 去除 "发生额 (Occurrence)" 的符号
            Occurrence_Remove_Symbols = Occurrence * (-1)

        # 本次发生额的余额 (类似于 "因 A 业务负债 50 元, B 业务负债 70 元, 本次用 100 元还款, 剩余负债 20 元")
        Occurrence_Remaining:float = Occurrence_Remove_Symbols

        Cumulative_Comsuming:float = 0
        while (Cumulative_Comsuming < Occurrence_Remove_Symbols and self.OUT != []):
            # 从 "栈 (Stack)" 顶开始消耗资产
            PROPERTY = jmespath.search(f""" [0].Remaining """, self.OUT)  # 筛选出第 1 条并取 Remaining 的值
            # ......................................
            Cumulative_Comsuming = Cumulative_Comsuming + PROPERTY
            # ......................................
            if (Cumulative_Comsuming > Occurrence_Remove_Symbols):
                # 如果: 累计消耗额 > 发生额 (无符号)
                # 计算 "溢出 (Overflow) 部分"
                Overflow = Cumulative_Comsuming - Occurrence_Remove_Symbols
                # 修改 "栈 (Stack)" 顶的余额为 "溢出 (Overflow)" 数
                self.OUT[0]["Remaining"] = round(Overflow, 4)
                # ..................................
                Occurrence_Remaining = 0
                # ..................................
                # 将已经被消耗的部分转移到 DISUSE 队列
                FERRY = self.OUT[0].copy()  # 必须 "拷贝 (Copy)" 而不是 "引用 (Quote)"
                FERRY["Consumed"] = round(FERRY["Occurrence"] - Overflow, 4)
                FERRY["Consumer"] = ID
                #TRASH = FERRY.pop("Remaining")
                # ..................................
                self.DISUSE.append(FERRY)
                # ..................................
                # "栈 (Stack)" 顶尚存在余额, 跳过 "转移到 DISUSE 队列" 的过程
                break
            if (Cumulative_Comsuming == Occurrence_Remove_Symbols):
                # 如果: 累计消耗额 == 发生额 (无符号)
                # 直至本次消耗, 刚好将 "发生额 (无符号)" 冲抵为 0, 本次消耗后 "栈 (Stack)" 顶余额为 0, 转移到 DISUSE 队列
                Occurrence_Remaining = 0
                # ..................................
                FERRY = self.OUT.pop(0)
                FERRY["Consumed" ] = FERRY["Remaining"]
                FERRY["Consumer" ] = ID
                FERRY["Remaining"] = 0
                #TRASH = FERRY.pop("Remaining")
                # ..................................
                self.DISUSE.append(FERRY)
                break
            if (Cumulative_Comsuming < Occurrence_Remove_Symbols):
                # 如果: 累计消耗额 < 发生额 (无符号)
                # 直至本次消耗, 尚未将 "发生额 (无符号)" 冲抵为 0, 本次消耗后 "栈 (Stack)" 顶余额为 0, 转移到 DISUSE 队列
                FERRY = self.OUT.pop(0)
                FERRY["Consumed" ] = FERRY["Remaining"]
                FERRY["Consumer" ] = ID
                FERRY["Remaining"] = 0
                #TRASH = FERRY.pop("Remaining")
                # ..................................
                self.DISUSE.append(FERRY)

        # 如果: 队列消耗完后, "累计消耗额 < 发生额 (无符号)" 依然成立 (偿清队列中存在的所有负债尚有剩余)
        if (Cumulative_Comsuming < Occurrence_Remove_Symbols):
            # 本次发生额尚有剩余 (Occurrence Remaining)
            Occurrence_Remaining = Occurrence_Remove_Symbols - Cumulative_Comsuming

        return round(Occurrence_Remaining, 4)

# #################### EXAMPLES ####################

# >>> STACKAccounting = STACK_for_Accounting()
# >>> STACKAccounting.IN.append({"ROW_NUM": 1, "ID": 25, "Direction": "IN", "Occurrence": 125.80, "Remaining": 125.80})
# >>> STACKAccounting.IN.append({"ROW_NUM": 2, "ID": 26, "Direction": "IN", "Occurrence": 188.81, "Remaining": 188.81})
# >>> STACKAccounting.IN.append({"ROW_NUM": 3, "ID": 27, "Direction": "IN", "Occurrence": 252.02, "Remaining": 252.02})
# >>> print("[DEBUG] STACK_for_Accounting 中的 IN 队列:")
# >>> print(str(STACKAccounting.IN).replace("},", '},\n'))
# >>> print("[DEBUG] JSONPath-NG 测试 (XPATH 表达式取值): ", jsonpath_ng.parse('$.[0].ID').find(STACKAccounting.IN)[0].value)
# [DEBUG] STACK_for_Accounting 中的 IN 队列:
# [{'ROW_NUM': 1, 'ID': 25, 'Direction': 'IN', 'Occurrence': 125.8, 'Remaining': 125.8},
#  {'ROW_NUM': 2, 'ID': 26, 'Direction': 'IN', 'Occurrence': 188.81, 'Remaining': 188.81},
#  {'ROW_NUM': 3, 'ID': 27, 'Direction': 'IN', 'Occurrence': 252.02, 'Remaining': 252.02}]
# [DEBUG] JSONPath-NG 测试 (XPATH 表达式取值):  25
# >>>
# >>> STACKAccounting = STACK_for_Accounting()
# >>> STACKAccounting.IN.append({"ROW_NUM": 1, "ID": 25, "Direction": "IN", "Occurrence": 125.80, "Remaining": 125.80})
# >>> STACKAccounting.IN.append({"ROW_NUM": 2, "ID": 26, "Direction": "IN", "Occurrence": 188.81, "Remaining": 188.81})
# >>> STACKAccounting.IN.append({"ROW_NUM": 3, "ID": 27, "Direction": "IN", "Occurrence": 252.02, "Remaining": 252.02})
# >>> print("[DEBUG] 发生额冲抵前的 IN 队列:")
# >>> print(str(STACKAccounting.IN).replace("},", '},\n'))
# >>> print("[DEBUG] 本次发生额: 600.00, 余额: ", STACKAccounting.Comsuming_for_IN(ID = 52, Occurrence = 600.00))
# >>> print("[DEBUG] 发生额冲抵后的 IN 队列:")
# >>> print(str(STACKAccounting.IN).replace("},", '},\n'))
# >>> print("[DEBUG] 发生额冲抵后的 DISUSE 队列:")
# >>> print(str(STACKAccounting.DISUSE).replace("},", '},\n'))
# >>>
# [DEBUG] 发生额冲抵前的 IN 队列:
# [{'ROW_NUM': 1, 'ID': 25, 'Direction': 'IN', 'Occurrence': 125.8, 'Remaining': 125.8},
#  {'ROW_NUM': 2, 'ID': 26, 'Direction': 'IN', 'Occurrence': 188.81, 'Remaining': 188.81},
#  {'ROW_NUM': 3, 'ID': 27, 'Direction': 'IN', 'Occurrence': 252.02, 'Remaining': 252.02}]
# [DEBUG] 本次发生额: 600.00, 余额:  33.37
# [DEBUG] 发生额冲抵后的 IN 队列:
# []
# [DEBUG] 发生额冲抵后的 DISUSE 队列:
# [{'ROW_NUM': 1, 'ID': 25, 'Direction': 'IN', 'Occurrence': 125.8, 'Remaining': 0, 'Consumed': 125.8, 'Consumer': 52},
#  {'ROW_NUM': 2, 'ID': 26, 'Direction': 'IN', 'Occurrence': 188.81, 'Remaining': 0, 'Consumed': 188.81, 'Consumer': 52},
#  {'ROW_NUM': 3, 'ID': 27, 'Direction': 'IN', 'Occurrence': 252.02, 'Remaining': 0, 'Consumed': 252.02, 'Consumer': 52}]
# >>>
# >>> STACKAccounting = STACK_for_Accounting()
# >>> STACKAccounting.IN.append({"ROW_NUM": 1, "ID": 28, "Direction": "IN", "Occurrence": 125.80, "Remaining": 125.80})
# >>> STACKAccounting.IN.append({"ROW_NUM": 2, "ID": 29, "Direction": "IN", "Occurrence": 188.81, "Remaining": 188.81})
# >>> STACKAccounting.IN.append({"ROW_NUM": 3, "ID": 30, "Direction": "IN", "Occurrence": 252.02, "Remaining": 252.02})
# >>> print("[DEBUG] 发生额冲抵前的 IN 队列:")
# >>> print(str(STACKAccounting.IN).replace("},", '},\n'))
# >>> print("[DEBUG] 本次发生额: 600.00, 余额: ", STACKAccounting.Comsuming_for_IN(ID = 53, Occurrence = 60.00))
# >>> print("[DEBUG] 本次发生额: 600.00, 余额: ", STACKAccounting.Comsuming_for_IN(ID = 54, Occurrence = 70.00))
# >>> print("[DEBUG] 发生额冲抵后的 IN 队列:")
# >>> print(str(STACKAccounting.IN).replace("},", '},\n'))
# >>> print("[DEBUG] 发生额冲抵后的 DISUSE 队列:")
# >>> print(str(STACKAccounting.DISUSE).replace("},", '},\n'))
# [DEBUG] 发生额冲抵前的 IN 队列:
# [{'ROW_NUM': 1, 'ID': 28, 'Direction': 'IN', 'Occurrence': 125.8, 'Remaining': 125.8},
#  {'ROW_NUM': 2, 'ID': 29, 'Direction': 'IN', 'Occurrence': 188.81, 'Remaining': 188.81},
#  {'ROW_NUM': 3, 'ID': 30, 'Direction': 'IN', 'Occurrence': 252.02, 'Remaining': 252.02}]
# [DEBUG] 本次发生额: 600.00, 余额:  0
# [DEBUG] 本次发生额: 600.00, 余额:  0
# [DEBUG] 发生额冲抵后的 IN 队列:
# [{'ROW_NUM': 2, 'ID': 29, 'Direction': 'IN', 'Occurrence': 188.81, 'Remaining': 184.61},
#  {'ROW_NUM': 3, 'ID': 30, 'Direction': 'IN', 'Occurrence': 252.02, 'Remaining': 252.02}]
# [DEBUG] 发生额冲抵后的 DISUSE 队列:
# [{'ROW_NUM': 1, 'ID': 28, 'Direction': 'IN', 'Occurrence': 125.8, 'Remaining': 65.8, 'Consumed': 60.0, 'Consumer': 53},
#  {'ROW_NUM': 1, 'ID': 28, 'Direction': 'IN', 'Occurrence': 125.8, 'Remaining': 0, 'Consumed': 65.8, 'Consumer': 54},
#  {'ROW_NUM': 2, 'ID': 29, 'Direction': 'IN', 'Occurrence': 188.81, 'Remaining': 184.61, 'Consumed': 4.2, 'Consumer': 54}]
# >>>
# >>> STACKAccounting = STACK_for_Accounting()
# >>> STACKAccounting.OUT.append({"ROW_NUM": 6, "ID": 31, "Direction": "OUT", "Occurrence": 220.05, "Remaining": 220.05})
# >>> STACKAccounting.OUT.append({"ROW_NUM": 7, "ID": 32, "Direction": "OUT", "Occurrence": 169.87, "Remaining": 169.87})
# >>> STACKAccounting.OUT.append({"ROW_NUM": 8, "ID": 33, "Direction": "OUT", "Occurrence": 180.50, "Remaining": 180.50})
# >>> print("[DEBUG] 发生额冲抵前的 OUT 队列:")
# >>> print(str(STACKAccounting.OUT).replace("},", '},\n'))
# >>> print("[DEBUG] 本次发生额: 530.00, 余额: ", STACKAccounting.Comsuming_for_OUT(ID = 66, Occurrence = 530.00))
# >>> print("[DEBUG] 发生额冲抵后的 OUT 队列:")
# >>> print(str(STACKAccounting.OUT).replace("},", '},\n'))
# >>> print("[DEBUG] 发生额冲抵后的 DISUSE 队列:")
# >>> print(str(STACKAccounting.DISUSE).replace("},", '},\n'))
# [DEBUG] 发生额冲抵前的 OUT 队列:
# [{'ROW_NUM': 6, 'ID': 31, 'Direction': 'OUT', 'Occurrence': 220.05, 'Remaining': 220.05},
#  {'ROW_NUM': 7, 'ID': 32, 'Direction': 'OUT', 'Occurrence': 169.87, 'Remaining': 169.87},
#  {'ROW_NUM': 8, 'ID': 33, 'Direction': 'OUT', 'Occurrence': 180.5, 'Remaining': 180.5}]
# [DEBUG] 本次发生额: 530.00, 余额:  0
# [DEBUG] 发生额冲抵后的 OUT 队列:
# [{'ROW_NUM': 8, 'ID': 33, 'Direction': 'OUT', 'Occurrence': 180.5, 'Remaining': 40.42}]
# [DEBUG] 发生额冲抵后的 DISUSE 队列:
# [{'ROW_NUM': 6, 'ID': 31, 'Direction': 'OUT', 'Occurrence': 220.05, 'Remaining': 0, 'Consumed': 220.05, 'Consumer': 66},
#  {'ROW_NUM': 7, 'ID': 32, 'Direction': 'OUT', 'Occurrence': 169.87, 'Remaining': 0, 'Consumed': 169.87, 'Consumer': 66},
#  {'ROW_NUM': 8, 'ID': 33, 'Direction': 'OUT', 'Occurrence': 180.5, 'Remaining': 40.42, 'Consumed': 140.08, 'Consumer': 66}]

# Signed by GF.
