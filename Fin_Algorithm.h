//
// Created by GF on 2023/2/21.
//

#ifndef FIN_ALGORITHM_H
#define FIN_ALGORITHM_H

void EXE_Algorithm_Running(struct Finance* Ptr_Fin, int Rows_Num);

//结构体数据计算Timestamp并存入结构体。
void compute_timestamp(struct Finance* Ptr_Fin, int Rows_Num);

void compute_rise_fall_amt(struct Finance* Ptr_Fin, int Rows_Num);

void compute_rise_fall_rate(struct Finance* Ptr_Fin, int Rows_Num);

void compute_S803XXX(struct Finance* Ptr_Fin, int Rows_Num);

void compute_S8021XX(struct Finance* Ptr_Fin, int Rows_Num);

void compute_S8025XX(struct Finance* Ptr_Fin, int Rows_Num);

void compute_S8026XX(struct Finance* Ptr_Fin, int Rows_Num);

void compute_S8024XX(struct Finance* Ptr_Fin, int Rows_Num);

void compute_ND1S803XXX(struct Finance* Ptr_Fin, int Rows_Num);

#endif //FIN_ALGORITHM_H
