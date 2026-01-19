# APP_Stocks_DataFrame_Calculator.py
# Create By GF 2024-01-22 18:16

import pandas
# ..................................................
from Python3_Finance import PY3_Finance_Entanglement_Theory
from Python3_Finance import PY3_Finance_Indicator_EMA
from Python3_Finance import PY3_Finance_Indicator_KDJ
from Python3_Finance import PY3_Finance_Indicator_MACD
from Python3_Finance import PY3_Finance_Indicator_SMA
from Python3_Finance import PY3_Stocks_Data_Conv_Daily_to_Weekly
from Python3_Finance import PY3_Stocks_DataFrame_Preprocessing

# ##################################################

class APP_Stocks_DataFrame_Calculator(object):

    def __init__(self):

        self.ITERATOR_LENGTH:int = 0
        self.ITERATOR_MAXIDX:int = self.ITERATOR_LENGTH - 1
        self.ITERATOR_MOVING:int = 0
        # ..........................................
        self.PUBLIC_DATAFRAME = pandas.DataFrame()
        self.PUBLIC_DATAFRAME_LENGTH:int = self.PUBLIC_DATAFRAME.shape[0]
        # ..........................................
        self.PUBLIC_JSON_RECORDS:list = []

        self.Fin_Etg_Theory  = PY3_Finance_Entanglement_Theory.PY3_Finance_Entanglement_Theory()
        self.Fin_Ind_EMA_P12 = PY3_Finance_Indicator_EMA.PY3_Finance_Indicator_EMA()
        self.Fin_Ind_EMA_P26 = PY3_Finance_Indicator_EMA.PY3_Finance_Indicator_EMA()
        self.Fin_Ind_KDJ     = PY3_Finance_Indicator_KDJ.PY3_Finance_Indicator_KDJ()
        self.Fin_Ind_MACD    = PY3_Finance_Indicator_MACD.PY3_Finance_Indicator_MACD()
        self.Fin_Ind_SMA_P5  = PY3_Finance_Indicator_SMA.PY3_Finance_Indicator_SMA()
        self.Fin_Ind_SMA_P10 = PY3_Finance_Indicator_SMA.PY3_Finance_Indicator_SMA()
        # ..........................................
        self.Stocks_Data_Conv_Daily_to_Weekly = PY3_Stocks_Data_Conv_Daily_to_Weekly.PY3_Stocks_Data_Conv_Daily_to_Weekly()
        self.Stocks_DataFrame_Preprocessing   = PY3_Stocks_DataFrame_Preprocessing.PY3_Stocks_DataFrame_Preprocessing()

    def Init(self, DataFrame) -> int:

        self.PUBLIC_DATAFRAME = self.Stocks_DataFrame_Preprocessing.Before_Calculating_Stocks_Daily_Indicators(DataFrame)
        self.PUBLIC_DATAFRAME_LENGTH = self.PUBLIC_DATAFRAME.shape[0]
        # ..........................................
        self.ITERATOR_LENGTH = self.PUBLIC_DATAFRAME_LENGTH
        self.ITERATOR_MAXIDX = self.ITERATOR_LENGTH - 1
        self.ITERATOR_MOVING = 0
        # ..........................................
        return self.ITERATOR_LENGTH

    def Next(self) -> int:

        Index   = self.ITERATOR_MOVING
        ID      = self.PUBLIC_DATAFRAME.loc[Index, "id"]
        ROW_NUM = self.PUBLIC_DATAFRAME.loc[Index, "row_num"]
        High    = self.PUBLIC_DATAFRAME.loc[Index, "high"]
        Low     = self.PUBLIC_DATAFRAME.loc[Index, "low"]
        Close   = self.PUBLIC_DATAFRAME.loc[Index, "close"]
        # ..........................................
        EMA12       = self.Fin_Ind_EMA_P12.EMA(ROW_NUM = ROW_NUM, Period = 12, Close = Close)
        EMA26       = self.Fin_Ind_EMA_P26.EMA(ROW_NUM = ROW_NUM, Period = 26, Close = Close)
        MACD_DIF    = self.Fin_Ind_MACD.MACD_DIF(EMA12 = EMA12, EMA26 = EMA26)
        MACD_DEA    = self.Fin_Ind_MACD.MACD_DEA(ROW_NUM = ROW_NUM, MACD_DIF = MACD_DIF)
        MACD_STICK  = self.Fin_Ind_MACD.MACD_STICK(MACD_DIF = MACD_DIF, MACD_DEA = MACD_DEA)
        KDJ_K       = self.Fin_Ind_KDJ.KDJ_K(ROW_NUM = ROW_NUM, RSV_Prd = 9, K_Prd = 3, High = High, Low = Low, Close = Close)
        KDJ_D       = self.Fin_Ind_KDJ.KDJ_D(ROW_NUM = ROW_NUM, RSV_Prd = 9, D_Prd = 3, K_Val = KDJ_K)
        KDJ_J       = self.Fin_Ind_KDJ.KDJ_J(K_Val = KDJ_K, D_Val = KDJ_D)
        ETG_TRS     = self.Fin_Etg_Theory.Top_Reversal_Shape(ROW_NUM = ROW_NUM, Input_UpperEdge = High, Input_LowerEdge = Low)
        ETG_BRS     = self.Fin_Etg_Theory.Bottom_Reversal_Shape(ROW_NUM = ROW_NUM, Input_UpperEdge = High, Input_LowerEdge = Low)
        ETG_T_GROUP = self.Fin_Etg_Theory.Top_Reversal_Shape_s_Group_Top(ROW_NUM = ROW_NUM, Input_UpperEdge = High, Input_LowerEdge = Low)
        ETG_B_GROUP = self.Fin_Etg_Theory.Bottom_Reversal_Shape_s_Group_Bottom(ROW_NUM = ROW_NUM, Input_UpperEdge = High, Input_LowerEdge = Low)
        # ..........................................
        self.PUBLIC_JSON_RECORDS.append({
            "id":          ID,
            "sma5":        self.Fin_Ind_SMA_P5.SMA(ROW_NUM = ROW_NUM, Period = 5, Close = Close),
            "sma10":       self.Fin_Ind_SMA_P10.SMA(ROW_NUM = ROW_NUM, Period = 10, Close = Close),
            "ema12":       EMA12,
            "ema26":       EMA26,
            "macd_dif":    MACD_DIF,
            "macd_dea":    MACD_DEA,
            "macd_stick":  MACD_STICK,
            "kdj_k":       KDJ_K,
            "kdj_d":       KDJ_D,
            "kdj_j":       KDJ_J,
            "etg_trs":     ETG_TRS,
            "etg_brs":     ETG_BRS,
            "etg_t_group": ETG_T_GROUP,
            "etg_b_group": ETG_B_GROUP
        })
        # ..........................................
        self.ITERATOR_MOVING = self.ITERATOR_MOVING + 1
        # ..........................................
        return 1

# EOF Signed by GF.
