<?php

/*
 * GF_PHP5_CLASS/PHP5_cURL_GET_SSE.php
 * Create by GF 2025-10-24 21:42
 */

class PHP5_cURL_GET_SSE {

    /*
     * PHP 5 中 cURL 的常用选项:
     *
     * // PHP 5 中 cURL 基本配置
     * $ch = curl_init();  // 初始化 cURL 会话, 创建句柄
     * curl_setopt($ch, CURLOPT_URL, "http://example.com");  // 设置 URL
     * curl_setopt($ch, CURLOPT_TIMEOUT, 30);  // 超时时间 (秒)
     *
     * // PHP 5 中 cURL 基本配置: 响应内容返回方式
     * // 1. 返回所有响应内容 (数据作为字符串返回到变量中, 内存占用随接收增长),
     * //    此时 curl_exec($ch); 返回字符串 (String)
     * curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
     * // 2. 数据直接输出到标准输出或通过回调函数处理 (用于实时/流式处理, 内存占用保持稳定),
     * //    此时 curl_exec($ch); 返回布尔 (Bool) 值
     * curl_setopt($ch, CURLOPT_RETURNTRANSFER, false);
     * //    将响应数据写入回调函数 ($curl: cURL 资源句柄, $data: 本次接收到的数据块)
     * curl_setopt($ch, CURLOPT_WRITEFUNCTION, function($curl, $data) {...});
     *
     * // PHP 5 中 cURL 配置请求方法
     * curl_setopt($ch, CURLOPT_POST, true);  // 使用 POST 方法 (不设置, 默认为 GET 方法)
     * curl_setopt($ch, CURLOPT_HTTPGET, true);  // 显式设置使用 GET 方法
     * curl_setopt($ch, CURLOPT_POSTFIELDS, $data);  // POST 数据
     * curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "PUT");  // 自定义方法
     *
     * // PHP 5 中 cURL 配置请求头信息
     * curl_setopt($ch, CURLOPT_HTTPHEADER, ["Content-Type: application/json",
     *                                       "Authorization: Bearer token123"]);
     *
     * // PHP 5 中 cURL 其他配置
     * curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);  // 跟随重定向
     * curl_setopt($ch, CURLOPT_TCP_KEEPALIVE, true);  // 启用 TCP 保持连接活跃的机制
     * curl_setopt($ch, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1);  // 使用 HTTP 1.1 协议
     * curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);  // 忽略 SSL 证书验证 (测试用)
     *
     * // cURL 请求 Server-Sent Events (SSE) 处理过程:
     * // 1. 回调函数收到：data: {"message": "Hello", "type": "greeting"}\n\n
     * // 2. 提取出：{"message": "Hello", "type": "greeting"}
     * // 3. 将 JSON 解析为 PHP 数组：['message' => 'Hello', 'type' => 'greeting']
     * // 4. 调用 Process_Message(['message' => 'Hello', 'type' => 'greeting'])
     */

    public function Process_Message($Message) {

        echo json_encode($Message, JSON_UNESCAPED_UNICODE);
        echo "<br>";
        // ..........................................
        if (ob_get_level() >= 1) ob_flush();
        // ..........................................
        flush();
    }

