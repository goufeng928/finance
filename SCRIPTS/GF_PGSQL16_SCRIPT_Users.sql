/*
 * SCRIPTS/GF_PGSQL16_SCRIPT_Users.sql
 * Create by GF 2025-11-17 16:30
 *
 * **** Edit /opt/postgresql/16.10/pg_data/postgresql.conf ****
 *
 * ......
 *
 * listen_addresses = '*'                  # what IP address(es) to listen on;
 *                                         # comma-separated list of addresses;
 *                                         # defaults to 'localhost'; use '*' for all
 *
 * ......
 *
 * **** Edit /opt/postgresql/16.10/pg_data/pg_hba.conf ****
 *
 * ......
 *
 * # TYPE  DATABASE        USER            ADDRESS                 METHOD
 *
 * # "local" is for Unix domain socket connections only
 * local   all             all                                     scram-sha-256
 * # IPv4 local connections:
 * host    all             all             127.0.0.1/32            scram-sha-256
 * # IPv6 local connections:
 * host    all             all             ::1/128                 scram-sha-256
 * # Allow replication connections from localhost, by a user with the
 * # replication privilege.
 * local   replication     all                                     scram-sha-256
 * host    replication     all             127.0.0.1/32            scram-sha-256
 * host    replication     all             ::1/128                 scram-sha-256
 *
 * # ##############
 * # Part of Custom
 * # ##############
 *
 * host    all             reader          0.0.0.0/0               scram-sha-256  # << Insert This Row.
 * host    all             writer          0.0.0.0/0               scram-sha-256  # << Insert This Row.
 *
 */

-- 如果用户存在则删除用户 (避免重复创建产生冲突)
DROP USER IF EXISTS reader;
DROP USER IF EXISTS writer;

-- 错误: 无法删除 "test_user" 因为有其它对象依倚赖它
-- 解决方法: REVOKE ALL ON DATABASE <example_database> FROM <user_name>;

CREATE USER reader WITH PASSWORD 'abcd1234';
CREATE USER writer WITH PASSWORD 'abcd1234';

-- 授予指定模式中所有表的查询权限
GRANT SELECT ON ALL TABLES IN SCHEMA public TO reader;

/*
 * 授予指定表的查询权限:
 * GRANT SELECT ON accounting_contract_occur  TO reader;
 * GRANT SELECT ON accounting_subject_details TO reader;
 */

-- 授予指定模式中所有表的查询, 插入, 更新, 删除权限
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO writer;

-- 授予名为 public 的 Schema 中所有序列的所有权限
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO writer;

/* EOF Signed by GF */
