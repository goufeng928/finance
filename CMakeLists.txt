cmake_minimum_required(VERSION 3.16)
project(finance_analysis C)

set(CMAKE_C_STANDARD 99)

add_executable(finance_analysis main.c
               Fin_Header.c
               Fin_Header.h
               Fin_Text_Function.c
               Fin_Text_Function.h
               Fin_Struct_Function.c
               Fin_Struct_Function.h
               Fin_Time_Function.c
               Fin_Time_Function.h
               Fin_Algorithm.c
               Fin_Algorithm.h
               Fin_Statistics_Function.c
               Fin_Statistics_Function.h
               Fin_Analysis_Function.c
               Fin_Analysis_Function.h
               Fin_String_Function.c
               Fin_String_Function.h)