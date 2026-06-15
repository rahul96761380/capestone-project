-- PRODUCTS
CREATE TABLE products (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2),
    stock_quantity INTEGER,
    is_active BOOLEAN DEFAULT TRUE
);

INSERT INTO products VALUES
('PRD-101', 'Apple iPhone 15', 'Smartphones', 79999.00, 25, TRUE),
('PRD-102', 'Samsung Galaxy S25', 'Smartphones', 74999.00, 15, TRUE),
('PRD-103', 'Sony WH-1000XM5', 'Headphones', 29999.00, 12, TRUE),
('PRD-104', 'Dell Inspiron 15', 'Laptops', 65999.00, 0, TRUE),
('PRD-105', 'Apple Watch Series 10', 'Wearables', 45999.00, 18, TRUE),
('PRD-106', 'Old Test Product', 'Test', 999.00, 0, FALSE);

-- ORDERS
CREATE TABLE orders (
    order_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100),
    product_id VARCHAR(20),
    order_status VARCHAR(20),
    order_date TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT INTO orders VALUES
('ORD-001', 'Priya Sharma', 'PRD-101', 'SHIPPED', NOW() - INTERVAL '2 day'),
('ORD-002', 'Rahul Sekar', 'PRD-103', 'DELIVERED', NOW() - INTERVAL '7 day'),
('ORD-003', 'Ananya Singh', 'PRD-102', 'PROCESSING', NOW() - INTERVAL '1 day'),
('ORD-004', 'Vikram Patel', 'PRD-105', 'CANCELLED', NOW() - INTERVAL '5 day'),
('ORD-005', 'Sneha Reddy', 'PRD-104', 'PENDING', NOW());

-- SESSION HISTORY
CREATE TABLE session_history (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100),
    user_id VARCHAR(100),
    role VARCHAR(20),
    content TEXT,
    tool_calls TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);