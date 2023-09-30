//
// Created by GF on 2023/3/11.
//

#include <stdio.h>
#include <string.h>

#include "Fin_String_Function.h"

int StringLocChar(const char* Str, char Ch) {

    int i = 0;

    while (Str[i] != Ch && i < strlen(Str)) i++;

    return i;
}

int CharExistInChArr(char* ChArr, char Ch) {

    if (strlen(ChArr) == 0) {

        return 0;

    } else {

        int Counter = 0;

        for (int i = 0; i < strlen(ChArr); i++) {

            if (Ch == ChArr[i]) Counter += 1;
        }

        return Counter;
    }
}

//字符串就地截断。
void StringOnTheSpotCutOff(char* Str, char Ch) {

    char* PCH;
    char Match[2] = {Ch, '\0'};

    PCH = strstr(Str, Match);

    //特别针对fgets会读取换行符，将换行符替换为结束符，更便于存储取用。
    if (PCH != NULL) *PCH = '\0';
}

//字符串就地删除单个选定字符。
void StringOnTheSpotDelSingleChar(char* Str, char Ch) {

    char* Exist;
    char Match[2] = {Ch, '\0'};

    Exist = strstr(Str, Match);

    /* ******************** Separate ******************** */

    if (strlen(Str) == 0 || Exist == NULL) {

        return;

    } else if (strlen(Str) == 1 && Exist != NULL) {

        Str[0] = '\0';

    } else if (strlen(Str) > 1 && Exist != NULL) {

        char CopyChArr1[strlen(Str)];
        char CopyChArr2[strlen(Str)];

        strcpy(CopyChArr1, Str);

        /* ******************** Separate ******************** */

        char* PCH;

        PCH = strstr(CopyChArr1, Match);

        if (PCH != NULL) *PCH = '\0';

        /* ******************** Separate ******************** */

        PCH += 1;

        strcpy(CopyChArr2, PCH);

        strcpy(Str, strcat(CopyChArr1,CopyChArr2));
    }
}

//字符串就地删除所有选定字符。
void StringOnTheSpotDelAllChar(char* Str, char Ch) {

    char* Exist;
    char Match[2] = {Ch, '\0'};

    Exist = strstr(Str, Match);

    /* ******************** Separate ******************** */

    if (strlen(Str) == 0 || Exist == NULL) {

        return;

    } else if (strlen(Str) == 1 && Exist != NULL) {

        Str[0] = '\0';

    } else if (strlen(Str) > 1 && Exist != NULL) {

        char CopyChArr1[strlen(Str)];
        char CopyChArr2[strlen(Str)];

        strcpy(CopyChArr1, Str);

        /* ******************** Separate ******************** */

        char* PCH;

        PCH = strstr(CopyChArr1, Match);
        while (PCH != NULL) {

            *PCH = '\0';

            PCH += 1;

            strcpy(CopyChArr2, PCH);

            strcpy(CopyChArr1, strcat(CopyChArr1,CopyChArr2));

            PCH = strstr(CopyChArr1, Match);
        }

        strcpy(Str, CopyChArr1);
    }
}