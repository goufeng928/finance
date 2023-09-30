//
// Created by GF on 2023/2/24.
//

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "Fin_Header.h"
#include "Fin_Statistics_Function.h"

void init_stats_table() {

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
    for (int row = 0; row < STATS_TABLE_ROWS_NUM; row++) {
        for (int col = 0; col < STATS_TABLE_COLS_NUM; col++) {
            strcpy(STATS_TABLE_COUNT[row][col], "0");
        }
    }

    /* ************************* Subject ************************** */
    strcpy(STATS_TABLE_COUNT[0][0], "Subject");
    /* ************************* S803XXX ************************** */
    strcpy(STATS_TABLE_COUNT[0][1], "803401");
    strcpy(STATS_TABLE_COUNT[0][2], "803402");
    strcpy(STATS_TABLE_COUNT[0][3], "803403");
    strcpy(STATS_TABLE_COUNT[0][4], "803404");
    strcpy(STATS_TABLE_COUNT[0][5], "803405");
    strcpy(STATS_TABLE_COUNT[0][6], "803406");
    strcpy(STATS_TABLE_COUNT[0][7], "803407");
    strcpy(STATS_TABLE_COUNT[0][8], "803408");
    strcpy(STATS_TABLE_COUNT[0][9], "803409");
    strcpy(STATS_TABLE_COUNT[0][10], "803410");
    strcpy(STATS_TABLE_COUNT[0][11], "803500");
    strcpy(STATS_TABLE_COUNT[0][12], "803601");
    strcpy(STATS_TABLE_COUNT[0][13], "803602");
    strcpy(STATS_TABLE_COUNT[0][14], "803603");
    strcpy(STATS_TABLE_COUNT[0][15], "803604");
    strcpy(STATS_TABLE_COUNT[0][16], "803605");
    strcpy(STATS_TABLE_COUNT[0][17], "803606");
    strcpy(STATS_TABLE_COUNT[0][18], "803607");
    strcpy(STATS_TABLE_COUNT[0][19], "803608");
    strcpy(STATS_TABLE_COUNT[0][20], "803609");
    strcpy(STATS_TABLE_COUNT[0][21], "803610");
    /* ************************** Amount ************************** */
    strcpy(STATS_TABLE_COUNT[0][22], "Amount");
    /* ************************* S8021XX ************************** */
    strcpy(STATS_TABLE_COUNT[1][0], "802100");
    strcpy(STATS_TABLE_COUNT[2][0], "802101");
    strcpy(STATS_TABLE_COUNT[3][0], "802102");
    strcpy(STATS_TABLE_COUNT[4][0], "802103");
    strcpy(STATS_TABLE_COUNT[5][0], "802104");
    strcpy(STATS_TABLE_COUNT[6][0], "802105");
    strcpy(STATS_TABLE_COUNT[7][0], "802106");
    strcpy(STATS_TABLE_COUNT[8][0], "802107");
    strcpy(STATS_TABLE_COUNT[9][0], "802108");
    strcpy(STATS_TABLE_COUNT[10][0], "802109");
    strcpy(STATS_TABLE_COUNT[11][0], "802110");
    strcpy(STATS_TABLE_COUNT[12][0], "802111");
    strcpy(STATS_TABLE_COUNT[13][0], "802112");
    strcpy(STATS_TABLE_COUNT[14][0], "802113");
    strcpy(STATS_TABLE_COUNT[15][0], "802114");
    strcpy(STATS_TABLE_COUNT[16][0], "802115");
    strcpy(STATS_TABLE_COUNT[17][0], "802116");
    strcpy(STATS_TABLE_COUNT[18][0], "802117");
    strcpy(STATS_TABLE_COUNT[19][0], "802118");
    strcpy(STATS_TABLE_COUNT[20][0], "802119");
    strcpy(STATS_TABLE_COUNT[21][0], "802120");
    /* ************************* S8025XX ************************** */
    strcpy(STATS_TABLE_COUNT[22][0], "802500");
    strcpy(STATS_TABLE_COUNT[23][0], "802501");
    strcpy(STATS_TABLE_COUNT[24][0], "802502");
    strcpy(STATS_TABLE_COUNT[25][0], "802503");
    strcpy(STATS_TABLE_COUNT[26][0], "802504");
    strcpy(STATS_TABLE_COUNT[27][0], "802505");
    strcpy(STATS_TABLE_COUNT[28][0], "802506");
    strcpy(STATS_TABLE_COUNT[29][0], "802507");
    strcpy(STATS_TABLE_COUNT[30][0], "802508");
    strcpy(STATS_TABLE_COUNT[31][0], "802509");
    strcpy(STATS_TABLE_COUNT[32][0], "802510");
    /* ************************* S8026XX ************************** */
    strcpy(STATS_TABLE_COUNT[33][0], "802600");
    strcpy(STATS_TABLE_COUNT[34][0], "802601");
    strcpy(STATS_TABLE_COUNT[35][0], "802602");
    strcpy(STATS_TABLE_COUNT[36][0], "802603");
    strcpy(STATS_TABLE_COUNT[37][0], "802604");
    strcpy(STATS_TABLE_COUNT[38][0], "802605");
    strcpy(STATS_TABLE_COUNT[39][0], "802606");
    strcpy(STATS_TABLE_COUNT[40][0], "802607");
    strcpy(STATS_TABLE_COUNT[41][0], "802608");
    strcpy(STATS_TABLE_COUNT[42][0], "802609");
    strcpy(STATS_TABLE_COUNT[43][0], "802610");
    /* ************************* S8024XX ************************** */
    strcpy(STATS_TABLE_COUNT[44][0], "802400");
    strcpy(STATS_TABLE_COUNT[45][0], "802401");
    strcpy(STATS_TABLE_COUNT[46][0], "802402");
    strcpy(STATS_TABLE_COUNT[47][0], "802403");
    strcpy(STATS_TABLE_COUNT[48][0], "802404");
    strcpy(STATS_TABLE_COUNT[49][0], "802405");
    strcpy(STATS_TABLE_COUNT[50][0], "802406");
    strcpy(STATS_TABLE_COUNT[51][0], "802407");
    strcpy(STATS_TABLE_COUNT[52][0], "802408");
    strcpy(STATS_TABLE_COUNT[53][0], "802409");
    strcpy(STATS_TABLE_COUNT[54][0], "802410");

    /* *********************** Copy Table ************************* */
    memcpy(STATS_TABLE_PROB, STATS_TABLE_COUNT, sizeof(STATS_TABLE_PROB));

    /* ************************* Separate ************************* */
    printf("[ Statistics ] Init Stats Table: Finished.\n");
}

