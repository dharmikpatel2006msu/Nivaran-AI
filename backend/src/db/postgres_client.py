"""PostgreSQL database client and transaction manager for Nivaran AI.

Provides connection pooling, schema migration execution, parameterized queries,
order lifecycle updates, and product catalog persistence using psycopg2.
"""

import os
import logging
from contextlib import contextmanager
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from src.config import DATABASE_URL

logger = logging.getLogger(__name__)

# Allowed status transitions for the order lifecycle
ALLOWED_ORDER_STATUSES = [
    "Booked",
    "Shipped",
    "Out for Delivery",
    "Delivered",
    "Returned",
]

_pg_pool: Optional[pool.ThreadedConnectionPool] = None


def get_connection_pool() -> pool.ThreadedConnectionPool:
    """Initializes and returns the singleton psycopg2 connection pool."""
    global _pg_pool
    if _pg_pool is None:
        if not DATABASE_URL:
            logger.error("❌ DATABASE_URL is not configured in environment!")
            raise RuntimeError("DATABASE_URL is not set")
        try:
            logger.info("🔌 Initializing PostgreSQL connection pool...")
            _pg_pool = pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=20,
                dsn=DATABASE_URL,
                cursor_factory=RealDictCursor
            )
            logger.info("✅ PostgreSQL connection pool initialized successfully.")
        except Exception as e:
            logger.error(f"❌ Failed to connect to PostgreSQL: {e}")
            raise
    return _pg_pool


@contextmanager
def get_db_connection():
    """Context manager for obtaining a database connection from the pool.
    
    Automatically rolls back on uncaught exception and returns the connection.
    """
    p = get_connection_pool()
    conn = p.getconn()
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    finally:
        p.putconn(conn)


def execute_query(
    query: str,
    params: Optional[tuple] = None,
    fetch: bool = True,
    commit: bool = False
) -> List[Dict[str, Any]]:
    """Executes a parameterized SQL query safely against PostgreSQL."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            results = []
            if fetch:
                try:
                    rows = cur.fetchall()
                    results = [dict(row) for row in rows]
                except psycopg2.ProgrammingError:
                    results = []
            if commit:
                conn.commit()
            return results


def run_migrations_if_needed():
    """Runs pending SQL migrations to guarantee schema synchronization."""
    migrations_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "migrations"))
    if not os.path.exists(migrations_dir):
        logger.warning(f"⚠️ Migrations directory not found at {migrations_dir}")
        return

    migration_files = sorted([f for f in os.listdir(migrations_dir) if f.endswith(".sql")])
    logger.info(f"🔄 Checking {len(migration_files)} migration files in {migrations_dir}...")

    with get_db_connection() as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            for mf in migration_files:
                fpath = os.path.join(migrations_dir, mf)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        sql_content = f.read()

                    # Gracefully skip pgvector extension creation if vector extension is not available
                    cleaned = []
                    for line in sql_content.splitlines():
                        if "CREATE EXTENSION" in line and "vector" in line:
                            continue
                        cleaned.append(line)
                    sql_to_run = "\n".join(cleaned)

                    # Execute migration block
                    cur.execute(sql_to_run)
                    logger.info(f"  ✅ Applied migration: {mf}")
                except Exception as e:
                    logger.warning(f"  ⚠️ Note on migration {mf}: {e}")


# =========================================================================
# Order Management Functions
# =========================================================================

def get_admin_orders(
    status_filter: Optional[str] = None,
    search: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Retrieves all orders with customer and product names joined."""
    query = """
        SELECT 
            o.id AS order_id,
            o.customer_name,
            COALESCE(o.customer_email, u.email, 'dharmikpatel290929@gmail.com') AS customer_email,
            COALESCE(p.name, 'Product #' || COALESCE(o.product_id::text, 'N/A')) AS product_name,
            o.product_id,
            o.quantity,
            o.total,
            o.status,
            o.created_at,
            u.id AS user_id,
            u.telegram_id,
            u.email AS user_email
        FROM orders o
        LEFT JOIN products p ON o.product_id = p.id
        LEFT JOIN users u ON o.user_id = u.id
        WHERE 1=1
    """
    params: List[Any] = []

    if status_filter:
        query += " AND o.status = %s"
        params.append(status_filter)

    if search:
        search_pattern = f"%{search.strip()}%"
        query += " AND (o.id ILIKE %s OR o.customer_name ILIKE %s OR p.name ILIKE %s)"
        params.extend([search_pattern, search_pattern, search_pattern])

    query += " ORDER BY o.created_at DESC;"

    rows = execute_query(query, tuple(params), fetch=True)
    
    # Format dates as ISO string
    for r in rows:
        if isinstance(r.get("created_at"), datetime):
            r["created_at"] = r["created_at"].isoformat()
        if r.get("total") is not None:
            r["total"] = float(r["total"])
        r["quantity"] = int(r.get("quantity") or 1)

    return rows


