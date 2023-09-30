//
// Created by GF on 2023/3/4.
//

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "Fin_Header.h"
#include "Fin_Text_Function.h"

// External Functions Needed.
// [- StringOnTheSpotCutOff]
#include "Fin_String_Function.h"

void ASCII_Judge() {

    FILE* fp1, * fp2;
    signed char ch_ascii; //如果是char类型来保存ASCII，则保存的汉字值为负数。
    //int ch_ascii; //如果是int类型来保存ASCII，则保存的汉字值为200以上的3位数。

    //CSV文件需要转换成GBK或GB2312编码，否则中文输出为乱码。
    fp1 = fopen("./ASCII_Judge_Input.csv", "r");
    fp2 = fopen("./ASCII_Judge_Result.csv", "w");

    if (fp1 == NULL) {
        printf("[ Function ] ASCII Judge: Open CSV Failed.\n");
    }
    else {
        while ((ch_ascii = (signed char)getc(fp1)) != EOF) {
            //ASCII码中，10为\n(换行符)。
            if (ch_ascii != 10) fprintf(fp2, "%d,", ch_ascii);
            else putc(ch_ascii, fp2);
        }
        printf("[ Function ] ASCII Judge: Finished, Result File in \"./ASCII_Judge_Result.csv\"\n");
    }
    fclose(fp1);
    fclose(fp2);
}

//读取CSV文件数据到动态内存数组。
char* CsvToMem(const char* CsvPath) {

    FILE* fp;
    signed char Ch_ASCII;

    //malloc分配空间地址后返回的是一个指针。
    char* Content = Content = (char*)malloc(sizeof(char) * 3); //因为1个汉字占2-3个Char。

    //CSV文件需要转换成GBK或GB2312编码，否则中文输出为乱码。
    fp = fopen(CsvPath, "r");

    if (fp == NULL) {

        printf("[ Function ] CSV To Memory: Open CSV Failed.\n");

        fclose(fp);

        return NULL;

    } else {

        int i = 0;
        while ((Ch_ASCII = (signed char)getc(fp)) != EOF) {

            //ASCII码中，32为SPACE(空格)，34为"(英文双引号)，39为'(英文单引号)。
            if (Ch_ASCII != 32 && Ch_ASCII != 34 && Ch_ASCII != 39) { //条件判断用于清洗扔掉不要的数据。

                Content[i] = Ch_ASCII;

                //分配一个全新的内存空间。
                Content = realloc(Content, (sizeof(char) * (i + 2) * 3));

                i++;
            }
        }
        printf("[ Function ] CSV To Memory: Finished.\n");

        fclose(fp);

        return Content;
    }
}

//利用getc清洗原始CSV文件并保存到新文件。
void wash_org_csv_by_getc(char* Org_CSV_Path) {

    FILE* fp1, * fp2;
    int ch_ascii;

    //CSV文件需要转换成GBK或GB2312编码，否则中文输出为乱码。
    fp1 = fopen(Org_CSV_Path, "r");
    fp2 = fopen("./CSV_Pretreated.csv", "w");

    if (fp1 == NULL) {
        printf("[ Function ] Wash Org CSV: Open CSV Failed.\n");
    }
    else {
        while ((ch_ascii = getc(fp1)) != EOF) {
            //ASCII码中，32为SPACE(空格)，34为"(英文双引号)，39为'(英文单引号)。
            if (ch_ascii != 32 && ch_ascii != 34 && ch_ascii != 39) putc(ch_ascii, fp2);
        }
        printf("[ Function ] Wash Org CSV: Finished, Washed File in \"./CSV_Pretreated.csv\"\n");
    }
    fclose(fp1);
    fclose(fp2);
}

