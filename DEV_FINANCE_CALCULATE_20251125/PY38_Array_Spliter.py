# GF_PY3_CLASS/PY38_Array_Spliter.py
# Create by GF 2025-09-20 00:53

class PY38_Array_Spliter(object):

    def Init_Array_Min_Index(self) -> int:
        return 0

    def Init_Array_Max_Index(self, Array_Length:int) -> int:
        return Array_Length - 1

    def Matrix_Flattening_for_Concatenate_Vector_and_Expand_Columns(self, Matrix:list, Vector:list) -> list:

        # 矩阵 (Matrix) 展平 (Flattening) for 拼接向量 (Concatenate Vector) and 扩展列 (Expand Columns)
        # 例如, 从 m * n 的矩阵扩展到 m * (n + k), 类似的典型应用: 线性方程组中增广矩阵添加常数列。
        # 步骤 1: 计算矩阵各行的元素数 [[1, 2], [3, 4], [5, 6]] -> [2, 2, 2]
        # 步骤 2: 将矩阵展平 (flatten) [[1, 2], [3, 4], [5, 6]] -> [1, 2, 3, 4, 5, 6]
        # 步骤 3: 将向量 [7, 8, 9] 拼接在矩阵展平的末尾: [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # 步骤 4: 扩展列, 通过向量 [7, 8, 9] 的元素数量, 计算拼接向量后的矩阵各行的元素数 [2, 2, 2] -> [3, 3, 3]
        # 步骤 5: 通过拼接向量后的矩阵各行的元素数量, 重新分组拼接后的矩阵展平: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        # Examples:
        # >>> Matrix = [[1]]
        # >>> Vector = [2, 3]
        # >>> Result = Matrix_Flattening_for_Concatenate_Vector_and_Expand_Columns(Matrix = Matrix, Vector = Vector)
        # >>> print(Result)
        # [[1, 2, 3]]
        # >>>
        # >>> Matrix = [[1, 2], [3, 4]]
        # >>> Vector = [5, 6, 7]
        # >>> Result = Matrix_Flattening_for_Concatenate_Vector_and_Expand_Columns(Matrix = Matrix, Vector = Vector)
        # >>> print(Result)
        # [[1, 2, 3, 4], [5, 6, 7]]
        # >>>
        # >>> Matrix = [[1, 2], [3, 4], [5, 6]]
        # >>> Vector = [7, 8, 9, 10]
        # >>> Result = Matrix_Flattening_for_Concatenate_Vector_and_Expand_Columns(Matrix = Matrix, Vector = Vector)
        # >>> print(Result)
        # [[1, 2, 3, 4], [5, 6, 7], [8, 9, 10]]

        Matrix_Rows_Count:int        = len(Matrix)
        Matrix_Max_Index:int         = self.Init_Array_Max_Index(Matrix_Rows_Count)
        Vector_Elements_Count:int    = len(Vector)
        Vector_Max_Index:int         = self.Init_Array_Max_Index(Vector_Elements_Count)
        Matrix_Flattened:list        = []
        Matrix_Expanded_Columns:list = []  # Return Result.
        # ..........................................
        # 矩阵各行元素数量
        # 如果 Matrix = [[1, 2], [3, 4], [5, 6]]
        # 那么矩阵各行元素数量 Matrix_Each_Row_Elements_Count = [2, 2, 2]
        # 如果 Matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        # 那么矩阵各行元素数量 Matrix_Each_Row_Elements_Count = [3, 3, 3]
        Matrix_Each_Row_Elements_Count:list = []
        # ..........................................
        # 矩阵 (Matrix) 展平 (Flattening)
        # 如果 Matrix = [[1, 2], [3, 4], [5, 6,]]
        # 那么矩阵的展平 Matrix_Flattened = [1, 2, 3, 4, 5, 6]
        # 如果 Matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        # 那么矩阵的展平 Matrix_Flattened = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        i:int = self.Init_Array_Min_Index()
        while (i <= Matrix_Max_Index):
            Elements_Count:int = len(Matrix[i])
            Matrix_Each_Row_Elements_Count.append(Elements_Count)
            Matrix_Flattened.extend(Matrix[i])
            i = i + 1
        # ..........................................
        # 拼接向量 (Concatenate Vector)
        Matrix_Flattened.extend(Vector)
        # ..........................................
        # Data Volume (数据量) <=> Elements Count (元素数)
        Matrix_Flattened_Elements_Count:int             = len(Matrix_Flattened)
        Matrix_Flattened_Max_Index:int                  = self.Init_Array_Max_Index(Matrix_Flattened_Elements_Count)
        Matrix_Each_Row_Elements_Count_s_Data_Volume    = len(Matrix_Each_Row_Elements_Count)
        Matrix_Each_Row_Elements_Count_s_Data_Max_Index = self.Init_Array_Max_Index(Matrix_Each_Row_Elements_Count_s_Data_Volume)
        # ..........................................
        # 根据向量 (Vector) 中的元素数量,
        # 计算矩阵各行元素数量 (Matrix Each Row Elements Count) 拼接向量 (Concatenate Vector) 后的数量。
        i:int = self.Init_Array_Min_Index()
        j:int = Vector_Elements_Count
        while (j > 0):
            Matrix_Each_Row_Elements_Count[i] = Matrix_Each_Row_Elements_Count[i] + 1
            j = j - 1
            if (i == Matrix_Each_Row_Elements_Count_s_Data_Max_Index):
                i = self.Init_Array_Min_Index()
            else:
                i = i + 1
        # ..........................................
        i:int = self.Init_Array_Min_Index()
        j:int = self.Init_Array_Min_Index()
        while (i <= Matrix_Each_Row_Elements_Count_s_Data_Max_Index):
            Row:list         = []
            Count:int        = 0
            Target_Count:int = Matrix_Each_Row_Elements_Count[i]
            i = i + 1
            while (j <= Matrix_Flattened_Max_Index):
                Row.append(Matrix_Flattened[j])
                Count = Count + 1
                j = j + 1
                if (Count == Target_Count):
                    Matrix_Expanded_Columns.append(Row)
                    break
        # ..........................................
        return Matrix_Expanded_Columns

    def Split_Array_into_Multi_Segment_Array_By_Equally(self, Array:list, Segments_Count:int = 1, Allocate_Remaining:int = 1) -> dict:

        # Examples:
        # >>> Arr = [1, 2]
        # >>> Res = Split_Array_into_Multi_Segment_Array_By_Equally(Array = Arr, Segments_Count = 2, Allocate_Remaining = 0)
        # >>> print(Res)
        # {'multi_segment_array': [[1], [2]], 'remaining_array': []}
        # >>>
        # >>> Arr = [1, 2, 3]
        # >>> Res = Split_Array_into_Multi_Segment_Array_By_Equally(Array = Arr, Segments_Count = 2, Allocate_Remaining = 0)
        # >>> print(Res)
        # {'multi_segment_array': [[1], [2]], 'remaining_array': [3]}
        # >>>
        # >>> Arr = [1, 2, 3]
        # >>> Res = Split_Array_into_Multi_Segment_Array_By_Equally(Array = Arr, Segments_Count = 2, Allocate_Remaining = 1)
        # >>> print(Res)
        # {'multi_segment_array': [[1, 2], [3]], 'remaining_array': []}
        # >>>
        # >>> Arr = [1, 2, 3, 4, 5]
        # >>> Res = Split_Array_into_Multi_Segment_Array_By_Equally(Array = Arr, Segments_Count = 3, Allocate_Remaining = 0)
        # >>> print(Res)
        # {'multi_segment_array': [[1], [2], [3]], 'remaining_array': [4, 5]}
        # >>>
        # >>> Arr = [1, 2, 3, 4, 5]
        # >>> Res = Split_Array_into_Multi_Segment_Array_By_Equally(Array = Arr, Segments_Count = 3, Allocate_Remaining = 1)
        # >>> print(Res)
        # {'multi_segment_array': [[1, 2], [3, 4], [5]], 'remaining_array': []}

        Array_Length:int = len(Array)
        Array_MaxIdx:int = self.Init_Array_Max_Index(Array_Length)
        # ..........................................
        Remainder:int           = (Array_Length % Segments_Count)  # 计算余数
        Each_Segment_Length:int = (Array_Length - Remainder) / (Segments_Count)
        # ..........................................
        Multi_Segment_Array:list       = []
        Multi_Segment_Array_MaxIdx:int = self.Init_Array_Max_Index(Segments_Count)
        Remaining_Array:list           = []  # 将剩余未分配的数组元素放入 Remaining Array
        # ..........................................
        Total:int = 0  # 总数
        Phase:int = 0  # 阶段总数 (每处理完 1 个 Chunk 的数量为 1 个阶段)
        Segment:list = []
        # ..........................................
        i:int = self.Init_Array_Min_Index()
        while (i <= Array_MaxIdx):
            Element = Array[i]
            Total = Total + 1  # 先计数, 后处理 (计入总数)
            Phase = Phase + 1  # 先计数, 后处理 (计入阶段总数)
            Segment.append(Element)
            if (Phase == Each_Segment_Length):
                Phase = 0
                Multi_Segment_Array.append(Segment.copy())  # 必须拷贝 (Copy) 而不是引用 (Quote)
                Segment.clear()
            if (Total == Each_Segment_Length * Segments_Count):
                break
            i = i + 1
        # ..........................................
        if (Remainder != 0):
            j:int = i + 1
            while (j <= Array_MaxIdx):
                Remaining_Array.append(Array[j])
                j = j + 1
        # ..........................................
        if (Remainder != 0 and Allocate_Remaining == 1):
            Multi_Segment_Array = self.Matrix_Flattening_for_Concatenate_Vector_and_Expand_Columns(
                Matrix = Multi_Segment_Array, Vector = Remaining_Array)
            Remaining_Array.clear()
        # ..........................................
        return {"multi_segment_array": Multi_Segment_Array, "remaining_array": Remaining_Array}

# EOF Signed by GF.
