# GF_PY3_CLASS/Python3_Database/PY3_MySQL8_By_SQLAlchemy2.py
# Create by GF 2025-04-02 23:42

import pandas
import sqlalchemy

# ##################################################

class PY3_MySQL8_By_SQLAlchemy2(object):

    # Example for "Python 3 + SQLAlchemy 2 -> PostgreSQL 9":
    # >>> OBJ_PY3_MySQL8_By_SQLAlchemy2 = PY3_MySQL8_By_SQLAlchemy2()
    # >>> OBJ_PY3_MySQL8_By_SQLAlchemy2.DB_HOST = "127.0.0.1"
    # >>> OBJ_PY3_MySQL8_By_SQLAlchemy2.DB_NAME = "example_database"
    # >>> OBJ_PY3_MySQL8_By_SQLAlchemy2.DB_USER = "root"
    # >>> OBJ_PY3_MySQL8_By_SQLAlchemy2.DB_PASSWORD = "12345678"
    # >>> Result = OBJ_PY3_MySQL8_By_SQLAlchemy2.Query("SELECT * FROM example;")
    # >>> print(Result)
    #     id      date   open   high    low  close   volume
    #  0   1  20240731  21.52  21.80  21.40  21.52  1065652
    #  1   2  20240731  21.62  21.92  21.80  21.90  1032323
    # 70  70  20240731  24.30  24.45  24.00  24.20  2050554

    def __init__(self):

        self.DB_HOST     = "127.0.0.1"
        self.DB_NAME     = "unknow_database"
        self.DB_USER     = "unknow_user"
        self.DB_PASSWORD = "unknow_password"

    def Query(self, SQL_Statment:str):

        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:3306/{self.DB_NAME}")
        # ..........................................
        Result = pandas.read_sql_query(SQL_Statment, con = engine)
        # ..........................................
        return Result

    def APPEND_Xlsx(self, Xlsx_Path:str, Sheet_Name:str, DB_TABLE:str) -> int:

        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:3306/{self.DB_NAME}")
        # ..........................................
        DataFrame = pandas.read_excel(Xlsx_Path, sheet_name = Sheet_Name)
        # ..........................................
        Affected_Rows = DataFrame.to_sql(DB_TABLE, con = engine, index = False, if_exists = 'append', method = 'multi')
        # ..........................................
        return Affected_Rows

    def APPEND_DataFrame(self, DataFrame, DB_TABLE:str) -> int:

        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:3306/{self.DB_NAME}")
        # ..........................................
        # pandas.DataFrame.to_sql(name:str, con:object, index = False, if_exists = "append", method:str)
        # 参数说明 (Params):
        # - method = None: 使用标准的 SQL INSERT 语句 (每行一个)。
        # - method = "multi": 在一个 INSERT 语句中传递多个值。
        # 返回值 (Return Value):
        # - int: Number of Affected Rows (method = None / method = "multi").
        # 其它说明 (Other):
        # - If Pandas DataFrame is Empty in (if_exists="append") Mode, return 0.
        Affected_Rows = DataFrame.to_sql(DB_TABLE, con = engine, index = False, if_exists = 'append', method = 'multi')
        # ..........................................
        return Affected_Rows

# EOF Signed by GF.
