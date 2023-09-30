//
// Created by GF on 2023/2/21.
//

#include <stdio.h>

#include "Fin_Header.h"
#include "Fin_Algorithm.h"

// External Functions Needed.
// [- time_stamp_use_char_by_mktime]
#include "Fin_Time_Function.h"

void EXE_Algorithm_Running(struct Finance* Ptr_Fin, int Rows_Num) {

    compute_rise_fall_amt(Ptr_Fin, Rows_Num);
    compute_rise_fall_rate(Ptr_Fin, Rows_Num);
    compute_S803XXX(Ptr_Fin, Rows_Num);
    compute_S8021XX(Ptr_Fin, Rows_Num);
    compute_S8025XX(Ptr_Fin, Rows_Num);
    compute_S8026XX(Ptr_Fin, Rows_Num);
    compute_S8024XX(Ptr_Fin, Rows_Num);
    compute_ND1S803XXX(Ptr_Fin, Rows_Num);
}

//结构体数据计算Timestamp并存入结构体。
void compute_timestamp(struct Finance* Ptr_Fin, int Rows_Num) {

    for (int i = 0; i < Rows_Num; i++) {
        (Ptr_Fin + i)->TimeStamp = time_stamp_use_char_by_mktime((Ptr_Fin + i)->Date);
    }

    printf("[ Algorithm ] Compute Timestamp: Finished.\n");
}

void compute_rise_fall_amt(struct Finance* Ptr_Fin, int Rows_Num) {

    for (int i = 0; i < Rows_Num; i++) {

        Ptr_Fin->Rise_Fall_Amt = Ptr_Fin->Close - Ptr_Fin->Pre_Close;
        Ptr_Fin += 1;
    }
}

void compute_rise_fall_rate(struct Finance* Ptr_Fin, int Rows_Num) {

    for (int i = 0; i < Rows_Num; i++) {

        if (Ptr_Fin->Volume == 0) {
            Ptr_Fin->Rise_Fall_Rate = 0;
        } else {
            Ptr_Fin->Rise_Fall_Rate = Ptr_Fin->Rise_Fall_Amt / Ptr_Fin->Pre_Close;
        }
        Ptr_Fin += 1;
    }
}