def get_order_by_id(order_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a single order record with product and customer details."""
    query = """
        SELECT 
            o.id AS order_id,
            o.customer_name,
            COALESCE(o.customer_email, u.email, 'dharmikpatel290929@gmail.com') AS customer_email,
            COALESCE(p.name, 'Product #' || COALESCE(o.product_id::text, 'N/A')) AS product_name,
            o.product_id,
            o.quantity,
            o.total,
            o.status,
            o.created_at,
            o.user_id,
            u.telegram_id,
            u.email AS user_email
        FROM orders o
        LEFT JOIN products p ON o.product_id = p.id
        LEFT JOIN users u ON o.user_id = u.id
        WHERE o.id = %s;
    """
    rows = execute_query(query, (order_id.strip(),), fetch=True)
    if not rows:
        return None
    r = rows[0]
    if isinstance(r.get("created_at"), datetime):
        r["created_at"] = r["created_at"].isoformat()
    if r.get("total") is not None:
        r["total"] = float(r["total"])
    return r


# Allowed sequential status transitions
ALLOWED_TRANSITIONS = {
    "Booked": ["Shipped", "Returned"],
    "Shipped": ["Out for Delivery", "Returned"],
    "Out for Delivery": ["Delivered", "Returned"],
    "Delivered": ["Returned"],
    "Returned": []  # Final terminal state
}


def update_order_status(order_id: str, new_status: str) -> Optional[Dict[str, Any]]:
    """Updates the status of an order within an atomic database transaction.
    
    Validates against strict sequential state progression and terminal state rules.
    """
    if new_status not in ALLOWED_ORDER_STATUSES:
        raise ValueError(
            f"Invalid status '{new_status}'. Allowed statuses are: {', '.join(ALLOWED_ORDER_STATUSES)}"
        )

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Check existence and current status
            cur.execute("SELECT id, status FROM orders WHERE id = %s FOR UPDATE;", (order_id,))
            order_row = cur.fetchone()
            if not order_row:
                conn.rollback()
                return None

            current_status = order_row["status"]
            if current_status == "Returned" and new_status != "Returned":
                conn.rollback()
                raise ValueError("Order is already marked as Returned (Final state) and cannot be updated.")

            if current_status != new_status:
                allowed_next = ALLOWED_TRANSITIONS.get(current_status, [])
                if new_status not in allowed_next:
                    conn.rollback()
                    raise ValueError(
                        f"Cannot transition order from '{current_status}' to '{new_status}'. "
                        f"Allowed next status: {', '.join(allowed_next) if allowed_next else 'None (Final status)'}"
                    )

            # Update orders table
            cur.execute(
                "UPDATE orders SET status = %s WHERE id = %s RETURNING id, status;",
                (new_status, order_id)
            )
            updated = cur.fetchone()

            # Also sync with store_orders if table exists in postgres
            try:
                cur.execute(
                    "UPDATE store_orders SET status = %s WHERE id = %s;",
                    (new_status, order_id)
                )
            except Exception:
                pass

            conn.commit()

    # Synchronize status directly to Supabase store_orders
    try:
        from src.services.chat_service import get_supabase_client
        supabase = get_supabase_client()
        supabase.table("store_orders").update({"status": new_status}).eq("id", order_id).execute()
        logger.info(f"✅ Synced order '{order_id}' status to '{new_status}' in Supabase store_orders.")
    except Exception as sb_err:
        logger.warning(f"⚠️ Notice syncing order status to Supabase store_orders: {sb_err}")

    return get_order_by_id(order_id)


# =========================================================================
# Inventory Management Functions
# =========================================================================

def get_admin_products() -> List[Dict[str, Any]]:
    """Retrieves all products for manager inventory, including active and inactive."""
def normalize_image_url(image_url: Optional[str]) -> Optional[str]:
    """Ensures local file paths or image references are converted to accessible web paths."""
    if not image_url or not isinstance(image_url, str):
        return image_url
    image_url = image_url.strip()
    if not image_url:
        return None
    # If already a valid web URL or static path
    if image_url.startswith("http://") or image_url.startswith("https://") or image_url.startswith("/uploads/") or image_url.startswith("/store/"):
        return image_url
        
    # Check if local file path or refers to earbuds
    clean_path = image_url.replace("file:///", "").replace("file://", "").strip('"\'')
    if "earbuds" in clean_path.lower():
        return "/uploads/earbuds.jpg"
        
    if (os.path.isabs(clean_path) or ":" in clean_path) and os.path.isfile(clean_path):
        try:
            import shutil
            frontend_uploads = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "frontend", "uploads"))
            os.makedirs(frontend_uploads, exist_ok=True)
            filename = os.path.basename(clean_path)
            dest_path = os.path.join(frontend_uploads, filename)
            shutil.copy(clean_path, dest_path)
            return f"/uploads/{filename}"
        except Exception as e:
            logger.warning(f"Failed to copy local image {clean_path}: {e}")

    fname = os.path.basename(clean_path.replace("\\", "/"))
    if any(fname.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp", ".svg"]):
        return f"/uploads/{fname}"

    return image_url


def get_admin_products() -> List[Dict[str, Any]]:
    """Retrieves all products for manager inventory management."""
    query = """
        SELECT id, name, description, price, image_url, stock, is_active, created_at
        FROM products
        ORDER BY id ASC;
    """
    rows = execute_query(query, fetch=True)
    for r in rows:
        if isinstance(r.get("created_at"), datetime):
            r["created_at"] = r["created_at"].isoformat()
        if r.get("price") is not None:
            r["price"] = float(r["price"])
        r["stock"] = int(r.get("stock") or 0)
        r["is_active"] = bool(r.get("is_active", True))
        r["image_url"] = normalize_image_url(r.get("image_url"))
    return rows


def get_active_products() -> List[Dict[str, Any]]:
    """Retrieves only currently active and available products for customer storefront."""
    query = """
        SELECT id, name, description, price, image_url, stock, is_active, created_at
        FROM products
        WHERE is_active = TRUE
        ORDER BY id ASC;
    """
    rows = execute_query(query, fetch=True)
    for r in rows:
        if isinstance(r.get("created_at"), datetime):
            r["created_at"] = r["created_at"].isoformat()
        if r.get("price") is not None:
            r["price"] = float(r["price"])
        r["stock"] = int(r.get("stock") or 0)
        r["is_active"] = True
        r["image_url"] = normalize_image_url(r.get("image_url"))
    return rows


def create_product(
    name: str,
    price: float,
    description: Optional[str] = None,
    stock: int = 10,
    image_url: Optional[str] = None
) -> Dict[str, Any]:
    """Inserts a new product into PostgreSQL."""
    if not name or not name.strip():
        raise ValueError("Product name cannot be empty")
    if price is None or price <= 0:
        raise ValueError("Product price must be a positive number")

    image_url = normalize_image_url(image_url)

    query = """
        INSERT INTO products (name, price, description, stock, image_url, is_active, created_at)
        VALUES (%s, %s, %s, %s, %s, TRUE, CURRENT_TIMESTAMP)
        RETURNING id, name, price, description, stock, image_url, is_active, created_at;
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (name.strip(), price, description, stock, image_url))
            new_prod = dict(cur.fetchone())

            # Sync to store_products table if it exists in PostgreSQL
            try:
                cur.execute("""
                    INSERT INTO store_products (id, name, price, description, stock, image_url, status)
                    VALUES (%s, %s, %s, %s, %s, %s, 'active')
                    ON CONFLICT (id) DO UPDATE SET
                        name = EXCLUDED.name,
                        price = EXCLUDED.price,
                        description = EXCLUDED.description,
                        stock = EXCLUDED.stock,
                        image_url = EXCLUDED.image_url,
                        status = 'active';
                """, (new_prod["id"], name.strip(), price, description, stock, image_url))
            except Exception:
                pass

            conn.commit()

    # Synchronize new product to Supabase store_products
    try:
        from src.services.chat_service import get_supabase_client
        supabase = get_supabase_client()
        supabase.table("store_products").upsert({
            "id": new_prod["id"],
            "name": name.strip(),
            "price": float(price),
            "description": description or "",
            "stock": int(stock),
            "image_url": image_url or "/uploads/earbuds.jpg",
            "status": "active"
        }).execute()
        logger.info(f"✅ Product #{new_prod['id']} synced to Supabase store_products.")
    except Exception as sb_err:
        logger.warning(f"⚠️ Failed to sync product #{new_prod['id']} to Supabase: {sb_err}")

    if isinstance(new_prod.get("created_at"), datetime):
        new_prod["created_at"] = new_prod["created_at"].isoformat()
    new_prod["price"] = float(new_prod["price"])
    return new_prod


