//
// Created by GF on 2023/2/20.
//

#include <stdio.h>
#include <string.h>
#include "Fin_Header.h"
#include "Fin_Struct_Function.h"

// External Functions Needed.
// [- compute_timestamp]
#include "Fin_Algorithm.h"

//结构体数据删除指定行并返回删除行数。
int StructDeleteRow(struct Finance* Ptr_Fin, int Rows_Num) {

    int deleted_num = 0, matched_num = 0;

    //for循环比对每一行是否符合删除条件，并执行相应操作。
    for (int i = 0; i < Rows_Num; i++) {

        if ((Ptr_Fin + i)->Volume == 0) {
            //记录共有多少行需要删除，便于后面与真正删除的行数比对，如果数量一致则无问题。
            matched_num += 1;
            //在结构成员变量"备注"中添加"DELETE"标记以便其它操作。
            strcpy((Ptr_Fin + i)->Remarks, "DELETED");
        }
    }

    for (int i = 0; i < Rows_Num; i++) {

        //如果符合删除条件，是则将后面的行向前覆盖。
        if (strcmp((Ptr_Fin + i)->Remarks, "DELETED") == 0 && i != (Rows_Num - 1)) {
            for (int k = i; k < Rows_Num - 1; k++) {

                *(Ptr_Fin + k) = *(Ptr_Fin + k + 1);
                //或者 memcpy((Ptr_Fin + k), (Ptr_Fin + k + 1), sizeof(*(Ptr_Fin + k)));
            }

            int Ptr_Fin_Mem_Num = Rows_Num - deleted_num - 1;
            //将逐行向前覆盖后，末尾多出来的行填充0或清空结构体内数据。
            memset((Ptr_Fin + Ptr_Fin_Mem_Num), 0, sizeof(*(Ptr_Fin + Ptr_Fin_Mem_Num)));
            //记录删除了多少行。
            deleted_num += 1;
            //删除一行后将i回退到上一行，以避免"需删除的行B"覆盖"需删除的行A"，i递增后就会跳过"需删除的行B"。
            i--;

        } else if (strcmp((Ptr_Fin + i)->Remarks, "DELETED") == 0 && i == (Rows_Num - 1)) {

            //记录删除了多少行。
            deleted_num += 1;
        }
    }

    if (deleted_num == matched_num) {
        printf("[ Function ] Struct Delete Row: Finished, Delete %d Row.\n", deleted_num);
    } else {
        printf("[ Function Error ] Struct Delete Row: Matched Rows %d, Deleted %d.\n",matched_num, deleted_num);
    }

    /* ************************* Separate ************************* */

    return deleted_num;
}

//结构体数据冒泡排序(按时间升序)。
void StructBubblesortByTime(struct Finance* Ptr_Fin, int Rows_Num) {

    compute_timestamp(Ptr_Fin, Rows_Num);

    /* ************************* Separate ************************* */
    struct Finance temp_stu_for_sort;

    int skip = 0;

    //外层循环: 确保循环次数。
    for (int i = 0; i <= Rows_Num; i++) {

        //内层循环: 对比每两行数据并交换位置。
        for (int j = 0, k = 1; j < (Rows_Num - 1) || k < Rows_Num; j++, k++) {

            if ((Ptr_Fin+j)->TimeStamp == (Ptr_Fin+k)->TimeStamp) {

                skip += 1;
            } else if ((Ptr_Fin+j)->TimeStamp > (Ptr_Fin+k)->TimeStamp) {

                //三杯水交换法。
                temp_stu_for_sort = *(Ptr_Fin+j);

                *(Ptr_Fin+j) = *(Ptr_Fin+k);

                *(Ptr_Fin+k) = temp_stu_for_sort;
            }
        }
        //内层循环: 结束。
    }
    //外层循环: 结束。

    printf("[ Function ] Struct Bubblesort By Time: Sort Finished.\n");
}