void compute_S803XXX(struct Finance* Ptr_Fin, int Rows_Num) {

    for (int i=0; i<Rows_Num; i++) {

        if (Ptr_Fin->Rise_Fall_Rate == 0) {
            Ptr_Fin->S803XXX = 803500;

            //100、101与00、01无异，因为C语言不允许0开头的整数，只能用1作为填充，这样能够将样本数量扩大到101个数的范围(100~199个样本，单0代表NULL)。

        } else if (0 < Ptr_Fin->Rise_Fall_Rate && Ptr_Fin->Rise_Fall_Rate <= 0.01) {
            Ptr_Fin->S803XXX = 803601; //"0.001 ~ 0.010"。
        } else if (0.01 < Ptr_Fin->Rise_Fall_Rate && Ptr_Fin->Rise_Fall_Rate <= 0.02) {
            Ptr_Fin->S803XXX = 803602; //"0.011 ~ 0.020"。
        } else if (0.02 < Ptr_Fin->Rise_Fall_Rate && Ptr_Fin->Rise_Fall_Rate <= 0.03) {
            Ptr_Fin->S803XXX = 803603; //"0.021 ~ 0.030"。
        } else if (0.03 < Ptr_Fin->Rise_Fall_Rate && Ptr_Fin->Rise_Fall_Rate <= 0.04) {
            Ptr_Fin->S803XXX = 803604; //"0.031 ~ 0.040"。
        } else if (0.04 < Ptr_Fin->Rise_Fall_Rate && Ptr_Fin->Rise_Fall_Rate <= 0.05) {
            Ptr_Fin->S803XXX = 803605; //"0.041 ~ 0.050"。
        } else if (0.05 < Ptr_Fin->Rise_Fall_Rate && Ptr_Fin->Rise_Fall_Rate <= 0.06) {
            Ptr_Fin->S803XXX = 803606; //"0.051 ~ 0.060"。
        } else if (0.06 < Ptr_Fin->Rise_Fall_Rate && Ptr_Fin->Rise_Fall_Rate <= 0.07) {
            Ptr_Fin->S803XXX = 803607; //"0.061 ~ 0.070"。
        } else if (0.07 < Ptr_Fin->Rise_Fall_Rate && Ptr_Fin->Rise_Fall_Rate <= 0.08) {
            Ptr_Fin->S803XXX = 803608; //"0.071 ~ 0.080"。
        } else if (0.08 < Ptr_Fin->Rise_Fall_Rate && Ptr_Fin->Rise_Fall_Rate <= 0.09) {
            Ptr_Fin->S803XXX = 803609; //"0.081 ~ 0.090"。
        } else if (0.09 < Ptr_Fin->Rise_Fall_Rate && Ptr_Fin->Rise_Fall_Rate <= 0.10) {
            Ptr_Fin->S803XXX = 803610; //"0.091 ~ 0.100"。
        } else if (0.10 < Ptr_Fin->Rise_Fall_Rate) {
            Ptr_Fin->S803XXX = 803610; //"0.101 ~ 1.000"。

        } else if (-0.01 <= Ptr_Fin->Rise_Fall_Rate && Ptr_Fin->Rise_Fall_Rate < 0) {
            Ptr_Fin->S803XXX = 803401; //"-0.010 ~ -0.001"。
        } else if (-0.02 <= Ptr_Fin->Rise_Fall_Rate && Ptr_Fin->Rise_Fall_Rate < -0.01) {
            Ptr_Fin->S803XXX = 803402; //"-0.020 ~ -0.011"。
        } else if (-0.03 <= Ptr_Fin->Rise_Fall_Rate && Ptr_Fin->Rise_Fall_Rate < -0.02) {
            Ptr_Fin->S803XXX = 803403; //"-0.030 ~ -0.021"。
        } else if (-0.04 <= Ptr_Fin->Rise_Fall_Rate && Ptr_Fin->Rise_Fall_Rate < -0.03) {
            Ptr_Fin->S803XXX = 803404; //"-0.040 ~ -0.031"。
        } else if (-0.05 <= Ptr_Fin->Rise_Fall_Rate && Ptr_Fin->Rise_Fall_Rate < -0.04) {
            Ptr_Fin->S803XXX = 803405; //"-0.050 ~ -0.041"。
        } else if (-0.06 <= Ptr_Fin->Rise_Fall_Rate && Ptr_Fin->Rise_Fall_Rate < -0.05) {
            Ptr_Fin->S803XXX = 803406; //"-0.060 ~ -0.051"。
        } else if (-0.07 <= Ptr_Fin->Rise_Fall_Rate && Ptr_Fin->Rise_Fall_Rate < -0.06) {
            Ptr_Fin->S803XXX = 803407; //"-0.070 ~ -0.061"。
        } else if (-0.08 <= Ptr_Fin->Rise_Fall_Rate && Ptr_Fin->Rise_Fall_Rate < -0.07) {
            Ptr_Fin->S803XXX = 803408; //"-0.080 ~ -0.071"。
        } else if (-0.09 <= Ptr_Fin->Rise_Fall_Rate && Ptr_Fin->Rise_Fall_Rate < -0.08) {
            Ptr_Fin->S803XXX = 803409; //"-0.090 ~ -0.081"。
        } else if (-0.10 <= Ptr_Fin->Rise_Fall_Rate && Ptr_Fin->Rise_Fall_Rate < -0.09) {
            Ptr_Fin->S803XXX = 803410; //"-0.100 ~ -0.091"。
        } else if (Ptr_Fin->Rise_Fall_Rate < -0.10) {
            Ptr_Fin->S803XXX = 803410; //"-1.000 ~ -0.101"。
        }

        Ptr_Fin += 1;
    }

}

