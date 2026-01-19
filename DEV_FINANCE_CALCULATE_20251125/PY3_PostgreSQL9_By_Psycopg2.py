# GF_PY3_CLASS/Python3_Database/PY3_PostgreSQL9_By_Psycopg2.py
# Create by GF 2025-04-02 23:42

import numpy
import pandas
import psycopg2  # Psycopg2 2.9.11
# ..................................................
from psycopg2.extras import RealDictCursor

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

class PY3_PostgreSQL9_By_Psycopg2_INSERT_ITERATOR(object):

    # Examples:
    # >>> import pandas
    # >>> JSON_Records = [{"id": 1, ..., "close": 21.52}, ..., {"id": 70, ..., "close": 24.20}]
    # >>> df = pandas.DataFrame(JSON_Records)
    # >>> print(df)
    #     id      date   open   high    low  close
    #  0   1  20240731  21.52  21.80  21.40  21.52
    #  1   2  20240731  21.62  21.92  21.80  21.90
    # 70  70  20240731  24.30  24.45  24.00  24.20
    # >>>
    # >>> PGSQL_INSERT_ITERATOR = PY3_PostgreSQL9_By_Psycopg2_INSERT_ITERATOR()
    # >>> PGSQL_INSERT_ITERATOR.Pub_DB_Host = "127.0.0.1"
    # >>> PGSQL_INSERT_ITERATOR.Pub_DB_Database = "postgres"
    # >>> PGSQL_INSERT_ITERATOR.Pub_DB_User = "postgres"
    # >>> PGSQL_INSERT_ITERATOR.Pub_DB_Password = "12345678"
    # >>> PGSQL_INSERT_ITERATOR.Fit_Pandas_DataFrame(Pandas_DataFrame = df, DB_Table = "stocks_data")
    # >>> while (PGSQL_INSERT_ITERATOR.Pub_Index_Mov <= PGSQL_INSERT_ITERATOR.Pub_Index_Max):
    # ...     PGSQL_INSERT_ITERATOR.Pub_Index_Mov + 1
    # ...     PGSQL_INSERT_ITERATOR.Next()
    # >>> print(PGSQL_INSERT_ITERATOR.Pub_DB_Connection_Commit_Count)
    # 3

    def __init__(self):

        self.Pub_DB_Host:str     = "127.0.0.1"
        self.Pub_DB_Database:str = "unknow_database"
        self.Pub_DB_User:str     = "unknow_user"
        self.Pub_DB_Password:str = "unknow_password"
        # ..........................................
        self.Pub_DB_Table:str    = "unknow_table"
        # ..........................................
        # DB Connection Surpported Types:
        # - psycopg2.extensions.connection
        self.Pub_DB_Connection:object           = None
        self.Pub_DB_Connection_Commit_Count:int = 0
        # ..........................................
        # MaxIdx <==> Max Index
        # MinIdx <==> Min Index
        self.Pub_JSON_Records:list       = []
        self.Pub_JSON_Records_Length:int = 0
        self.Pub_JSON_Records_MaxIdx:int = self.Pub_JSON_Records_Length - 1
        # ..........................................
        self.Pub_Index_Mov:int = 0
        self.Pub_Index_Min:int = 0
        self.Pub_Index_Max:int = self.Pub_JSON_Records_MaxIdx

    def Init_DB_Connection(self) -> object:

        conn = psycopg2.connect(host     = self.Pub_DB_Host,
                                database = self.Pub_DB_Database,
                                user     = self.Pub_DB_User,
                                password = self.Pub_DB_Password)
        # ..........................................
        return conn

    def SELECT_INTEGER_PRIMARY_KEY_MAX(self, DB_Table:str, Primary_Key:str) -> int:

        conn = self.Init_DB_Connection()
        # ..........................................
        # 查询 <DB_Table> 中 PRIMARY KEY 的最大值
        SQL_CONDITION:str = "CASE WHEN MAX(%s) IS NULL THEN 0 ELSE MAX(%s) END" % (Primary_Key, Primary_Key)
        SQL_STATEMENT:str = "SELECT %s AS %s_max FROM %s;" % (SQL_CONDITION, Primary_Key, DB_Table)
        # ..........................................
        cursor = conn.cursor(cursor_factory = psycopg2.extensions.cursor)
        cursor.execute(SQL_STATEMENT)
        rows = cursor.fetchall()
        # ..........................................
        Primary_Key_Max:int = rows[0][0]
        # ..........................................
        cursor.close()
        conn.close()
        # ..........................................
        return Primary_Key_Max

    def Fit_JSON_Records(self, JSON_Records:list, DB_Table:str, Primary_Key:str = "<none>") -> int:

        self.Pub_JSON_Records        = JSON_Records
        self.Pub_JSON_Records_Length = len(self.Pub_JSON_Records)
        self.Pub_JSON_Records_MaxIdx = self.Pub_JSON_Records_Length - 1
        # ..........................................
        self.Pub_Index_Mov = 0
        self.Pub_Index_Max = self.Pub_JSON_Records_Length - 1
        # ..........................................
        if (Primary_Key != "<none>"):
            Primary_Key_Max = self.SELECT_INTEGER_PRIMARY_KEY_MAX(DB_Table = DB_Table, Primary_Key = Primary_Key)
            Primary_Key_Gen = PY3_Integer_Primary_Key(Start = PRIMARY_KEY_Max + 1)
            i:int = 0
            while (i <= self.Pub_JSON_Records_MaxIdx):
                self.Pub_JSON_Records[i].update({Primary_Key: Primary_Key_Gen.Auto_Increment()})
                i = i + 1
        # ..........................................
        self.Pub_DB_Table      = DB_Table
        self.Pub_DB_Connection = self.Init_DB_Connection()
        # ..........................................
        return self.Pub_JSON_Records_Length

    def Fit_Pandas_DataFrame(self, Pandas_DataFrame, DB_Table:str, Primary_Key:str = "<none>") -> int:

        # 将 Pandas DataFrame 保存为 JSON Records 格式。
        df = Pandas_DataFrame.copy()
        # ..........................................
        # 将 Pandas DataFrame 中的空值 (NaN, NaT, ...) 替换为 Python 3 标准空值 None
        # 1. 使用 pandas.DataFrame( ... ).map 结合 pandas.isna() 和 pandas.isnull() 替换空值
        #     pandas.isnull(pandas.NaT) 函数可以检测缺失值 (包括 NaN, NaT, None 等),
        #     但是在 Pandas 中, NaN 表示浮点数类型的缺失值 (典型的如 numpy.nan, 它的类型为 numpy.float64(nan)),
        #     如果列的数据类型是数值型, 那么 None 会被自动转换为 NaN,
        #     如果列是 object 类型, 则 None 可能会被保留。
        #     所以: 使用 df = df.map(lambda x: None if (pandas.isnull(x) == True) else x) 转换空值可能并不彻底,
        #           特别是当列的数据类型是数值型时, NaN 可能在转换为 None 后又被自动转回 NaN, 或是保持 NaN。
        #     注意: pandas.isna() 和 pandas.isnull() 功能相同, 函数命名不同。
        #           pandas.isna() 遵循 "R 语言 / 数据库" 函数命名风格,
        #           pandas.isnull() 遵循 "NumPy" 函数命名风格。
        # 2. 使用 pandas.DataFrame( ... ).replace({numpy.nan: None, pandas.NaT: None}) 替换空值
        #     pandas.DataFrame( ... ).replace 会触发类型转换 (向量化操作, 一次性处理整个数组),
        #     pandas.DataFrame( ... ).map 不会触发类型转换 (逐元素操作),
        #     相当于 pandas.DataFrame( ... ).replace 创建了一个新数组, 改变了数据类型,
        #     可以将数值列从 float64 转换为 object 类型, 使得 Python 3 标准空值 None 可以存在,
        #     pandas.DataFrame( ... ).replace 可能使用更多内存, 因为 object 类型比 float64 占用更多空间。
        # ..........................................
        df = df.replace({numpy.nan: None, pandas.NA: None, pandas.NaT: None})
        # ..........................................
        JSON_Records        = df.to_dict(orient = "records")
        JSON_Records_Length = self.Fit_JSON_Records(JSON_Records = JSON_Records,
                                                    DB_Table     = DB_Table,
                                                    Primary_Key  = Primary_Key)
        # ..........................................
        return JSON_Records_Length

    def Next(self, Commit:int = 1) -> int:

        Record = self.Pub_JSON_Records[self.Pub_Index_Mov]
        # ..........................................
        # Psycopg2 2.9.11 构造参数化 "插入 (INSERT)" 语句
        # >>> import psycopg2
        # >>> conn = psycopg2.connect(host     = "127.0.0.1",
        # ...                         database = "postgres",
        # ...                         user     = "reader",
        # ...                         password = "123456")
        # >>> cursor = conn.cursor()
        # >>>
        # >>> # 构造基本参数化 "插入 (INSERT)" 语句 (使用 %s 占位符, 推荐):
        # >>> values = ('John', 'Doe', 30)
        # >>> sql = "INSERT INTO users (first_name, last_name, age) VALUES (%s, %s, %s);"
        # >>> cursor.execute(sql, values)
        # >>> conn.commit()
        # >>>
        # >>> # 使用 psycopg2.connect( ... ).cursor().executemany() 批量 INSERT
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
        SQL_Statement_Part_A:str = "INSERT INTO %s (" % self.Pub_DB_Table
        SQL_Statement_Part_B:str = ") VALUES ("
        # ..........................................
        Fields_List:list = list(Record.keys())
        a:int            = 0
        b:int            = len(Fields_List) - 1
        # ..........................................
        while (a <= b):
            if (a == 0):
                SQL_Statement_Part_A = "%s%s" % (SQL_Statement_Part_A, Fields_List[a])
                SQL_Statement_Part_B = "%s%s" % (SQL_Statement_Part_B, "%s")
            if (a >= 1):
                SQL_Statement_Part_A = "%s,%s" % (SQL_Statement_Part_A, Fields_List[a])
                SQL_Statement_Part_B = "%s,%s" % (SQL_Statement_Part_B, "%s")
            a = a + 1
        # ..........................................
        SQL_Statement:str = "%s%s);" % (SQL_Statement_Part_A, SQL_Statement_Part_B)
        # ..........................................
        cursor = self.Pub_DB_Connection.cursor()
        cursor.execute(SQL_Statement, tuple(Record.values()))
        # ..........................................
        # 获取 INSERT / UPDATE / DELETE 操作后受影响的行数
        Affected_Rows_Number = cursor.rowcount
        # ..........................................
        # 在每行 SQL 语句占用的字节 (Bytes) 数相同的情况下,
        # 每条 INSERT 语句执行后立即 Commit (多次 Commit 事务, 速度更慢, 内存 (Memory) 占用更少),
        # 多条 INSERT 语句执行后一次 Commit (单次 Commit 事务, 速度更快, 内存 (Memory) 占用更多),
        # 可使用 SELECT pg_column_size(t.*) FROM example_table t; 查看行 (Rows) 大小。
        if (Commit == 1):
            self.Pub_DB_Connection.commit()
            self.Pub_DB_Connection_Commit_Count = self.Pub_DB_Connection_Commit_Count + 1
        # ..........................................
        self.Pub_Index_Mov = self.Pub_Index_Mov + 1
        # ..........................................
        return Affected_Rows_Number

