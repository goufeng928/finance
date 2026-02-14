# GF_PY3_CLASS/Python3_Database/PY3_MySQL8_Based_on_SQLAlchemy2.py
# Create by GF 2025-04-02 23:42

import pandas      # Pandas 2.0.3
import sqlalchemy  # SQLAlchemy 2.0.49

# ##################################################

class PY3_MySQL8_Based_on_SQLAlchemy2(object):

    # Examples:
    # >>> MYSQL = PY3_MySQL8_Based_on_SQLAlchemy2()
    # >>> MYSQL.Pub_DB_Host     = "127.0.0.1"
    # >>> MYSQL.Pub_DB_Database = "example_database"
    # >>> MYSQL.Pub_DB_User     = "root"
    # >>> MYSQL.Pub_DB_Password = "12345678"
    # >>> result = MYSQL.Query("SELECT * FROM example;")
    # >>> print(result)
    #     id      date   open   high    low  close   volume
    #  0   1  20240731  21.52  21.80  21.40  21.52  1065652
    #  1   2  20240731  21.62  21.92  21.80  21.90  1032323
    # 70  70  20240731  24.30  24.45  24.00  24.20  2050554

    def __init__(self):

        self.Pub_DB_Host:str     = "127.0.0.1"
        self.Pub_DB_Port:str     = "3306"
        self.Pub_DB_Database:str = "unknow_database"
        self.Pub_DB_User:str     = "unknow_user"
        self.Pub_DB_Password:str = "unknow_password"

    def Execute(self, statment:str, params = None) -> int:

        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.Pub_DB_User}:{self.Pub_DB_Password}@{self.Pub_DB_Host}:{self.Pub_DB_Port}/{self.Pub_DB_Database}")
        # ..........................................
        conn = engine.connect()
        conn.execute(statement = sqlalchemy.text(statment), parameters = params)
        conn.commit()
        conn.close()
        # ..........................................
        return 1

    def Query(self, statment:str, dtype = None):

        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.Pub_DB_User}:{self.Pub_DB_Password}@{self.Pub_DB_Host}:{self.Pub_DB_Port}/{self.Pub_DB_Database}")
        # ..........................................
        result = pandas.read_sql_query(statment, con = engine, dtype = dtype)
        # ..........................................
        return result

    def APPEND_BY_xlsx(self, xlsx_Path:str, sheet_name, dbTable:str) -> int:

        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.Pub_DB_User}:{self.Pub_DB_Password}@{self.Pub_DB_Host}:{self.Pub_DB_Port}/{self.Pub_DB_Database}")
        # ..........................................
        DataFrame = pandas.read_excel(xlsx_Path, sheet_name = sheet_name)
        # ..........................................
        Affected_Rows = DataFrame.to_sql(dbTable, con = engine, index = False, if_exists = "append", method = "multi")
        # ..........................................
        return Affected_Rows

    def APPEND_BY_DataFrame(self, DataFrame, dbTable:str) -> int:

        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.Pub_DB_User}:{self.Pub_DB_Password}@{self.Pub_DB_Host}:{self.Pub_DB_Port}/{self.Pub_DB_Database}")
        # ..........................................
        # pandas.DataFrame( ... ).to_sql(name:str, con:object, index = False, if_exists = "append", method:str)
        # - 参数说明 (Params):
        #   method = None: 使用标准的 SQL INSERT 语句 (每行一个)。
        #   method = "multi": 在一个 INSERT 语句中传递多个值。
        # - 返回值 (Return Value):
        #   int: Number of Affected Rows (method = None / method = "multi").
        # - 其它说明 (Other):
        #   If Pandas DataFrame is Empty in (if_exists="append") Mode, return 0.
        Affected_Rows = DataFrame.to_sql(dbTable, con = engine, index = False, if_exists = "append", method = "multi")
        # ..........................................
        return Affected_Rows

# EOF Signed by GF.