//计数CSV文件内首行的字段数。
int CsvFieldsNum(char* CsvPath) {

    FILE *fp;
    int ch_ascii, field_num = 0;

    fp = fopen(CsvPath, "r");

    if (fp == NULL) {
        printf("[ Function Error ] CSV Fields Num: Open CSV Failed.\n");
    } else {
        while ((ch_ascii = getc(fp)) != 10) { //十进制ASCII码"10"为"LF/NL"，也就是"\n"。
            //十进制ASCII码"44"为","，也就是"英文逗号"。
            if (ch_ascii == 44) field_num += 1;
        }
        field_num = field_num + 1;
        printf("[ Function ] CSV Fields Num: Finished, Have %d Field.\n", field_num);
    }
    fclose(fp);

    return field_num;
}

//计数CSV文件内数据的行数。
int CsvRowsNum(char* CsvPath, int Header) {

    FILE *fp;
    int rows_num = 0;
    char row[500];

    fp = fopen(CsvPath, "r");

    if (fp == NULL) {
        printf("[ Function Error ] CSV Rows Num: Open CSV Failed.\n");
    } else {
        while (fgets(row, 500, fp)) rows_num += 1;
    }
    fclose(fp);

    //设定Option选项，如果Option的值为1，则行数包含表头，如果Option的值为0，则行数不包含表头。
    if (Header == 0) {
        rows_num = rows_num - 1;
        printf("[ Function ] CSV Rows Num: Finished, Have %d Rows (None-Header).\n", rows_num);
        return rows_num;
    } else { //或者 Header == 1。
        printf("[ Function ] CSV Rows Num: Finished, Have %d Rows (Have-Header).\n", rows_num);
        return rows_num;
    }

}

//CSV字段顺序初始化。
void CsvFieldSeqLoad() {

    FILE* fp;
    char trash50[50];

    fp = fopen("./CSV_Field_Name_Seq_CH_zh_GB18030.csv", "r");

    if (fp == NULL) {

        printf("[ Function Error ] CSV Field Seq Load: Load Field Name&Seq File Failed.\n");

        fclose(fp);

        return;

    } else {

        for (int i = 0; i < LOADED_FIELD_ROWS_NUM; i++) {

            fgets(trash50, 50, fp);

            //fgets会读取换行符，将换行符替换为结束符，便于后面字符串的对比。
            StringOnTheSpotCutOff(trash50, '\n');

            char* ptr_str;

            ptr_str = strtok(trash50, ",");
            LOADED_FIELD_SEQ[i] = atoi(ptr_str);

            ptr_str = strtok(NULL, ",");
            strcpy(LOADED_FIELD_NAME[i], ptr_str);
        }

        printf("[ Function ] CSV Field Seq Load: Load Field Name&Seq File Successful.\n");

        fclose(fp);
    }
}

//查询CSV文件内首行的字段顺序。
void CsvFieldSeqQuery(char* CsvPath) {

    CsvFieldSeqLoad();

    /* ************************* Separate ************************* */
    FILE *fp;
    char row[500];

    fp = fopen(CsvPath, "r");

    if (fp == NULL) {

        printf("[ Function Error ] CSV Field Seq Query: Open CSV Failed.\n");

        fclose(fp);

        return;

    } else {

        fgets(row, 500, fp);

        //fgets会读取换行符，将换行符替换为结束符，便于后面字符串的对比。
        StringOnTheSpotCutOff(row, '\n');

        int i = 0;
        const char* delim = ",";
        char* ptr_str;

        ptr_str = strtok(row, delim);
        while (ptr_str != NULL && i < FIELDS_NUM) {

            if (strcmp(ptr_str, LOADED_FIELD_NAME[0]) == 0) FIELD_SEQ_Date = i;
            else if (strcmp(ptr_str, LOADED_FIELD_NAME[1]) == 0) FIELD_SEQ_Name = i;
            else if (strcmp(ptr_str, LOADED_FIELD_NAME[2]) == 0) FIELD_SEQ_Code = i;
            else if (strcmp(ptr_str, LOADED_FIELD_NAME[3]) == 0) FIELD_SEQ_Open = i;
            else if (strcmp(ptr_str, LOADED_FIELD_NAME[4]) == 0) FIELD_SEQ_High = i;
            else if (strcmp(ptr_str, LOADED_FIELD_NAME[5]) == 0) FIELD_SEQ_Low = i;
            else if (strcmp(ptr_str, LOADED_FIELD_NAME[6]) == 0) FIELD_SEQ_Close = i;
            else if (strcmp(ptr_str, LOADED_FIELD_NAME[7]) == 0) FIELD_SEQ_Pre_Close = i;
            else if (strcmp(ptr_str, LOADED_FIELD_NAME[11]) == 0) FIELD_SEQ_Volume = i;

            ptr_str = strtok(NULL, delim);
            i++;
        }
        printf("[ Function ] CSV Field Seq Query: Assign Sequence Number Finished.\n");

        fclose(fp);
    }
}

