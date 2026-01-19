# GF_PY3_CLASS/Python_3_Pandas_2/PY3_Pandas2_Read_Directory.py
# Create by GF 2025-09-19 16:53

import os
# ..................................................
import chardet  # chardet 5.2.0
import pandas  # Pandas 2.0.3 (Dependency: xlrd 2.0.2, OpenPyXL 3.1.5)

# ##################################################

class PY3_Pandas2_Read_Directory(object):

    def Walk_Directory(self, Directory:str) -> list:

        File_Path_List:list = []
        # ..........................................
        for root, directories, files in os.walk(Directory):
            for file in files:
                File_Path = os.path.join(root, file)
                File_Path_List.append(File_Path)
        # ..........................................
        return File_Path_List

    def Detect_Text_File_Encoding(self, Text_File_Path:str, Sample_Size:int = 10000) -> str:

        Binary_File_Object  = open(Text_File_Path, mode = "rb")
        Binary_File_Content = Binary_File_Object.read(Sample_Size)  # 只读取文件的一部分以提高性能
        Binary_File_Object.close()
        # ..........................................
        Detected = chardet.detect(Binary_File_Content)
        # ..........................................
        # 字符编码映射 (将原始字符编码映射为兼容性更好, 更合适的字符编码)
        # 类似于像 "0xd9" 这种编码 GB2312 不能解码, 但是 GBK 可以解码
        Encoding_Mapping = {"UTF-8-SIG": "UTF-8", "GB2312": "GBK", "GB18030": "GBK"}
        # ..........................................
        Text_File_Encoding            = Detected["encoding"]
        Text_File_Encoding            = Encoding_Mapping.get(Text_File_Encoding, Text_File_Encoding)
        Text_File_Encoding_Confidence = Detected["confidence"]
        # ..........................................
        return Text_File_Encoding

    def Detect_Table_File_Header_Row_Index(self, Table_File_Path:str, Sheet_Name = 0, Sample_Rows:int = 10) -> int:

        Header_Row_Index:int = 0
        # ..........................................
        if (".csv" in Table_File_Path.lower()):
            # Require: chardet 5.2.0
            Detected_Encoding:str = self.Detect_Text_File_Encoding(Table_File_Path)
            df = pandas.read_csv(Table_File_Path, encoding = Detected_Encoding, header = None, dtype = str, nrows = Sample_Rows)
            # ......................................
            Count_Non_Empty_Rows = df.notna().sum(axis = 1)   # 统计每行的非空值数量
            Header_Row_Index = Count_Non_Empty_Rows.idxmax()  # 找到非空值最多的行
        # ..........................................
        if (".xls" in Table_File_Path.lower() or ".xlsx" in Table_File_Path.lower()):
            # Require: xlrd 2.0.2, OpenPyXL 3.1.5
            df = pandas.read_excel(Table_File_Path, sheet_name = Sheet_Name, header = None, dtype = str, nrows = Sample_Rows)
            # ......................................
            Count_Non_Empty_Rows = df.notna().sum(axis = 1)
            Header_Row_Index = Count_Non_Empty_Rows.idxmax()
        # ..........................................
        return Header_Row_Index

    def Detect_Directory_Files_Details(self, Directory:str) -> list:

        # Output Example:
        # [
        #     {
        #         "file_path": "/home/username/example_1.csv",
        #         "file_format": ".csv",
        #         "file_encoding": "utf-8",
        #         "header_row_index": 0,
        #     },
        #     {
        #         "file_path": "/home/username/example_2.xlsx",
        #         "file_format": ".xlsx",
        #         "file_encoding": "skip detect",
        #         "header_row_index": 1,
        #     },
        #     ......
        # ]

        JSON_Records:list   = []
        File_Path_List:list = self.Walk_Directory(Directory)
        # ..........................................
        # 筛选特定的文件格式
        for File_Path in File_Path_List:
            if (".csv" in File_Path.lower()):
                Record:dict = {
                    "file_path":        File_Path,
                    "file_format":      ".csv",
                    "file_encoding":    self.Detect_Text_File_Encoding(File_Path),
                    "header_row_index": self.Detect_Table_File_Header_Row_Index(File_Path)
                }
                # ..................................
                JSON_Records.append(Record)
            # ......................................
            elif (".xls" in File_Path.lower()):
                Record:dict = {
                    "file_path":        File_Path,
                    "file_format":      ".xls",
                    "file_encoding":    "skip detect",
                    "header_row_index": self.Detect_Table_File_Header_Row_Index(File_Path)
                }
                # ..................................
                JSON_Records.append(Record)
            # ......................................
            elif (".xlsx" in File_Path.lower()):
                Record:dict = {
                    "file_path":        File_Path,
                    "file_format":      ".xlsx",
                    "file_encoding":    "skip detect",
                    "header_row_index": self.Detect_Table_File_Header_Row_Index(File_Path)
                }
                # ..................................
                JSON_Records.append(Record)
        # ..........................................
        return JSON_Records

    def Read_Directory(self, Directory:str, Header:int = (-1)):

        # Output Example:
        # [
        #     {
        #         "file_path": "/home/username/example_1.csv",
        #         "file_format": ".csv",
        #         "file_encoding": "utf-8",
        #         "header_row_index": 0,
        #         "dataframe": {
        #             "default": pandas.DataFrame()
        #         }
        #     },
        #     {
        #         "file_path": "/home/username/example_2.xlsx",
        #         "file_format": ".xlsx",
        #         "file_encoding": "skip detect",
        #         "header_row_index": 1,
        #         "dataframe": {
        #             "Sheet1": pandas.DataFrame(),
        #             "Sheet2": pandas.DataFrame(),
        #             "Sheet3": pandas.DataFrame()
        #         }
        #     },
        #     ......
        # ]

        JSON_Records:list          = self.Detect_Directory_Files_Details(Directory)
        JSON_Records_Count:int     = len(JSON_Records)
        JSON_Records_Max_Index:int = JSON_Records_Count - 1
        # ..........................................
        if (Header != (-1)):
            i:int = 0
            while (i <= JSON_Records_Max_Index):
                JSON_Records[i].update({"header_row_index": Header})
                i = i + 1
        # ..........................................
        i:int = 0
        while (i <= JSON_Records_Max_Index):
            Record = JSON_Records[i]
            # ......................................
            if (Record["file_format"] == ".csv"):
                DICT_DataFrame:dict = {}
                df = pandas.read_csv(Record["file_path"], encoding = Record["file_encoding"], header = Record["header_row_index"], dtype = str)
                DICT_DataFrame.update({"default": df})
                JSON_Records[i].update({"dataframe": DICT_DataFrame})
            # ......................................
            if (Record["file_format"] == ".xls" or Record["file_format"] == ".xlsx"):
                OBJECT_Excel = pandas.ExcelFile(Record["file_path"])  # 创建 ExcelFile 对象
                DICT_DataFrame:dict = {}
                for Sheet_Name in OBJECT_Excel.sheet_names:
                    df = pandas.read_excel(Record["file_path"], sheet_name = Sheet_Name, header = Record["header_row_index"], dtype = str)
                    DICT_DataFrame.update({Sheet_Name: df})
                JSON_Records[i].update({"dataframe": DICT_DataFrame})
            # ......................................
            i = i + 1
        # ..........................................
        return JSON_Records

    def Read_Directory_s_All_Excel_Sheet_s_Auto_Header(self, Directory:str) -> dict:

        # Output Example:
        # [
        #     {
        #         "file_name": "example.xlsx",
        #         "file_path": "/home/username/example.xlsx",
        #         "sheet_dataframe": {
        #             "Sheet1": pandas.DataFrame(),
        #             "Sheet2": pandas.DataFrame(),
        #             "Sheet3": pandas.DataFrame()
        #         }
        #     },
        #     ......
        # ]

        JSON_Records:list = []

        for root, directories, files in os.walk(Directory):
            for file in files:

                if (".xls" in file or ".xlsx" in file):

                    file_path = os.path.join(root, file)
                    # ..............................
                    OBJECT_Excel = pandas.ExcelFile(file_path)  # 创建 ExcelFile 对象

                    sheet_dataframe = {}
                    for sheet_name in OBJECT_Excel.sheet_names:

                        Header_Row_Index:int = self.Detect_Table_File_Header_Row_Index(File_Path, Sheet_Name = sheet_name)
                        # ..........................
                        df = pandas.read_excel(file_path, sheet_name = sheet_name, header = Header_Row_Index, dtype = str)
                        # ..........................
                        sheet_dataframe.update({sheet_name: df})

                    Record = {
                        "file_name":file,
                        "file_path": file_path,
                        "sheet_dataframe": sheet_dataframe
                    }
                    # ..............................
                    JSON_Records.append(Record)

        return JSON_Records

# EOF Signed by GF.
