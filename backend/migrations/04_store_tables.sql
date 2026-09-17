-- Migration 04: Customer Storefront Products, Orders & Order Items Schema

-- Create Store Products Table
CREATE TABLE IF NOT EXISTS store_products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    image_url TEXT,
    stock INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Create Store Orders Table
CREATE TABLE IF NOT EXISTS store_orders (
    id VARCHAR(50) PRIMARY KEY,
    customer_name TEXT NOT NULL,
    address TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    total NUMERIC(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'processing',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Create Store Order Items Table
CREATE TABLE IF NOT EXISTS store_order_items (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(50) REFERENCES store_orders(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES store_products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL
);

-- Index for order lookups
CREATE INDEX IF NOT EXISTS idx_store_orders_email ON store_orders(email);
CREATE INDEX IF NOT EXISTS idx_store_order_items_order ON store_order_items(order_id);

-- Seed Initial Products
INSERT INTO store_products (id, name, description, price, image_url, stock, status)
VALUES 
    (1, 'Aura Wireless Headphones', 'Active noise cancelling wireless headphones with 40h battery life and spatial audio.', 129.99, 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=60', 15, 'active'),
    (2, 'Pulse Fitness Smartwatch', 'Waterproof fitness smartwatch with AMOLED display, heart rate tracking, and GPS.', 179.99, 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&auto=format&fit=crop&q=60', 8, 'active'),
    (3, 'SonicBoom Bluetooth Speaker', 'Compact waterproof Bluetooth speaker delivering 360-degree immersive bass sound.', 69.99, 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500&auto=format&fit=crop&q=60', 20, 'active'),
    (4, 'ZenErgo Mechanical Keyboard', 'RGB tactile wireless mechanical keyboard with hot-swappable switches and wrist rest.', 119.99, 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500&auto=format&fit=crop&q=60', 5, 'active'),
    (5, 'Clarion HD Ergonomic Earbuds', 'True wireless in-ear earbuds with dual mic noise suppression and instant pairing.', 49.99, 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500&auto=format&fit=crop&q=60', 0, 'active')
ON CONFLICT (id) DO UPDATE 
SET 
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    price = EXCLUDED.price,
    image_url = EXCLUDED.image_url,
    stock = EXCLUDED.stock,
    status = EXCLUDED.status;