void compute_S8021XX(struct Finance* Ptr_Fin, int Rows_Num) {

    double fluctuation_range, amp;

    for (int i=0; i < Rows_Num; i++) {

        fluctuation_range = (Ptr_Fin+i)->High - (Ptr_Fin+i)->Low;

        if ((Ptr_Fin+i)->Pre_Close != 0.0) amp = fluctuation_range / (Ptr_Fin+i)->Pre_Close;
        else amp = 0.0;

        //A股市场是10%的涨跌幅限制，所以振幅最大是20%。
        if (amp == 0.000) {
            (Ptr_Fin+i)->S8021XX = 802100;
        } else if (0.00 < amp && amp <= 0.01) {
            (Ptr_Fin+i)->S8021XX = 802101;
        } else if (0.01 < amp && amp <= 0.02) {
            (Ptr_Fin+i)->S8021XX = 802102;
        } else if (0.02 < amp && amp <= 0.03) {
            (Ptr_Fin+i)->S8021XX = 802103;
        } else if (0.03 < amp && amp <= 0.04) {
            (Ptr_Fin+i)->S8021XX = 802104;
        } else if (0.04 < amp && amp <= 0.05) {
            (Ptr_Fin+i)->S8021XX = 802105;
        } else if (0.05 < amp && amp <= 0.06) {
            (Ptr_Fin+i)->S8021XX = 802106;
        } else if (0.06 < amp && amp <= 0.07) {
            (Ptr_Fin+i)->S8021XX = 802107;
        } else if (0.07 < amp && amp <= 0.08) {
            (Ptr_Fin+i)->S8021XX = 802108;
        } else if (0.08 < amp && amp <= 0.09) {
            (Ptr_Fin+i)->S8021XX = 802109;
        } else if (0.09 < amp && amp <= 0.10) {
            (Ptr_Fin+i)->S8021XX = 802110;
        } else if (0.10 < amp && amp <= 0.11) {
            (Ptr_Fin+i)->S8021XX = 802111;
        } else if (0.11 < amp && amp <= 0.12) {
            (Ptr_Fin+i)->S8021XX = 802112;
        } else if (0.12 < amp && amp <= 0.13) {
            (Ptr_Fin+i)->S8021XX = 802113;
        } else if (0.13 < amp && amp <= 0.14) {
            (Ptr_Fin+i)->S8021XX = 802114;
        } else if (0.14 < amp && amp <= 0.15) {
            (Ptr_Fin+i)->S8021XX = 802115;
        } else if (0.15 < amp && amp <= 0.16) {
            (Ptr_Fin+i)->S8021XX = 802116;
        } else if (0.16 < amp && amp <= 0.17) {
            (Ptr_Fin+i)->S8021XX = 802117;
        } else if (0.17 < amp && amp <= 0.18) {
            (Ptr_Fin+i)->S8021XX = 802118;
        } else if (0.18 < amp && amp <= 0.19) {
            (Ptr_Fin+i)->S8021XX = 802119;
        } else if (0.19 < amp && amp <= 0.20) {
            (Ptr_Fin+i)->S8021XX = 802120;
        } else if (0.20 < amp) {
            (Ptr_Fin+i)->S8021XX = 802120;
        }
    }
}

void compute_S8025XX(struct Finance* Ptr_Fin, int Rows_Num) {

    double fluctuation_range, candle_entity;
    double close_open_difference; // 收盘价与开盘价的差额。

    for (int i = 0; i < Rows_Num; i++) {

        fluctuation_range = (Ptr_Fin + i)->High - (Ptr_Fin + i)->Low;
        close_open_difference = (Ptr_Fin + i)->Close - (Ptr_Fin + i)->Open;

        if (close_open_difference == 0.0) candle_entity = 0.0;
        else if (0.0 < close_open_difference) candle_entity = (Ptr_Fin + i)->Close - (Ptr_Fin + i)->Open;
        else if (close_open_difference < 0.0) candle_entity = (Ptr_Fin + i)->Open - (Ptr_Fin + i)->Close;

        if ((candle_entity / fluctuation_range) == 0.0) {
            (Ptr_Fin + i)->S8025XX = 802500;
        } else if (0.0 < (candle_entity / fluctuation_range) && (candle_entity / fluctuation_range) <= 0.1) {
            (Ptr_Fin + i)->S8025XX = 802501;
        } else if (0.1 < (candle_entity / fluctuation_range) && (candle_entity / fluctuation_range) <= 0.2) {
            (Ptr_Fin + i)->S8025XX = 802502;
        } else if (0.2 < (candle_entity / fluctuation_range) && (candle_entity / fluctuation_range) <= 0.3) {
            (Ptr_Fin + i)->S8025XX = 802503;
        } else if (0.3 < (candle_entity / fluctuation_range) && (candle_entity / fluctuation_range) <= 0.4) {
            (Ptr_Fin + i)->S8025XX = 802504;
        } else if (0.4 < (candle_entity / fluctuation_range) && (candle_entity / fluctuation_range) <= 0.5) {
            (Ptr_Fin + i)->S8025XX = 802505;
        } else if (0.5 < (candle_entity / fluctuation_range) && (candle_entity / fluctuation_range) <= 0.6) {
            (Ptr_Fin + i)->S8025XX = 802506;
        } else if (0.6 < (candle_entity / fluctuation_range) && (candle_entity / fluctuation_range) <= 0.7) {
            (Ptr_Fin + i)->S8025XX = 802507;
        } else if (0.7 < (candle_entity / fluctuation_range) && (candle_entity / fluctuation_range) <= 0.8) {
            (Ptr_Fin + i)->S8025XX = 802508;
        } else if (0.8 < (candle_entity / fluctuation_range) && (candle_entity / fluctuation_range) <= 0.9) {
            (Ptr_Fin + i)->S8025XX = 802509;
        } else if (0.9 < (candle_entity / fluctuation_range) && (candle_entity / fluctuation_range) <= 1.0) {
            (Ptr_Fin + i)->S8025XX = 802510;
        }
    }
}