def delete_or_deactivate_product(product_id: int) -> bool:
    """Safely soft-deactivates or deletes product while preserving historical order records."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Check if product exists
            cur.execute("SELECT id FROM products WHERE id = %s;", (product_id,))
            exists = cur.fetchone()
            if not exists:
                return False

            # Check if referenced in orders
            cur.execute("SELECT COUNT(*) AS cnt FROM orders WHERE product_id = %s;", (product_id,))
            order_refs = cur.fetchone()["cnt"]

            if order_refs > 0:
                # Soft delete: mark inactive
                cur.execute("UPDATE products SET is_active = FALSE WHERE id = %s;", (product_id,))
                try:
                    cur.execute("UPDATE store_products SET status = 'inactive' WHERE id = %s;", (product_id,))
                except Exception:
                    pass
                logger.info(f"🔒 Product #{product_id} soft-deactivated (referenced in {order_refs} orders).")
            else:
                # Safe to mark inactive or remove
                cur.execute("UPDATE products SET is_active = FALSE WHERE id = %s;", (product_id,))
                try:
                    cur.execute("UPDATE store_products SET status = 'inactive' WHERE id = %s;", (product_id,))
                except Exception:
                    pass
                logger.info(f"🗑️ Product #{product_id} deactivated.")

            conn.commit()

    # Synchronize deactivation to Supabase store_products
    try:
        from src.services.chat_service import get_supabase_client
        supabase = get_supabase_client()
        supabase.table("store_products").update({"status": "inactive"}).eq("id", product_id).execute()
        logger.info(f"✅ Product #{product_id} marked inactive in Supabase store_products.")
    except Exception as sb_err:
        logger.warning(f"⚠️ Failed to deactivate product #{product_id} in Supabase: {sb_err}")

    return True


# =========================================================================
# Aggregate Statistics
# =========================================================================

def get_manager_stats() -> Dict[str, int]:
    """Calculates live database-derived overview metrics for the manager dashboard.
    
    Active orders exclude Delivered and Returned statuses.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS cnt FROM orders;")
            total_orders = cur.fetchone()["cnt"]

            cur.execute(
                "SELECT COUNT(*) AS cnt FROM orders WHERE status NOT IN ('Delivered', 'Returned');"
            )
            active_orders = cur.fetchone()["cnt"]

            cur.execute("SELECT COUNT(*) AS cnt FROM products;")
            total_products = cur.fetchone()["cnt"]

            cur.execute("SELECT COUNT(*) AS cnt FROM products WHERE is_active = TRUE;")
            active_products = cur.fetchone()["cnt"]

    return {
        "total_orders": int(total_orders),
        "active_orders": int(active_orders),
        "total_products": int(total_products),
        "active_products": int(active_products),
    }


