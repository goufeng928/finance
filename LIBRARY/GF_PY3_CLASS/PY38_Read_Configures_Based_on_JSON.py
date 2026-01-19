# GF_PY3_CLASS/PY38_Read_Configures_Based_on_JSON.py
# Create by GF 2025-04-02 23:42

import json

# ##################################################

class PY38_Read_Configures_Based_on_JSON(object):

    def __init__(self):

        self.Pub_JSON_File_Path:str = "configures.json"

    def JSON_Text_to_List(self, JSON_Text:str) -> list:

        try:
            JSON_List:list = json.loads(JSON_Text)
        # ..........................................
        except Exception as e:
            print("[DEBUG] PY38_Configures_Based_on_JSON.JSON_Text_to_List: %s" % str(e))
        # ..........................................
        return JSON_List

    def JSON_Text_to_Dict(self, JSON_Text:str) -> dict:

        try:
            JSON_Dict:dict = json.loads(JSON_Text)
        # ..........................................
        except Exception as e:
            print("[DEBUG] PY38_Configures_Based_on_JSON.JSON_Text_to_Dict: %s" % str(e))
        # ..........................................
        return JSON_Dict

    def Read(self, JSON_File_Path:str) -> object:

        JSON_File     = open(JSON_File_Path, mode = 'r')
        JSON_Text:str = JSON_File.read()
        JSON_File.close()
        # ..........................................
        JSON_Type:str = str('')
        # ..........................................
        # 遍历字符串中 (String) 所有字符 (Char), 当 Char 为 '[' 或 '{' 时停止。
        i:int = 0
        while (i < len(JSON_Text)):
            Char:str = JSON_Text[i]
            # ......................................
            if (Char == '['):
                JSON_Type = "list"
                break
            # ......................................
            if (Char == '{'):
                JSON_Type = "dict"
                break
            i = i + 1
        # ..........................................
        if (JSON_Type == "list"):
            return self.JSON_Text_to_List(JSON_Text = JSON_Text)
        # ..........................................
        if (JSON_Type == "dict"):
            return self.JSON_Text_to_Dict(JSON_Text = JSON_Text)

# EOF Signed by GF.
