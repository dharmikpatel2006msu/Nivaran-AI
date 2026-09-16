-- Migration 04: E-Commerce Storefront Products & Orders Schema

-- Create Products Table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    description TEXT
);

-- Create Orders Table
CREATE TABLE IF NOT EXISTS orders (
    id VARCHAR(50) PRIMARY KEY,
    user_id BIGINT REFERENCES users(telegram_id) ON DELETE SET NULL,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'processing',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Seed Dummy Products
INSERT INTO products (id, name, price, description)
VALUES 
    (1, 'Wireless Headphones', 99.99, 'Premium noise-canceling wireless headphones with high-fidelity sound.'),
    (2, 'Smartwatch', 149.99, 'Next-gen fitness tracker and smartwatch with heart rate monitoring.'),
    (3, 'Bluetooth Speaker', 59.99, 'Portable waterproof Bluetooth speaker with deep bass.')
ON CONFLICT (id) DO UPDATE 
SET 
    name = EXCLUDED.name,
    price = EXCLUDED.price,
    description = EXCLUDED.description;

-- Index for fast user order retrieval
CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);
