# Py3_Script_Finance_Tools_Func.py
# Create By GF 2024-01-22 18:16

# 全局变量(Global Variable) for The FinTool.
# ##################################################
# Stock Terms Interpretation:
# Long Buy   : 买多/多方
# Short Sell : 卖空/空方
# Hold       : 持仓
# Idle       : 空仓
# --------------------------------------------------
Funds_Rest:float = 1000000.00
Stock_Holdings:int = 0
Stock_Value:float = 0.00
Long_Buy_Price:list = []
Short_Sell_Price:list = []

# ######################################### Normal Function ##########################################

def Safe_Divide(Divisor:float, Dividend:float) -> float:
    
    if ((Dividend == 0.0) or (Dividend == None)): # -> 如果分母为 0 或者分母为 None。
        return None
    else:
        Result:float = (Divisor / Dividend)
        # ..........................................
        return Result
    # ##############################################
    # End of Function.

def List_Average(Lst:list) -> float:
    
    Result = (sum(Lst) / len(Lst))
    # ----------------------------------------------
    return Result
    # ##############################################
    # End of Function.

def String_is_Integer(String:str) -> bool:

    Count:int = 0
    # ..............................................
    String_Length:int = len(String)
    
    # ----------------------------------------------
    for i in range(0, String_Length):
        if (String[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
            Count += 1
    
    # ----------------------------------------------
    if (Count == String_Length):
        return True
    else:
        return False
    # ##############################################
    # End of Function.

def String_is_Decimal(String:str) -> bool:

    Count:int = 0
    # ..............................................
    String_Length:int = len(String)
    
    # ----------------------------------------------
    for i in range(0, String_Length):
        if (String[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']):
            Count += 1
    
    # ----------------------------------------------
    if (Count == String_Length):
        return True
    else:
        return False
    # ##############################################
    # End of Function.

# ######################################### FinFunc FinTool ##########################################

def FinFunc_FinTool_Backtest_Buy_or_Sell_Lots(Close:float, Min_Lots:int=100, Action_Position:str="All", Rtn:str="Tuple"):
    
    """
    [Require] Global Variable:
              * Funds_Rest:float
              * Stock_Holdings:int
              
              Function: 
              * String_is_Integer(String:str) -> bool
              * String_is_Decimal(String:str) -> bool

    [Explain] 手数(Lots)默认值为 100, 即为 1 手, 通常 100 个数量单位的股票被视为 1 手。
    """
    global Funds_Rest     # -> global 关键字, 用于访问全局变量。
    global Stock_Holdings # -> global 关键字, 用于访问全局变量。
    
    # ----------------------------------------------
    Buy_Lots:int  = 0
    Sell_Lots:int = 0

    # ----------------------------------------------
    if   (Action_Position.lower() == "all"):
    
        Max_Lots = (Funds_Rest - (Funds_Rest % (Close * Min_Lots))) / Close
        # ..........................................
        Buy_Lots  = Max_Lots
        Sell_Lots = Stock_Holdings
        
    elif (String_is_Integer(Action_Position) == True) and (int(Action_Position) % Min_Lots == 0):
    
        Buy_Lots  = int(Action_Position)
        Sell_Lots = int(Action_Position)
    
    elif (String_is_Decimal(Action_Position) == True) and (0 <= float(Action_Position)) and (float(Action_Position) <= 1):
    
        Max_Lots = (Funds_Rest - (Funds_Rest % (Close * Min_Lots))) / Close
        # ..........................................
        Buy_Lots  = Max_Lots * float(Action_Position)
        Sell_Lots = Stock_Holdings * float(Action_Position)
    
    else:
        
        Buy_Lots  = Min_Lots
        Sell_Lots = Min_Lots
    
    # Return Value.
    # ----------------------------------------------
    if   (Rtn.lower() == "buy"):
        return Buy_Lots
    elif (Rtn.lower() == "sell"):
        return Sell_Lots
    else:
        return (Buy_Lots, Sell_Lots)
    # ##############################################
    # End of Function.

# Finance 函数 - 金融工具(Finance Tools) - 开仓(Open Position) - 多方(Long Buy).
def FinFunc_FinTool_Backtest_Open_Position_by_Long_Buy(Close:float, Buy_Lots:int) -> int:
    
    """
    [Require] Global Variable:
              * Funds_Rest:float
              * Stock_Holdings:int
              * Stock_Value:float
              * Long_Buy_Price:list
    """
    global Funds_Rest     # -> global 关键字, 用于访问全局变量。
    global Stock_Holdings # -> global 关键字, 用于访问全局变量。
    global Stock_Value    # -> global 关键字, 用于访问全局变量。
    global Long_Buy_Price # -> global 关键字, 用于访问全局变量。
    
    # ----------------------------------------------
    Skip:int = 0
    
    # ----------------------------------------------
    Long_Buy_Price.append(Close)
    
    # ----------------------------------------------
    Funds_Spent = (Close * Buy_Lots)
    # ..............................................
    if (Funds_Rest < Funds_Spent):
        Skip = Skip + 1
        # ..........................................
        return int(0)
    else:
        Funds_Rest = (Funds_Rest - Funds_Spent)
        Stock_Holdings = (Stock_Holdings + Buy_Lots)
        Stock_Value = (Close * Stock_Holdings)
        # ..........................................
        return int(1)
    # ##############################################
    # End of Function.

# Finance 函数 - 金融工具(Finance Tools) - 开仓(Open Position) - 空方(Short Sell).
def FinFunc_FinTool_Backtest_Open_Position_by_Short_Sell(Close:float, Open_Lots:int) -> int:
    
    """
    [Require] Global Variable:
              * Funds_Rest:float
              * Stock_Holdings:int
              * Stock_Value:float
              * Short_Sell_Price:list
    
              Function:
              * List_Average(Lst:list) -> float
    
    [Explain] 1. 卖空盈利 = 卖空均价 - 当前价
                 Short Sell Profit = Average Short Sell Price - Current Price
              
              2. 持仓市值(卖空) = 卖空均价 * 持仓数量 + 卖空盈利 * 持仓数量
                 Position Market Value (Short Sell) = Average Short Sell Price * Number of Holdings + Short Sell Profit * Number of Holdings
    """
    global Funds_Rest       # -> global 关键字, 用于访问全局变量。
    global Stock_Holdings   # -> global 关键字, 用于访问全局变量。
    global Stock_Value      # -> global 关键字, 用于访问全局变量。
    global Short_Sell_Price # -> global 关键字, 用于访问全局变量。
    
    # ----------------------------------------------
    Skip:int = 0
    
    # ----------------------------------------------
    Short_Sell_Price.append(Close)
    
    # ----------------------------------------------
    Funds_Spent = (Close * Open_Lots)
    # ..............................................
    if (Funds_Rest < Funds_Spent):
        Skip = Skip + 1
        # ..........................................
        return int(0)
    else:
        Funds_Rest = (Funds_Rest - Funds_Spent)
        Stock_Holdings = (Stock_Holdings + Open_Lots)
        Stock_Value = ((List_Average(Short_Sell_Price) + (List_Average(Short_Sell_Price) - Close)) * Stock_Holdings)
        # ..........................................
        return int(1)
    # ##############################################
    # End of Function.

# Finance 函数 - 金融工具(Finance Tools) - 平仓(Close Position) - 多方(Long Buy).
def FinFunc_FinTool_Backtest_Close_Position_by_Long_Buy(Close:float, Sell_Lots:int) -> int:
    
    """
    [Require] Global Variable:
              * Funds_Rest:float
              * Stock_Holdings:int
              * Stock_Value:float
              * Long_Buy_Price:list
    """
    global Funds_Rest     # -> global 关键字, 用于访问全局变量。
    global Stock_Holdings # -> global 关键字, 用于访问全局变量。
    global Stock_Value    # -> global 关键字, 用于访问全局变量。
    global Long_Buy_Price # -> global 关键字, 用于访问全局变量。
    
    # ----------------------------------------------
    Skip:int = 0
    
    # ----------------------------------------------
    Funds_Income = (Close * Sell_Lots)
    # ..............................................
    if (Stock_Holdings < Sell_Lots):
        Skip = Skip + 1
        # ..........................................
        return int(0)
    else:
        # ..........................................
        Funds_Rest = (Funds_Rest + Funds_Income)
        Stock_Holdings = (Stock_Holdings - Sell_Lots)
        Stock_Value = (Close * Stock_Holdings)
        # ..........................................
        if (Stock_Holdings == 0):
            Long_Buy_Price.clear()
        # ..........................................
        return int(1)
    # ##############################################
    # End of Function.

# Finance 函数 - 金融工具(Finance Tools) - 平仓(Open Position) - 空方(Short Sell).
def FinFunc_FinTool_Backtest_Close_Position_by_Short_Sell(Close:float, Close_Lots:int) -> int:
    
    """
    [Require] Global Variable:
              * Funds_Rest:float
              * Stock_Holdings:int
              * Stock_Value:float
              * Short_Sell_Price:list
    
              Function:
              * List_Average(Lst:list) -> float
    
    [Explain] 1. 卖空盈利 = 卖空均价 - 当前价
                 Short Sell Profit = Average Short Sell Price - Current Price
              
              2. 持仓市值(卖空) = 卖空均价 * 持仓数量 + 卖空盈利 * 持仓数量
                 Position Market Value (Short Sell) = Average Short Sell Price * Number of Holdings + Short Sell Profit * Number of Holdings
    """
    global Funds_Rest       # -> global 关键字, 用于访问全局变量。
    global Stock_Holdings   # -> global 关键字, 用于访问全局变量。
    global Stock_Value      # -> global 关键字, 用于访问全局变量。
    global Short_Sell_Price # -> global 关键字, 用于访问全局变量。
    
    # ----------------------------------------------
    Skip:int = 0
    
    # ----------------------------------------------
    if ((Stock_Holdings < Close_Lots) or (len(Short_Sell_Price) == 0)):
        Skip = Skip + 1
        # ..........................................
        return int(0)
    else:
        # 买平后[闲置资金] = [闲置资金] + [卖空均价] * [买平手数] + ([卖空均价] - [当前价]) * [买平手数]
        # ..........................................
        Funds_Rest = (Funds_Rest + ((List_Average(Short_Sell_Price) * Close_Lots) + (List_Average(Short_Sell_Price) - Close) * Close_Lots))
        Stock_Holdings = (Stock_Holdings - Close_Lots)
        Stock_Value = ((List_Average(Short_Sell_Price) + (List_Average(Short_Sell_Price) - Close)) * Stock_Holdings)
        # ..........................................
        if (Stock_Holdings == 0):
            Short_Sell_Price.clear()
        # ..........................................
        return int(1)
    # ##############################################
    # End of Function.

# Finance 函数 - 金融工具(Finance Tools) - 止盈(Stop Profit) - 多方(Long Buy).
def FinFunc_FinTool_Backtest_Stop_Profit_by_Long_Buy(Close:float, Sell_Lots:int, Stop_Profit:str="Null") -> int:
    
    """
    [Require] Global Variable:
              * Long_Buy_Price:list
    
              Function:
              * List_Average(Lst:list) -> float
              * FinFunc_FinTool_Backtest_Close_Position_by_Long_Buy(Close:float, Sell_Lots:int) -> int
    
    [Explain] FinFunc_FinTool_Backtest_Stop_Profit_by_Long_Buy(Close:float, Sell_Lots:int, Stop_Profit:str="NULL") -> int
              * Stop_Profit = "NULL"        : 什么也不做 (Nothing).
              * Stop_Profit = "percent:0.2" : 按盈利率止盈, 盈利率达到 20% (Stop Profit by Profit Margin, With a Profit Margin of 20%).
              * Stop_Profit = "price:150"   : 按价格止盈, 价格达到 150 (Stop Profit Based on Price, Price Reaches 150).
    """
    global Long_Buy_Price
    
    # ----------------------------------------------
    Method_and_Numerical:list = []
    Method:str = str('')
    Numerical:float = float(0.0)
    
    # ----------------------------------------------
    if (Stop_Profit.lower() != str("null")):
        Method_and_Numerical:list = Stop_Profit.split(':')
        # ..........................................
        Method:str      = str(Method_and_Numerical[0])
        Numerical:float = float(Method_and_Numerical[1])
    
    # 止盈动作 (Stop Profit Action)。
    # ----------------------------------------------
    if   (len(Long_Buy_Price) != 0) and (("percent" in Method.lower()) or ("pct" in Method.lower())):
        
        if ((Close - List_Average(Long_Buy_Price)) / List_Average(Long_Buy_Price) >= Numerical):
            
            # Calling Other Function.
            # ......................................
            FinFunc_FinTool_Backtest_Close_Position_by_Long_Buy(Close=Close, Sell_Lots=Sell_Lots)
            # ......................................
            return int(1)
        
    elif (len(Long_Buy_Price) != 0) and (("price" in Method.lower()) or ("pc" in Method.lower())):
            
        if (Close >= Numerical):
            
            # Calling Other Function.
            # ......................................
            FinFunc_FinTool_Backtest_Close_Position_by_Long_Buy(Close=Close, Sell_Lots=Sell_Lots)
            # ......................................
            return int(1)
    else:
        
        return int(0)
    # ##############################################
    # End of Function.

# Finance 函数 - 金融工具(Finance Tools) - 止损(Stop Loss) - 多方(Long Buy).
def FinFunc_FinTool_Backtest_Stop_Loss_by_Long_Buy(Close:float, Sell_Lots:int, Stop_Profit:str="Null") -> int:
    
    """
    [Require] Global Variable:
              * Long_Buy_Price:list
    
              Function:
              * List_Average(Lst:list) -> float
              * FinFunc_FinTool_Backtest_Close_Position_by_Long_Buy(Close:float, Sell_Lots:int) -> int
    
    [Explain] FinFunc_FinTool_Backtest_Stop_Profit_by_Long_Buy(Close:float, Sell_Lots:int, Stop_Profit:str="NULL") -> int
              * Stop_Profit = "NULL"        : 什么也不做 (Nothing).
              * Stop_Profit = "percent:-0.2" : 按损失率止损, 损失率达到 -20% (Stop Loss by Loss Rate, With a Loss Rate of -20%).
              * Stop_Profit = "price:110"   : 按价格止损, 价格达到 110 (Stop Loss Based on Price, Price Reaches 110).
    """
    global Long_Buy_Price
    
    # ----------------------------------------------
    Method_and_Numerical:list = []
    Method:str = str('')
    Numerical:float = float(0.0)
    
    # ----------------------------------------------
    if (Stop_Profit.lower() != str("null")):
        Method_and_Numerical:list = Stop_Profit.split(':')
        # ..........................................
        Method:str      = str(Method_and_Numerical[0])
        Numerical:float = float(Method_and_Numerical[1])
    
    # 止损动作 (Stop Loss Action)。
    # ----------------------------------------------
    if   (len(Long_Buy_Price) != 0) and (("percent" in Method.lower()) or ("pct" in Method.lower())):
        
        if ((Close - List_Average(Long_Buy_Price)) / List_Average(Long_Buy_Price) <= Numerical):
            
            # Calling Other Function.
            # ......................................
            FinFunc_FinTool_Backtest_Close_Position_by_Long_Buy(Close=Close, Sell_Lots=Sell_Lots)
            # ......................................
            return int(1)
        
    elif (len(Long_Buy_Price) != 0) and (("price" in Method.lower()) or ("pc" in Method.lower())):
            
        if (Close <= Numerical):
            
            # Calling Other Function.
            # ......................................
            FinFunc_FinTool_Backtest_Close_Position_by_Long_Buy(Close=Close, Sell_Lots=Sell_Lots)
            # ......................................
            return int(1)
    else:
        
        return int(0)
    # ##############################################
    # End of Function.

# ######################################### MapFunc FinTool ##########################################

def MapFunc_FinTool_Backtest_Signal(*args, How="All") -> int:
    
    """
    [Explain] >>> def ExpFunc_Demo1(*args):
                      
                      print(args)

              >>> def ExpFunc_Demo2(tuple):
              
                      print(tuple)
              
              >>> ExpFunc_Demo1(1, 2, 3)
              (1, 2, 3)
              
              >>> ExpFunc_Demo2(tuple=(1, 2, 3))
              (1, 2, 3)
              
              若 args 前面不加 * 则 ExpFunc_Demo1 只能接收一个参数, 参数多给或少给都会报错。
              若 args 前面加上 * 则 ExpFunc_Demo1 把接收到的多个参数打包成了一个元组(Tuple), 并赋值给 args 形参。
    """
    Count:int = 0
    # ----------------------------------------------
    for Idx in range(0, len(args)):
        if (args[Idx] == True):
            Count += 1
    # ----------------------------------------------
    if   ((How.lower() == "all") and (Count == len(args))):
        return int(1)
    elif ((How.lower() == "any") and (Count >= int(1))):
        return int(1)
    else:
        return int(0)
    # ##############################################
    # End of Function.

# Map 函数 - 金融工具(Finance Tools) - 回测(Backtesting) - 实时资产 (买多)。
def MapFunc_FinTool_Backtest_Real_Time_Asset_by_Long_Buy(
        Sig_Buy:int, Sig_Sell:int, Close:float, Act_Posi:str="ALL", Stop_Profit:str="Null", Stop_Loss:str="Null", Rtn:str="Tuple"):
    
    """
    [Require] Function:
              * FinFunc_FinTool_Backtest_Buy_or_Sell_Lots(Close:float, Min_Lots:int=100, Action_Position:str="All", Rtn:str="Tuple")
              * FinFunc_FinTool_Backtest_Open_Position_by_Long_Buy(Close:float, Buy_Lots:int) -> int
              * FinFunc_FinTool_Backtest_Close_Position_by_Long_Buy(Close:float, Sell_Lots:int) -> int
              * FinFunc_FinTool_Backtest_Stop_Profit_by_Long_Buy(Close:float, Sell_Lots:int, Stop_Profit:str="Null") -> int
              * FinFunc_FinTool_Backtest_Stop_Loss_by_Long_Buy(Close:float, Sell_Lots:int, Stop_Profit:str="Null") -> int
    """
    Skip:int = 0
    
    # Calling Other Function.
    # ----------------------------------------------
    Buy_Lots:int  = FinFunc_FinTool_Backtest_Buy_or_Sell_Lots(Close=Close, Min_Lots=100, Action_Position=Act_Posi, Rtn="Buy")
    Sell_Lots:int = FinFunc_FinTool_Backtest_Buy_or_Sell_Lots(Close=Close, Min_Lots=100, Action_Position=Act_Posi, Rtn="Sell")
    
    # Calling Other Function.
    # ----------------------------------------------
    Stop_Profit_Status:int = FinFunc_FinTool_Backtest_Stop_Profit_by_Long_Buy(Close=Close, Sell_Lots=Sell_Lots, Stop_Profit=Stop_Profit)
    Stop_Loss_Status:int   = FinFunc_FinTool_Backtest_Stop_Profit_by_Long_Buy(Close=Close, Sell_Lots=Sell_Lots, Stop_Profit=Stop_Loss)
    
    # 买卖动作 (Buying and Selling Actions)。
    # ----------------------------------------------
    if   ((Sig_Buy == 1) and (Sig_Sell == 0) and (Stop_Profit_Status == 0) and (Stop_Loss_Status == 0)): # -> 买入做多信号。
        
        # Calling Other Function.
        # ..........................................
        FinFunc_FinTool_Backtest_Open_Position_by_Long_Buy(Close=Close, Buy_Lots=Buy_Lots)
    
    elif ((Sig_Buy == 0) and (Sig_Sell == 1) and (Stop_Profit_Status == 0) and (Stop_Loss_Status == 0)): # -> 卖出平仓信号.
        
        # Calling Other Function.
        # ..........................................
        FinFunc_FinTool_Backtest_Close_Position_by_Long_Buy(Close=Close, Sell_Lots=Sell_Lots)
    
    else:
        
        Skip = Skip + 1
    
    # Return Value.
    # ----------------------------------------------
    if   (Rtn.lower() == "funds_rest"):
        return Funds_Rest
    elif (Rtn.lower() == "stock_holdings"):
        return Stock_Holdings
    elif (Rtn.lower() == "stock_value"):
        return Stock_Value
    else:
        return (Funds_Rest, Stock_Holdings, Stock_Value)
    # ##############################################
    # End of Function.

# Map 函数 - 金融工具(Finance Tools) - 回测(Backtesting) - 实时资产 (卖空)。
def MapFunc_FinTool_Backtest_Real_Time_Asset_by_Short_Sell(
        Sig_Buy:int, Sig_Sell:int, Close:float, Act_Posi:str="All", Rtn:str="Tuple"):
    
    """
    [Require] Function:
              * FinFunc_FinTool_Backtest_Buy_or_Sell_Lots(Close:float, Min_Lots:int=100, Action_Position:str="All", Rtn:str="Tuple")
              * FinFunc_FinTool_Backtest_Open_Position_by_Short_Sell(Close:float, Buy_Lots:int) -> int
              * FinFunc_FinTool_Backtest_Close_Position_by_Short_Sell(Close:float, Sell_Lots:int) -> int
    """
    Skip:int = 0
    
    # Calling Other Function.
    # ----------------------------------------------
    Open_Lots:int  = FinFunc_FinTool_Backtest_Buy_or_Sell_Lots(Close=Close, Min_Lots=100, Action_Position=Act_Posi, Rtn="Buy")
    Close_Lots:int = FinFunc_FinTool_Backtest_Buy_or_Sell_Lots(Close=Close, Min_Lots=100, Action_Position=Act_Posi, Rtn="Sell")

    # ----------------------------------------------
    if   (Sig_Buy == 0 and Sig_Sell == 1): # -> 卖出做空信号。
        
        # Calling Other Function.
        # ..........................................
        FinFunc_FinTool_Backtest_Open_Position_by_Short_Sell(Close=Close, Open_Lots=Open_Lots)
    
    elif (Sig_Buy == 1 and Sig_Sell == 0): # -> 买入平仓信号。
        
        # Calling Other Function.
        # ..........................................
        FinFunc_FinTool_Backtest_Close_Position_by_Short_Sell(Close=Close, Close_Lots=Close_Lots)
    
    else:
        
        Skip = Skip + 1
    
    # Return Value.
    # ----------------------------------------------
    if   (Rtn.lower() == "funds_rest"):
        return Funds_Rest
    elif (Rtn.lower() == "stock_holdings"):
        return Stock_Holdings
    elif (Rtn.lower() == "stock_value"):
        return Stock_Value
    else:
        return (Funds_Rest, Stock_Holdings, Stock_Value)
    # ##############################################
    # End of Function.