//读取CSV数据并保存到结构变量中。
void CsvToMemToStruct(struct Finance** PPtr_Fin, char* CsvPath) {

    ROWS_NUM = CsvRowsNum(CsvPath, 0);
    FIELDS_NUM = CsvFieldsNum(CsvPath);
    CsvFieldSeqQuery(CsvPath);

    /* ************************* Separate ************************* */
    char* MemCsv = CsvToMem(CsvPath);

    /* ************************* Separate ************************* */
    *PPtr_Fin = (struct Finance*)malloc(sizeof(struct Finance) * ROWS_NUM);

    /* ************************* Separate ************************* */
    FILE *fp;
    char Row500[500], Trash500[500];
    int ReadCharNum = 0;
    int ReadCharTotalNum = 0;
    unsigned long long MemCsvLen = strlen(MemCsv);

    //CSV文件需要转换成GBK编码，否则中文输出为乱码。
    fp = fopen(CsvPath, "r");

    if (fp == NULL) {

        printf("[ Function Error ] CSV To Mem To Struct: Open CSV Failed.\n");

        fclose(fp);

        return;

    } else {

        //丢弃表头行。
        sscanf(MemCsv, "%s%n", Trash500, &ReadCharNum);

        MemCsv += ReadCharNum;

        ReadCharTotalNum += ReadCharNum;

        for (int i = 0; i < ROWS_NUM && ReadCharTotalNum <= MemCsvLen; i++) {

            sscanf(MemCsv, "%s%n", Row500, &ReadCharNum);

            MemCsv += ReadCharNum;

            ReadCharTotalNum += ReadCharNum;

            int k = 0;
            const char* sep = ",";
            char* ptr_str;

            ptr_str = strtok(Row500, sep);
            while (ptr_str != NULL && k < FIELDS_NUM) {

                if (k == FIELD_SEQ_Date) strcpy((*PPtr_Fin + i)->Date, ptr_str);
                else if (k == FIELD_SEQ_Name) strcpy((*PPtr_Fin + i)->Name, ptr_str);
                else if (k == FIELD_SEQ_Code) strcpy((*PPtr_Fin + i)->Code, ptr_str);
                else if (k == FIELD_SEQ_Open) (*PPtr_Fin + i)->Open = atof(ptr_str);
                else if (k == FIELD_SEQ_High) (*PPtr_Fin + i)->High = atof(ptr_str);
                else if (k == FIELD_SEQ_Low) (*PPtr_Fin + i)->Low = atof(ptr_str);
                else if (k == FIELD_SEQ_Close) (*PPtr_Fin + i)->Close = atof(ptr_str);
                else if (k == FIELD_SEQ_Pre_Close) (*PPtr_Fin + i)->Pre_Close = atof(ptr_str);
                else if (k == FIELD_SEQ_Volume) (*PPtr_Fin + i)->Volume = atof(ptr_str);

                ptr_str = strtok(NULL, sep);
                k++;
            }
        }
        printf("[ Function ] CSV To Mem To Struct: Finished.\n");

        fclose(fp);
    }
}

