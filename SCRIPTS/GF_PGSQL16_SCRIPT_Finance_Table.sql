/*
 * SCRIPTS/GF_PGSQL16_SCRIPT_Finance_Table.sql
 * Create by GF 2025-11-28 22:30
 */


CREATE TABLE IF NOT EXISTS logs (
    id        SERIAL PRIMARY KEY,  -- ID (Identification)
   "time"     VARCHAR(128),        -- 时间 (Time)
   "object"   VARCHAR(128),        -- 对象 (Object)
    event     VARCHAR(128),        -- 事件 (Event)
    afct_num  INTEGER,             -- 影响数量 (Affected Number)
    unit      VARCHAR(128),        -- 单位 (Unit)
    memo      VARCHAR(128)         -- 备注 (Memo)
);

CREATE TABLE IF NOT EXISTS mapping (
    id        SERIAL PRIMARY KEY,  -- ID (Identification)
    project   VARCHAR(128),        -- 项目 (Project)
    orig      VARCHAR(128),        -- 原始 (Original)
    dest      VARCHAR(128),        -- 终点 (Destination)
   "comment"  VARCHAR(128),        -- 注释 (Comment)
    memo      VARCHAR(128)         -- 备注 (Memo)
);

CREATE TABLE IF NOT EXISTS stocks_en_us_daily_to_weekly (

    -- CREATE TABLE stocks_en_us_daily_to_weekly
    -- CREATE TABLE stocks_en_us_daily_to_weekly_interim

    id        SERIAL PRIMARY KEY,  -- ID (Identification)
    code      VARCHAR(128),        -- 代码 (Code)
   "time"     VARCHAR(128),        -- 时间 (Time)
    week_num  INTEGER,
   "open"     DECIMAL(28,4),
    high      DECIMAL(28,4),
    low       DECIMAL(28,4),
   "close"    DECIMAL(28,4),
    change    DECIMAL(28,4),
    volume    DECIMAL(28,4),
    memo      VARCHAR(128)
);

CREATE TABLE IF NOT EXISTS stocks_en_us_daily_to_weekly_indicator (

    -- CREATE TABLE stocks_en_us_daily_to_weekly_indicator
    -- CREATE TABLE tushare_api_cache_en_us_indicator

    id           SERIAL PRIMARY KEY,
    sma5         DECIMAL(28,4),
    sma10        DECIMAL(28,4),
    ema12        DECIMAL(28,4),
    ema26        DECIMAL(28,4),
    macd_dif     DECIMAL(28,4),
    macd_dea     DECIMAL(28,4),
    macd_stick   DECIMAL(28,4),
    kdj_k        DECIMAL(28,4),
    kdj_d        DECIMAL(28,4),
    kdj_j        DECIMAL(28,4),
    etg_trs      INTEGER,
    etg_brs      INTEGER,
    etg_t_group  INTEGER,
    etg_b_group  INTEGER,
    memo         VARCHAR(128)
);

CREATE TABLE IF NOT EXISTS tushare_api_cache_en_us (
    id         SERIAL PRIMARY KEY, -- ID (Identification)
   "unique"    VARCHAR(128),       -- 唯一标识 (Unique)
    ts_code    VARCHAR(128),       -- Tushare 代码 (Tushare Code)
   "time"      VARCHAR(128),       -- 时间 (Time)
   "open"      DECIMAL(28,4),
    high       DECIMAL(28,4),
    low        DECIMAL(28,4),
   "close"     DECIMAL(28,4),
    pre_close  DECIMAL(28,4),
    change     DECIMAL(28,4),
    pct_chg    DECIMAL(28,4),
    vol        DECIMAL(28,4),
    amount     DECIMAL(28,4),
    memo       VARCHAR(128)        -- 备注 (Memo)
);

CREATE TABLE IF NOT EXISTS vars (
    id        SERIAL PRIMARY KEY,  -- ID (Identification)
    name      VARCHAR(128),        -- 名称 (Name)
   "type"     VARCHAR(128),        -- 类型 (Type)
   "value"    VARCHAR(128),        -- 值 (Value)
   "comment"  VARCHAR(128),        -- 注释 (Comment)
    memo      VARCHAR(128)         -- 备注 (Memo)
);

/* EOF Signed by GF */
