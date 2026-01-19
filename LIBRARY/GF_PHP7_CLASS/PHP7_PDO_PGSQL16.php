<?php

/*
 * GF_PHP7_CLASS/PHP7_PDO_PGSQL16.php
 * Create by GF 2025-10-23 19:30
 */

class PHP7_PDO_PGSQL16 {

    private $OBJECT_PDO;
    // ..............................................
    public  $HOST     = "127.0.0.1";
    public  $PORT     = "5432";
    public  $DB_NAME  = "postgres";
    public  $USER     = "postgres";
    public  $PASSWORD = "abcd1234";

    public function Init() {

        $function_status = "failure";
        // ..........................................
        // "$dsn" be Similar to: "pgsql:host=host.docker.internal;port=5432;dbname=postgres"
        $dsn = "pgsql:host=" . $this->HOST . ";port=" . $this->PORT . ";dbname=" . $this->DB_NAME;
        // ..........................................
        try {
            // PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION (错误处理模式 => 异常模式)
            // PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC (默认的获取数据模式 => 关联数组)
            $this->OBJECT_PDO = new PDO($dsn,
                                        $this->USER,
                                        $this->PASSWORD,
                                        [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                                         PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
            // ......................................
            $function_status = "success";
        } catch (PDOException $e) {
            die("[DEBUG] PostgreSQL connection failed: " . $e->getMessage());
            // ......................................
            $function_status = "failure";
        }
        // ..........................................
        return $function_status;
    }

    // 查询 (Query)
    public function Query($Statement, $Parameters = []) {

        // 准备 SQL 语句
        $Prepared_Statement = $this->OBJECT_PDO->prepare($Statement);
        // ..........................................
        // 执行查询 (可选: 传入参数)
        $Prepared_Statement->execute($Parameters);
        // ..........................................
        // 返回所有结果
        return $Prepared_Statement->fetchAll();
    }

    // 增 (INSERT) / 删 (DELETE) / 改 (UPDATE)
    public function Execute($Statement, $Parameters = []) {

        // 准备 SQL 语句
        $Prepared_Statement = $this->OBJECT_PDO->prepare($Statement);
        // ..........................................
        // 执行操作, 返回是否成功 (可选: 传入参数)
        return $Prepared_Statement->execute($Parameters);
    }
}

// ##################################################

/*
 * PHP7_PDO_PGSQL16 使用示例:
 *
 * php > $OBJECT_PHP7_PDO_PGSQL16 = new PHP7_PDO_PGSQL16();
 * php > $OBJECT_PHP7_PDO_PGSQL16->HOST     = "host.docker.internal";
 * php > $OBJECT_PHP7_PDO_PGSQL16->DB_NAME  = "finance";
 * php > $OBJECT_PHP7_PDO_PGSQL16->USER     = "goufeng";
 * php > $OBJECT_PHP7_PDO_PGSQL16->PASSWORD = "abcd1234";
 * php > $OBJECT_PHP7_PDO_PGSQL16->Init();
 * php > 
 * php > // 查询数据 (使用参数)
 * php > $result = $OBJECT_PHP7_PDO_PGSQL16->Query("SELECT * FROM users WHERE age > ?", [18]);
 * php > print_r($result);
 * Array([1] => Array("id" => 1, "name" => "Jack", "age" => 19, "email" => "jack@example.com"),
 *       [2] => Array("id" => 2, "name" => "Alice", "age" => 20, "email" => "alice@example.com"),
 *       [3] => Array("id" => 2, "name" => "John", "age" => 22, "email" => "john@example.com"))
 * php > 
 * php > // 查询数据 (未使用参数)
 * php > $result = $OBJECT_PHP7_PDO_PGSQL16->Query("SELECT * FROM users WHERE age > 18");
 * php > print_r($result);
 * Array([1] => Array("id" => 1, "name" => "Jack", "age" => 19, "email" => "jack@example.com"),
 *       [2] => Array("id" => 2, "name" => "Alice", "age" => 20, "email" => "alice@example.com"),
 *       [3] => Array("id" => 2, "name" => "John", "age" => 22, "email" => "john@example.com"))
 * php > 
 * php > // 插入数据
 * php > $result = $OBJECT_PHP7_PDO_PGSQL16->Execute("INSERT INTO users (name, email) VALUES (?, ?)", 
 * php *                                             ["Alen", "alen@example.com"]);
 * php > 
 * php > // 更改数据
 * php > $result = $OBJECT_PHP7_PDO_PGSQL16->Execute("UPDATE users SET name = ? WHERE id = ?",
 * php *                                             ["Brown", 3]);
 * php >
 * php > // 删除用户
 * php > $result = $OBJECT_PHP7_PDO_PGSQL16->Execute("DELETE FROM users WHERE id = ?",
 * php *                                             [3]);
 */

?>
