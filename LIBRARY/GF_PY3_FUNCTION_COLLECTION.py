# GF_PY3_FUNCTION_COLLECTION.py
# Environment: Python
# Create By GF 2025-01-20 20:00

# ################################################################################
# Beautifualsoup4 to Version 3.12.0 of Python.

from bs4 import BeautifulSoup

def Beautofulsoup_4_x_Picking_HTML_Tag(htmlString:str, htmlTag:str) -> str:

    # Example:
    # 查找所有 <li> 标签。
    # soup.find_all('li')
    
    soup = BeautifulSoup(htmlString, 'html.parser')
    htmlTagObjectList = soup.find_all(htmlTag)
    # ..............................................
    htmlTagStringList = []
    iterator = map(lambda x: htmlTagStringList.append(x.prettify()), htmlTagObjectList)
    list(iterator)
    result = str('').join(htmlTagStringList)
    # ..............................................
    return result

def Beautofulsoup_4_x_Picking_HTML_Class(htmlString:str, htmlClass:str) -> str:

    # Example:
    # 选择所有 class 为 "story" 的标签。
    # soup.select('.story')
    
    soup = BeautifulSoup(htmlString, 'html.parser')
    htmlTagObjectList = soup.select(htmlClass)
    # ..............................................
    htmlTagStringList = []
    iterator = map(lambda x: htmlTagStringList.append(x.prettify()), htmlTagObjectList)
    list(iterator)
    result = str('').join(htmlTagStringList)
    # ..............................................
    return result

def Beautofulsoup_4_x_HTML_Get_Text(htmlString:str) -> str:

    # Example:
    # 获取 <div> 标签及其子标签的所有文本内容, 并将它们合并成一个字符串‌。
    # text = soup.find('div').get_text()
    
    soup = BeautifulSoup(htmlString, 'html.parser')
    # ..............................................
    result = soup.get_text()
    # ..............................................
    return result

# ################################################################################
# List 1D Functions Related to Version 3.8.0 of Python.

def List_1D_Interlace_Extract_Row1_Row2(inputList:list) -> list:

    # Example:
    #
    # Input:
    # general.architecture
    # qwen2
    # general.basename
    # DeepSeek-R1-Distill-Qwen
    # general.file_type
    # 15
    # general.name
    # DeepSeek R1 Distill Qwen 14B
    # ......
    #
    # Output:
    # general.architecture  qwen2
    # general.basename      DeepSeek-R1-Distill-Qwen
    # general.file_type     15
    # general.name          DeepSeek R1 Distill Qwen 14B
    # ......

    listLength = len(inputList)
    headIndex = 0
    tailIndex = listLength - 1

    result:list = [[], []]
    
    row_1_idx = headIndex
    row_2_idx = row_1_idx + 1

    while (row_1_idx <= tailIndex):
        result[0].append(inputList[row_1_idx])
        row_1_idx = row_1_idx + 2

    while (row_2_idx <= tailIndex):
        result[1].append(inputList[row_2_idx])
        row_2_idx = row_2_idx + 2

    return result

def List_1D_Interlace_Extract_Row1_Row2_Row3(inputList:list) -> list:

    # Example:
    #
    # Input:
    # Name
    # Type
    # Shape
    # token_embd.weight
    # Q4_K
    # [5120, 152064]
    # blk.0.attn_k.bias
    # F32
    # [1024]
    # ......
    #
    # Output:
    # Name               Type  Shape
    # token_embd.weight  Q4_K  [5120, 152064]
    # blk.0.attn_k.bias  F32   [1024]
    # ......
    
    listLength = len(inputList)
    headIndex = 0
    tailIndex = listLength - 1

    result:list = [[], [], []]
    
    row_1_idx = headIndex
    row_2_idx = row_1_idx + 1
    row_3_idx = row_1_idx + 2

    while (row_1_idx <= tailIndex):
        result[0].append(inputList[row_1_idx])
        row_1_idx = row_1_idx + 3

    while (row_2_idx <= tailIndex):
        result[1].append(inputList[row_2_idx])
        row_2_idx = row_2_idx + 3

    while (row_3_idx <= tailIndex):
        result[2].append(inputList[row_3_idx])
        row_3_idx = row_3_idx + 3

    return result

# ################################################################################
# Mathematics Functions Related to Version 3.8.0 of Python.

def Safe_Multiply(self, multiplicand:float, Multiplier:float) -> float:

    if ((multiplicand == None) or (Multiplier == None)):
        # 如果被乘数为 None 或者乘数为 None。
        # ..........................................
        return None
    else:
        Result:float = (multiplicand * Multiplier)
        # ..........................................
        return Result

def Safe_Divide(self, Divisor:float, Dividend:float) -> float:

    if ((Dividend == 0.0) or (Dividend == None)):
        # 如果分母为 0 或者分母为 None。
        # ..........................................
        return None
    else:
        Result:float = (Divisor / Dividend)
        # ..........................................
        return Result

def List_Average(self, Lst:list) -> float:

    Result = self.Safe_Divide(sum(Lst), len(Lst))
    # ..............................................
    return Result

# ################################################################################
# JSON Functions Related to Version 3.8.0 of Python.

import json

def Read_JSONFile_and_Remove_Comments(JSONFilePath:str):

    JSONFile = open(JSONFilePath, 'r', encoding="utf-8")
    JSONString = JSONFile.read()
    
    # Define Regular Expressions to Match C-Style Comments.
    # (定义正则表达式来匹配 C 风格的注释)
    Comment_Pattern_1 = re.compile(r"\/\*.*\*\/")
    Comment_Pattern_2 = re.compile(r"\/\/.*")

    # Replace Comments with Regular Expressions.
    # (使用正则表达式替换掉注释)
    New_JSON_String = re.sub(Comment_Pattern_1, str(''), JSONString)
    New_JSON_String = re.sub(Comment_Pattern_2, str(''), New_JSON_String)

    # Parse JSON String.
    # (解析 JSON 字符串)
    ParsedJSON = json.loads(New_JSON_String)
    # ..............................................
    return ParsedJSON

def JSONString_Extract_Element_By_Index(JSONString:str, Index:int):

    # Convert "JSON String" to "Python List" (将 JSON 字符串转为 Python 列表)
    List_Obj = json.loads(JSONString)

    Element = List_Obj[Index]
    # ..............................................
    return Element

def JSONString_Replace_Element_By_Index(JSONString:str, Index:int, New_Element):

    # Convert "JSON String" to "Python List" (将 JSON 字符串转为 Python 列表)
    List_Obj = json.loads(JSONString)

    List_Obj[Index] = New_Element

    # 例如: Python 列表 [1, 2, 3] 将输出 '[1, 2, 3]'
    # (注意这里的输出实际上是带有双引号的, 并且数字之间有空格, 符合 JSON 标准)
    New_JSON_String = json.dumps(List_Obj)
    # ..............................................
    return New_JSON_String

# EOF Signed by GF.
