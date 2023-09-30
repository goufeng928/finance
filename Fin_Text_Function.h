//
// Created by GF on 2023/3/4.
//

#ifndef FIN_TEXT_FUNCTION_H
#define FIN_TEXT_FUNCTION_H

void ASCII_Judge();

//读取CSV文件数据到动态内存数组。
char* CsvToMem(const char* CsvPath);

//利用getc清洗原始CSV文件并保存到新文件。
void wash_org_csv_by_getc(char* Org_CSV_Path);

//计数CSV文件内首行的字段数。
int CsvFieldsNum(char* CsvPath);

//计数CSV文件内数据的行数。
int CsvRowsNum(char* CsvPath, int Header);

//CSV字段顺序初始化。
void CsvFieldSeqLoad();

//查询CSV文件内首行的字段顺序。
void CsvFieldSeqQuery(char* CsvPath);

//读取CSV数据并保存到结构变量中。
void CsvToMemToStruct(struct Finance** PPtr_Fin, char* CsvPath);

//读取计算后的CSV数据并保存到结构变量中。
void Computed_Csv_To_Struct(struct Finance** PPtr_Cmptd_Fin, char* CsvPath);

#endif //FIN_TEXT_FUNCTION_H
