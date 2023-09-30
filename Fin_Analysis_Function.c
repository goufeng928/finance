//
// Created by GF on 2023/3/2.
//

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "Fin_Header.h"
#include "Fin_Analysis_Function.h"

// External Functions Needed.
// [- CsvToMem]
// [- CsvRowsNum]
// [- CsvFieldsNum]
#include "Fin_Text_Function.h"

// External Functions Needed.
// [- compute_rise_fall_amt]
// [- compute_rise_fall_rate]
// [- compute_S803XXX]
// [- compute_S8021XX]
// [- compute_S8025XX]
// [- compute_S8026XX]
// [- compute_S8024XX]
// [- compute_ND1S803XXX]
#include "Fin_Algorithm.h"

void Init_Anal_Table() {

    /* ********************** Table Explain *********************** */
    /*
     * +-------------------+---------------------+-------+-------------------+
     * |  [0][0]: Subject  |  [0][1]: S803XXX    |  ...  |  [0][22]: Amount  |
     * +------------------+----------------------+-------+-------------------+
     * |  [1][0]: Sbj Val  |  [1][1]: Table Val  |  ...  |         ...       |
     * +-------------------+---------------------+-------+-------------------+
     * |        ...        |         ...         |  ...  |         ...       |
     * +-------------------+---------------------+-------+-------------------+
     */

    /* ********************** Cyclic Assign *********************** */
    for (int row = 0; row < ANAL_TABLE_ROWS_NUM; row++) {
        for (int col = 0; col < STATS_TABLE_COLS_NUM; col++) {
            strcpy(ANAL_TABLE_PROB[row][col], "0");
        }
    }

    /* ************************* Subject ************************** */
    strcpy(ANAL_TABLE_PROB[0][0], "Subject");
    /* ************************* S803XXX ************************** */
    strcpy(ANAL_TABLE_PROB[0][1], "803401");
    strcpy(ANAL_TABLE_PROB[0][2], "803402");
    strcpy(ANAL_TABLE_PROB[0][3], "803403");
    strcpy(ANAL_TABLE_PROB[0][4], "803404");
    strcpy(ANAL_TABLE_PROB[0][5], "803405");
    strcpy(ANAL_TABLE_PROB[0][6], "803406");
    strcpy(ANAL_TABLE_PROB[0][7], "803407");
    strcpy(ANAL_TABLE_PROB[0][8], "803408");
    strcpy(ANAL_TABLE_PROB[0][9], "803409");
    strcpy(ANAL_TABLE_PROB[0][10], "803410");
    strcpy(ANAL_TABLE_PROB[0][11], "803500");
    strcpy(ANAL_TABLE_PROB[0][12], "803601");
    strcpy(ANAL_TABLE_PROB[0][13], "803602");
    strcpy(ANAL_TABLE_PROB[0][14], "803603");
    strcpy(ANAL_TABLE_PROB[0][15], "803604");
    strcpy(ANAL_TABLE_PROB[0][16], "803605");
    strcpy(ANAL_TABLE_PROB[0][17], "803606");
    strcpy(ANAL_TABLE_PROB[0][18], "803607");
    strcpy(ANAL_TABLE_PROB[0][19], "803608");
    strcpy(ANAL_TABLE_PROB[0][20], "803609");
    strcpy(ANAL_TABLE_PROB[0][21], "803610");
    /* ************************** Amount ************************** */
    strcpy(ANAL_TABLE_PROB[0][22], "Amount");

    /* ************************* Separate ************************* */
    printf("[ Analysis ] Init Anal Table: Finished.\n");
}