    public function GET_SSE($STRING_URL) {

        // 配置 HTTP 输出头 (当前 PHP 脚本)
        header("Content-Type: text/html; charset=utf-8");
        header("Cache-Control: no-cache");
        header("X-Accel-Buffering: no"); // 禁用 Nginx 缓冲 (用于流式逐行输出)
        header("Content-Encoding: none"); // 禁用压缩 (压缩过程可能影响流式逐行输出)

        $ch = curl_init();
        // ..........................................
        $ARRAY_Headers = [
            "Accept: text/event-stream",
            "Cache-Control: no-cache",
            "Connection: keep-alive"
        ];
        // ..........................................
        curl_setopt($ch, CURLOPT_URL, $STRING_URL);
        curl_setopt($ch, CURLOPT_HTTPGET, true);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, false);
        curl_setopt($ch, CURLOPT_TIMEOUT, 0);  // 超时设置为 0 表示无超时限制
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
        curl_setopt($ch, CURLOPT_TCP_KEEPALIVE, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $ARRAY_Headers);
        curl_setopt($ch, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1);
        curl_setopt($ch, CURLOPT_WRITEFUNCTION, function($curl, $data) {
            
                /*
                 * PHP 5 中 cURL 的 WRITEFUNCTION 回调函数必须显式返回接收到的数据长度
                 * 1. 可以使用 return strlen($data) 显式返回接收到的数据长度
                 * 2. cURL 需要知道您处理了多少数据 (控制数据流)
                 * 3. 如果返回的值与数据长度不符, cURL 会认为出错 (错误处理)
                 * 4. 确保数据被正确处理和释放 (内存管理)
                 *
                 * PHP 5 中 cURL 的 WRITEFUNCTION 回调函数参数说明 ($curl, $data)
                 * 1. $curl - cURL 资源句柄 (使得在回调函数内部也能访问和控制当前的 cURL 会话)
                 * 2. $data - 本次接收到的数据块 (数据是分块到达的, 不是一次性完整数据)
                 * 注意: 参数名称可以任意更改, 比如 $curl 改为 $ch, $data 改为 $dt 等
                 *       重要的是参数的位置和顺序 (第 1 个参数是 cURL 句柄, 第 2 个参数是数据)
                 */

                if (strpos($data, "data:") === 0) {  // 解析 SSE 格式 (SSE 数据以 "data:" 开头)

                    /*
                     * // PHP 5 中 substr(string, start, length) 函数示例:
                     * php > echo substr("Hello Word", 6)
                     * "Word"
                     * php > echo substr("Hello Word", 1, 4)
                     * "ello"
                     * php > echo substr("Hello Word", -4) // 从倒数第 4 个字符开始, 截取至末尾
                     * "Word"
                     * php > echo substr("Hello Word", -9, 4) // 从倒数第 9 个字符开始, 截取 4 个字符
                     * "ello"
                     */
                    $message = substr($data, 5);  // 去掉前 5 个字符 (data:)
                    $message = trim($message);  // 去除首尾空白字符

                    if ($message != "[DONE]" && empty($message) == false) {  // 过滤特殊信号和空消息

                        $decoded = json_decode($message, true);  // 解析 JSON 字符串为 PHP 数组

                        if (json_last_error() == JSON_ERROR_NONE) {  // 检查 JSON 解析是否成功

                            $this->Process_Message($decoded);  // 处理有效的 JSON 数据

                        } else {

                            echo "[DEBUG] JSON parsing error: " . json_last_error_msg() . "<br>";
                        }
                    }
                }

                return strlen($data);  // 必须显式返回接收到的数据长度
            }
        );
        // ..........................................
        $response  = curl_exec($ch);  // 执行 cURL 请求
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);  // 获取 HTTP 状态码
        $error     = curl_error($ch);  // 检查 cURL 执行是否出错
        // ..........................................
        curl_close($ch);  // 关闭 cURL 会话, 释放资源

        return ["success"   => ($http_code === 200),
                "response"  => $response,
                "http_code" => $http_code,
                "error"     => $error];
    }
}

// ##################################################

/*
 * PHP5_cURL_GET_SSE 测试:
 * $URL = "http://host.docker.internal:8080/GF_PHP5_SCRIPT_HTTP_Server_GET_SSE.php?stream=true";
 * $OBJECT_PHP5_cURL_GET_SSE = new PHP5_cURL_GET_SSE();
 * $OBJECT_PHP5_cURL_GET_SSE->GET_SSE($URL = $URL);
 */

$URL = "http://host.docker.internal:8080/GF_PHP5_SCRIPT_HTTP_Server_GET_SSE.php?stream=true";
$OBJECT_PHP5_cURL_GET_SSE = new PHP5_cURL_GET_SSE();
$OBJECT_PHP5_cURL_GET_SSE->GET_SSE($URL = $URL);

?>
