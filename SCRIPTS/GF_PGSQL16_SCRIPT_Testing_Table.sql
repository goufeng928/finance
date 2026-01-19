/*
 * SCRIPTS/GF_PGSQL16_SCRIPT_Testing_Table.sql
 * Create by GF 2025-11-28 22:30
 */

CREATE TABLE testing_users (

    -- Testing 用户 (Users)

    id         SERIAL PRIMARY KEY,
    username   VARCHAR(50) UNIQUE NOT NULL,
    email      VARCHAR(100) UNIQUE NOT NULL,
    full_name  VARCHAR(100),
    age        INTEGER,
    city       VARCHAR(50),
    country    VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    is_active  BOOLEAN DEFAULT true,
    balance    DECIMAL(10, 2) DEFAULT 0.00
);

INSERT INTO testing_users (username, email, full_name, age, city, country, is_active, balance)
VALUES ('john_doe',    'john@example.com',  'John Doe',    28, 'New York',    'USA',       true,  1500.00),
       ('jane_smith',  'jane@example.com',  'Jane Smith',  34, 'London',      'UK',        true,  2300.50),
       ('bob_wilson',  'bob@example.com',   'Bob Wilson',  45, 'Toronto',     'Canada',    true,   800.75),
       ('alice_jones', 'alice@example.com', 'Alice Jones', 29, 'Sydney',      'Australia', false,  300.00),
       ('mike_brown',  'mike@example.com',  'Mike Brown',  52, 'Berlin',      'Germany',   true,  4200.00),
       ('sara_miller', 'sara@example.com',  'Sara Miller', 31, 'Paris',       'France',    true,  1750.25),
       ('tom_davis',   'tom@example.com',   'Tom Davis',   26, 'Tokyo',       'Japan',     true,   950.00),
       ('lisa_wang',   'lisa@example.com',  'Lisa Wang',   38, 'Beijing',     'China',     true,  3200.75),
       ('peter_chen',  'peter@example.com', 'Peter Chen',  41, 'Shanghai',    'China',     true,  2800.50),
       ('emma_taylor', 'emma@example.com',  'Emma Taylor', 27, 'Los Angeles', 'USA',       false, 1200.00);

CREATE TABLE testing_products (

    -- Testing 产品 (Products)

    id             SERIAL PRIMARY KEY,
    product_name   VARCHAR(100) NOT NULL,
    category       VARCHAR(50),
    price          DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    created_at     TIMESTAMP DEFAULT NOW()
);

INSERT INTO testing_products (product_name, category, price, stock_quantity)
VALUES ('Laptop Pro',     'Electronics', 1299.99,  50),
       ('Wireless Mouse', 'Electronics',   29.99, 200),
       ('Office Chair',   'Furniture',    199.99,  30),
       ('Desk Lamp',      'Home',          49.99, 100),
       ('Coffee Maker',   'Kitchen',       89.99,  75),
       ('Running Shoes',  'Sports',        79.99, 120),
       ('Backpack',       'Fashion',       59.99,  80),
       ('Water Bottle',   'Sports',        24.99, 150),
       ('Notebook',       'Stationery',     9.99, 300),
       ('Headphones',     'Electronics',  149.99,  60);

CREATE TABLE testing_orders (

    -- Testing 订单 (Orders)

    id           SERIAL PRIMARY KEY,
   "user_id"     INTEGER REFERENCES testing_users(id),
    order_date   DATE DEFAULT CURRENT_DATE,
    total_amount DECIMAL(10, 2),
    status       VARCHAR(20) DEFAULT 'pending'
);

INSERT INTO testing_orders (user_id, order_date, total_amount, status)
VALUES (1, '2024-01-15', 1429.98, 'completed'),
       (2, '2024-01-16',  229.98, 'completed'),
       (3, '2024-01-17',  199.99, 'pending'  ),
       (1, '2024-01-18',   89.99, 'shipped'  ),
       (4, '2024-01-19',   79.99, 'completed');

CREATE TABLE testing_order_detail (

    -- Testing 订单详情 (Orders Detail)

    id         SERIAL PRIMARY KEY,
    order_id   INTEGER REFERENCES testing_orders(id),
    product_id INTEGER REFERENCES testing_products(id),
    quantity   INTEGER NOT NULL,
    unit_price DECIMAL(10, 2),
    subtotal   DECIMAL(10, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED
);

INSERT INTO testing_order_detail (order_id, product_id, quantity, unit_price)
VALUES (1, 1, 1, 1299.99),
       (1, 2, 1,   29.99),
       (2, 6, 2,   79.99),
       (2, 8, 2,   24.99),
       (3, 3, 1,  199.99),
       (4, 5, 1,   89.99),
       (5, 6, 1,   79.99);

/* EOF Signed by GF */
