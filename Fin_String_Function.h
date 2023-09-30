//
// Created by GF on 2023/3/11.
//

#ifndef FIN_STRING_FUNCTION_H
#define FIN_STRING_FUNCTION_H

int StringLocChar(const char* Str, char Ch);

int CharExistInChArr(char* ChArr, char Ch);

//字符串就地截断。
void StringOnTheSpotCutOff(char* Str, char Ch);

//字符串就地删除单个选定字符。
void StringOnTheSpotDelSingleChar(char* Str, char Ch);

//字符串就地删除所有选定字符。
void StringOnTheSpotDelAllChar(char* Str, char Ch);

#endif //FIN_STRING_FUNCTION_H
