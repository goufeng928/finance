# GF_PY3_CLASS/Python3_Database/PY3_SQLite3_Based_on_SQLAlchemy2.py
# Create by GF 2025-04-02 23:42

# 能力补充库 (Ability Supplementary Library)
import sqlite3
# ..................................................
import pandas
import sqlalchemy

# ##################################################

class PY3_SQLite3_Based_on_SQLAlchemy2:

    # Example for "Python 3 + SQLAlchemy 2 -> SQLite 3":
    # >>> SQLITE = PY3_SQLite3_Based_on_SQLAlchemy2()
    # >>> SQLITE.DB_PATH = "C:\\EXAMPLE.db"
    # >>> Result = SQLITE.Query("SELECT * FROM example;")
    # >>> print(Result)
    #     id      date   open   high    low  close   volume
    #  0   1  20240731  21.52  21.80  21.40  21.52  1065652
    #  1   2  20240731  21.62  21.92  21.80  21.90  1032323
    # 70  70  20240731  24.30  24.45  24.00  24.20  2050554

    def __init__(self):

        # SQLite 3 DataBase Path:
        # - Linux Format: /data/EXAMPLE.db
        # - Windows Format: C:\EXAMPLE.db
        self.DB_PATH = "/data/EXAMPLE.db"

    def Query(self, SQL_Statment:str):

        # SQLite 3 in SQLalchemy URI be Similar to: "sqlite:///C:\\EXAMPLE.db"
        engine = sqlalchemy.create_engine(f"sqlite:///{self.DB_PATH}")
        # ..........................................
        Result = pandas.read_sql_query(SQL_Statment, con = engine)
        # ..........................................
        return Result

    def APPEND_DataFrame(self, DataFrame, dbTable:str) -> int:

        engine = sqlalchemy.create_engine(f"sqlite:///{self.DB_PATH}")
        # ..........................................
        Affected_Rows = DataFrame.to_sql(dbTable, con = engine, index = False, if_exists = 'append')
        # ..........................................
        return Affected_Rows

    def APPEND_Xlsx(self, Xlsx_Path:str, Sheet_Name:str, dbTable:str) -> int:

        engine = sqlalchemy.create_engine(f"sqlite:///{self.DB_PATH}")
        # ..........................................
        DataFrame = pandas.read_excel(Xlsx_Path, sheet_name = Sheet_Name)
        # ..........................................
        Affected_Rows = DataFrame.to_sql(dbTable, con = engine, index = False, if_exists = 'append')
        # ..........................................
        return Affected_Rows

    def TRUNCATE_TABLE(self, dbTable:str) -> int:

        # 能力补充函数 (Ability Supplement Function)

        # 连接到 SQLite 3 数据库 (如果文件不存在, 会自动创建)
        connection = sqlite3.connect(self.DB_PATH)
        # ..........................................
        # 创建一个 Cursor 对象并调用其 execute() 方法执行 SQL 命令
        cursor = connection.cursor()
        # ..........................................
        # Sqlite 3.5x.x 不支持 TRUNCATE TABLE 语句
        cursor.execute(f"DELETE FROM {dbTable};")
        # ..........................................
        # 提交事务
        connection.commit()
        # ..........................................
        # 关闭 Cursor 和 Connection
        cursor.close()
        connection.close()
        # ..........................................
        return 1

# EOF Signed by GF.
