# GF_PY3_CLASS/Python3_Text/PY3_Text_Time_to_ISO_8601.py
# Create by GF 2025-01-20 12:35

# ##################################################

class PY3_Text_Time_to_ISO_8601(object):

    # ISO 8601 日期和时间国际标准
    #
    # ISO 8601 日期和时间国际标准, 由国际标准化组织 (ISO) 制定, 全称为 <<数据存储和交换形式-信息交换-日期和时间的表示方法>>。
    # 该标准旨在提供一种统一、结构化的日期和时间表示方式, 以便在全球范围内进行数据交换和记录, 减少因地区习惯和格式差异带来的误解。‌
    #
    # 日期格式‌:
    # 标准日期格式为 YYYY-MM-DD, 例如 2025-04-04 表示 2025 年 4 月 4 日。
    #
‌    # 时间格式‌:
    # 标准时间格式为 HH:MM:SS, 例如 14:30:05 表示下午 2 点 30 分 5 秒。可以进一步精确到毫秒, 例如 14:30:05.000。
‌    #
    # 日期时间组合‌表示:
    # 日期和时间的组合表示为 YYYY-MM-DDTHH:MM:SS, 其中 T 是日期和时间之间的分隔符。
    # 例如 2025-04-04T14:30:05 表示 2025 年 4 月 4 日下午 2 点 30 分 5 秒。
    #
‌    # 时区表示‌:
    # 使用 Z 表示协调世界时 (UTC), 或者使用 ±hh:mm 格式表示与 UTC 的偏移。
    # 例如 14:30:05Z 表示 UTC 时间下午 2 点 30 分 5 秒, 22:30:05+08:00 表示比 UTC 快 8 小时的时区 (如北京时间)。
    #
‌    # 年份表示‌:
    # 年份由 4 位数组成, 以公历公元 1 年为 0001 年, 公元前 1 年为 0000 年, 公元前 2 年为 -0001 年, 以此类推。
    #
