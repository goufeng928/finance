# APP_API_Call_Tushare_Stocks_Data_to_PGSQL16.py
# Create by GF 2025-08-12 12:55

import re
import traceback
# ..................................................
import PY3_API_Call_Tushare1424_Stocks_Data_to_PGSQL16

# ##################################################

# KNOWLEDGE:
# 16 进制空格字符 ----> \x20
# Unicode 空格字符 ---> \u0020

# ##################################################

try:

    print(f"""[DEBUG] API Call Tushare Stocks Data to PostgreSQL 20251125 版""")
    print(f"""==================================================""")
    print(f"""[DEBUG] 输入 <任意数字> 按下 <Enter> 开始任务""")
    Inputed = input()

    print(f"""[DEBUG] <日期> 说明: 格式 YYYY-mm-dd, 格式示例 2025-01-01""")
    print(f"""[DEBUG] <日期> 说明: 使用 \\x20 (16 进制空格) 或 \\u0020 (Unicode 空格) 分隔""")
    print(f"""[DEBUG] <日期> 说明: 可输入单个或多个日期, 单日期 2025-01-01, 多日期 2025-01-01 2025-01-02 ...""")
    print(f"""[DEBUG] 输入 <日期>:""")
    Inputed = input()
    Inputed = re.sub("\x20+",   '+', Inputed)  # 替换 16 进制空格
    Inputed = re.sub("\u0020+", '+', Inputed)  # 替换 Unicode 空格
    Inputed = Inputed.split('+')

    for x in Inputed:
        y = PY3_API_Call_Tushare1424_Stocks_Data_to_PGSQL16.PY3_API_Call_Tushare1424_Stocks_Data_to_PGSQL16(TEXT_Time = x)
        print(f"""[DEBUG] INPUT: {x}, RETURN: {y}""")

    print(f"""==================================================""")
    print(f"""[DEBUG] 输入 <任意数字> 按下 <Enter> 退出程序""")
    Inputed = input()

except Exception as e:

    print(f"""[DEBUG] 发生异常""")
    print(f"""==================================================""")
    traceback.print_exc()  # 打印异常信息到控制台, 而不是引发异常后退出
    print(f"""==================================================""")
    print(f"""[DEBUG] 输入 <任意数字> 按下 <Enter> 退出程序""")
    Inputed = input()

# Signed by GF.
