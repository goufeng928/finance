#! /usr/bin/env python3

# Create By GF 2023-09-12 13:34

# Library : PyMySQL 1.0.2
# Library : Pandas 1.4.1

import pymysql
import pandas as pd

class Fin_PyMySQL(object):

    def __init__(self):
    
        # 数据库相关。
        self.Host = "localhost"
        self.User = "root"
        self.Password = "12345678"
        self.Database = "gf_finance"
        
    def Connect(self):
    
        # 创建 MySQL 数据库连接。
        Connection = pymysql.connect(host=self.Host,         # -> 主机名 / IP地址 (本地连接使用 localhost 或者 127.0.0.1)。
                                     user=self.User,         # -> MySQL 数据库用户名。
                                     port=3306,              # -> MySQL 数据库端口 (默认为3306)。
                                     password=self.Password, # -> MySQL 数据库用户密码。
                                     database=self.Database, # -> (可选项) 要使用的数据库。
                                     charset='utf8mb4',      # -> (可选项) 要使用的字符集。
                                     cursorclass=pymysql.cursors.DictCursor) # -> (可选项) 游标类型。
        
        return Connection

    def Query(self,SQL_String:str):
    
        Connection = self.Connect()
    
        # 从创建的 MySQL 数据库连接使用 .cursor() 方法获取游标并保存到 cursor 变量。
        cursor = Connection.cursor()
        
        cursor.execute(SQL_String)
        
        # 以列表形式返回所有查询数据，查询数据以字典形式呈现。
        data = cursor.fetchall()
        
        # 返回字段 (列名)。
        headers = [h[0] for h in cursor.description]
    
        # 将查询到的结果保存在 Pandas 的 DataFrame 中。
        df = pd.DataFrame(list(data), columns=headers)
        
        # 关闭连接。
        Connection.close()
        
        return df

# --------------------------------------------------
# EOF
