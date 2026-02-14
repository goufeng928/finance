# PY3_Requests2_GET_Download_File.py
# Create by GF 2025-12-26 14:13

import requests

# ##################################################

class PY3_Requests2_GET_Download_File():

    def __init__(self):

        self.Pub_Dify1114_API_Key:str = "unknow_dify1114_api_key"

    def From_Dify1114(self, URL, Save_Path) -> int:  # 返回 bytes Number (字节序列长度)

        # Requirement: Requests 2.32.0
        # Examples:
        # >>> url = "http://127.0.0.1/v1/files/f00e5935-3976-4142-be91-4bcc8d53f6ae/preview?as_attachment=true"
        # >>> Requests_2_x_Download_File(url, "f00e5935-3976-4142-be91-4bcc8d53f6ae")
        # 1191382

        headers:dict = {"Authorization": "Bearer %s" % self.Pub_Dify1114_API_Key}
        # ..........................................
        response = requests.get(URL, headers = headers, stream = True)
        # response.content 类型 (Type) 详解:
        # response.content 对于二进制文件则返回 bytes (字节序列):
        #     b'\x1f\x8b\x08\x08\x8c\xa0\x98T
        #       \x02\xffdist/pip-6.0.1.tar\x00
        #       ......
        #       \xcf\xe6\xd9\x9bg\xf3l\x9e\xcd
        #       \xf3\xfWn\x84\xf3\x00\xe8:\x00'
        # 其中 \x1f 是 1 个字节, 占 8 位 (bit), 用十六进制表示 (00-FF, 即 0-255 的十进制)
        # b'\x1f\x8b\x08\x08\x8c' 这样的字节序列用 Python 3.8 的 len() 函数可返回其长度为 5 (字节)
        # ..........................................
        if (response.status_code == 200):
            Download_File_Size = len(response.content)
            Download_File      = open(Save_Path, 'wb')
            Download_File.write(response.content)
            Download_File.close()
            return Download_File_Size
        # ..........................................
        else:
            return 0

# EOF Signed by GF.
