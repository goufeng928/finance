# GF_PY3_CLASS/PY3_HTTP_URL_Path_Operate.py
# Create by GF 2025-09-08 12:53

class PY3_HTTP_URL_Path_Operate(object):

    # Examples for Get URL Protocol:
    # >>> URL_Path = PY3_HTTP_URL_Path_Operate()
    # >>>
    # >>> Result = URL_Path.Get_URL_Protocol(URL = "https://www.msn.cn/zh-cn/play/arcade?ocid=cgbinghp")
    # >>> print(Result)
    # https:
    # >>> Result = URL_Path.Get_URL_Protocol(URL = "ftp://ftp.mirrorservice.org/sites/sourceware.org/pub/gcc/releases")
    # >>> print(Result)
    # ftp:

    # Examples for Get URL Path:
    # >>> URL_Path = PY3_HTTP_URL_Path_Operate()
    # >>>
    # >>> Result = URL_Path.Get_URL_Path(URL = "https://www.msn.cn/zh-cn/play/arcade?ocid=cgbinghp")
    # >>> print(Result)
    # www.msn.cn/zh-cn/play/arcade?ocid=cgbinghp
    # >>> Result = URL_Path.Get_URL_Path(URL = "ftp://ftp.mirrorservice.org/sites/sourceware.org/pub/gcc")
    # >>> print(Result)
    # ftp.mirrorservice.org/sites/sourceware.org/pub/gcc

    # Examples for Get URL Basename:
    # >>> URL_Path = PY3_HTTP_URL_Path_Operate()
    # >>>
    # >>> Result = URL_Path.Get_URL_Basename(URL = "https://www.php.net/distributions/php-8.2.29.tar.gz")
    # >>> print(Result)
    # php-8.2.29.tar.gz
    # >>> Result = URL_Path.Get_URL_Basename(URL = "ftp://ftp.mirrorservice.org/sites/sourceware.org/pub/gcc")
    # >>> print(Result)
    # gcc

    # Examples for URL Protocol and URL Path:
    # >>> URL_Path = PY3_HTTP_URL_Path_Operate()
    # >>>
    # >>> Result = URL_Path.Combining_URL_Protocol_and_URL_Path(URL_Protocol = "http:", URL_Path = "www.bing.com/images")
    # >>> print(Result)
    # http://www.bing.com/images
    # >>> Result = URL_Path.Combining_URL_Protocol_and_URL_Path(URL_Protocol = "ftp:", URL_Path = "ftp.mirrorservice.org/sites")
    # >>> print(Result)
    # ftp://ftp.mirrorservice.org/sites

    # Examples for Backward:
    # >>> URL_Path = PY3_HTTP_URL_Path_Operate()
    # >>>
    # >>> Result = URL_Path.Backward(URL = "https://www.msn.cn/zh-cn/play/arcade?ocid=cgbinghp")
    # >>> print(Result)
    # https://www.msn.cn/zh-cn/play
    # >>> Result = URL_Path.Backward(URL = "ftp://ftp.mirrorservice.org/sites/sourceware.org/pub/gcc")
    # >>> print(Result)
    # ftp://ftp.mirrorservice.org/sites/sourceware.org/pub

    def Get_URL_Protocol(self, URL:str, Protocol_Separator:str = "//") -> str:

        # URL Protocol Types:
        # - http: 超文本传输协议, 不加密。
        # - https: 安全的超文本传输协议, 在 HTTP 基础上增加了 SSL/TLS 加密。
        # - ftp: 文件传输协议。
        # - file: 用于访问本地计算机上的文件。
        # - mailto: 用于打开邮件客户端发送邮件。

        URL_Transform:str = URL
        # ..........................................
        URL_Split:list = URL_Transform.split(Protocol_Separator)
        # ..........................................
        return URL_Split[0]

    def Get_URL_Path(self, URL:str, Protocol_Separator:str = "//") -> str:

        URL_Transform:str = URL
        # ..........................................
        URL_Split:list = URL_Transform.split(Protocol_Separator)
        # ..........................................
        return URL_Split[1]

    def Get_URL_Basename(self, URL:str, Protocol_Separator:str = "//") -> str:

        URL_Path:str = self.Get_URL_Path(URL = URL)
        # ..........................................
        URL_Path_Split:list = URL_Path.split('/')
        # ..........................................
        return URL_Path_Split[-1]

    def Combining_URL_Protocol_and_URL_Path(self, URL_Protocol:str, URL_Path:str) -> str:

        URL_Protocol_Transform:str = URL_Protocol
        URL_Protocol_Transform     = URL_Protocol_Transform.lstrip('/')
        URL_Protocol_Transform     = URL_Protocol_Transform.rstrip('/')
        # ..........................................
        URL_Path_Transform:str = URL_Path
        URL_Path_Transform     = URL_Path_Transform.lstrip('/')
        URL_Path_Transform     = URL_Path_Transform.rstrip('/')
        # ..........................................
        return URL_Protocol_Transform + "//" + URL_Path_Transform

    def Backward(self, URL:str) -> str:

        URL_Protocol:str = self.Get_URL_Protocol(URL = URL)
        URL_Path:str     = self.Get_URL_Path(URL = URL)
        # ..........................................
        URL_Path_Split:list = URL_Path.split('/')
        URL_Path_Split      = URL_Path_Split[0:len(URL_Path_Split) - 1]
        URL_Path            = str('/').join(URL_Path_Split)
        # ..........................................
        return self.Combining_URL_Protocol_and_URL_Path(URL_Protocol = URL_Protocol, URL_Path = URL_Path)

# EOF Signed by GF.