class PY3_PostgreSQL9_By_Psycopg2(object):

    # Examples:
    # >>> PGSQL = PY3_PostgreSQL9_By_Psycopg2()
    # >>> PGSQL.Pub_DB_Host = "127.0.0.1"
    # >>> PGSQL.Pub_DB_Database = "postgres"
    # >>> PGSQL.Pub_DB_User = "postgres"
    # >>> PGSQL.Pub_DB_Password = "12345678"
    # >>> Qeried = PGSQL.Query("SELECT * FROM example;")
    # >>> print(Qeried)
    #     id      date   open   high    low  close   volume
    #  0   1  20240731  21.52  21.80  21.40  21.52  1065652
    #  1   2  20240731  21.62  21.92  21.80  21.90  1032323
    # 70  70  20240731  24.30  24.45  24.00  24.20  2050554

    def __init__(self):

        self.Pub_DB_Host:str     = "127.0.0.1"
        self.Pub_DB_Database:str = "unknow_database"
        self.Pub_DB_User:str     = "unknow_user"
        self.Pub_DB_Password:str = "unknow_password"
        # ..........................................
        self.INSERT_ITERATOR = PY3_PostgreSQL9_By_Psycopg2_INSERT_ITERATOR()

    def Set_DB_Host(self, DB_Host:str) -> int:

        self.Pub_DB_Host                 = DB_Host
        self.INSERT_ITERATOR.Pub_DB_Host = DB_Host
        # ..........................................
        return 1

    def Set_DB_Database(self, DB_Database:str) -> int:

        self.Pub_DB_Database                 = DB_Database
        self.INSERT_ITERATOR.Pub_DB_Database = DB_Database
        # ..........................................
        return 1

    def Set_DB_User(self, DB_User:str) -> int:

        self.Pub_DB_User                 = DB_User
        self.INSERT_ITERATOR.Pub_DB_User = DB_User
        # ..........................................
        return 1

    def Set_DB_Password(self, DB_Password:str) -> int:

        self.Pub_DB_Password                 = DB_Password
        self.INSERT_ITERATOR.Pub_DB_Password = DB_Password
        # ..........................................
        return 1

    def Init_DB_Connection(self) -> object:

        conn = psycopg2.connect(host     = self.Pub_DB_Host,
                                database = self.Pub_DB_Database,
                                user     = self.Pub_DB_User,
                                password = self.Pub_DB_Password)
        # ..........................................
        return conn

    def Query(self, SQL_Statement:str) -> list:

        conn = self.Init_DB_Connection()
        # ..........................................
        # Psycopg2 2.9.11 游标类型:
        # - psycopg2.extensions.cursor        # 2.9.11 版本默认游标, 返回元组形式的结果。
        # - psycopg2.extensions.namedcursor   # 返回带名称的游标, 可通过名称引用。
        # - psycopg2.extras.NamedTupleCursor  # 返回命名元组形式的结果。
        # - psycopg2.extras.DictCursor        # 返回类似字典的对象, 支持索引和键名访问 (内存使用稍低)。
        # - psycopg2.extras.RealDictCursor    # 返回真正字典形式的结果, 支持通过列名访问数据 (内存使用稍高)。
        # ..........................................
        # psycopg2.extensions.cursor 游标返回值示例:
        # >>> import psycopg2
        # >>> conn = psycopg2.connect(host     = "127.0.0.1",
        # ...                         database = "postgres",
        # ...                         user     = "reader",
        # ...                         password = "123456")
        # >>> cursor = conn.cursor(cursor_factory = extensions.cursor)
        # >>> cursor.execute("SELECT id, name, age, salary FROM employees;")
        # >>> rows = cursor.fetchall()
        # >>> print(rows)
        # [
        #     (1, 'Annie', 22, Decimal('2688.50')),
        #     ......
        #     (9, 'Jack', 24, Decimal('3200.00'))
        # ]
        # ..........................................
        # psycopg2.extras.RealDictCursor 游标返回值示例:
        # >>> import psycopg2
        # >>> from psycopg2.extras import RealDictCursor
        # >>> conn = psycopg2.connect(host     = "127.0.0.1",
        # ...                         database = "postgres",
        # ...                         user     = "reader",
        # ...                         password = "123456")
        # >>> cursor = conn.cursor(cursor_factory = RealDictCursor)
        # >>> cursor.execute("SELECT id, name, age, salary FROM employees;")
        # >>> rows = cursor.fetchall()
        # >>> print(rows)
        # [
        #     RealDictRow([('id', 1), ('name', 'Annie'), ('age', '22'), ('salary', Decimal('2688.50'))]),
        #     ......
        #     RealDictRow([('id', 1), ('name', 'Jack'), ('age', '24'), ('salary', Decimal('3200.00'))])
        # ]
        # ..........................................
        cursor = conn.cursor(cursor_factory = RealDictCursor)
        cursor.execute(SQL_Statement)
        rows = cursor.fetchall()
        # ..........................................
        cursor.close()
        conn.close()
        # ..........................................
        return pandas.DataFrame(rows)

    def TRUNCATE_TABLE(self, DB_Table:str, Primary_Key:str = "<none>") -> int:

        conn = self.Init_DB_Connection()
        # ..........................................
        cursor = conn.cursor()
        cursor.execute("DELETE FROM %s;" % DB_Table)
        # ..........................................
        # 获取 INSERT / UPDATE / DELETE 操作后受影响的行数
        Affected_Rows_Number = cursor.rowcount
        # ..........................................
        if (Primary_Key != "<none>"):
            # 执行 DELETE FROM <table_name>; 后, 表数据被删除, 但序列值仍保留上次生成的值。
            # 例如, 若原序列值为 100, 删除数据后下一条记录的主键仍从 101 开始。
            # 通过 ALTER SEQUENCE <table_name>_<sequence_name>_seq RESTART WITH 1; 重置序列起始值。
            # 或者通过 SELECT setval('<table_name>_<sequence_name>_seq', 1, false); 重置序列起始值。
            # 在 PostgreSQL 9 命令行客户端 (Cli) 中执行 ALTER SEQUENCE 示例:
            #     postgres=# ALTER SEQUENCE users_id_seq RESTART WITH 1;
            #     ALTER SEQUENCE
             # 在 PostgreSQL 9 命令行客户端 (Cli) 中执行 SELECT setval() 示例:
            #     postgres=# SELECT setval('users_id_seq', 1, false);
            #      setval
            #     --------
            #           1
            #     (1 行记录)
            cursor.execute("SELECT setval('%s_%s_seq', 1, false);" % (DB_Table, Primary_Key))
        # ..........................................
        conn.commit()
        # ..........................................
        cursor.close()
        conn.close()
        # ..........................................
        return Affected_Rows_Number

# EOF Signed by GF.