//计算后的结构体数据写入CSV。
void Computed_Struct_To_Csv(struct Finance *ptr_stu, int rows_num) {

    FILE *fp;

    fp = fopen("./CSV_Computed.csv", "w");

    if (fp == NULL) {
        printf("[ Function Error ] Computed Struct Data To CSV: Open CSV Failed.\n");
    }else {

        /* Col.01: Date */fprintf(fp,"%s,", "Date");
        /* Col.02: Name */fprintf(fp,"%s,", "Name");
        /* Col.03: Code */fprintf(fp,"%s,", "Code");
        /* Col.04: Open */fprintf(fp,"%s,", "Open");
        /* Col.05: High */fprintf(fp,"%s,", "High");
        /* Col.06: Low */fprintf(fp,"%s,", "Low");
        /* Col.07: Close */fprintf(fp,"%s,", "Close");
        /* Col.08: Pre Close */fprintf(fp,"%s,", "Pre_Close");
        /* Col.09: Rise Fall Amt */fprintf(fp,"%s,", "Rise_Fall_Amt");
        /* Col.10: Rise Fall Rate */fprintf(fp,"%s,", "Rise_Fall_Rate");
        /* Col.11: Volume */fprintf(fp,"%s,", "Volume");
        /* Col.12: S803XXX */fprintf(fp,"%s,", "S803XXX");
        /* Col.13: ND1S803XXX */fprintf(fp,"%s,", "ND1S803XXX");
        /* Col.14: S8021XX */fprintf(fp,"%s,", "S8021XX");
        /* Col.15: S8025XX */fprintf(fp,"%s,", "S8025XX");
        /* Col.16: S8026XX */fprintf(fp,"%s,", "S8026XX");
        /* Col.17: S8024XX */fprintf(fp,"%s\n", "S8024XX");

        for (int i = 0; i < rows_num; i++) {

            /* Col.01: Date */fprintf(fp,"%s,", ptr_stu->Date);
            /* Col.02: Name */fprintf(fp,"%s,", ptr_stu->Name);
            /* Col.03: Code */fprintf(fp,"%s,", ptr_stu->Code);
            /* Col.04: Open */fprintf(fp,"%.4f,", ptr_stu->Open);
            /* Col.05: High */fprintf(fp,"%.4f,", ptr_stu->High);
            /* Col.06: Low */fprintf(fp,"%.4f,", ptr_stu->Low);
            /* Col.07: Close */fprintf(fp,"%.4f,", ptr_stu->Close);
            /* Col.08: Pre Close */fprintf(fp,"%.4f,", ptr_stu->Pre_Close);
            /* Col.09: Rise Fall Amt */fprintf(fp,"%.4f,", ptr_stu->Rise_Fall_Amt);
            /* Col.10: Rise Fall Rate */fprintf(fp,"%.4f,", ptr_stu->Rise_Fall_Rate);
            /* Col.11: Volume */fprintf(fp,"%.4f,", ptr_stu->Volume);
            /* Col.12: S803XXX */fprintf(fp,"%d,", ptr_stu->S803XXX);
            /* Col.13: ND1S803XXX */fprintf(fp,"%d,", ptr_stu->ND1S803XXX);
            /* Col.14: S8021XX */fprintf(fp,"%d,", ptr_stu->S8021XX);
            /* Col.15: S8025XX */fprintf(fp,"%d,", ptr_stu->S8025XX);
            /* Col.16: S8026XX */fprintf(fp,"%d,", ptr_stu->S8026XX);
            /* Col.17: S8024XX */fprintf(fp,"%d\n", ptr_stu->S8024XX);

            ptr_stu += 1;
        }
        printf("[ Function ] Computed Struct Data To CSV: Finished.\n");

    }
    fclose(fp);

}

//显示结构体数据(原始数据 & 计算数据)。
void display_struct_data(struct Finance* ptr_stu, int rows_num) {

    for (int i=0; i<rows_num; i++) {

        printf("%s,%s,%s,", (ptr_stu+i)->Date, (ptr_stu+i)->Name, (ptr_stu+i)->Code);
        printf("%.4f,%d,",(ptr_stu+i)->Rise_Fall_Rate, (ptr_stu+i)->S803XXX);
        printf("%d,", (ptr_stu+i)->S8026XX);
        printf("%d\n", (ptr_stu+i)->S8024XX);
    }
    //函数运行结束: 打印函数提示。
    printf("[ Function ] Display Struct Part Data: Display Finished, Total in %d rows\n", rows_num);
}