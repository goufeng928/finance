<?php

/*
 * GF_PHP5_SCRIPT/PHP5_HTTP_Server_GET_SSE.php
 * Create by GF 2025-10-23 19:30
 */

// 设置响应头: 告诉浏览器这是 SSE 流
header("Content-Type: text/event-stream");  // 重要: Server-Sent Events 必须是这个类型
header("Cache-Control: no-cache");          // 禁止缓存
header("Connection: keep-alive");           // 保持连接
header("Access-Control-Allow-Origin: *");   // 允许跨域访问
header("X-Accel-Buffering: no");            // 禁用 Nginx 的代理缓冲功能 (否则无法实现实时逐个输出效果)
header('Content-Encoding: none');           // 禁用 Apache 服务器的内容压缩
header('X-Powered-By: None');               // 移除 Apache 服务器的标识

// ##################################################

/* 关闭输出缓冲, 确保数据立即发送
 *
 * ob_get_level() 输出示例:
 *
 * php > echo ob_get_level();  // 初始缓冲级别
 * 0
 * php > ob_start();  // 第 1 次开启缓冲
 * php > echo ob_get_level();
 * 1
 * php > ob_start();  // 第 2 次开启缓冲
 * php > echo ob_get_level();
 * 2
 * php > ob_end_flush();  // 结束 1 层缓冲
 * php > echo ob_get_level();
 * 1
 * php > ob_end_clean();  // 结束所有缓冲
 * php > echo ob_get_level();
 * 0
 */
while (ob_get_level() != 0) ob_end_clean();

/*
 * 启用隐式自动刷新
 * 让 PHP 在每次输出后自动执行刷新操作, 无需手动调用 flush();
 */
ob_implicit_flush(true);

// ##################################################

// 检查 GET 请求是否存在 "?stream=true" 参数
$BOOL_is_Stream = false;
// ..................................................
if (isset($_GET['stream']) == true && $_GET['stream'] == "true") $BOOL_is_Stream = true;

// ##################################################

// 发送 Server-Sent Events (SSE) 事件
function Send_SSE_Event($ARRAY_Message, $Event = null) {

    /*
     * $Event = "close";  // 标记 SSE 流正常结束
     * $Event = "end";    // 标记 SSE 流正常结束
     * $Event = "error";  // 通知客户端在处理 SSE 流时发生了错误
     * $Event = "status"; // 用于发送后台任务的状态
     * $Event = "update"; // 发送增量更新或状态变化
     *
     * Example: 标记 SSE 流正常结束
     * event: end
     * data: {"status": "completed", "reason": "normal"}
     *
     * Example: 发送后台任务的状态:
     * event: status
     * data: {"job_id": "123", "status": "completed"}
     */

    if ($Event != null) echo "event: " . $Event . "\n";
    // ..............................................
    // SSE 格式: data: {"id": "68fb3184b1c04", "content": "Example content", ...}\n\n
    echo "data: " . json_encode($ARRAY_Message, JSON_UNESCAPED_UNICODE) . "\n\n";
    // ..............................................
    // 刷新最顶层的 "输出控制" 缓冲区
    // (把当前由 ob_start() 开启的输出控制缓冲区中的内容推送到 PHP 的内部输出缓冲区)
    ob_flush();
    // ..............................................
    // 刷新 PHP 的内部输出缓冲区 (立刻把 PHP 内部输出缓冲区中已经准备好的所有数据推送给 Web 服务器)
    flush();
    // ..............................................
    /*
     * 检查客户端是否保持连接, 如果断开则停止发送
     * connection_aborted() == 0 时, 表示客户端连接仍然正常
     * connection_aborted() == 1 时, 表示客户端连接已断开
     */
    if (connection_aborted() == 1) exit;
}

// Server-Sent Events (SSE) 流式响应
function Response_SSE_Stream($ARRAY_Messages) {

    $ARRAY_Messages_Length = count($ARRAY_Messages);

    // 逐个发送数据块
    for ($i = 0; $i <= $ARRAY_Messages_Length - 1; $i++) {

        $data = ['id' => uniqid(), 'content' => $ARRAY_Messages[$i]];
        // ..........................................
        // 发送 SSE 格式数据
        Send_SSE_Event($data);
        // ..........................................
        // 等待 1 秒, 模拟处理时间
        sleep(1);
    }

    // 发送结束信号
    Send_SSE_Event(["status" => "completed", "reason" => "normal"], $Event = "end");
}

// General Text (普通文本) 非流式响应
function Response_General_Text($STRING_Message) {
    
    // 设置 JSON 响应头
    header('Content-Type: application/json');
    // ..............................................
    $response = ["id" => uniqid(), "content" => $STRING_Message, "status" => "success"];
    // ..............................................
    echo json_encode($response, JSON_UNESCAPED_UNICODE);
}

// ##################################################

// Server-Sent Events (SSE) 流式响应数据准备
$ARRAY_Messages = [
    "How's it going?",
    "What have you been up to?",
    "Long time no see!",
    "It's great to see you again."
];

// General Text (一般文本) 响应数据准备
$STRING_Message = "Could you point me in the direction of the nearest metro station?";

// ##################################################

if ($BOOL_is_Stream == true) {

    // 流式响应
    Response_SSE_Stream($ARRAY_Messages = $ARRAY_Messages);

} else {

    // 普通响应
    Response_General_Text($STRING_Message = $STRING_Message);
}

// ##################################################

/*
 * 使用 cURL 进行测试:
 * curl "http://127.0.0.1:8080/GF_PHP5_SCRIPT_HTTP_Server_GET_SSE.php?stream=true"
 */

?>
