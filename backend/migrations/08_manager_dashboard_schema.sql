-- Migration 08: Manager Dashboard Schema for Nivaran AI
-- Products catalog, customer orders, and status lifecycle tracking

-- 1. Create or align products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    image_url TEXT,
    stock INTEGER NOT NULL DEFAULT 10,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Ensure all columns exist on products even if products table was created in an earlier migration
ALTER TABLE products ADD COLUMN IF NOT EXISTS name TEXT;
ALTER TABLE products ADD COLUMN IF NOT EXISTS description TEXT;
ALTER TABLE products ADD COLUMN IF NOT EXISTS price NUMERIC(10, 2) NOT NULL DEFAULT 0.00;
ALTER TABLE products ADD COLUMN IF NOT EXISTS image_url TEXT;
ALTER TABLE products ADD COLUMN IF NOT EXISTS stock INTEGER NOT NULL DEFAULT 10;
ALTER TABLE products ADD COLUMN IF NOT EXISTS is_active BOOLEAN NOT NULL DEFAULT TRUE;
ALTER TABLE products ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP;

-- 2. Create or align orders table
CREATE TABLE IF NOT EXISTS orders (
    id VARCHAR(50) PRIMARY KEY,
    customer_name TEXT NOT NULL DEFAULT 'Guest Customer',
    user_id INT,
    product_id INT,
    quantity INT NOT NULL DEFAULT 1,
    total NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    status VARCHAR(50) NOT NULL DEFAULT 'Booked',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Ensure all columns exist on orders even if orders table was created in an earlier migration
ALTER TABLE orders ADD COLUMN IF NOT EXISTS customer_name TEXT NOT NULL DEFAULT 'Guest Customer';
ALTER TABLE orders ADD COLUMN IF NOT EXISTS customer_email TEXT;
ALTER TABLE orders ADD COLUMN IF NOT EXISTS user_id INT;
ALTER TABLE orders ADD COLUMN IF NOT EXISTS product_id INT;
ALTER TABLE orders ADD COLUMN IF NOT EXISTS quantity INT NOT NULL DEFAULT 1;
ALTER TABLE orders ADD COLUMN IF NOT EXISTS total NUMERIC(10, 2) NOT NULL DEFAULT 0.00;
ALTER TABLE orders ADD COLUMN IF NOT EXISTS status VARCHAR(50) NOT NULL DEFAULT 'Booked';
ALTER TABLE orders ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP;

-- 3. Performance Indexes
CREATE INDEX IF NOT EXISTS idx_products_is_active ON products(is_active);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_customer_name ON orders(customer_name);
CREATE INDEX IF NOT EXISTS idx_orders_customer_email ON orders(customer_email);
CREATE INDEX IF NOT EXISTS idx_orders_product_id ON orders(product_id);
CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at DESC);

-- 4. Sync store_products if available or seed default products
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'store_products') THEN
        INSERT INTO products (id, name, description, price, image_url, stock, is_active, created_at)
        SELECT 
            id, 
            name, 
            description, 
            price, 
            image_url, 
            stock, 
            (status = 'active') AS is_active,
            created_at
        FROM store_products
        ON CONFLICT (id) DO UPDATE
        SET 
            name = EXCLUDED.name,
            description = EXCLUDED.description,
            price = EXCLUDED.price,
            image_url = EXCLUDED.image_url,
            stock = EXCLUDED.stock,
            is_active = EXCLUDED.is_active;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM products LIMIT 1) THEN
        INSERT INTO products (id, name, description, price, image_url, stock, is_active)
        VALUES 
            (1, 'Aura Wireless Headphones', 'Active noise cancelling wireless headphones with 40h battery life and spatial audio.', 129.99, 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=60', 15, TRUE),
            (2, 'Pulse Fitness Smartwatch', 'Waterproof fitness smartwatch with AMOLED display, heart rate tracking, and GPS.', 179.99, 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&auto=format&fit=crop&q=60', 8, TRUE),
            (3, 'SonicBoom Bluetooth Speaker', 'Compact waterproof Bluetooth speaker delivering 360-degree immersive bass sound.', 69.99, 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500&auto=format&fit=crop&q=60', 20, TRUE),
            (4, 'ZenErgo Mechanical Keyboard', 'RGB tactile wireless mechanical keyboard with hot-swappable switches and wrist rest.', 119.99, 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500&auto=format&fit=crop&q=60', 5, TRUE),
            (5, 'Clarion HD Ergonomic Earbuds', 'True wireless in-ear earbuds with dual mic noise suppression and instant pairing.', 49.99, 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500&auto=format&fit=crop&q=60', 0, TRUE)
        ON CONFLICT (id) DO NOTHING;
    END IF;
END $$;

-- 5. Safe sequence update for products id
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_class WHERE relkind = 'S' AND relname = 'products_id_seq') THEN
        PERFORM setval('products_id_seq', COALESCE((SELECT MAX(id) FROM products), 1));
    END IF;
END $$;

-- 6. Seed demo orders if orders table is empty
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM orders LIMIT 1) THEN
        INSERT INTO orders (id, customer_name, user_id, product_id, quantity, total, status, created_at)
        VALUES 
            ('ORD-10101', 'Alice Smith', NULL, 1, 1, 129.99, 'Booked', NOW() - INTERVAL '2 hours'),
            ('ORD-10102', 'Bob Jones', NULL, 2, 1, 179.99, 'Shipped', NOW() - INTERVAL '1 day'),
            ('ORD-10103', 'Charlie Brown', NULL, 3, 2, 139.98, 'Out for Delivery', NOW() - INTERVAL '6 hours'),
            ('ORD-10104', 'Diana Prince', NULL, 4, 1, 119.99, 'Delivered', NOW() - INTERVAL '3 days'),
            ('ORD-10105', 'Evan Wright', NULL, 5, 1, 49.99, 'Returned', NOW() - INTERVAL '5 days')
        ON CONFLICT (id) DO NOTHING;
    END IF;
END $$;
