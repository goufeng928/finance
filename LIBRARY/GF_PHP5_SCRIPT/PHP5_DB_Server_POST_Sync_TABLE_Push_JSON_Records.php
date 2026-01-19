<?php

/*
 * GF_PHP5_SCRIPT/PHP5_DB_Server_POST_Sync_TABLE_Push_JSON_Records.php
 * Create by GF 2025-10-23 19:30
 */

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

// ##################################################

// 只接受 POST 请求
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {

    http_response_code(405);
    // ..............................................
    echo json_encode(['status' => 'error', 'message' => 'Method not allowed']);
    // ..............................................
    exit;
}

// ##################################################

// 使用 php://input 流读取原始的 JSON 数据
$input = file_get_contents('php://input');
$data  = json_decode($input, true);

// ##################################################

// 检查 JSON 解码是否成功
if (json_last_error() !== JSON_ERROR_NONE) {

    http_response_code(400);
    // ..............................................
    echo json_encode(['status' => 'error', 'message' => 'Invalid JSON data']);
    // ..............................................
    exit;
}

// ##################################################

function Conv_2D_Associative_Array_to_2D_Indexed_Array($The_2D_Associative_Array) {

    /*
     * Example for "Convert 2D Associative Array to 2D Indexed Array":
     * php > $The_2D_Associative_Array = array(
     * php *     array("id" => 1, "name" => "Jack", "age" => 19, "email" => "jack@example.com"),
     * php *     array("id" => 2, "name" => "Alice", "age" => 20, "email" => "alice@example.com"),
     * php *     array("id" => 3, "name" => "John", "age" => 22, "email" => "john@example.com"));
     * php > $The_2D_Indexed_Array = Conv_2D_Associative_Array_to_2D_Indexed_Array($The_2D_Associative_Array);
     * php > print_r($The_2D_Indexed_Array);
     * Array(
     *     [0] => Array([0] => 1, [1] => "Jack", [2] => 19, [3] => "jack@example.com"),
     *     [1] => Array([0] => 2, [1] => "Alice", [2] => 20, [3] => "alice@example.com"),
     *     [2] => Array([0] => 3, [1] => "John", [2] => 22, [3] => "john@example.com")
     * )
     */

    $The_2D_Indexed_Array = array();
    // ..............................................
    foreach ($The_2D_Associative_Array as $Key => $Row) {

        // 转换为普通二维数组 (去掉内层关联键名)
        $Indexed_Array = array_values($Row);
        // ..........................................
        // 向数组 (Array) 末尾添加元素
        array_push($The_2D_Indexed_Array, $Indexed_Array);
    }
    // ..............................................
    return $The_2D_Indexed_Array;
}

function Conv_2D_Indexed_Array_to_1D_Params_Array($The_2D_Indexed_Array) {

    /*
     * Example for "Convert 2D Indexed Array to 1D Params Array":
     * php > $The_2D_Indexed_Array = array(
     * php *     0 => array(0 => 1, 1 => "Jack", 2 => 19, 3 => "jack@example.com"),
     * php *     1 => array(0 => 2, 1 => "Alice", 2 => 20, 3 => "alice@example.com"),
     * php *     2 => array(0 => 3, 1 => "John", 2 => 22, 3 => "john@example.com"));
     * php > $The_1D_Params_Array = Conv_2D_Indexed_Array_to_1D_Params_Array($The_2D_Indexed_Array);
     * php > print_r($The_1D_Params_Array);
     * Array([0] => 1, [1] => "Jack", [2] => 19, [3] => "jack@example.com",
     *       [4] => 2, [5] => "Alice", [6] => 20, [7] => "alice@example.com",
     *       [8] => 3, [9] => "John", [10] => 22, [11] => "john@example.com")
     */

    $The_1D_Params_Array = array();
    // ..............................................
    foreach ($The_2D_Indexed_Array as $Idx => $The_1D_Indexed_Array) {
        foreach ($The_1D_Indexed_Array as $i => $Value) {

            // 向数组 (Array) 末尾添加元素
            array_push($The_1D_Params_Array, $Value);
        }
    }
    // ..............................................
    return $The_1D_Params_Array;
}

// ##################################################

// 获取 JSON 包含的请求参数 (使用三元表达式)
$DB_TABLE     = isset($data["db_table"])     ? $data["db_table"]     : "unknow";
$JSON_Records = isset($data["json_records"]) ? $data["json_records"] : array(array("unknow" => "unknow"));
// ..................................................
$JSON_Records_Rows_Count   = count($JSON_Records);
$JSON_Records_Rows_Max_Idx = $JSON_Records_Rows_Count -1;

/*
 * 获取关联数组中第 1 个子关联数组的所有键
 * php > $Associative_Array = array(
 * php *     array("id" => 1, "name" => "Jack", "age" => 19, "email" => "jack@example.com"),
 * php *     array("id" => 2, "name" => "Alice", "age" => 20, "email" => "alice@example.com"),
 * php *     array("id" => 3, "name" => "John", "age" => 22, "email" => "john@example.com"));
 * php > $Associative_Array_Keys = array_keys($Associative_Array[0]);
 * php > print_r($Associative_Array_Keys);
 * Array( [0] => id, [1] => name, [2] => age, [3] => email )
 */
