# GF_PY3_CLASS/Python3_Database/PY3_PostgreSQL9_Based_on_SQLAlchemy2.py
# Create by GF 2025-04-02 23:42

import pandas
import sqlalchemy

# ##################################################

class PY3_Integer_Primary_Key():

    def __init__(self, Start:int = 1):

        self.Current:int = Start

    def Auto_Increment(self) -> int:

        Copy:int = self.Current
        # ..........................................
        self.Current = self.Current + 1
        # ..........................................
        return Copy

class PY3_PostgreSQL9_Based_on_SQLAlchemy2(object):

    # Examples:
    # >>> PGSQL = PY3_PostgreSQL9_Based_on_SQLAlchemy2()
    # >>> PGSQL.Pub_DB_Host     = "127.0.0.1"
    # >>> PGSQL.Pub_DB_Database = "postgres"
    # >>> PGSQL.Pub_DB_User     = "postgres"
    # >>> PGSQL.Pub_DB_Password = "12345678"
    # >>> Queried = PGSQL.Query("SELECT * FROM example;")
    # >>> print(Queried)
    #     id      date   open   high    low  close   volume
    #  0   1  20240731  21.52  21.80  21.40  21.52  1065652
    #  1   2  20240731  21.62  21.92  21.80  21.90  1032323
    # 70  70  20240731  24.30  24.45  24.00  24.20  2050554

    def __init__(self):

        self.Pub_DB_Host     = "127.0.0.1"
        self.Pub_DB_Database = "unknow_database"
        self.Pub_DB_User     = "unknow_user"
        self.Pub_DB_Password = "unknow_password"

    def Create_Engine(self) -> object:

        DB_Host     = self.Pub_DB_Host
        DB_Database = self.Pub_DB_Database
        DB_User     = self.Pub_DB_User
        DB_Password = self.Pub_DB_Password
        # ..........................................
        Engine = sqlalchemy.create_engine(f"postgresql://{DB_User}:{DB_Password}@{DB_Host}:5432/{DB_Database}")
        # ..........................................
        return Engine

    def Query(self, SQL_Statement:str):

        Engine = self.Create_Engine()
        # ..........................................
        Queried_DataFrame = pandas.read_sql_query(SQL_Statement, con = Engine)
        # ..........................................
        return Queried_DataFrame

    def TRUNCATE_TABLE(self, DB_Table:str, Primary_Key:str = "<none>") -> bool:

        Engine = self.Create_Engine()
        # ..........................................
        # 使用 sqlalchemy.create_engine( ... ).connect() 的 execute 方法执行原生 SQL 语句
        connection = Engine.connect()
        # 在 PostgreSQL 9 中执行 DELETE 语句清空表:
        # 语句 (1) 无返回值: DELETE FROM users;
        #     SQLALchemy 2.0.x 中的执行返回结果 (错误提示):
        #         ResourceClosedError: This result object does not return rows. It has been closed automatically.
        #     PostgreSQL 9 命令行客户端 (Cli) 中的执行返回结果 (Query Message):
        #         DELETE 2
        # 语句 (2) 有返回值: DELETE FROM users RETURNING *;
        #     SQLALchemy 2.0.x 中的执行返回结果 (可迭代对象):
        #         可迭代对象 <sqlalchemy.engine.cursor.CursorResult at 0x191f3b9e030> 中包含:
        #             (1, "Jack", 22, "jack@email.com")
        #             (2, "Annie", 21, "annie@email.com")
        #     PostgreSQL 9 命令行客户端 (Cli) 中的执行返回结果 (已删除的数据):
        #          id | name  | age | email
        #         ----+-------+-----+----------------
        #          1  | Jack  | 22  | jack@email.com
        #          2  | Annie | 21  | annie@email.com
        #         (2 行记录)
        #
        #         DELETE 2
        connection.execute(sqlalchemy.text("DELETE FROM %s RETURNING *;" % DB_Table))
        connection.commit()
        # ..........................................
        if (Primary_Key != "<none>"):
            connection.execute(sqlalchemy.text(("SELECT setval('%s_%s_seq', 1, false);" % (DB_Table, Primary_Key))))
        # ..........................................
        connection.close()
        # ..........................................
        return True

    def APPEND_BY_Xlsx(self, Xlsx_Path:str, Sheet_Name:str, DB_Table:str) -> int:

        Engine = self.Create_Engine()
        # ..........................................
        df = pandas.read_excel(Xlsx_Path, sheet_name = Sheet_Name)
        # ..........................................
        Affected_Rows_Number = df.to_sql(DB_Table, con = Engine, index = False, if_exists = 'append', method = 'multi')
        # ..........................................
        return Affected_Rows_Number

    def APPEND_BY_Pandas_DataFrame(self, Pandas_DataFrame, DB_Table:str, Primary_Key:str = "<none>") -> int:

        df = Pandas_DataFrame.copy()

        if (Primary_Key != "<none>"):
            # 查询 <DB_Table> 中 PRIMARY KEY 的最大值
            SQL_Condition:str = "CASE WHEN MAX(%s) IS NULL THEN 0 ELSE MAX(%s) END" % (Primary_Key, Primary_Key)
            SQL_Statement:str = "SELECT %s AS %s_max FROM %s;" % (SQL_Condition, Primary_Key, DB_Table)
            # ......................................
            Queried_DataFrame = self.Query(SQL_Statement)
            Primary_Key_Max = Queried_DataFrame[("%s_max" % Primary_Key)].values[0]
            # ......................................
            # 在 Pandas DataFrame 中生成 PRIMARY KEY
            Primary_Key_Gen = PY3_Integer_Primary_Key(Start = Primary_Key_Max + 1)
            df[Primary_Key] = 0  # 创建字段 (Field) 并使用 0 初始化字段 (Field) 值
            df[Primary_Key] = df[Primary_Key].apply(lambda x: Primary_Key_Gen.Auto_Increment())

        Engine = self.Create_Engine()
        # ..........................................
        # pandas.DataFrame.to_sql(name:str, con:object, index = False, if_exists = "append", method:str)
        # 参数说明 (Params):
        # - method = None: 使用标准的 SQL INSERT 语句 (每行一个)。
        # - method = "multi": 在一个 INSERT 语句中传递多个值。
        # 返回值 (Return Value):
        # - int: Number of Affected Rows (method = None / method = "multi").
        # 其它说明 (Other):
        # - If Pandas DataFrame is Empty in (if_exists="append") Mode, return 0.
        Affected_Rows_Number = df.to_sql(DB_Table, con = Engine, index = False, if_exists = 'append', method = 'multi')
        # ..........................................
        return Affected_Rows_Number

# EOF Signed by GF.
