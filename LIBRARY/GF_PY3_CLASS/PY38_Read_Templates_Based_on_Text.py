# GF_PY3_CLASS/PY38_Read_Templates_Based_on_Text.py
# Create by GF 2025-04-02 23:42

class PY38_Read_Templates_Based_on_Text(object):

    def Read(self, Text_File_Path:str) -> str:

        Text_File     = open(Text_File_Path, mode = 'r')
        Text_Ctnt:str = Text_File.read()
        Text_File.close()
        # ..........................................
        return Text_Ctnt

# EOF Signed by GF.
