# GF_PY3_CLASS/PY38_JSON_Records_Pager.py
# Create by GF 2025-09-08 12:53

import math

# ##################################################

class PY38_JSON_Records_Pager(object):

    # Examples:
    # >>> # 测试数据: 员工信息
    # >>> JSON_Records:list = [
    # ...     {"姓名": "张三", "年龄": "25", "职业": "工程师"},
    # ...     {"姓名": "李四", "年龄": "30", "职业": "设计师"},
    # ...     {"姓名": "王五", "年龄": "28", "职业": "产品经理"},
    # ...     {"姓名": "赵六", "年龄": "35", "职业": "总监"}
    # ... ]
    # >>>
    # >>> Pager = PY38_JSON_Records_Pager()
    # >>>
    # >>> # 测试用例 (1): 将 "员工信息" 分成 N 页, 每页 3 行数据, 求 N 的值 (总共可分成多少页)
    # >>> Pager.Number_of_Page(JSON_Records = JSON_Records, Length_of_Single_Page = 3)
    # 2
    # >>>
    # >>> # 测试用例 (2): 将 "员工信息" 分成 N 页, 每页 3 行数据, 求最后 1 页的数据行数
    # >>> Pager.Length_of_Last_Page(JSON_Records = JSON_Records, Length_of_Single_Page = 3)
    # 1
    # >>>
    # >>> # 测试用例 (3): 将 "员工信息" 分成 N 页, 每页 2 行数据
    # >>> Pager.Locate_to_Page(JSON_Records = JSON_Records, Length_of_Single_Page = 2, Locate_to_Page = 1) # 第 1 页数据
    # [{'姓名': '张三', '年龄': '25', '职业': '工程师'},
    #  {'姓名': '李四', '年龄': '30', '职业': '设计师'}]
    # >>> Pager.Locate_to_Page(JSON_Records = JSON_Records, Length_of_Single_Page = 2, Locate_to_Page = 2) # 第 2 页数据
    # [{'姓名': '王五', '年龄': '28', '职业': '产品经理'},
    #  {'姓名': '赵六', '年龄': '35', '职业': '总监'}]
    # >>>
    # >>> # 测试用例 (4): 将 "员工信息" 分成 N 页, 每页 3 行数据
    # >>> Pager.Locate_to_Page(JSON_Records = JSON_Records, Length_of_Single_Page = 3, Locate_to_Page = 1) # 第 1 页数据
    # [{'姓名': '张三', '年龄': '25', '职业': '工程师'},
    #  {'姓名': '李四', '年龄': '30', '职业': '设计师'},
    #  {'姓名': '王五', '年龄': '28', '职业': '产品经理'}]
    # >>> Pager.Locate_to_Page(JSON_Records = JSON_Records, Length_of_Single_Page = 3, Locate_to_Page = 2) # 第 2 页数据
    # [{'姓名': '赵六', '年龄': '35', '职业': '总监'}]

    def Number_of_Page(self, JSON_Records:list, Length_of_Single_Page:int) -> int:

        Length_of_JSON_Records:int = len(JSON_Records)
        # ..........................................
        Number_of_Page:float = Length_of_JSON_Records / Length_of_Single_Page
        # ..........................................
        if (Number_of_Page > math.floor(Number_of_Page)):    # 如果 "向下取整前的页数" 大于 "向下取整后的页数"
            Number_of_Page = math.floor(Number_of_Page) + 1  # 那么 "页数" 的小数部分 (小于单页长度) 应占 1 页
        # ..........................................
        return int(Number_of_Page)

    def Length_of_Last_Page(self, JSON_Records:list, Length_of_Single_Page:int) -> int:

        Number_of_Page:int      = self.Number_of_Page(JSON_Records = JSON_Records, Length_of_Single_Page = Length_of_Single_Page)
        Length_of_Last_Page:int = Length_of_Single_Page  # "最后 1 页的长度" 默认等于 "单页长度"
        # ..........................................
        Real_Length_of_JSON_Records:int = len(JSON_Records)                       # 真实的 JSON Records 长度
        Hope_Length_of_JSON_Records:int = Length_of_Single_Page * Number_of_Page  # 理想的 JSON Records 长度 (每页长度相等)
        # ..........................................
        if (Hope_Length_of_JSON_Records > Real_Length_of_JSON_Records):  # 如果 "理想的 JSON Records 长度" 大于 "真实的 JSON Records 长度"
            Length_of_Last_Page = Length_of_Single_Page - (Hope_Length_of_JSON_Records - Real_Length_of_JSON_Records)
        # ..........................................
        return int(Length_of_Last_Page)

    def Locate_to_Page(self, JSON_Records:list, Length_of_Single_Page:int, Locate_to_Page:int) -> list:

        Number_of_Page:int      = self.Number_of_Page(JSON_Records = JSON_Records, Length_of_Single_Page = Length_of_Single_Page)
        Length_of_Last_Page:int = self.Length_of_Last_Page(JSON_Records = JSON_Records, Length_of_Single_Page = Length_of_Single_Page)
        # ..........................................
        Page:int         = 1
        Taken_Length:int = 0  # 取过的长度 (可理解为: 翻书时, 每页存在多个段落, 那么已经翻过了多少个段落)
        Start_Index:int  = 0
        # ..........................................
        while (Page <= Locate_to_Page):
            # 逐页累加 "取过的总长度"
            if (Page < Number_of_Page):
                Taken_Length = Taken_Length + Length_of_Single_Page
                Start_Index  = Taken_Length - Length_of_Single_Page
            if (Page == Number_of_Page):
                Taken_Length = Taken_Length + Length_of_Last_Page
                Start_Index  = Taken_Length - Length_of_Last_Page
            Page = Page + 1
        # ..........................................
        return JSON_Records[Start_Index: Taken_Length]

# Signed by GF.