void compute_S8026XX(struct Finance* Ptr_Fin, int Rows_Num) {

    double fluctuation_range, candle_upper_hatching;
    double close_open_difference; // 收盘价与开盘价的差额。

    for (int i = 0; i < Rows_Num; i++) {

        fluctuation_range = (Ptr_Fin + i)->High - (Ptr_Fin + i)->Low;
        close_open_difference = (Ptr_Fin + i)->Close - (Ptr_Fin + i)->Open;

        if (close_open_difference == 0.0) candle_upper_hatching = 0.0;
        else if (0.0 < close_open_difference) candle_upper_hatching = (Ptr_Fin + i)->High - (Ptr_Fin + i)->Close;
        else if (close_open_difference < 0.0) candle_upper_hatching = (Ptr_Fin + i)->High - (Ptr_Fin + i)->Open;

        if ((candle_upper_hatching / fluctuation_range) == 0.0) {
            (Ptr_Fin + i)->S8026XX = 802600;
        } else if (0.0 < (candle_upper_hatching / fluctuation_range) && (candle_upper_hatching / fluctuation_range) <= 0.1) {
            (Ptr_Fin + i)->S8026XX = 802601;
        } else if (0.1 < (candle_upper_hatching / fluctuation_range) && (candle_upper_hatching / fluctuation_range) <= 0.2) {
            (Ptr_Fin + i)->S8026XX = 802602;
        } else if (0.2 < (candle_upper_hatching / fluctuation_range) && (candle_upper_hatching / fluctuation_range) <= 0.3) {
            (Ptr_Fin + i)->S8026XX = 802603;
        } else if (0.3 < (candle_upper_hatching / fluctuation_range) && (candle_upper_hatching / fluctuation_range) <= 0.4) {
            (Ptr_Fin + i)->S8026XX = 802604;
        } else if (0.4 < (candle_upper_hatching / fluctuation_range) && (candle_upper_hatching / fluctuation_range) <= 0.5) {
            (Ptr_Fin + i)->S8026XX = 802605;
        } else if (0.5 < (candle_upper_hatching / fluctuation_range) && (candle_upper_hatching / fluctuation_range) <= 0.6) {
            (Ptr_Fin + i)->S8026XX = 802606;
        } else if (0.6 < (candle_upper_hatching / fluctuation_range) && (candle_upper_hatching / fluctuation_range) <= 0.7) {
            (Ptr_Fin + i)->S8026XX = 802607;
        } else if (0.7 < (candle_upper_hatching / fluctuation_range) && (candle_upper_hatching / fluctuation_range) <= 0.8) {
            (Ptr_Fin + i)->S8026XX = 802608;
        } else if (0.8 < (candle_upper_hatching / fluctuation_range) && (candle_upper_hatching / fluctuation_range) <= 0.9) {
            (Ptr_Fin + i)->S8026XX = 802609;
        } else if (0.9 < (candle_upper_hatching / fluctuation_range) && (candle_upper_hatching / fluctuation_range) <= 1.0) {
            (Ptr_Fin + i)->S8026XX = 802610;
        }
    }
}

