//
// Created by GF on 2023/3/8.
//

#include "Fin_Header.h"

// Global Variable.
int ROWS_NUM = 0;
int FIELDS_NUM = 0;
int CMPTD_ROWS_NUM = 0;

// Global Variable: CSV Information.
char FIELD_NAME_DATE_GB_ZH[5] = {-56,-43,-58,-38,0};

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