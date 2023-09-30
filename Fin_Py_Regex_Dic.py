RegexDateDic = {"EastMoney日期": "[0-9]{2,4}-[0-9]{1,2}-[0-9]{1,2}"}

RegexNameDic = {"EastMoney玻璃(FG)": "玻璃[0-9]{1,4}"}

RegexCodeDic = {"EastMoney代码": "[a-zA-Z]{1,3}[0-9]{1,4}"}

RegexMarketDic = {"EastMoney开盘价": "今开.{0,3}[0-9]+",
                  "EastMoney最高价": "最高.{0,3}[0-9]+",
                  "EastMoney最低价": "最低.{0,3}[0-9]+",
                  "EastMoney收盘价": "收盘.{0,3}[0-9]+",
                  "EastMoney前收盘": "昨收.{0,3}[0-9]+"}
