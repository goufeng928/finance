# PY3_DB_Server_Client_POST_Sync_TABLE_Pull_JSON_Records.py
# Create by GF 2025-11-24 19:11

import json
import sys
# ..................................................
import requests

# ##################################################

class PY3_DB_Server_Client_POST_Sync_TABLE_Pull_JSON_Records():

    # Examples for "POST_for_PGSQL_Query_Rows_Number":
    # >>> OBJ = PY3_DB_Server_Client_POST_Sync_TABLE_Pull_JSON_Records()
    # >>> URL = "http://192.168.81.130/PHP5_DB_Server_POST_Sync_TABLE_Pull_JSON_Records.php"
    # >>> JSON_Records = OBJ.POST_for_PGSQL_Query_Rows_Number(URL, "SELECT * FROM logs;")
    # >>> print(JSON_Records)
    # [{'rows_num': '129'}]

    # Examples for "POST_for_PGSQL_Query_Datas":
    # >>> OBJ = PY3_DB_Server_Client_POST_Sync_TABLE_Pull_JSON_Records()
    # >>> URL = "http://192.168.81.130/PHP5_DB_Server_POST_Sync_TABLE_Pull_JSON_Records.php"
    # >>> JSON_Records = OBJ.POST_for_PGSQL_Query_Datas(URL, "SELECT * FROM logs;")
    # [DEBUG] Processing -> Records Number: 1156048 (Block: 116/116)
    # >>> print(JSON_Records)
    # [{'id': 1,
    #   'time': '2025-07-02',
    #   'object': 'tushare_api_cache_en_us',
    #   'event': 'insert',
    #   'afct_num': 5403,
    #   'unit': 'row',
    #   'memo': '日数据/不复权'},
    #  ......
    #  {'id': 1156048,
    #   'time': '2025-10-20',
    #   'object': 'tushare_api_cache_en_us',
    #   'event': 'insert',
    #   'afct_num': 5430,
    #   'unit': 'row',
    #   'memo': '日数据/不复权'}]

    def __init__(self):

        self.HTTP_Requests_Headers:dict  = {"Content-Type": "application/json"}
        self.Query_Rows_Number_Limit:int = 10000

    def SQL_Statement_Remove_Ending_Symbol(self, SQL_Statement:str) -> str:

        SQL_Statement_Copy:str  = SQL_Statement
        SQL_Statement_Copy      = SQL_Statement_Copy.lstrip()
        SQL_Statement_Copy      = SQL_Statement_Copy.rstrip()
        SQL_Statement_Copy_Leng = len(SQL_Statement_Copy)
        SQL_Statement_Copy_Cuts = SQL_Statement_Copy[0:(SQL_Statement_Copy_Leng - 1)]
        SQL_Statement_Copy_Tail = SQL_Statement_Copy[-1]
        SQL_Statement_Copy      = SQL_Statement_Copy_Cuts if (SQL_Statement_Copy_Tail == ';') else SQL_Statement_Copy
        # ..........................................
        return SQL_Statement_Copy

    def POST_for_PGSQL_Query_Rows_Number(self, URL:str, SQL_Statement:str) -> dict:

        SQL_Statement_Copy:str = self.SQL_Statement_Remove_Ending_Symbol(SQL_Statement)
        # ..........................................
        HTTP_Requests_Data:dict = {
            "db_type":       "postgresql",
            "sql_statement": "SELECT COUNT(*) as rows_num FROM (" + SQL_Statement_Copy + ");"
        }
        # ..........................................
        response = requests.post(URL, headers = self.HTTP_Requests_Headers, data = json.dumps(HTTP_Requests_Data))
        # ..........................................
        return json.loads(response.text)

    def POST_for_PGSQL_Query_Datas(self, URL:str, SQL_Statement:str) -> dict:

        Queried_JSON_Records:list = self.POST_for_PGSQL_Query_Rows_Number(URL = URL, SQL_Statement = SQL_Statement)
        Queried_Rows_Number:int   = Queried_JSON_Records[0].get("rows_num", None)
        Queried_Rows_Number       = int(Queried_Rows_Number)
        # ..........................................
        Queried_JSON_Records:list = []
        # ..........................................
        if (Queried_Rows_Number <= self.Query_Rows_Number_Limit):
            HTTP_Requests_Data:dict = {
                "db_type":       "postgresql",
                "sql_statement": SQL_Statement
            }
            # ......................................
            response = requests.post(URL, headers = self.HTTP_Requests_Headers, data = json.dumps(HTTP_Requests_Data))
            Queried_JSON_Records = json.loads(response.text)
            # ......................................
            print(f"[DEBUG] Processing -> Records Number: {len(Queried_JSON_Records)} (Block: 1/1)")
        # ..........................................
        if (Queried_Rows_Number > self.Query_Rows_Number_Limit):
            Fetched_Rows:int = 0
            Quotient:int     = divmod(Queried_Rows_Number, self.Query_Rows_Number_Limit)[0]
            Remainder:int    = divmod(Queried_Rows_Number, self.Query_Rows_Number_Limit)[1]
            Loop_Count:int   = Quotient if (Remainder == 0) else Quotient + 1
            # ......................................
            SQL_Statement_Copy:str = self.SQL_Statement_Remove_Ending_Symbol(SQL_Statement)
            # ......................................
            i:int = 1
            while (i <= Loop_Count):
                HTTP_Requests_Data:dict = {
                    "db_type":       "postgresql",
                    "sql_statement": SQL_Statement_Copy + f" OFFSET {Fetched_Rows} ROWS FETCH NEXT {self.Query_Rows_Number_Limit} ROWS ONLY;"
                }
                # ..................................
                response = requests.post(URL, headers = self.HTTP_Requests_Headers, data = json.dumps(HTTP_Requests_Data))
                Queried_JSON_Records.extend(json.loads(response.text))
                # ..................................
                Fetched_Rows = len(Queried_JSON_Records)
                # ..................................
                sys.stdout.write(f"\r[DEBUG] Processing -> Records Number: {Fetched_Rows} (Block: {i}/{Loop_Count})")
                sys.stdout.flush()
                # ..................................
                i = i + 1
        # ..........................................
        return Queried_JSON_Records

# EOF Signed by GF.