//读取计算后的CSV数据并保存到结构变量中。
void Computed_Csv_To_Struct(struct Finance** PPtr_Cmptd_Fin, char* CsvPath) {

    CMPTD_ROWS_NUM = CsvRowsNum(CsvPath, 0);

    int Fields_Num = CsvFieldsNum(CsvPath);

    /* ************************* Separate ************************* */
    *PPtr_Cmptd_Fin = (struct Finance*)malloc(sizeof(struct Finance) * CMPTD_ROWS_NUM);

    /* ************************* Separate ************************* */
    FILE *fp;
    char Row500[500], Trash500[500];
    char ch_cell[Fields_Num][13];

    //CSV文件需要转换成GBK编码，否则中文输出为乱码。
    fp = fopen(CsvPath, "r");

    if (fp == NULL) {

        printf("[ Function Error ] Computed CSV To Struct: Open CSV Failed.\n");

        fclose(fp);

        return;

    } else {

        //把fp指针移动到离文件开头 0 字节处，SEEK_SET 与 0 是等价的。
        //fseek(fp,0L,SEEK_SET);
        fseek(fp,0L,0);

        //利用fgets的特性，读到换行符后文件指针自动下移，以便于跳过表头。
        fgets(Trash500, 500, fp);

        for (int i = 0; i < CMPTD_ROWS_NUM; i++) {

            fgets(Row500, 500, fp);

            char* ptr_cell;
            int j = 0;

            ptr_cell = strtok(Row500, ",");
            while (ptr_cell != NULL && j < Fields_Num) {

                strcpy(ch_cell[j], ptr_cell);

                ptr_cell = strtok(NULL, ",");

                j++;
            }

            strcpy((*PPtr_Cmptd_Fin + i)->Date,ch_cell[0]); /* Col.01: Date */
            strcpy((*PPtr_Cmptd_Fin + i)->Name,ch_cell[1]); /* Col.02: Name */
            strcpy((*PPtr_Cmptd_Fin + i)->Code,ch_cell[2]); /* Col.03: Code */

            (*PPtr_Cmptd_Fin + i)->Open = atof(ch_cell[3]); /* Col.04: Open */
            (*PPtr_Cmptd_Fin + i)->High = atof(ch_cell[4]); /* Col.05: High */
            (*PPtr_Cmptd_Fin + i)->Low = atof(ch_cell[5]); /* Col.06: Low */
            (*PPtr_Cmptd_Fin + i)->Close = atof(ch_cell[6]); /* Col.07: Close */
            (*PPtr_Cmptd_Fin + i)->Pre_Close = atof(ch_cell[7]); /* Col.08: Pre Close */
            (*PPtr_Cmptd_Fin + i)->Rise_Fall_Rate = atof(ch_cell[8]); /* Col.09: Rise Fall Amt */
            (*PPtr_Cmptd_Fin + i)->Rise_Fall_Rate = atof(ch_cell[9]); /* Col.10: Rise Fall Rate */
            (*PPtr_Cmptd_Fin + i)->Volume = atof(ch_cell[10]); /* Col.11: Volume */

            (*PPtr_Cmptd_Fin + i)->S803XXX = atoi(ch_cell[11]); /* Col.12: S803XXX */
            (*PPtr_Cmptd_Fin + i)->ND1S803XXX = atoi(ch_cell[12]); /* Col.13: ND1S803XXX */
            (*PPtr_Cmptd_Fin + i)->S8021XX = atoi(ch_cell[13]); /* Col.14: S8021XX */
            (*PPtr_Cmptd_Fin + i)->S8025XX = atoi(ch_cell[14]); /* Col.15: S8025XX */
            (*PPtr_Cmptd_Fin + i)->S8026XX = atoi(ch_cell[15]); /* Col.16: S8026XX */
            (*PPtr_Cmptd_Fin + i)->S8024XX = atoi(ch_cell[16]); /* Col.17: S8024XX */
        }
        printf("[ Function ] Computed CSV Date To Struct: Finished.\n");

        fclose(fp);
    }
}