# =========================================================================
# Order Tracking for Telegram Bot & RAG
# =========================================================================

def lookup_customer_orders(
    order_id: Optional[str] = None,
    telegram_id: Optional[int] = None,
    email: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Grounded PostgreSQL lookup for real-time order tracking in Telegram Chatbot."""
    conditions = []
    params = []

    if order_id:
        conditions.append("o.id ILIKE %s")
        params.append(order_id.strip())

    if telegram_id:
        conditions.append("u.telegram_id = %s")
        params.append(telegram_id)

    if email:
        conditions.append("(u.email ILIKE %s OR o.customer_email ILIKE %s)")
        clean_email = email.strip().lower()
        params.extend([clean_email, clean_email])

    if not conditions:
        return []

    where_clause = " OR ".join(conditions) if not order_id else "o.id ILIKE %s"
    if order_id:
        params = [order_id.strip()]

    query = f"""
        SELECT 
            o.id AS order_id,
            o.customer_name,
            COALESCE(o.customer_email, u.email) AS customer_email,
            COALESCE(p.name, 'Product #' || COALESCE(o.product_id::text, 'N/A')) AS product_name,
            o.product_id,
            o.quantity,
            o.total,
            o.status,
            o.created_at,
            u.telegram_id,
            COALESCE(o.customer_email, u.email) AS user_email
        FROM orders o
        LEFT JOIN products p ON o.product_id = p.id
        LEFT JOIN users u ON o.user_id = u.id
        WHERE {where_clause}
        ORDER BY o.created_at DESC;
    """
    rows = execute_query(query, tuple(params), fetch=True)
    for r in rows:
        if isinstance(r.get("created_at"), datetime):
            r["created_at"] = r["created_at"].isoformat()
        if r.get("total") is not None:
            r["total"] = float(r["total"])
    return rows