//统计ND1S803XXX。
void statistics_ND1S803XXX(struct Finance* Ptr_Cmptd_Fin, int Cmptd_Rows_Num) {

    init_stats_table();

    /* ***************** Compute S803XXX Quantity ***************** */
    //外层循环(第1层)。
    for (int row = 1; row < STATS_TABLE_ROWS_NUM; row++) {

        //内层循环(第2层)。
        for (int col = 1; col < (STATS_TABLE_COLS_NUM - 1); col++) { //排除Amount列。

            int Total;

            //内层循环(第3层)。
            for (int i = 0; i < Cmptd_Rows_Num; i++) {

                char Buffer[21];
                Total = atoi(STATS_TABLE_COUNT[row][col]);

                //条件判断。
                if (atoi(STATS_TABLE_COUNT[row][0]) == (Ptr_Cmptd_Fin + i)->S8021XX &&
                    atoi(STATS_TABLE_COUNT[0][col]) == (Ptr_Cmptd_Fin + i)->ND1S803XXX)

                    Total += 1;

                else if (atoi(STATS_TABLE_COUNT[row][0]) == (Ptr_Cmptd_Fin + i)->S8025XX &&
                         atoi(STATS_TABLE_COUNT[0][col]) == (Ptr_Cmptd_Fin + i)->ND1S803XXX)

                    Total += 1;

                else if (atoi(STATS_TABLE_COUNT[row][0]) == (Ptr_Cmptd_Fin + i)->S8026XX &&
                         atoi(STATS_TABLE_COUNT[0][col]) == (Ptr_Cmptd_Fin + i)->ND1S803XXX)

                    Total += 1;

                else if (atoi(STATS_TABLE_COUNT[row][0]) == (Ptr_Cmptd_Fin + i)->S8024XX &&
                         atoi(STATS_TABLE_COUNT[0][col]) == (Ptr_Cmptd_Fin + i)->ND1S803XXX)

                    Total += 1;
                //条件判断：结束。

                itoa(Total, Buffer, 10);
                strcpy(STATS_TABLE_COUNT[row][col], Buffer);
            }
            //内层循环(第3层): 结束。
        }
        //内层循环(第2层): 结束。
    }
    //外层循环(第1层)。: 结束。

    /* ************* Compute ND1S803XXX Count Amount ************** */
    //外层循环(第1层)。
    for (int row = 1; row < STATS_TABLE_ROWS_NUM; row++) {

        char Char_Buffer[21];
        int Amt = 0;

        //内层循环(第2层)。
        for (int col = 1; col < (STATS_TABLE_COLS_NUM - 1); col++) { //排除Amount列。

            Amt += atoi(STATS_TABLE_COUNT[row][col]);
        }
        //内层循环(第2层): 结束。

        itoa(Amt, Char_Buffer, 10);
        strcpy(STATS_TABLE_COUNT[row][22], Char_Buffer);
    }
    //外层循环(第1层)。: 结束。

    /* ************** Compute ND1S803XXX Probability ************** */
    //外层循环(第1层)。
    for (int row = 1; row < STATS_TABLE_ROWS_NUM; row++) {

        double dividend;
        dividend = atof(STATS_TABLE_COUNT[row][22]);

        //内层循环(第2层)。
        for (int col = 1; col < (STATS_TABLE_COLS_NUM - 1); col++) { //排除Amount列。

            if (dividend != 0.0) {

                double divisor;
                divisor = atof(STATS_TABLE_COUNT[row][col]);

                double result;
                result = divisor / dividend;

                sprintf(STATS_TABLE_PROB[row][col], "%.4f", result);
            }
        }
        //内层循环(第2层): 结束。
    }
    //外层循环(第1层)。: 结束。

    /* ************************* Separate ************************* */
    printf("[ Statistics ] Statistic ND1S803XXX: Finished.\n");

    /* ************************ Debugging ************************* */
    FILE* Debug_fp_1;
    FILE* Debug_fp_2;
    Debug_fp_1 = fopen("./CSV_Debugging_Statistic_Count.csv","w");
    Debug_fp_2 = fopen("./CSV_Debugging_Statistic_Prob.csv","w");

    for (int row = 0; row < STATS_TABLE_ROWS_NUM; row++) {

        for (int col = 0; col < STATS_TABLE_COLS_NUM; col++) {

            fprintf(Debug_fp_1, "%8s|", STATS_TABLE_COUNT[row][col]);
            fprintf(Debug_fp_2, "%8s|", STATS_TABLE_PROB[row][col]);
        }

        fprintf(Debug_fp_1,"\n");
        fprintf(Debug_fp_2,"\n");
    }

    fclose(Debug_fp_1);
    fclose(Debug_fp_2);
}