<?php

/*
 * GF_PHP5_SCRIPT/PHP5_HTTP_Server_POST_Pull_JSON_Records.php
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

    $Result = array();
    // ..............................................
    $ASSOCIATIVE_ARRAY_LENGTH = count($Associative_Array);

    for ($i = 0; $i <= $ASSOCIATIVE_ARRAY_LENGTH - 1; $i++) {

        $Record = $Associative_Array[$i];
        // ..........................................
        // 向数组 (Array) 末尾添加元素
        array_push($Result, $Record);
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
    return json_encode($Result, JSON_UNESCAPED_UNICODE);
}

// ##################################################

include_once "GF_PHP7_PDO_PGSQL16.php";

$OBJECT_PHP7_PDO_PGSQL16 = new PHP7_PDO_PGSQL16();
$OBJECT_PHP7_PDO_PGSQL16->HOST     = "host.docker.internal";
$OBJECT_PHP7_PDO_PGSQL16->DB_NAME  = "finance";
$OBJECT_PHP7_PDO_PGSQL16->USER     = "goufeng";
$OBJECT_PHP7_PDO_PGSQL16->PASSWORD = "abcd1234";
$OBJECT_PHP7_PDO_PGSQL16->Init();

// ##################################################

$Associative_Array = array(array("id" => 1, "name" => "Jack", "age" => 19, "email" => "jack@example.com"),
                           array("id" => 2, "name" => "Alice", "age" => 20, "email" => "alice@example.com"),
                           array("id" => 3, "name" => "John", "age" => 22, "email" => "john@example.com"));
//$Associative_Array = $OBJECT_PHP7_PDO_PGSQL16->Query("SELECT * FROM logs;");
// ..................................................
$STRING_JSON_Records = Conv_Associative_Array_to_JSON_Records($Associative_Array = $Associative_Array);
// ..................................................
echo $STRING_JSON_Records;

// ##################################################

/*
 * 使用 cURL 进行测试:
 * curl -X POST "http://127.0.0.1:8080/GF_PHP5_SCRIPT_HTTP_Server_POST_JSON_Records.php"
 */

?>
