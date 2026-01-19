# GF_PY3_CLASS/Python3_Pandas2/PY3_Pandas2_DataFrame_Cells_Search.py
# Create by GF 2025-09-19 16:53

import pandas  # Pandas 2.0.3 (Dependency: xlrd 2.0.2, OpenPyXL 3.1.5)

# ##################################################

class PY3_Pandas2_DataFrame_Cells_Search(object):

    def Decimal_Compare_Without_Errors(self, Decimal_A:float, Decimal_B:float) -> int:

        try:
            if (Decimal_A == Decimal_B):
                return 1
            else:
                return 0
        except Exception as e:
            return 0

    def Integer_Compare_Without_Errors(self, Integer_A:int, Integer_B:int) -> int:

        try:
            if (Integer_A == Integer_B):
                return 1
            else:
                return 0
        except Exception as e:
            return 0

    def String_Compare_Without_Errors(self, Short_String:str, Long_String:str) -> int:

        try:
            if (Short_String in Long_String):
                return 1
            else:
                return 0
        except Exception as e:
            return 0

    def Cells_Search(self, DataFrame, Target:object, First_N_Rows:int = 0) -> list:

        df = DataFrame
        # ..........................................
        LIST_Result:list = []
        # ..........................................
        for Row in DataFrame.index:
            for Col in DataFrame.columns:
                Cell_Value = df.loc[Row, Col]
                # ..................................
                if (isinstance(Target, float) == True):
                    if (self.Decimal_Compare_Without_Errors(Target, Cell_Value) == 1):
                        LIST_Result.append(Cell_Value)
                # ..................................
                if (isinstance(Target, int) == True):
                    if (self.Integer_Compare_Without_Errors(Target, Cell_Value) == 1):
                        LIST_Result.append(Cell_Value)
                # ..................................
                if (isinstance(Target, str) == True):
                    if (self.String_Compare_Without_Errors(Target, Cell_Value) == 1):
                        LIST_Result.append(Cell_Value)
            # ......................................
            if (First_N_Rows > 0 and First_N_Rows == Row):
                    break
        # ..........................................
        return LIST_Result

# EOF Signed by GF.
