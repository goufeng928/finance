# GF_PY3_CLASS/Python3_Requests2/PY3_Requests2_BS4_HTTP_Collect.py
# Create by GF 2025-09-08 12:53

import time
# ..................................................
import bs4
import requests
# ..................................................
import PY3_HTTP_URL_Path_Operate
# ..................................................
URL_Path_Operate = PY3_HTTP_URL_Path_Operate.PY3_HTTP_URL_Path_Operate()

class PY3_Requests2_BS4_HTTP_Collect():

    def __init__(self):

        self.Current_Page:str = ""
        self.HTTP_Headers:dict = {}
        self.Tags_a:list = []

    def href_URL_Relative_Path_to_Absolute_Path(self, Curr_URL:str, href_URL:str) -> str:

        # Examples:
        # >>> Curr_URL = "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/pip"
        # >>> href_URL = "../../packages/47/3e/68be2af/pip-25.0.tar.gz"
        # >>> href_URL = href_URL_Relative_Path_to_Absolute_Path(Curr_URL = Curr_URL, href_URL = href_URL)
        # >>> print(href_URL)
        # https://mirrors.tuna.tsinghua.edu.cn/pypi/web/packages/47/3e/68be2af/pip-25.0.tar.gz

        Curr_URL_Copy = Curr_URL
        href_URL_Copy = href_URL
        # ..........................................
        A:int = 0
        B:int = 3
        Capture = href_URL[A:B]
        # ..........................................
        if ("../" in Capture):
            while ("../" in Capture):
                Curr_URL_Copy = URL_Path_Operate.Backward(Curr_URL_Copy)
                A = A + 3
                B = B + 3
                Capture  = href_URL[A:B]
            # ......................................
            href_URL_Copy = Curr_URL_Copy + '/' + href_URL[A:]
        # ..........................................
        return href_URL_Copy

    def GET_Page_Source(self, URL:str) -> str:

        # Requirement: Requests 2.32.0

        Response        = requests.get(URL, headers = self.HTTP_Headers)
        Page_Source:str = Response.text
        # ..........................................
        if ("tsinghua.edu.cn" in URL):
            time.sleep(3)
        # ..........................................
        return Page_Source

    def GET_Download_File(self, URL, Save_Path) -> int:  # 返回 bytes Number (字节序列长度)

        # Requirement: Requests 2.32.0
        # Examples:
        # >>> url = "https://example.com/pip-6.0.1.tar.gz"
        # >>> Requests_2_x_Download_File(url, "pip-6.0.1.tar.gz")
        # 1191382

        response = requests.get(URL, headers = self.HTTP_Headers, stream = True)
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

    def GET_Tags_a(self, URL:str) -> list:

        # Requirement: Beautifulsoup4 4.10.0

        Page_Source:str = self.GET_Page_Source(URL = URL)
        # ..........................................
        Soup = bs4.BeautifulSoup(Page_Source, 'html.parser')
        # ..........................................
        # 查找所有的 <a> 标签
        # find_all 返回值: bs4.element.ResultSet (可迭代对象)
        # find_all 内含值: 每个元素是一个 bs4.element.Tag 类型
        Tags_a = Soup.find_all('a')
        # ..........................................
        return Tags_a

    def GET_Tags_a_Attrs_href(self, URL:str) -> list:

        # Explanation: Attrs == Attributes
        # Requirement: Beautifulsoup4 4.10.0

        Tags_a:list = self.GET_Tags_a(URL = URL)
        # ..........................................
        # 提取所有的 <a> 标签中的 href 内容, 提取为 str 类型
        Tags_a_Attrs_href:list = []
        for a in Tags_a:
            href = a.get('href')
            href = self.href_URL_Relative_Path_to_Absolute_Path(Curr_URL = URL, href_URL = href)
            Tags_a_Attrs_href.append(href)
        # ..........................................
        return Tags_a_Attrs_href

# EOF Signed by GF.