void Analysis(struct Finance** PPtr_Input_Fin) {

    int Input_Rows_Num = CsvRowsNum("./CSV_Analysis.csv", 0);
    int Input_Fields_Num = CsvFieldsNum("./CSV_Analysis.csv");

    /* ************************* Separate ************************* */
    char* MemCsv = CsvToMem("./CSV_Analysis.csv");

    /* ************************* Separate ************************* */
    *PPtr_Input_Fin = (struct Finance*)malloc(sizeof(struct Finance) * Input_Rows_Num);

    /* ************************* Separate ************************* */
    FILE *fp;
    char Row500[500], Trash500[500];
    int ReadCharNum = 0;
    int ReadCharTotalNum = 0;
    unsigned long long MemCsvLen = strlen(MemCsv);

    //CSV文件需要转换成GBK编码，否则中文输出为乱码。
    fp = fopen("./CSV_Analysis.csv", "r");

    if (fp == NULL) {

        printf("[ Analysis Error ] Analysis: Open CSV Failed.\n");

        fclose(fp);

        return;

    } else {

        //丢弃表头行。
        sscanf(MemCsv, "%s%n", Trash500, &ReadCharNum);

        MemCsv += ReadCharNum;

        ReadCharTotalNum += ReadCharNum;

        for (int i = 0; i < Input_Rows_Num && ReadCharTotalNum <= MemCsvLen; i++) {

            sscanf(MemCsv, "%s%n", Row500, &ReadCharNum);

            MemCsv += ReadCharNum;

            ReadCharTotalNum += ReadCharNum;

            int k = 0;
            const char* sep = ",";
            char* ptr_str;

            ptr_str = strtok(Row500, sep);
            while (ptr_str != NULL && k < Input_Fields_Num) {

                if (k == 0) strcpy((*PPtr_Input_Fin + i)->Date, ptr_str);
                else if (k == 1) strcpy((*PPtr_Input_Fin + i)->Name, ptr_str);
                else if (k == 2) strcpy((*PPtr_Input_Fin + i)->Code, ptr_str);
                else if (k == 3) (*PPtr_Input_Fin + i)->Open = atof(ptr_str);
                else if (k == 4) (*PPtr_Input_Fin + i)->High = atof(ptr_str);
                else if (k == 5) (*PPtr_Input_Fin + i)->Low = atof(ptr_str);
                else if (k == 6) (*PPtr_Input_Fin + i)->Close = atof(ptr_str);
                else if (k == 7) (*PPtr_Input_Fin + i)->Pre_Close = atof(ptr_str);
                else if (k == 8) (*PPtr_Input_Fin + i)->Volume = atof(ptr_str);

                ptr_str = strtok(NULL, sep);
                k++;
            }
        }
        printf("[ Analysis ] Analysis: Read CSV To Struct Finished.\n");

        fclose(fp);
    }

    /* ************************* Separate ************************* */
    compute_rise_fall_amt(*PPtr_Input_Fin, Input_Rows_Num);
    compute_rise_fall_rate(*PPtr_Input_Fin, Input_Rows_Num);
    compute_S803XXX(*PPtr_Input_Fin, Input_Rows_Num);
    compute_S8021XX(*PPtr_Input_Fin, Input_Rows_Num);
    compute_S8025XX(*PPtr_Input_Fin, Input_Rows_Num);
    compute_S8026XX(*PPtr_Input_Fin, Input_Rows_Num);
    compute_S8024XX(*PPtr_Input_Fin, Input_Rows_Num);
    //compute_ND1S803XXX(*PPtr_Input_Fin, Input_Rows_Num);

    /* ************************* Separate ************************* */
    Init_Anal_Table();

    char Buffer[21];

    itoa((*PPtr_Input_Fin)->S8021XX, Buffer, 10);
    strcpy(ANAL_TABLE_PROB[1][0], Buffer);

    itoa((*PPtr_Input_Fin)->S8025XX, Buffer, 10);
    strcpy(ANAL_TABLE_PROB[2][0], Buffer);

    itoa((*PPtr_Input_Fin)->S8026XX, Buffer, 10);
    strcpy(ANAL_TABLE_PROB[3][0], Buffer);

    itoa((*PPtr_Input_Fin)->S8024XX, Buffer, 10);
    strcpy(ANAL_TABLE_PROB[4][0], Buffer);

    /* ************************* ProbSum ************************** */
    strcpy(ANAL_TABLE_PROB[5][0], "ProbSum");

    /* ************************* Pick Up ************************** */
    /* for循环第1层 */
    for (int i = 1; i < (ANAL_TABLE_ROWS_NUM - 1); i++) { //跳过末行“ProbSum”。

        /* for循环第2层 */
        for (int j = 1; j < STATS_TABLE_ROWS_NUM; j++) {

            /* 条件判断 */
            if (strcmp(ANAL_TABLE_PROB[i][0], STATS_TABLE_PROB[j][0]) == 0) {

                for (int k = 1; k < STATS_TABLE_COLS_NUM; k++) {

                    strcpy(ANAL_TABLE_PROB[i][k], STATS_TABLE_PROB[j][k]);

                }
            }
            /* 条件判断：结束 */
        }
        /* for循环第2层：结束 */
    }
    /* for循环第1层：结束 */

    /* ************************ Summarize ************************* */
    /* for循环第1层 */
    for (int col = 1; col < (STATS_TABLE_COLS_NUM - 1); col++) { //跳过末列“Amount”。

        double ProbSum = 0;

        char Char_Buffer[21];

        /* for循环第2层 */
        for (int row = 1; row < (ANAL_TABLE_ROWS_NUM - 1); row++) { //跳过末行“ProbSum”。

            ProbSum += atof(ANAL_TABLE_PROB[row][col]);
        }
        /* for循环第2层：结束 */

        sprintf(Char_Buffer, "%.4f", ProbSum/4);

        strcpy(ANAL_TABLE_PROB[5][col], Char_Buffer);
    }
    /* for循环第1层：结束 */

    /* ************************ Debugging ************************* */
    FILE* Debug_fp;
    Debug_fp = fopen("./CSV_Debugging_Analysis_Prob.csv","w");

    for (int row = 0; row < ANAL_TABLE_ROWS_NUM; row++) {

        for (int col = 0; col < STATS_TABLE_COLS_NUM; col++) {

            fprintf(Debug_fp, "%8s|", ANAL_TABLE_PROB[row][col]);
        }
        fprintf(Debug_fp,"\n");
    }
    fclose(Debug_fp);

}
