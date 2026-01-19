# GF_PY3_CLASS/Python3_Path/PY3_Path_for_Operate_System.py
# Create by GF 2025-09-08 12:53

import os

# ##################################################

class PY3_Path_for_Operate_System(object):

    # Cautions:
    # (1) 在 Windows 系统 + Python 3.12.0 中, os.listdir("D:") 返回的是当前工作目录在 D 盘下的内容, 而不是 D 盘根目录的内容。
    #     os.listdir("D:") 返回的是 D 盘当前工作目录的内容
    #     os.listdir("D:\\") 或 os.listdir("D:/") 才会返回 D 盘根目录的内容

    # Examples for Get Partition:
    # >>> POS = PY3_Path_for_Operate_System()
    # >>>
    # >>> Result = POS.Get_Partition(Path = "C:", Separator = '\\')
    # >>> print(Result)
    # C:\\
    # >>> Result = POS.Get_Partition(Path = "C:\\Windows\\System32", Separator = '\\')
    # >>> print(Result)
    # C:\\
    # >>> Result = POS.Get_Partition(Path = "/home", Separator = '/')
    # >>> print(Result)
    # /home/
    # >>> Result = POS.Get_Partition(Path = "/home/goufeng/.cshrc", Separator = '/')
    # >>> print(Result)
    # /home/

    # Examples for Get Directory:
    # >>> POS = PY3_Path_for_Operate_System()
    # >>>
    # >>> Result = POS.Get_Directory(Path = "C:", Separator = '\\')
    # >>> print(Result)
    # <Empty Character>
    # >>> Result = POS.Get_Directory(Path = "C:\\Windows\\System32", Separator = '\\')
    # >>> print(Result)
    # Windows\\System32
    # >>> Result = POS.Get_Directory(Path = "/home", Separator = '/')
    # >>> print(Result)
    # <Empty Character>
    # >>> Result = POS.Get_Directory(Path = "/home/goufeng/.cshrc", Separator = '/')
    # >>> print(Result)
    # goufeng/.cshrc

    # Examples for Combining Partition and Directory:
    # >>> POS = PY3_Path_for_Operate_System()
    # >>>
    # >>> Result = POS.Combining_Partition_and_Directory(Partition = "C:", Directory = "\\Program Files", Separator = '\\')
    # >>> print(Result)
    # C:\\Program Files
    # >>> Result = POS.Combining_Partition_and_Directory(Partition = "C:", Directory = "Program Files", Separator = '\\')
    # >>> print(Result)
    # C:\\Program Files
    # >>> Result = POS.Combining_Partition_and_Directory(Partition = "home", Directory = "/goufeng", Separator = '/')
    # >>> print(Result)
    # /home/goufeng
    # >>> Result = POS.Combining_Partition_and_Directory(Partition = "home", Directory = "goufeng", Separator = '/')
    # >>> print(Result)
    # /home/goufeng

    # Examples for Backward:
    # >>> POS = PY3_Path_for_Operate_System()
    # >>>
    # >>> Result = POS.Backward(Path = "C:\\Windows", Separator = '\\')
    # >>> print(Result)
    # C:\\
    # >>> Result = POS.Backward(Path = "C:\\Windows\\System32", Separator = '\\')
    # >>> print(Result)
    # C:\\Windows
    # >>> Result = POS.Backward(Path = "/home/goufeng", Separator = '/')
    # >>> print(Result)
    # /home/
    # >>> Result = POS.Backward(Path = "/home/goufeng/.cshrc", Separator = '/')
    # >>> print(Result)
    # /home/goufeng

    def Get_Partition(self, Path:str, Separator:str = os.sep) -> str:

        POS_Transform:str = Path
        # ..........................................
        if (POS_Transform[0] == '/'):
            # Purpose for Linux: "/home/username/.cshrc" => "home/username/.cshrc"
            POS_Transform = POS_Transform[1:len(POS_Transform)]
        # ..........................................
        POS_Split:list = POS_Transform.split(Separator)
        # ..........................................
        if (Path[0] == '/'):
            return Separator + POS_Split[0] + Separator
        # ..........................................
        if (Path[0] != '/' and ':' in POS_Split[0]):
            return POS_Split[0] + Separator

    def Get_Directory(self, Path:str, Separator:str = os.sep) -> str:

        POS_Transform:str = Path
        # ..........................................
        if (POS_Transform[0] == '/'):
            # Purpose for Linux: "/home/username/.cshrc" => "home/username/.cshrc"
            POS_Transform = POS_Transform[1:len(POS_Transform)]
        # ..........................................
        POS_Directory:str = Path
        # ..........................................
        POS_Part:str   = self.Get_Partition(Path = Path, Separator = Separator)
        POS_Part       = POS_Part.lstrip(Separator)
        POS_Part       = POS_Part.rstrip(Separator)
        POS_Split:list = POS_Transform.split(Separator)
        # ..........................................
        if (len(POS_Split) == 1 and POS_Split[0] == POS_Part):
            # Purpose for Windows: "C:" => str('')
            # Purpose for Linux: "/home" => str('')
            POS_Directory = str('')
        if (len(POS_Split) >= 2 and POS_Split[0] == POS_Part):
            # Purpose for Windows: "C:\\Windows\\System32" => "Windows\\System32"
            # Purpose for Linux: "/home/goufeng/.cshrc" => "goufeng/.cshrc"
            POS_Directory = Separator.join(POS_Split[1:len(POS_Split)])
        # ..........................................
        return POS_Directory

    def Combining_Partition_and_Directory(self, Partition:str, Directory:str, Separator:str = os.sep) -> str:

        Partition_Transform:str = Partition
        Directory_Transform:str = Directory
        Directory_Transform     = Directory.lstrip(Separator)
        Directory_Transform     = Directory.rstrip(Separator)
        # ..........................................
        return Partition_Transform + Directory_Transform

    def Backward(self, Path:str, Separator:str = os.sep) -> str:

        Partition:str = self.Get_Partition(Path = Path, Separator = Separator)
        Directory:str = self.Get_Directory(Path = Path, Separator = Separator)
        # ..........................................
        if (Directory == str('')):
            return Path
        # ..........................................
        if (Directory != str('')):
            if (Directory[0] == Separator):
                # Purpose for Windows: "\\Windows\\System32" => "Windows\\System32"
                # Purpose for Linux: "/goufeng/.cshrc" => "goufeng/.cshrc"
                Directory = Directory[1:len(Directory)]
            # ......................................
            Directory_Split:list = Directory.split(Separator)
            Directory_Split      = Directory_Split[0:len(Directory_Split) - 1]
            Directory            = Separator.join(Directory_Split)
            # ......................................
            return self.Combining_Partition_and_Directory(Partition = Partition, Directory = Directory, Separator = Separator)

# Signed by GF.
