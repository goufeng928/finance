# PY3_Debian12_Parse_deb_Mirrors_Packages.py
# Create by GF 2025-05-19 20:45

import gzip
import re

# ##################################################

class PY3_Debian12_Parse_deb_Mirrors_Packages(object):

    # Example:
    # >>> Parse_Mirrors_Packages = PY3_Debian12_Parse_deb_Mirrors_Packages()
    # >>> Packages_Path = "./Packages.gz"                                          # 1. Locate the position of "Packages.gz".
    # >>> Packages_Text = Parse_Mirrors_Packages.Read_Packages(Packages_Path)      # 2. Read "Packages.gz" content as a text string.
    # >>> Packages_Filename = Parse_Mirrors_Packages.Find_Filename(Packages_Path)  # 3. Find all "Filename" in the "Packages.gz" content.
    # >>> print(Packages_Filename)
    # ['Filename: pool/contrib/1/1oom/1oom_1.0-2_amd64.deb',
    #  'Filename: pool/contrib/a/alien-arena/alien-arena_7.71.3+dfsg-3_amd64.deb',
    #  'Filename: pool/contrib/a/alien-arena/alien-arena-server_7.71.3+dfsg-3_amd64.deb',
    #  ......
    #  'Filename: pool/contrib/z/zmat/matlab-zmat_0.9.8+ds-8_all.deb',
    #  'Filename: pool/contrib/z/zsnapd/zsnapd_0.8.12-1_all.deb',
    #  'Filename: pool/contrib/z/zsnapd/zsnapd-rcmd_0.8.12-1_all.deb']

    def Read_Packages(self, Path:str = "Packages.gz", Output_Format:str = "text"):
        
        GZip_File:object   = gzip.open(Path, mode = "rb")
        Readed_Bytes:bytes = GZip_File.read()
        GZip_File.close()
        # ------------------------------------------
        Readed:object = None
        # ------------------------------------------
        if (Output_Format == "text"):
            # Output Content Example:
            # ......
            # Section: contrib/games
            # Priority: optional
            # Filename: pool/contrib/1/1oom/1oom_1.0-2_amd64.deb
            # Size: 506180
            # MD5sum: d6ddb9189f14e76d7336246104cd0d2c
            # ......
            Readed_Text:str = Readed_Bytes.decode("utf-8")
            Readed          = Readed_Text
        # ------------------------------------------
        return Readed
    
    def Find_Filename(self, Path:str = "Packages.gz") -> list:

        Packages_Text:str = self.Read_Packages(Path = Path, Output_Format = "text")
        # ------------------------------------------
        # ......
        # Section: contrib/games
        # Priority: optional
        # Filename: pool/contrib/1/1oom/1oom_1.0-2_amd64.deb  # <- Match Target
        # Size: 506180
        # MD5sum: d6ddb9189f14e76d7336246104cd0d2c
        # ......
        Matched_List:list = re.findall("Filename.*", Packages_Text)
        # ------------------------------------------
        return Matched_List
