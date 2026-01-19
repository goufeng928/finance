# GF_PY3_CLASS/Python3_Text/PY3_Text_Progress_Bar.py
# Create by GF 2025-09-20 00:53

class PY3_Text_Progress_Bar(object):

    # Examples for "Python 3 Text Progress Bar - Double Line Arrow":
    # >>> OBJECT_PY3_Text_Progress_Bar = PY3_Text_Progress_Bar()
    # >>>
    # >>> progress_bar = OBJECT_PY3_Text_Progress_Bar.Double_Line_Arrow(Count = 1, Total = 10)
    # >>> print(progress_bar)
    # [==>                  ] Pct: 0.10 | 1/10
    # >>>
    # >>> progress_bar = OBJECT_PY3_Text_Progress_Bar.Double_Line_Arrow(Count = 3, Total = 10)
    # >>> print(progress_bar)
    # [======>              ] Pct: 0.33 | 3/10

    def Double_Line_Arrow(self, Count:int, Total:int) -> str:

        # Python 3 Text Progress Bar - Double Line Arrow

        Progress:float = round(Count / Total, 2)

        Text_Progress_Bar_0_0:str = "[>                    ] Pct: %.2f | %d/%d" % (Progress, Count, Total)
        Text_Progress_Bar_0_1:str = "[==>                  ] Pct: %.2f | %d/%d" % (Progress, Count, Total)
        Text_Progress_Bar_0_2:str = "[====>                ] Pct: %.2f | %d/%d" % (Progress, Count, Total)
        Text_Progress_Bar_0_3:str = "[======>              ] Pct: %.2f | %d/%d" % (Progress, Count, Total)
        Text_Progress_Bar_0_4:str = "[========>            ] Pct: %.2f | %d/%d" % (Progress, Count, Total)
        Text_Progress_Bar_0_5:str = "[==========>          ] Pct: %.2f | %d/%d" % (Progress, Count, Total)
        Text_Progress_Bar_0_6:str = "[============>        ] Pct: %.2f | %d/%d" % (Progress, Count, Total)
        Text_Progress_Bar_0_7:str = "[==============>      ] Pct: %.2f | %d/%d" % (Progress, Count, Total)
        Text_Progress_Bar_0_8:str = "[================>    ] Pct: %.2f | %d/%d" % (Progress, Count, Total)
        Text_Progress_Bar_0_9:str = "[==================>  ] Pct: %.2f | %d/%d" % (Progress, Count, Total)
        Text_Progress_Bar_1_0:str = "[====================>] Pct: %.2f | %d/%d" % (Progress, Count, Total)

        if (Progress >= 1.0):
            return Text_Progress_Bar_1_0
        if (Progress >= 0.9):
            return Text_Progress_Bar_0_9
        if (Progress >= 0.8):
            return Text_Progress_Bar_0_8
        if (Progress >= 0.7):
            return Text_Progress_Bar_0_7
        if (Progress >= 0.6):
            return Text_Progress_Bar_0_6
        if (Progress >= 0.5):
            return Text_Progress_Bar_0_5
        if (Progress >= 0.4):
            return Text_Progress_Bar_0_4
        if (Progress >= 0.3):
            return Text_Progress_Bar_0_3
        if (Progress >= 0.2):
            return Text_Progress_Bar_0_2
        if (Progress >= 0.1):
            return Text_Progress_Bar_0_1
        if (Progress >= 0.0):
            return Text_Progress_Bar_0_0

# EOF Signed by GF.
