# PY310_JSON_Records_Based_on_NumPy225.py
# Create by GF 2025-12-22 15:13

import numpy  # NumPy 2.2.5

# ##################################################

class PY310_JSON_Records_Based_on_NumPy225():

    def change_field_type(self, JSON_Records, Field:str, Type:str):

        # numpy.array( ... ).dtype.descr 输出示例:
        # >>> dtp = [('id', "int64"), ("name", "<U255"), ("salary", "float64")]
        # >>> data = [(1, "张三", 4068.00), (2, "李四", 3610.50)]
        # >>> arr = numpy.array(data, dtype = dtp)
        # >>> print(arr.dtype.descr)
        # [('id', "int64"), ("name", "<U255"), ("salary", "float64")]
        # ..........................................
        DataType_Old:list = list(JSON_Records.dtype.descr)
        DataType_New:list = []
        # ..........................................
        i:int = 0
        while (i < len(DataType_Old)):
            if (DataType_Old[i][0] == Field):
                DataType_New.append((Field, Type))
            else:
                DataType_New.append(DataType_Old[i])
            i = i + 1
        # ..........................................
        DataType_New = numpy.dtype(DataType_New)
        # ..........................................
        # numpy.array( ... ).tolist() 输出示例:
        # >>> dtp = [('id', "int64"), ("name", "<U255"), ("salary", "float64")]
        # >>> data = [(1, "张三", 4068.00), (2, "李四", 3610.50)]
        # >>> arr = numpy.array(data, dtype = dtp)
        # >>> print(arr.tolist())
        # [(1, "张三", 4068.00), (2, "李四", 3610.50)]
        # ..........................................
        return numpy.array(JSON_Records.tolist(), dtype = DataType_New)

    def extract_all_field_name(self, JSON_Records):
        return JSON_Records.dtype.names

    def fit(self, List_Like:list):

        First_Record:dict             = List_Like[0]
        First_Record_Fields_List:list = list(First_Record.keys())
        # ..........................................
        DataType:list = []
        # ..........................................
        i:int = 0
        while (i < len(First_Record_Fields_List)):
            # NumPy 2.2.5 需要指定字符串长度 (如 Unicode 类型 "U255", 字符串类型 "S16") 的原因:
            # - 内存布局因素: NumPy 数组在内存中是连续的, 所以需要知道每个元素的大小。
            # - 性能优化因素: 固定长度允许直接计算偏移量, 无需指针解引用。
            # - 向量化因素: SIMD 指令需要相同大小的数据单元。
            # - 如果确实需要无长度限制, 可使用 ("name", object) 或 ("name", 'O') 这样的形式指定, 但会损失性能。
            DataType.append((First_Record_Fields_List[i], 'O'))
            i = i + 1
        # ..........................................
        DataType = numpy.dtype(DataType)
        # ..........................................
        Tuple_of_Values_in_List:list = []
        # ..........................................
        m:int = 0
        while (m < len(List_Like)):
            Tuple_of_Values:tuple = tuple(List_Like[m].values())
            Tuple_of_Values_in_List.append(Tuple_of_Values)
            m = m + 1
        # ..........................................
        return numpy.array(Tuple_of_Values_in_List, dtype = DataType)

# EOF Signed by GF.
