# PY3_JSON_Records_Library.py
# Create by GF 2025-12-22 15:13

import copy

# ##################################################

class PY3_JSON_Records_Library(object):

    def Fill_Null(self, Records:list, Field, Value) -> list:

        Records_Copy:list = copy.deepcopy(Records)  # 深拷贝 (完全独立)
        # ..........................................
        i:int = 0
        while (i < len(Records_Copy)):
            if (Records_Copy[i].get(Field) is None):
                Records_Copy[i].update({Field: Value})
            i = i + 1
        # ..........................................
        return Records_Copy

    def Bubble_Sort_Ascending(self, Records:list, By:str) -> list:

        # Algorithm Description (Ascending):
        # Initial: Array = [5, 6, 4]
        # Round 0: Array = [5, 4, 6]  # 5 < 6 (Keep Position), 6 > 4 (Swap Position)
        # Round 1: Array = [4, 5, 6]  # 5 > 4 (Swap Position), 5 < 6 (Keep Position)

        Records_Copy:list = copy.deepcopy(Records)  # 深拷贝 (完全独立)
        # ..........................................
        Sort_Round:int = 0  # 第 N 轮排序
        Sort_Total:int = len(Records_Copy) - 1  # 排序总次数
        while (Sort_Round < Sort_Total):
            Swapped:int = 0  # 判断是否 Swapped (已经发生交换, 判断 "数组已经排序完毕" 的依据)
            # ......................................
            i:int = 0
            while (i < (Sort_Total - Sort_Round)):
                k:int = i + 1
                if (Records_Copy[i][By] > Records_Copy[k][By]):
                    Temporary:dict  = Records_Copy[i]  # 3 杯水交换法
                    Records_Copy[i] = Records_Copy[k]
                    Records_Copy[k] = Temporary
                    Swapped = 1
                i = i + 1
            # ......................................
            if (Swapped == 0):  # 数组没有发生任何交换, 说明数组已经完全有序
                break
            # ......................................
            Sort_Round = Sort_Round + 1
        # ..........................................
        return Records_Copy

    def Bubble_Sort_Descending(self, Records:list, By:str) -> list:

        # Algorithm Description (Descending):
        # Initial: Array = [5, 4, 6]
        # Round 0: Array = [5, 6, 4]  # 5 > 4 (Keep Position), 4 < 6 (Swap Position)
        # Round 1: Array = [6, 5, 4]  # 5 < 6 (Swap Position), 5 > 4 (Keep Position)

        Records_Copy:list = copy.deepcopy(Records)  # 深拷贝 (完全独立)
        # ..........................................
        Sort_Round:int = 0
        Sort_Total:int = len(Records_Copy) - 1
        while (Sort_Round < Sort_Total):
            Swapped:int = 0
            # ......................................
            i:int = 0
            while (i < (Sort_Total - Sort_Round)):
                k:int = i + 1
                if (Records_Copy[i][By] < Records_Copy[k][By]):
                    Temporary:dict  = Records_Copy[i]
                    Records_Copy[i] = Records_Copy[k]
                    Records_Copy[k] = Temporary
                    Swapped = 1
                i = i + 1
            # ......................................
            if (Swapped == 0):
                break
            # ......................................
            Sort_Round = Sort_Round + 1
        # ..........................................
        return Records_Copy

# EOF Signed by GF.
