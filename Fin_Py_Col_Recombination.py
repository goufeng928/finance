import codecs
import pandas as pd

def csv_col_recombination(csv_name):

    file = pd.read_csv(("../csv_source/" + csv_name), encoding="gb2312")

    df = pd.DataFrame(file)

    print("[ Function ] CSV Col Recombination: CSV Col Recombining...")

    finance_dict = {"日期": df["日期"].values.tolist(),
                    "名称": df["名称"].values.tolist(),
                    "代码": df["代码"].values.tolist(),
                    "开盘价": df["开盘价"].values.tolist(),
                    "最高价": df["最高价"].values.tolist(),
                    "最低价": df["最低价"].values.tolist(),
                    "收盘价": df["收盘价"].values.tolist(),
                    "前收盘": df["前收盘"].values.tolist(),
                    "成交量": df["成交量"].values.tolist()}

    finance_df = pd.DataFrame(finance_dict)

    finance_df.to_csv(("../csv_recombined/" + csv_name), index=False, encoding='gb2312')

    print("[ Function ] CSV Col Recombination: Save CSV File Finished.")

if __name__ == "__main__":

    csv_col_recombination("000422.csv")
