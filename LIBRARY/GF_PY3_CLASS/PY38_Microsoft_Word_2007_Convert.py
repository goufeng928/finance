# GF_PY3_CLASS/PY38_Microsoft_Word_2007_Convert.py
# Create by GF 2025-01-15 14:00

class PY38_Microsoft_Word_2007_Convert(object):

    # Microsoft Word 字号与 HTML/CSS 字号对照表 (20260116 更新)
    # Word中文字号 | Word英文字号 | 实际尺寸(磅) | HTML/CSS (px) | HTML/CSS (pt) | HTML/CSS (em/rem) | 常用场景
    # -------------+--------------+--------------+---------------+---------------+-------------------+-----------
    # 初号         |         42pt |         42磅 |          56px |          42pt |             3.5em | 超大标题
    # 小初         |         36pt |         36磅 |          48px |          36pt |               3em | 大标题
    # 一号         |         26pt |         26磅 |        34.7px |          26pt |            2.17em | 主标题
    # 小一         |         24pt |         24磅 |          32px |          24pt |               2em | 副标题
    # 二号         |         22pt |         22磅 |        29.3px |          22pt |            1.83em | 章标题
    # 小二         |         18pt |         18磅 |          24px |          18pt |             1.5em | 节标题
    # 三号         |         16pt |         16磅 |        21.3px |          16pt |            1.33em | 大标题
    # 小三         |         15pt |         15磅 |          20px |          15pt |            1.25em | 中标题
    # 四号         |         14pt |         14磅 |        18.7px |          14pt |            1.17em | 小标题
    # 小四         |         12pt |         12磅 |          16px |          12pt |               1em | 正文(稍大)
    # 五号         |       10.5pt |       10.5磅 |          14px |        10.5pt |           0.875em | 正文标准
    # 小五         |          9pt |          9磅 |          12px |           9pt |            0.75em | 注释/小字
    # 六号         |        7.5pt |        7.5磅 |          10px |         7.5pt |           0.625em | 脚注
    # 小六         |        6.5pt |        6.5磅 |         8.7px |         6.5pt |            0.54em | 极小字
    # 七号         |        5.5pt |        5.5磅 |         7.3px |         5.5pt |            0.46em | 几乎不用
    # 八号         |          5pt |          5磅 |         6.7px |           5pt |            0.42em | 几乎不用

    def __init__(self):

        self.Font_Size_Mapping:dict = {"初号": {"px":   "56px", "pt":   "42pt", "em":   "3.5em"},
                                       "小初": {"px":   "48px", "pt":   "36pt", "em":     "3em"},
                                       "一号": {"px": "34.7px", "pt":   "26pt", "em":  "2.17em"},
                                       "小一": {"px":   "32px", "pt":   "24pt", "em":     "2em"},
                                       "二号": {"px": "29.3px", "pt":   "22pt", "em":  "1.83em"},
                                       "小二": {"px":   "24px", "pt":   "18pt", "em":   "1.5em"},
                                       "三号": {"px": "21.3px", "pt":   "16pt", "em":  "1.33em"},
                                       "小三": {"px":   "20px", "pt":   "15pt", "em":  "1.25em"},
                                       "四号": {"px": "18.7px", "pt":   "14pt", "em":  "1.17em"},
                                       "小四": {"px":   "16px", "pt":   "12pt", "em":     "1em"},
                                       "五号": {"px":   "14px", "pt": "10.5pt", "em": "0.875em"},
                                       "小五": {"px":   "12px", "pt":    "9pt", "em":  "0.75em"},
                                       "六号": {"px":   "10px", "pt":  "7.5pt", "em": "0.625em"},
                                       "小六": {"px":  "8.7px", "pt":  "6.5pt", "em":  "0.54em"}}

    def Font_Size_to_HTML_CSS_em(self, Font_Size:str) -> str:

        return self.Font_Size_Mapping.get(Font_Size, {}).get("em", "0.875em")

# EOF Signed by GF.
