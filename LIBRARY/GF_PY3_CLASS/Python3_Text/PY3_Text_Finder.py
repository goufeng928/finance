# GF_PY3_CLASS/Python3_Text/PY3_Text_Finder.py
# Create by GF 2025-09-20 00:53

class PY3_Text_Finder(object):

    # Examples for "Find Starting Index of Sub Text in Text":
    # >>> OBJECT_PY3_Text_Finder = PY3_Text_Finder()
    # >>>
    # >>> Sentence = "Jack, Bob, and Adam's scores are 87.50, 92.00, and 89.50, respectively."
    # >>> Scores = ["87.50", "92.00", "89.50"]
    # >>>
    # >>> Result = OBJECT_PY3_Text_Finder.Find_Starting_Index_of_Sub_Text_in_Text(Text = Sentence, Sub_Text = "Bob")
    # >>> print(Result)
    # 6
    # >>> Result = OBJECT_PY3_Text_Finder.Find_Starting_Index_of_Sub_Text_in_Text(Text = Sentence, Sub_Text = '')
    # >>> print(Result)
    # 0

    # Examples for "Find Ending Index of Sub Text in Text":
    # >>> OBJECT_PY3_Text_Finder = PY3_Text_Finder()
    # >>>
    # >>> Sentence = "Jack, Bob, and Adam's scores are 87.50, 92.00, and 89.50, respectively."
    # >>> Scores = ["87.50", "92.00", "89.50"]
    # >>>
    # >>> Result = OBJECT_PY3_Text_Finder.Find_Ending_Index_of_Sub_Text_in_Text(Text = Sentence, Sub_Text = "Bob")
    # >>> print(Result)
    # 8
    # >>> Result = OBJECT_PY3_Text_Finder.Find_Ending_Index_of_Sub_Text_in_Text(Text = Sentence, Sub_Text = '')
    # >>> print(Result)
    # -1

    # Examples for "Find Text Fragments Around The Target Text":
    # >>> OBJECT_PY3_Text_Finder = PY3_Text_Finder()
    # >>>
    # >>> Sentence = "Jack, Bob, and Adam's scores are 87.50, 92.00, and 89.50, respectively."
    # >>> Target_Text = "and"
    # >>>
    # >>> Result = OBJECT_PY3_Text_Finder.Find_Text_Fragments_Around_The_Target_Text(Text = Sentence, Target_Text = Target_Text, Fragment_Length = 31)
    # >>> print(Result)
    # and Adam's scores are 87.50, 92.00
    # >>> Result = OBJECT_PY3_Text_Finder.Find_Text_Fragments_Around_The_Target_Text(Text = Sentence, Target_Text = Target_Text, Fragment_Length = (-11))
    # >>> print(Result)
    # Jack, Bob, and

    # Examples for "Find B from The Min Distance of A":
    # >>> OBJECT_PY3_Text_Finder = PY3_Text_Finder()
    # >>>
    # >>> Sentence = "Jack, Bob, and Adam's scores are 87.50, 92.00, and 89.50, respectively."
    # >>> Scores = ["87.50", "92.00", "89.50"]
    # >>>
    # >>> Result = OBJECT_PY3_Text_Finder.Find_B_from_The_Min_Distance_of_A(Full_Text = Sentence, A_Text = "Jack", B_List = Scores)
    # >>> print(Result)
    # 87.50

    # Examples for "Find B from The Max Distance of A":
    # >>> OBJECT_PY3_Text_Finder = PY3_Text_Finder()
    # >>>
    # >>> Sentence = "Jack, Bob, and Adam's scores are 87.50, 92.00, and 89.50, respectively."
    # >>> Scores = ["87.50", "92.00", "89.50"]
    # >>>
    # >>> Result = OBJECT_PY3_Text_Finder.Find_B_from_The_Max_Distance_of_A(Full_Text = Sentence, A_Text = "Adam", B_List = Scores)
    # >>> print(Result)
    # 89.50

    def __init__(self):

        self.Offset_Index_of_Array:int = 0 - 1
        self.Starting_Index_of_Array:int = 0
        self.Offset_for_Ending_Index_of_Array_Slice:int = 0 + 1

    def Find_Starting_Index_of_Sub_Text_in_Text(self, Text:str, Sub_Text:str) -> int:

        # 在文本中查找子文本的起始索引 (Find Starting Index of Sub Text in Text)

        Text_Length:int = len(Text)
        # ..........................................
        Sub_Text_Length:int = len(Sub_Text)
        Sub_Text_Start_Position:int = self.Starting_Index_of_Array
        Sub_Text_End_Position:int = Sub_Text_Start_Position + Sub_Text_Length - 1
        # ..........................................
        while (Sub_Text_End_Position < Text_Length):
            Found_Text:str = Text[Sub_Text_Start_Position: Sub_Text_End_Position + self.Offset_for_Ending_Index_of_Array_Slice]
            # ......................................
            if (Found_Text == Sub_Text):
                break
            # ......................................
            Sub_Text_Start_Position = Sub_Text_Start_Position + 1
            Sub_Text_End_Position = Sub_Text_Start_Position + Sub_Text_Length - 1
        # ..........................................
        return Sub_Text_Start_Position

    def Find_Ending_Index_of_Sub_Text_in_Text(self, Text:str, Sub_Text:str) -> int:

        # 在文本中查找子文本的结束索引 (Find Ending Index of Sub Text in Text)

        Text_Length:int = len(Text)
        # ..........................................
        Sub_Text_Length:int = len(Sub_Text)
        Sub_Text_Start_Position:int = self.Starting_Index_of_Array
        Sub_Text_End_Position:int = Sub_Text_Start_Position + Sub_Text_Length - 1
        # ..........................................
        while (Sub_Text_End_Position < Text_Length):
            Found_Text:str = Text[Sub_Text_Start_Position: Sub_Text_End_Position + self.Offset_for_Ending_Index_of_Array_Slice]
            # ......................................
            if (Found_Text == Sub_Text):
                break
            # ......................................
            Sub_Text_Start_Position = Sub_Text_Start_Position + 1
            Sub_Text_End_Position = Sub_Text_Start_Position + Sub_Text_Length - 1
        # ..........................................
        return Sub_Text_End_Position

    def Find_Text_Fragments_Around_The_Target_Text(self, Text:str, Target_Text:str, Fragment_Length:int) -> str:

        # 在目标文本周围查找文本片段 (Find Text Fragments Around The Target Text)

        Text_Fragment:str = ''
        # ..........................................
        if (Fragment_Length == 0):
            Text_Fragment = Target_Text
        # ..........................................
        if (Fragment_Length < 0):
            Target_Text_Length:int = len(Target_Text)
            Text_Fragment_End_Position:int = self.Find_Ending_Index_of_Sub_Text_in_Text(Text = Text, Sub_Text = Target_Text)
            Text_Fragment_Start_Position:int = Text_Fragment_End_Position - Target_Text_Length - (Fragment_Length * (-1)) + 1
            # ......................................
            if (Text_Fragment_Start_Position < self.Starting_Index_of_Array):
                Text_Fragment_Start_Position = self.Starting_Index_of_Array
            # ......................................
            Text_Fragment = Text[Text_Fragment_Start_Position:Text_Fragment_End_Position + self.Offset_for_Ending_Index_of_Array_Slice]
        # ..........................................
        if (Fragment_Length > 0):
            Target_Text_Length:int = len(Target_Text)
            Text_Fragment_Start_Position:int = self.Find_Starting_Index_of_Sub_Text_in_Text(Text = Text, Sub_Text = Target_Text)
            Text_Fragment_End_Position:int = Text_Fragment_Start_Position + Target_Text_Length + Fragment_Length - 1
            # ......................................
            if (Text_Fragment_Start_Position > len(Text)):
                Text_Fragment_Start_Position = len(Text)
            # ......................................
            Text_Fragment = Text[Text_Fragment_Start_Position:Text_Fragment_End_Position + self.Offset_for_Ending_Index_of_Array_Slice]
        # ..........................................
        return Text_Fragment

    def Find_B_from_The_Min_Distance_of_A(self, Full_Text:str, A_Text:str, B_List:list) -> str:

        # 从 A 的最小距离找到 B (Find B from The Min Distance of A)

        Full_Text_Length:int = len(Full_Text)
        # ..........................................
        A_End_Position:int = self.Find_Ending_Index_of_Sub_Text_in_Text(Text = Full_Text, Sub_Text = A_Text)
        # ..........................................
        Candidate_List:list = []
        Distance_List:list = []
        # ..........................................
        i:int = 0
        while (i <= len(B_List) + self.Offset_Index_of_Array):
            B_Text:str = B_List[i]
            B_Text_Length:int = len(B_Text)
            B_Start_Position:int = A_End_Position + 1
            B_End_Position:int = B_Start_Position + B_Text_Length - 1
            # ......................................
            while (B_End_Position < Full_Text_Length):
                Found_Text:str = Full_Text[B_Start_Position: B_End_Position + self.Offset_for_Ending_Index_of_Array_Slice]
                # ..................................
                if (Found_Text == B_Text):
                    Candidate_List.append(Found_Text)
                    Distance_List.append(B_Start_Position - A_End_Position - 1)
                    break  # 找到第 1 个匹配字符串就停止内层循环, 避免重复添加查找结果
                # ..................................
                B_Start_Position = B_Start_Position + 1
                B_End_Position = B_Start_Position + B_Text_Length - 1
            # ......................................
            i = i + 1
        # ..........................................
        return Candidate_List[Distance_List.index(min(Distance_List))]

    def Find_B_from_The_Max_Distance_of_A(self, Full_Text:str, A_Text:str, B_List:list) -> str:

        # 从 A 的最大距离找到 B (Find B from The Max Distance of A)

        Full_Text_Length:int = len(Full_Text)
        # ..........................................
        A_End_Position:int = self.Find_Ending_Index_of_Sub_Text_in_Text(Text = Full_Text, Sub_Text = A_Text)
        # ..........................................
        Candidate_List:list = []
        Distance_List:list = []
        # ..........................................
        i:int = 0
        while (i <= len(B_List) + self.Offset_Index_of_Array):
            B_Text:str = B_List[i]
            B_Text_Length:int = len(B_Text)
            B_Start_Position:int = A_End_Position + 1
            B_End_Position:int = B_Start_Position + B_Text_Length - 1
            # ......................................
            while (B_End_Position < Full_Text_Length):
                Found_Text:str = Full_Text[B_Start_Position: B_End_Position + self.Offset_for_Ending_Index_of_Array_Slice]
                # ..................................
                if (Found_Text == B_Text):
                    Candidate_List.append(Found_Text)
                    Distance_List.append(B_Start_Position - A_End_Position - 1)
                    break  # 找到第 1 个匹配字符串就停止内层循环, 避免重复添加查找结果
                # ..................................
                B_Start_Position = B_Start_Position + 1
                B_End_Position = B_Start_Position + B_Text_Length - 1
            # ......................................
            i = i + 1
        # ..........................................
        return Candidate_List[Distance_List.index(max(Distance_List))]

# EOF Signed by GF.