void compute_S8024XX(struct Finance* Ptr_Fin, int Rows_Num) {

    double fluctuation_range, candle_lower_hatching;
    double close_open_difference; // 收盘价与开盘价的差额。

    for (int i = 0; i < Rows_Num; i++) {

        fluctuation_range = (Ptr_Fin + i)->High - (Ptr_Fin + i)->Low;
        close_open_difference = (Ptr_Fin + i)->Close - (Ptr_Fin + i)->Open;

        if (close_open_difference == 0.0) candle_lower_hatching = 0.0;
        else if (0.0 < close_open_difference) candle_lower_hatching = (Ptr_Fin + i)->Open - (Ptr_Fin + i)->Low;
        else if (close_open_difference < 0.0) candle_lower_hatching = (Ptr_Fin + i)->Close - (Ptr_Fin + i)->Low;

        if ((candle_lower_hatching / fluctuation_range) == 0.0) {
            (Ptr_Fin + i)->S8024XX = 802400;
        } else if (0.0 < (candle_lower_hatching / fluctuation_range) && (candle_lower_hatching / fluctuation_range) <= 0.1) {
            (Ptr_Fin + i)->S8024XX = 802401;
        } else if (0.1 < (candle_lower_hatching / fluctuation_range) && (candle_lower_hatching / fluctuation_range) <= 0.2) {
            (Ptr_Fin + i)->S8024XX = 802402;
        } else if (0.2 < (candle_lower_hatching / fluctuation_range) && (candle_lower_hatching / fluctuation_range) <= 0.3) {
            (Ptr_Fin + i)->S8024XX = 802403;
        } else if (0.3 < (candle_lower_hatching / fluctuation_range) && (candle_lower_hatching / fluctuation_range) <= 0.4) {
            (Ptr_Fin + i)->S8024XX = 802404;
        } else if (0.4 < (candle_lower_hatching / fluctuation_range) && (candle_lower_hatching / fluctuation_range) <= 0.5) {
            (Ptr_Fin + i)->S8024XX = 802405;
        } else if (0.5 < (candle_lower_hatching / fluctuation_range) && (candle_lower_hatching / fluctuation_range) <= 0.6) {
            (Ptr_Fin + i)->S8024XX = 802406;
        } else if (0.6 < (candle_lower_hatching / fluctuation_range) && (candle_lower_hatching / fluctuation_range) <= 0.7) {
            (Ptr_Fin + i)->S8024XX = 802407;
        } else if (0.7 < (candle_lower_hatching / fluctuation_range) && (candle_lower_hatching / fluctuation_range) <= 0.8) {
            (Ptr_Fin + i)->S8024XX = 802408;
        } else if (0.8 < (candle_lower_hatching / fluctuation_range) && (candle_lower_hatching / fluctuation_range) <= 0.9) {
            (Ptr_Fin + i)->S8024XX = 802409;
        } else if (0.9 < (candle_lower_hatching / fluctuation_range) && (candle_lower_hatching / fluctuation_range) <= 1.0) {
            (Ptr_Fin + i)->S8024XX = 802410;
        }
    }
}

void compute_ND1S803XXX(struct Finance* Ptr_Fin, int Rows_Num) {

    PTR_STU_COL_ND1S803XXX = &(*Ptr_Fin).ND1S803XXX;
    PTR_STU_COL_S803XXX = &(*Ptr_Fin).S803XXX;

    int* Ptr_Forecast = PTR_STU_COL_ND1S803XXX;
    int* Ptr_Sample = PTR_STU_COL_S803XXX;

    /* ************************* Separate ************************* */
    struct Finance Fin[2];

    /* ************************* Separate ************************* */
    //取出一些结构体的指针参数。
    long long Ptr_Dis_Int = &Fin[1].ND1S803XXX - &Fin[0].ND1S803XXX;

    /* ************************* Separate ************************* */
    long long STEP = Ptr_Dis_Int;

    /* ************************* Separate ************************* */
    long long limit_max = Ptr_Dis_Int * Rows_Num;
    long long limit_loop = limit_max - STEP;

    /* ************************* Separate ************************* */
    for (long long i = 0; i <= limit_loop; i += STEP) {

        if (i == limit_max) {

            *(Ptr_Forecast + i) = 0;//赋值0代表NULL。

        } else {

            *(Ptr_Forecast + i) = *(Ptr_Sample + i + STEP);
        }
        //条件判断结束。
    }
    //循环结束。
    printf("[ Algorithm ] Compute ND1S803XXX: Finished.\n");
}
