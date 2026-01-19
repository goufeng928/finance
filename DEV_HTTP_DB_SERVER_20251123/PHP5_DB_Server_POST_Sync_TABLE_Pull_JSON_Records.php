<?php

/*
 * GF_PHP5_SCRIPT/PHP5_DB_Server_POST_Sync_TABLE_Pull_JSON_Records.php
 * Create by GF 2025-10-23 19:30
 */

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

// ##################################################

$Query_Rows_Number_Limit = 10000;

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

function Conv_Associative_Array_to_JSON_Records($Associative_Array) {

    /*
     * Example for "Convert Associative Array to JSON Records":
     * php > $Associative_Array = array(
     * php *     array("id" => 1, "name" => "Jack", "age" => 19, "email" => "jack@example.com"),
     * php *     array("id" => 2, "name" => "Alice", "age" => 20, "email" => "alice@example.com"),
     * php *     array("id" => 3, "name" => "John", "age" => 22, "email" => "john@example.com"));
     * php > $STRING_JSON_Record = Conv_Associative_Array_to_JSON_Records($Associative_Array = $Associative_Array);
     * php > echo $STRING_JSON_Record;
     * [
     *     {"id": 1, "name": "Jack", "age": 19, "email": "jack@example.com"},
     *     {"id": 2, "name": "Alice", "age": 20, "email": "alice@example.com"},
     *     {"id": 3, "name": "John", "age": 22, "email": "john@example.com"}
     * ]
     */

    $Rsult = array();
    // ..............................................
    $ASSOCIATIVE_ARRAY_LENGTH = count($Associative_Array);

    for ($i = 0; $i <= $ASSOCIATIVE_ARRAY_LENGTH - 1; $i++) {

        $Record = $Associative_Array[$i];
        // ..........................................
        // 向数组 (Array) 末尾添加元素
        array_push($Rsult, $Record);
    }

    /*
     * 函数示例: json_encode()
     * php > $array = ["name" => "Jack", "age" => 25, "城市" => "北京"];
     * php > $json = json_encode($array);
     * php > echo $json;
     * {"name": "Jack", "age": 25, "\u57ce\u5e02": "\u5317\u4eac"}
     *
     * 函数示例: json_encode() 带 JSON_UNESCAPED_UNICODE 参数处理中文字符
     * php > $array = ["name" => "Jack", "age" => 25, "城市" => "北京"];
     * php > $json = json_encode($array, JSON_UNESCAPED_UNICODE);
     * php > echo $json;
     * {"name": "Jack", "age": 25, "城市": "北京"}
     */
    return json_encode($Rsult, JSON_UNESCAPED_UNICODE);
}

// ##################################################

// 获取 JSON 包含的请求参数 (使用三元表达式)
$DB_Type       = isset($data["db_type"])       ? $data["db_type"]       : "unknow";
$SQL_Statement = isset($data["sql_statement"]) ? $data["sql_statement"] : "unknow";
// ..................................................
if (substr($SQL_Statement, -1) == ';') $SQL_Statement = substr_replace($SQL_Statement, '', -1);

// ##################################################
// PostgreSQL 查询过程

if ($DB_Type == "postgresql") {

    // 创建 PostgreSQL 连接对象
    include_once "PHP5_PDO_PGSQL16.php";
    // ..............................................
    $OBJECT_PHP5_PDO_PGSQL16 = new PHP5_PDO_PGSQL16();
    $OBJECT_PHP5_PDO_PGSQL16->HOST     = "192.168.81.1";
    $OBJECT_PHP5_PDO_PGSQL16->DB_NAME  = "postgres";
    $OBJECT_PHP5_PDO_PGSQL16->USER     = "reader";
    $OBJECT_PHP5_PDO_PGSQL16->PASSWORD = "abcd1234";
    $Init_Result = $OBJECT_PHP5_PDO_PGSQL16->Init();

    // 检查 PostgreSQL 连接是否成功
    if ($Init_Result != "success") {
        http_response_code(500);
        echo json_encode(['status' => 'error', 'message' => 'Database connection failed']);
        exit;
    }

    // 验证 PostgreSQL 查询目标的行数
    $SQL_Statement_Count_Rows = "SELECT COUNT(*) as rows_num FROM (" . $SQL_Statement . ");";
    $Queried                  = $OBJECT_PHP5_PDO_PGSQL16->Query($SQL_Statement_Count_Rows);
    $Query_Target_Rows_Num    = $Queried[0]["rows_num"];
    // ..............................................
    if ($Query_Target_Rows_Num > $Query_Rows_Number_Limit) {
        echo json_encode(["status" => 'failure', "message" => "Each query cannot exceed " . $Query_Rows_Number_Limit . " rows"]);
        exit;
    }

    // 执行 PostgreSQL 查询语句
    $SQL_Statement = $SQL_Statement . ';';
    $Queried       = $OBJECT_PHP5_PDO_PGSQL16->Query($SQL_Statement);
    // ..............................................
    $STRING_JSON_Record = Conv_Associative_Array_to_JSON_Records($Queried);
    // ..............................................
    echo $STRING_JSON_Record;
    exit;
}

// ##################################################

/*
 * 使用 cURL 进行测试:
 * curl -X POST -H 'Content-Type: application/json' \
 *      -d '{"db_type": "postgresql", "sql_statement": "SELECT * FROM logs;"}' \
 *      "http://127.0.0.1/PHP5_DB_Server_POST_Sync_TABLE_Pull_JSON_Records.php"
 */

?>