‌    # 持续时间表示‌:
    # 使用 PnYnMnDTnHnMnS 格式表示时间段, 例如 P1Y2M3D 表示 1 年 2 个月 3 天的周期。
    #
    # 应用与意义:
    # ISO 8601 日期和时间国际标准广泛应用于计算机系统、数据交换、国际通信等领域, 确保日期和时间的一致性和可读性。
    # 例如, 在互联网协议中, RFC 3339 是基于 ISO 8601 的扩展, 增加了对时区和精度的额外要求。

    def Date(Text_Date:str) -> str:

        # 文本日期标准化 (Text Date Standardization)
        #
        # Parameters:
        # - Text_Date:str -> Text Type Date.
        #
        # 日期基本单位换算:
        # - 1 年 = 12 个月。
        # - 1, 3, 5, 7, 8, 10, 12 月 = 31 天。
        # - 4, 6, 9, 11 月 = 30 天。
        # - 2 月(平年) = 28 天。
        # - 2 月(闰年) = 29 天。

        Old_Text_Date:str = Text_Date
        New_Text_Date:str = None

        if ('.' in Text_Date): Old_Text_Date = Text_Date.replace('.', '-')
        if ('-' in Text_Date): Old_Text_Date = Text_Date.replace('/', '-')
        # ..........................................
        date_char_list:list = [char for char in Old_Text_Date]

        # 情况 1: 字符串类型日期大于等于 11 个字符, 不进入处理流程, 原样返回。
        if (len(Old_Text_Date) >= 11): New_Text_Date = Old_Text_Date

        # 情况 2: 字符串类型日期共 10 个字符, 且前 4 位是年份, 如 "2024-06-23" 等。
        if (len(Old_Text_Date) == 10): New_Text_Date = Old_Text_Date

        # 情况 3: 字符串类型日期共 9 个字符, 且前 4 位是年份, 如 "2024-6-23", "2023-12-1" 等。
        if ((len(date_char_list) == 9) and (date_char_list[6] == '-')):

            date_char_list.insert(5, '0')
            # ......................................
            New_Text_Date = str('').join(date_char_list)

        if ((len(date_char_list) == 9) and (date_char_list[7] == '-')):

            date_char_list.insert(8, '0')
            # ......................................
            New_Text_Date = str('').join(date_char_list)

        # 情况 4: 字符串类型日期共 8 个字符, 且前 4 位是年份, 如 "2024-6-8", "20231201" 等。
        if ((len(date_char_list) == 8) and (date_char_list[4] == '-') and (date_char_list[6] == '-')):

            # Tips: 列表(List)插入(Insert)元素是在指定索引(Index)的前面添加元素。
            # Tips: Inserting Elements into a List is Adding Elements Before a Specified Index.
            date_char_list.insert(7, '0')
            date_char_list.insert(5, '0') # -> 倒序连续插入 (前一次插入不影响后续定位)。
            # ......................................
            New_Text_Date = str('').join(date_char_list)

        if ((len(date_char_list) == 8) and (date_char_list[4].isdigit() == True) and (date_char_list[6].isdigit() == True)):

            # Tips: 列表(List)插入(Insert)元素是在指定索引(Index)的前面添加元素。
            # Tips: Inserting Elements into a List is Adding Elements Before a Specified Index.
            date_char_list.insert(6, '-')
            date_char_list.insert(4, '-')
            # ......................................
            New_Text_Date = str('').join(date_char_list)

        # 情况 5: 字符串类型日期共 7 个字符, 且前 4 位是年份, 如 "2024618", "2024131" 等 (特殊情况如: "2024101", "2024111", "2024121")。
        if ((len(date_char_list) == 7) and (int("%s%s" % (date_char_list[4], date_char_list[5])) > 12)):

            date_char_list.insert(4, '0')
            date_char_list.insert(4, '-')
            date_char_list.insert(5 + 2, '-') # -> 连续插入, 需要在后续插入动作的索引上加 1 (前一次插入改变了列表的长度及后续元素的位置)。
            # ......................................
            New_Text_Date = str('').join(date_char_list)

        if ((len(date_char_list) == 7) and (int("%s%s" % (date_char_list[4], date_char_list[5])) == 10)):

            date_char_list.insert(6, '0')
            date_char_list.insert(6, '-')
            date_char_list.insert(4, '-')
            # ......................................
            New_Text_Date = str('').join(date_char_list)

        if ((len(date_char_list) == 7) and ((int("%s%s" % (date_char_list[4], date_char_list[5])) == 11) or (int("%s%s" % (date_char_list[4], date_char_list[5])) == 12))):

            # Tips: For Now, Let's Process Items Like "2024111" and "2024121" as "2024-01-11" and "2024-01-21".
            # Tips: 暂且将诸如 "2024111" 和 "2024121" 处理为 "2024-01-11" 和 "2024-01-21"。

            date_char_list.insert(5, '-')
            date_char_list.insert(4, '0')
            date_char_list.insert(4, '-')
            # ......................................
            New_Text_Date = str('').join(date_char_list)

        return New_Text_Date

    def Date_is_Which_Week_of_The_Year(self, Text_Date:str, Year:int, Month:int, Day:int) -> int:
    
        # 一年中的第几周 (Which Week of The Year)
        #
        # Requirement: datetime (Python 3.12.0)
        #
        # Tips: 如何获取指定日期是所在年份中的第几周?
        # - 以 "2023年1月11日" 为例
        # - 1. 获取 [所在年份], 如 "2023"。
        # - 2. 获取 [所在年份的第 1 天], 如 "2023-01-01"。
        # - 3. 计算 [指定日期] 是 [所在年份] 中的第几天, 如 "[指定日期: 2023-01-11] - [所在年份的第 1 天: 2023-01-01] + 1 = 11 天"。
        # - 4. 计算 [指定日期] 是 [所在年份] 中的第几周, 如 "[指定日期是所在年份的第 11 天: 11] // 7 + 1 = 2 天"。
        # (其中 "//" 双斜杠符号是 Python 中的整除运算符, 3 // 2 = 1, 约去了 0.5)
        # ..........................................
        # Tips: 每年第 1 天是星期几? (数据参考)
        # - 2022-01-01,星期六(Saturday)
        # - 2023-01-01,星期日(Sunday)
        # - 2024-01-01,星期一(Monday)

        Corrected_Date = self.Date(Text_Date)
        Formulaic_Date = datetime.strptime(Corrected_Date, "%Y-%m-%d")  # 算式化 (Formulaic) 的日期

        Year  = Formulaic_Date.year
        Month = Formulaic_Date.month
        Day   = Formulaic_Date.day

        Current_Date          = datetime.datetime(Year, Month, Day)
        First_Day_of_The_Year = datetime.datetime(Year, 1, 1)
        # ..............................................
        Days_Difference = (Current_Date - First_Day_of_The_Year).days
        # ..............................................
        Result = (Days_Difference + 1) // 7 + 1

        return Result

# EOF Signed by GF.
