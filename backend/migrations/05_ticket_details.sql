-- Migration 05: Add order_id, issue, and issue_description to tickets table

ALTER TABLE tickets
ADD COLUMN IF NOT EXISTS order_id VARCHAR(50) REFERENCES store_orders(id) ON DELETE SET NULL,
ADD COLUMN IF NOT EXISTS issue TEXT,
ADD COLUMN IF NOT EXISTS issue_description TEXT;

-- Create index on order_id for fast lookup
CREATE INDEX IF NOT EXISTS idx_tickets_order_id ON tickets(order_id);
