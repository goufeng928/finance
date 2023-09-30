//
// Created by GF on 2023/2/20.
//

#ifndef FIN_STRUCT_FUNCTION_H
#define FIN_STRUCT_FUNCTION_H

//结构体数据删除指定行并返回删除行数。
int StructDeleteRow(struct Finance* Ptr_Fin, int Rows_Num);

//结构体数据冒泡排序(按时间升序)。
void StructBubblesortByTime(struct Finance* Ptr_Fin, int Rows_Num);

//计算后的结构体数据写入CSV。
void Computed_Struct_To_Csv(struct Finance *ptr_stu, int rows_num);

//显示结构体数据(原始数据 & 计算数据)。
void display_struct_data(struct Finance *pstu, int rows_num);

#endif //FIN_STRUCT_FUNCTION_H
