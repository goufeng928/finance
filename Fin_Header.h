//
// Created by GF on 2023/2/20.
//

#ifndef FIN_HEADER_H
#define FIN_HEADER_H

// Global Constant.
#define STATS_TABLE_ROWS_NUM 1 + 54 //Field(1) + Subject(54).
#define STATS_TABLE_COLS_NUM 1 + 21 + 1 //Subject(1) + ND1S803XXX(21) + Amount(1).
#define ANAL_TABLE_ROWS_NUM 1 + 4 + 1 //Field(1) + Subject(4) + ProbSum(1).

// Global Constant: CSV Information.
#define LOADED_FIELD_ROWS_NUM 15

// Global Variable.
int ROWS_NUM;
int FIELDS_NUM;
int CMPTD_ROWS_NUM;

// Global Variable: CSV Information.
char FIELD_NAME_DATE_GB_ZH[5];

char LOADED_FIELD_NAME[LOADED_FIELD_ROWS_NUM][9];
int  LOADED_FIELD_SEQ[LOADED_FIELD_ROWS_NUM];

int FIELD_SEQ_Date;
int FIELD_SEQ_Name;
int FIELD_SEQ_Code;
int FIELD_SEQ_Open;
int FIELD_SEQ_High;
int FIELD_SEQ_Low;
int FIELD_SEQ_Close;
int FIELD_SEQ_Pre_Close;
int FIELD_SEQ_Volume;

// Global Variable: Struct Pointer Information.
int* PTR_STU_COL_S803XXX;
int* PTR_STU_COL_ND1S803XXX;

// Global Variable: Statistics Table.
char STATS_TABLE_COUNT[STATS_TABLE_ROWS_NUM][STATS_TABLE_COLS_NUM][21];
char STATS_TABLE_PROB[STATS_TABLE_ROWS_NUM][STATS_TABLE_COLS_NUM][21];
char ANAL_TABLE_PROB[ANAL_TABLE_ROWS_NUM][STATS_TABLE_COLS_NUM][21];

// Struct.
struct Finance_Subject {

    int S8021XX;
    int S8022XX;
    int S8025XX;
    int S8026XX;
    int S8024XX;
};

struct Finance {

    // 金融的基本数据(现成数据)字段。
    char Date[11];                // 01.日期。
    char Name[13];                // 02.名称。每个汉字在UTF-8编码下占3个char字节，在GBK编码下占2个char字节。
    char Code[8];                 // 03.代码。
    double Open;                  // 04.开盘价。“亿”为9位char字节数字，千亿为12位char字节数字。
    double High;                  // 05.最高价。
    double Low;                   // 06.最低价。
    double Close;                 // 07.收盘价。
    double Pre_Close;             // 08.前收盘(Previous Close)。
    double Rise_Fall_Amt;         // 09.涨跌额(Rise and Fall Amount)。
    double Rise_Fall_Rate;        // 10.涨跌率(Rise and Fall Rate)。
    double Turnover_Rate;         // 11.换手率(Turnover Rate)。
    double Volume;                // 12.成交量。
    double Trading_Volumes;       // 13.成交额(Trading Volumes)。
    double Market_Cap;            // 14.总市值(Market Cap)。
    double Circ_Market_Value;     // 15.流通市值(Circulation Market Value)。

    // 时间戳的计算数据(需要计算)字段。
    double TimeStamp;

    // 金融的计算数据(需要计算)字段。
    int S803XXX;

    // 当前状态下的次日(或3日/5日后)状态。
    int ND1S803XXX;

    // 金融的计算数据(需要计算)字段。
    int S8021XX;
    int S8025XX;
    int S8026XX;
    int S8024XX;

    struct Finance_Subject Subject;
    char Remarks[8];
};

#endif //FIN_HEADER_H

/*
 *
 * 缩写约定:
 *
 * [ analysis       : anal  ]
 * [ characteristic : chara ]
 * [ compute        : cmpt  ]
 * [ current        : cur   ]
 * [ distance       : dis   ]
 * [ member         : mem   ]
 * [ original       : org   ]
 * [ other          : oth   ]
 * [ probability    : prob  ]
 * [ quantity       : qty   ]
 * [ sample         : spl   ]
 * [ sequence       : seq   ]
 * [ statistics     : stats ]
 *
 * 163股票字段:
 *
 * [一开盘价 : TOPEN               ]
 * [一最高价 : HIGH                ]
 * [一最低价 : LOW                 ]
 * [一收盘价 : TCLOSE              ]
 * [前收盘价 : LCLOSE              ]
 * [一涨跌额 : CHG (Change)        ]
 * [一涨跌幅 : PCHG (Price Change) ]
 * [一换手率 : TURNOVER            ]
 * [一成交量 : VOTURNOVER          ]
 * [成交金额 : VATURNOVER          ]
 * [一总市值 : TCAP                ]
 * [流通市值 : MCAP                ]
 *
 */
