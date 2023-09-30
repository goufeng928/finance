//
// Created by GF on 2023/3/6.
//

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "Fin_Time_Function.h"

//mktime读取日期生成时间戳(改良版本: 传入字符串自动分解tm参数)。
int time_stamp_use_char_by_mktime(char* datetime) {

    char Ch_Year[5], Ch_Month[3], Ch_Day[3];
    int Year, Month, Day;

    sscanf(datetime, "%[0-9]-%[0-9]-%[0-9]", Ch_Year, Ch_Month, Ch_Day);
    Year = atoi(Ch_Year); Month = atoi(Ch_Month); Day = atoi(Ch_Day);

    //创建并初始化time_t类型数据。
    time_t res_sec = 0;

    struct tm p;
    p.tm_year = Year-1900;
    p.tm_mon = Month-1;
    p.tm_mday = Day;
    p.tm_hour = 0;
    p.tm_min = 0;
    p.tm_sec = 0;
    p.tm_isdst = 0;

    res_sec = mktime(&p);

    //time(&res_sec)函数将现在的时间转换成秒并保存在res_sec变量中。
    //time(&res_sec);

    return res_sec;
}