# API_Call_Tushare1424_Stocks_Data_to_PGSQL16.py
# Create by GF 2025-08-12 12:55

import json
# ..................................................
import pandas
import tushare
# ..................................................
import PY3_PostgreSQL9_By_SQLAlchemy2

# ##################################################

def Text_Unique_Washing(TEXT_Unique:str) -> str:

    TEXT_Unique_Copy:str = TEXT_Unique
    # ..............................................
    TEXT_Unique_Copy     = TEXT_Unique_Copy.replace(' ', '-')
    TEXT_Unique_Copy     = TEXT_Unique_Copy.replace(',', '-')
    TEXT_Unique_Copy     = TEXT_Unique_Copy.replace('.', '-')
    TEXT_Unique_Copy     = TEXT_Unique_Copy.replace('_', '-')
    # ..............................................
    TEXT_Unique_Copy     = TEXT_Unique_Copy.replace("，", '-')
    TEXT_Unique_Copy     = TEXT_Unique_Copy.replace("。", '-')
    # ..............................................
    return TEXT_Unique_Copy

# ##################################################

def PY3_API_Call_Tushare1424_Stocks_Data_to_PGSQL16(TEXT_Time:str):

    if (('-' not in TEXT_Time) or (len(TEXT_Time) < 10)):
        return {"error": "<Input_Date> Format Should be <YYYY-mm-dd>, Example: 2025-01-01"}

    pandas_time_object = pandas.to_datetime(TEXT_Time, format="mixed")

    # 读取 API Call Configuration (JSON 文件)
    # ..............................................
    FILE_Object = open("./APP_API_Call_Configuration.json", mode = 'r', encoding = "utf-8")
    TEXT_Readed = FILE_Object.read()
    FILE_Object.close()
    DICT_Config = json.loads(TEXT_Readed)
    # ..............................................
    db_host     = DICT_Config.get("postgresql", {}).get("16.10", {}).get("host", "unknow_host")
    db_port     = DICT_Config.get("postgresql", {}).get("16.10", {}).get("port", "unknow_port")
    db_database = DICT_Config.get("postgresql", {}).get("16.10", {}).get("init_database", "unknow_db_name")
    db_user     = DICT_Config.get("postgresql", {}).get("16.10", {}).get("user", "unknow_user")
    db_password = DICT_Config.get("postgresql", {}).get("16.10", {}).get("password", "unknow_password")
    # ..............................................
    option_time_scale = DICT_Config.get("tushare", {}).get("1.4.24", {}).get("stocks", {}).get("option_time_scale", "unknow_time_scale")
    option_adjusted   = DICT_Config.get("tushare", {}).get("1.4.24", {}).get("stocks", {}).get("option_adjusted", "unknow_adjusted")

    # 初始化 PostgreSQL 16.10 连接
    # ..............................................
    PGSQL = PY3_PostgreSQL9_By_SQLAlchemy2.PY3_PostgreSQL9_By_SQLAlchemy2()
    PGSQL.Pub_DB_Host     = db_host
    PGSQL.Pub_DB_Database = db_database
    PGSQL.Pub_DB_User     = db_user
    PGSQL.Pub_DB_Password = db_password

    if (option_time_scale == "daily" and option_adjusted == None):

        # 查询 Vars 中 Tusahre API Key 的值
        # ..........................................
        Queried_DataFrame = PGSQL.Query("SELECT value FROM vars WHERE name = 'tushare_api_key';")
        # ..........................................
        TUSHARE_API_KEY = Queried_DataFrame["value"].values[0]

        # 查询 Logs 中特定日期的数据插入记录
        # ..........................................
        Queried_DataFrame = PGSQL.Query(
            f"""
            SELECT
                COUNT(*) AS rows_count
            FROM
                logs
            WHERE
                time = '{TEXT_Time}' AND
                POSITION('股票' IN memo) > 0 AND
                POSITION('日数据' IN memo) > 0 AND
                POSITION('不复权' IN memo) > 0;
            """
        )
        # ..........................................
        logs_existing_rows_count = Queried_DataFrame["rows_count"].values[0]

        df = pandas.DataFrame()
        affected_number_of_dist:int = 0
        if (logs_existing_rows_count == 0): # 如果日志 (dateset.logs) 中存在的行数 == 0, 则获取 Tushare API 数据
            bgn_time:str = pandas_time_object.strftime("%Y%m%d")
            end_time:str = pandas_time_object.strftime("%Y%m%d")
            # ......................................
            tushare_pro_api = tushare.pro_api(TUSHARE_API_KEY)
            df = tushare_pro_api.daily(adj = option_adjusted, start_date = bgn_time, end_date = end_time)
            # ......................................
            df["date"  ] = pandas.to_datetime(df["trade_date"], format="mixed")
            df["time"  ] = df["date"].dt.strftime("%Y-%m-%d")  # 将日期时间格式转换为字符串格式
            df["unique"] = 'stock-' + df["ts_code"] + "-daily-" + df["date"].dt.strftime("%Y%m%d") + "-bfq"
            df["unique"] = df["unique"].apply(lambda x: Text_Unique_Washing(x))  # 文本唯一值清洗
            df["memo"  ] = "股票/日数据/不复权"
            df = df.drop(["trade_date", "date"], axis=1)
            # ......................................
            affected_number_of_dist = PGSQL.APPEND_BY_Pandas_DataFrame(df, "tushare_api_cache_en_us", Primary_Key = "id")

        affected_number_of_logs = 0
        if (affected_number_of_dist >= 1): # 如果被影响行数 >= 1, 则写入日志 (dateset.logs)
            df = pandas.DataFrame([{
                "time"     : pandas_time_object.strftime("%Y-%m-%d"),
                "object"   : "tushare_api_cache_en_us",
                "event"    : "insert",
                "afct_num" : affected_number_of_dist,
                "unit"     : "row",
                "memo"     : "股票/日数据/不复权"
            }])
            # ......................................
            affected_number_of_logs = PGSQL.APPEND_BY_Pandas_DataFrame(df, "logs", Primary_Key = "id")

        return {"affected_number_of_dist": affected_number_of_dist, "affected_number_of_logs": affected_number_of_logs}

# EOF Signed by GF.
