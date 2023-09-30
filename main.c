//
// Created by GF on 2023/2/20.
//

#include <stdio.h>
#include "Fin_Header.h"
#include "Fin_Text_Function.h"
#include "Fin_Struct_Function.h"
#include "Fin_Algorithm.h"
#include "Fin_Statistics_Function.h"
#include "Fin_Analysis_Function.h"

int main() {

    //初始化结构体。
    struct Finance* Ptr_Fin;

    CsvToMemToStruct(&Ptr_Fin, "./000422.csv"); /* ROWS_NUM 首次赋值 */

    ROWS_NUM = ROWS_NUM - StructDeleteRow(Ptr_Fin, ROWS_NUM);

    StructBubblesortByTime(Ptr_Fin, ROWS_NUM);

    EXE_Algorithm_Running(Ptr_Fin, ROWS_NUM);

    //计算后得结构体数据写入CSV。
    Computed_Struct_To_Csv(Ptr_Fin, ROWS_NUM);

    printf("******************** Separate ********************\n");

    //初始化结构体。
    struct Finance *Ptr_Cmptd_Fin;

    //读取计算后的CSV数据并保存到结构变量中。
    Computed_Csv_To_Struct(&Ptr_Cmptd_Fin,"./CSV_Computed.csv"); /* CMPTD_ROWS_NUM 首次赋值 */

    statistics_ND1S803XXX(Ptr_Cmptd_Fin, CMPTD_ROWS_NUM);

    //初始化结构体(输入数据)。
    struct Finance* Ptr_Input_Fin;

    Analysis(&Ptr_Input_Fin);

    //显示结构体数据(原始数据 & 计算数据)。
    //display_struct_part_data(ptr_cmpt_stu, cmpt_rows_num);

    return 0;
}