$JSON_Records_Keys         = array_keys($JSON_Records[0]);
$JSON_Records_Keys_Count   = count($JSON_Records_Keys);
$JSON_Records_Keys_Max_Idx = $JSON_Records_Keys_Count - 1;

// ##################################################

/*
 * 根据 JSON Records 组合 SQL 语句
 * ..................................................
 * 如果 JSON Records = [{"name": "Jack", "age": 19, "email": "jack@example.com"}];
 * 那么 SQL 语句 = "INSERT INTO finance (name, age, email) VALUES (?, ?, ?);"
 * ..................................................
 * 如果 JSON Records = [{"name": "Jack", "age": 19, "email": "jack@example.com"},
 *                      {"name": "Alice", "age": 20, "email": "alice@example.com"},
 *                      {"name": "John", "age": 22, "email": "john@example.com"}];
 * 那么 SQL 语句 = "INSERT INTO finance (name, age, email) VALUES (?, ?, ?), (?, ?, ?), (?, ?, ?);"
 */
$SQL_Statment_INSERT_INTO  = "INSERT INTO ";
$SQL_Statment_TABLE_FIELDS = $DB_TABLE . " (";
$SQL_Statment_VALUES       = "VALUES (";
// ..................................................
for ($Row = 0; $Row <= $JSON_Records_Rows_Max_Idx; $Row++) {

    if ($Row == 0) {

        for ($Col = 0; $Col <= $JSON_Records_Keys_Max_Idx; $Col++) {

            $SQL_Statment_TABLE_FIELDS = $SQL_Statment_TABLE_FIELDS . $JSON_Records_Keys[$Col];
            $SQL_Statment_VALUES       = $SQL_Statment_VALUES . "?";
            // ......................................
            if ($Col < $JSON_Records_Keys_Max_Idx) {
                $SQL_Statment_TABLE_FIELDS = $SQL_Statment_TABLE_FIELDS . ", ";
                $SQL_Statment_VALUES       = $SQL_Statment_VALUES . ", ";
            }
            // ......................................
            if ($Col == $JSON_Records_Keys_Max_Idx) {
                $SQL_Statment_TABLE_FIELDS = $SQL_Statment_TABLE_FIELDS . ") ";
                $SQL_Statment_VALUES       = $SQL_Statment_VALUES . ")";
            }
        }
    }

    if ($Row >= 1) {

        $SQL_Statment_VALUES = $SQL_Statment_VALUES . ", (";

        for ($Col = 0; $Col <= $JSON_Records_Keys_Max_Idx; $Col++) {

            $SQL_Statment_VALUES = $SQL_Statment_VALUES . "?";
            // ......................................
            if ($Col < $JSON_Records_Keys_Max_Idx) {
                $SQL_Statment_VALUES = $SQL_Statment_VALUES . ", ";
            }
            // ......................................
            if ($Col == $JSON_Records_Keys_Max_Idx) {
                $SQL_Statment_VALUES = $SQL_Statment_VALUES . ")";
            }
        }
    }
}
// ..................................................
$SQL_Statment = $SQL_Statment_INSERT_INTO . $SQL_Statment_TABLE_FIELDS . $SQL_Statment_VALUES . ';';

// ##################################################

include_once "../GF_PHP7_CLASS/PHP7_PDO_PGSQL16.php";

$OBJECT_PHP7_PDO_PGSQL16 = new PHP7_PDO_PGSQL16();
$OBJECT_PHP7_PDO_PGSQL16->HOST     = "host.docker.internal";
$OBJECT_PHP7_PDO_PGSQL16->DB_NAME  = "finance";
$OBJECT_PHP7_PDO_PGSQL16->USER     = "goufeng";
$OBJECT_PHP7_PDO_PGSQL16->PASSWORD = "abcd1234";
$OBJECT_PHP7_PDO_PGSQL16->Init();

$The_1D_Params_Array = Conv_2D_Indexed_Array_to_1D_Params_Array($JSON_Records);
// ..................................................
$Execute_Result = $OBJECT_PHP7_PDO_PGSQL16->Execute($SQL_Statment, $The_1D_Params_Array);
// ..................................................
echo json_encode(['status' => 'success',
                  'message' => 'The execution result is '. $Execute_Result,
                  'affected_rows' => $JSON_Records_Rows_Count]);

// ##################################################

/*
 * 使用 cURL 进行测试 (单条 Record):
 * curl -X POST -H 'Content-Type: application/json' \
 *      -d '{"db_table": "users", "json_records": [{"name": "Jack", "age": 20, "email": "jack@mail.com"}]}' \
 *      "http://127.0.0.1:8080/GF_PHP5_SCRIPT/PHP5_DB_Server_POST_Sync_TABLE_Push_JSON_Records.php"
 *
 * 使用 cURL 进行测试 (多条 Record):
 * curl -X POST -H 'Content-Type: application/json' \
 *      -d '{"db_table": "users", "json_records": [{"name": "Jack", "age": 20}, {"name": "Alice", "age": 21}]}' \
 *      "http://127.0.0.1:8080/GF_PHP5_SCRIPT/PHP5_DB_Server_POST_Sync_TABLE_Push_JSON_Records.php"
 */

?>
