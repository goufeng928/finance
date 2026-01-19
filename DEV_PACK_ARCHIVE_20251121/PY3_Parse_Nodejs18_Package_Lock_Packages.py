# PY3_Parse_Nodejs18_Package_Lock_Packages.py
# Create by GF 2025-12-28 20:45

import json
import re

# ##################################################

class PY3_Parse_Nodejs18_Package_Lock_Packages(object):

    def Read_Package_Lock_as_Text(self, Path:str) -> str:
        
        # 输出示例:
        # {
        #   "name": "@nocobase/plugin-external-datasource-mssql",
        #   "version": "0.1.0",
        #   "lockfileVersion": 3,
        #   "requires": true,
        #   "packages": {
        #     "": {
        #       "name": "@nocobase/plugin-external-datasource-mssql",
        #       "version": "0.1.0",
        #       "license": "MIT",
        #       "dependencies": {
        #         "mssql": "^10.0.1",
        #         "tedious": "^16.6.1"
        #       },
        #       ......
        #     },
        #     "node_modules/@adobe/css-tools": {
        #       "version": "4.4.4",
        #       "resolved": "https://registry.npm.taobao.org/@adobe/css-tools/-/css-tools-4.4.4.tgz",
        #       "integrity": "sha512-Elp+iwUx5rN5+Y8xLt5/GRoG20WGoDCQ/1Fb+1LiGtvwbDavuSk0jhD/eZdckHAuzcDzccnkv+rEjyWfRx18gg==",
        #       "dev": true,
        #       "license": "MIT",
        #       "peer": true
        #     },
        #     ......
        #   }
        # }
        
        Opened_File:object = open(Path, mode = "r")
        Readed_Text:str    = Opened_File.read()
        Opened_File.close()
        # ..........................................
        return Readed_Text

    def Read_Package_Lock_as_Dict(self, Path:str) -> dict:

        Readed_Text:str = self.Read_Package_Lock_as_Text(Path = Path)
        # ..........................................
        return json.loads(Readed_Text)

    def Find_All_Tgz(self, Path:str) -> list:

        # 输出示例:
        # ['https://registry.npm.taobao.org/@adobe/css-tools/-/css-tools-4.4.4.tgz',
        #  'https://registry.npm.taobao.org/@ahooksjs/use-url-state/-/use-url-state-3.5.1.tgz',
        #  'https://registry.npm.taobao.org/@ampproject/remapping/-/remapping-2.3.0.tgz',
        #  'https://registry.npm.taobao.org/@ant-design/colors/-/colors-7.2.1.tgz',
        #  'https://registry.npm.taobao.org/@ant-design/cssinjs/-/cssinjs-1.24.0.tgz',
        #  ......]

        Readed_Text:str = self.Read_Package_Lock_as_Text(Path = Path)
        # ..........................................
        All_Tgz_List:list = re.findall(r"http.*\.tgz", Readed_Text)
        # ..........................................
        return All_Tgz_List

# EOF Signed by GF.
