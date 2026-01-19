# GF_PY3_CLASS/Python3_Database/PY3_MySQL8_Based_on_PyMySQL.py
# Create by GF 2025-04-02 23:42

import pymysql

# ##################################################

class PY3_MySQL8_Based_on_PyMySQL(object):

    # Example:
    # >>> MYSQL = PY3_MySQL8_Based_on_PyMySQL()
    # >>> MYSQL.Pub_DB_Host     = "127.0.0.1"
    # >>> MYSQL.Pub_DB_Database = "example_database"
    # >>> MYSQL.Pub_DB_User     = "root"
    # >>> MYSQL.Pub_DB_Password = "12345678"
    # >>> Result = MYSQL.Query("SELECT * FROM example;")
    # >>> print(Result)
    # [{"id": 1, "date": "20240731", "open": 21.52, "high": 21.80, "low": 21.40, "close": 21.52, "volume": 1065652},
    #  {"id": 2, "date": "20240731", "open": 21.62, "high": 21.92, "low": 21.80, "close": 21.90, "volume": 1032323},
    #  {"id": 3, "date": "20240731", "open": 24.30, "high": 24.45, "low": 24.00, "close": 24.20, "volume": 2050554}]

    def __init__(self):

        self.Pub_DB_Host     = "127.0.0.1"
        self.Pub_DB_Port     = 3306
        self.Pub_DB_Database = "unknow_database"
        self.Pub_DB_User     = "unknow_user"
        self.Pub_DB_Password = "unknow_password"
        # ..........................................
        self.Pub_Fields_List_MinIdx:int = 0
        # ..........................................
        self.Pub_JSON_Records:list       = []
        self.Pub_JSON_Records_Length:int = len(self.Pub_JSON_Records)
        self.Pub_JSON_Records_MinIdx:int = 0
        self.Pub_JSON_Records_MaxIdx:int = self.Pub_JSON_Records_Length - 1

    def Init_Connection(self, Cursor_Class:object = pymysql.cursors.Cursor) -> object:

        # pymysql.connect( ... ) 中 cursorclass 参数说明:
        # - pymysql.cursors.Cursor     # 使查询结果以字典形式返回
        # - pymysql.cursors.DictCursor # 使查询结果以字典形式返回
        # ..........................................
        conn = pymysql.connect(host        = self.Pub_DB_Host,       # 主机地址
                               user        = self.Pub_DB_User,       # 用户名
                               password    = self.Pub_DB_Password,   # 密码
                               database    = self.Pub_DB_Database,   # 数据库名
                               port        = int(self.Pub_DB_Port),  # 端口 (默认 3306)
                               charset     = "utf8mb4",              # 字符编码
                               cursorclass = Cursor_Class)
        # ..........................................
        return conn

    def Execute(self, SQL_Statement:str, Params:tuple = None) -> int:

        conn = self.Init_Connection()
        # ..........................................
        cursor = conn.cursor()
        cursor.execute(SQL_Statement, args = Params)
        conn.commit()  # 提交事务
        # ..........................................
        # 获取 INSERT / UPDATE / DELETE 操作后受影响的行数
        Affected_Rows_Number = cursor.rowcount
        # ..........................................
        cursor.close()
        conn.close()
        # ..........................................
        return Affected_Rows_Number

    def Query(self, SQL_Statement:str, Params:tuple = None) -> list:

        conn = self.Init_Connection(Cursor_Class = pymysql.cursors.DictCursor)
        # ..........................................
        cursor = conn.cursor()
        cursor.execute(SQL_Statement, args = Params)
        result = cursor.fetchall()
        # ..........................................
        cursor.close()
        conn.close()
        # ..........................................
        return result

    def INSERT_BY_JSON_Record(self, JSON_Record:dict, DB_Table:str) -> int:

        conn = self.Init_Connection()
        # ..........................................
        # PyMySQL 1.1.2 构造参数化 "插入 (INSERT)" 语句
        # >>> import pymysql
        # >>> conn = pymysql.connect(host     = "127.0.0.1",
        # ...                        port     = 3306
        # ...                        database = "testing",
        # ...                        user     = "writer",
        # ...                        password = "123456",
        # ...                        charset  = "utf8mb4")
        # >>> cursor = conn.cursor()
        # >>>
        # >>> # 构造基本参数化 "插入 (INSERT)" 语句 (使用 %s 占位符, 推荐):
        # >>> values = ('John', 'Doe', 30)
        # >>> sql = "INSERT INTO users (first_name, last_name, age) VALUES (%s, %s, %s);"
        # >>> cursor.execute(sql, values)
        # >>> conn.commit()
        # >>>
        # >>> # 使用 pymysql.connect( ... ).cursor().executemany() 批量 INSERT
        # >>> values = [
        # ...     ('Alice',   'Smith',   25),
        # ...     ('Bob',     'Johnson', 35),
        # ...     ('Charlie', 'Brown',   28)
        # ... ]
        # >>> sql = "INSERT INTO users (first_name, last_name, age) VALUES (%s, %s, %s);"
        # >>> cursor.executemany(sql, values)
        # >>> conn.commit()
        # >>>
        # >>> # 构造字典参数化 "插入 (INSERT)" 语句 (使用 %(field_name)s 占位符, 按名称):
        # >>> values = {
        # ...     'first_name': 'Jane',
        # ...     'last_name': 'Doe',
        # ...     'age': 32
        # ... }
        # >>> sql = "INSERT INTO users (first_name, last_name, age) VALUES (%(first_name)s, %(last_name)s, %(age)s);"
        # >>> cursor.execute(sql, values)
        # >>> conn.commit()
        # ..........................................
        SQL_Statement_Part_A:str = "INSERT INTO %s (" % DB_Table
        SQL_Statement_Part_B:str = ") VALUES ("
        # ..........................................
        Fields_List:list       = list(JSON_Record.keys())
        Fields_List_MinIdx:int = self.Pub_Fields_List_MinIdx
        Fields_List_MaxIdx:int = len(Fields_List) - 1
        # ..........................................
        i:int = Fields_List_MinIdx
        while (i <= Fields_List_MaxIdx):
            if (i == 0):
                SQL_Statement_Part_A = "%s%s" % (SQL_Statement_Part_A, Fields_List[i])
                SQL_Statement_Part_B = "%s%s" % (SQL_Statement_Part_B, "%s")
            if (i >= 1):
                SQL_Statement_Part_A = "%s,%s" % (SQL_Statement_Part_A, Fields_List[i])
                SQL_Statement_Part_B = "%s,%s" % (SQL_Statement_Part_B, "%s")
            i = i + 1
        # ..........................................
        SQL_Statement:str = "%s%s);" % (SQL_Statement_Part_A, SQL_Statement_Part_B)
        # ..........................................
        cursor = conn.cursor()
        cursor.execute(SQL_Statement, tuple(JSON_Record.values()))
        conn.commit()  # 提交事务
        # ..........................................
        # 获取 INSERT / UPDATE / DELETE 操作后受影响的行数
        Affected_Rows_Number = cursor.rowcount
        # ..........................................
        cursor.close()
        conn.close()
        # ..........................................
        return Affected_Rows_Number

    def BATCH_INSERT_BY_JSON_Records(self, JSON_Records:list, DB_Table:str) -> int:

        JSON_Records_Length = len(JSON_Records)
        JSON_Records_MaxIdx = JSON_Records_Length - 1
        # ..........................................
        Affected_Rows_Number_Total:int = 0
        # ..........................................
        i:int = self.Pub_JSON_Records_MinIdx
        while (i <= JSON_Records_MaxIdx):
            Affected_Rows_Number       = self.INSERT_BY_JSON_Record(JSON_Record = JSON_Records[i], DB_Table = DB_Table)
            Affected_Rows_Number_Total = Affected_Rows_Number_Total + Affected_Rows_Number
            i = i + 1
        # ..........................................
        return Affected_Rows_Number_Total

# EOF Signed by GF.
