"""Admin panel REST API endpoints for customer support staff.

Provides read/write routes for ticket management, user conversation history inspection,
and dashboard statistics. Unblocks frontend development with schema-compliant endpoints.
"""

import logging
import os
import shutil
import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Path, Header, Depends, status, UploadFile, File
from src.config import ADMIN_API_KEY
from src.db.models import (
    Ticket,
    TicketStatus,
    TicketStatusUpdate,
    AdminStats,
    UserHistoryResponse,
    User,
    ChatMessage,
    ChatMessageRole,
    OrderStatusEnum,
    OrderStatusUpdateRequest,
    AdminOrderResponse,
    CreateProductRequest,
    AdminProductResponse,
    ManagerStatsResponse,
)
from src.db.supabase_client import get_supabase_client
from src.db.postgres_client import (
    get_admin_orders,
    get_order_by_id,
    update_order_status,
    get_admin_products,
    create_product,
    delete_or_deactivate_product,
    get_manager_stats,
)

logger = logging.getLogger(__name__)


def verify_admin_key(x_admin_api_key: Optional[str] = Header(None, alias="X-Admin-API-Key")) -> bool:
    """Validates the admin API key if configured in the environment."""
    if not ADMIN_API_KEY:
        return True  # Open access in local development if no key configured
    if x_admin_api_key != ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-Admin-API-Key header"
        )
    return True


router = APIRouter(
    prefix="/api/admin",
    tags=["Admin Panel"],
    dependencies=[Depends(verify_admin_key)]
)

# --- Mock Data Fallbacks for Frontend Unblocking ---
MOCK_USERS = [
    User(id=1, telegram_id=12345678, name="Alice Smith", created_at=datetime.utcnow(), last_active_at=datetime.utcnow()),
    User(id=2, telegram_id=87654321, name="Bob Jones", created_at=datetime.utcnow(), last_active_at=datetime.utcnow()),
]

MOCK_TICKETS = [
    Ticket(
        id=101,
        user_id=1,
        status=TicketStatus.OPEN,
        escalation_reason="Low retrieval confidence on return query",
        order_id="ORD-69Z2N",
        issue_description="Customer asking about return instructions for smartwatch.",
        created_at=datetime.utcnow()
    ),
    Ticket(
        id=102,
        user_id=2,
        status=TicketStatus.IN_PROGRESS,
        escalation_reason="Red-flag detected: 'damaged item'",
        order_id="ORD-88219",
        issue_description="i get the smart watch but it is not working ? and i think it is dammaged",
        created_at=datetime.utcnow()
    ),
    Ticket(
        id=103,
        user_id=1,
        status=TicketStatus.RESOLVED,
        escalation_reason="Manual escalation requested",
        order_id=None,
        issue_description="User requested human support agent connection.",
        created_at=datetime.utcnow(),
        resolved_at=datetime.utcnow()
    ),
]


@router.get("/tickets", response_model=List[Ticket], summary="List all support tickets")
async def list_tickets(status: Optional[TicketStatus] = Query(None, description="Filter tickets by status")):
    """Retrieves all escalated tickets, with optional status filtering (`open`, `in_progress`, `resolved`)."""
    try:
        supabase = get_supabase_client()
        query = supabase.table("tickets").select("*")
        if status:
            query = query.eq("status", status.value)
        res = query.order("created_at", desc=True).execute()

        if res.data:
            return res.data
    except Exception as e:
        logger.warning(f"Database query failed, returning mock data: {e}")

    # Fallback to mock data
    if status:
        return [t for t in MOCK_TICKETS if t.status == status]
    return MOCK_TICKETS


@router.patch("/tickets/{ticket_id}/status", response_model=Ticket, summary="Update ticket status")
async def update_ticket_status(
    ticket_id: int = Path(..., description="ID of ticket to update"),
    payload: TicketStatusUpdate = ...
):
    """Primary write path for staff to manually update ticket status (`open` -> `in_progress` -> `resolved`)."""
    now_iso = datetime.utcnow().isoformat()
    update_fields = {"status": payload.status.value}
    
    if payload.status == TicketStatus.RESOLVED:
        update_fields["resolved_at"] = now_iso
    else:
        update_fields["resolved_at"] = None

    try:
        supabase = get_supabase_client()
        res = supabase.table("tickets").update(update_fields).eq("id", ticket_id).execute()

        if res.data and len(res.data) > 0:
            logger.info(f"✅ Ticket #{ticket_id} updated to status '{payload.status.value}'")
            return res.data[0]
    except Exception as e:
        logger.warning(f"Database update failed for ticket #{ticket_id}, operating on mock fallback: {e}")

    # Fallback for mock environment
    for ticket in MOCK_TICKETS:
        if ticket.id == ticket_id:
            ticket.status = payload.status
            ticket.resolved_at = datetime.utcnow() if payload.status == TicketStatus.RESOLVED else None
            return ticket

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ticket #{ticket_id} not found")


@router.get("/users", response_model=List[User], summary="List all registered customers")
async def list_users():
    """Retrieves all registered Telegram users from database."""
    try:
        supabase = get_supabase_client()
        res = supabase.table("users").select("*").order("last_active_at", desc=True).execute()
        if res.data:
            return res.data
    except Exception as e:
        logger.warning(f"Database query failed for users list, returning mock fallback: {e}")

    return MOCK_USERS


@router.get("/users/{user_id}/history", response_model=UserHistoryResponse, summary="Get full user chat history")
async def get_user_chat_history(user_id: int = Path(..., description="ID of user")):
    """Retrieves a user's full conversation history and profile information."""
    try:
        supabase = get_supabase_client()
        user_res = supabase.table("users").select("*").eq("id", user_id).execute()
        
        if user_res.data:
            user_obj = user_res.data[0]
            msg_res = supabase.table("chat_history").select("*").eq("user_id", user_id).order("created_at").execute()
            messages = msg_res.data or []
            return UserHistoryResponse(user=user_obj, messages=messages)
    except Exception as e:
        logger.warning(f"Database query failed for user #{user_id}, returning mock fallback: {e}")

    # Fallback mock data
    mock_user = next((u for u in MOCK_USERS if u.id == user_id), MOCK_USERS[0])
    mock_messages = [
        ChatMessage(id=1, user_id=user_id, role=ChatMessageRole.USER, content="Hello, where is my order?", created_at=datetime.utcnow()),
        ChatMessage(id=2, user_id=user_id, role=ChatMessageRole.ASSISTANT, content="Let me check store policy for order tracking.", created_at=datetime.utcnow()),
    ]
    return UserHistoryResponse(user=mock_user, messages=mock_messages)


@router.get("/stats", response_model=AdminStats, summary="Get aggregate admin metrics")
async def get_admin_stats():
    """Returns aggregated stats for the admin dashboard: total users, ticket counts by status."""
    try:
        supabase = get_supabase_client()
        users_count = len(supabase.table("users").select("id").execute().data or [])
        tickets = supabase.table("tickets").select("*").execute().data or []

        total_tickets = len(tickets)
        open_tickets = sum(1 for t in tickets if t.get("status") == "open")
        in_progress_tickets = sum(1 for t in tickets if t.get("status") == "in_progress")
        resolved_tickets = sum(1 for t in tickets if t.get("status") == "resolved")

        return AdminStats(
            total_users=users_count,
            total_tickets=total_tickets,
            open_tickets=open_tickets,
            in_progress_tickets=in_progress_tickets,
            resolved_tickets=resolved_tickets
        )
    except Exception as e:
        logger.warning(f"Database query for stats failed, returning mock dashboard metrics: {e}")

    return AdminStats(
        total_users=2,
        total_tickets=3,
        open_tickets=1,
        in_progress_tickets=1,
        resolved_tickets=1
    )


# =========================================================================
# Dynamic Manager Dashboard Endpoints
# =========================================================================

@router.get("/orders", response_model=List[AdminOrderResponse], summary="List all customer orders")
async def list_admin_orders(
    status: Optional[str] = Query(None, description="Filter orders by status: Booked, Shipped, Out for Delivery, Delivered, Returned"),
    search: Optional[str] = Query(None, description="Client-side or backend search by Order ID, Customer Name, or Product Name")
):
    """Retrieves all active and historical orders joined with products and customer accounts."""
    try:
        orders = get_admin_orders(status_filter=status, search=search)
        return orders
    except Exception as e:
        logger.error(f"❌ Failed to fetch admin orders from PostgreSQL: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database query failed: {str(e)}"
        )


@router.patch("/orders/{order_id}/status", response_model=AdminOrderResponse, summary="Update order lifecycle status")
async def update_order_status_endpoint(
    order_id: str = Path(..., description="Unique Order ID to update (e.g. ORD-10101)"),
    payload: OrderStatusUpdateRequest = ...
):
    """Primary write path for managers to transition order status within an atomic transaction.
    
    Allowed statuses: Booked, Shipped, Out for Delivery, Delivered, Returned.
    """
    try:
        updated = update_order_status(order_id=order_id, new_status=payload.status.value)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order '{order_id}' not found in database"
            )

        target_status = payload.status.value
        customer_email = updated.get("customer_email") or updated.get("user_email")

        # Dispatch structured email notification for lifecycle transitions
        if customer_email and target_status in ("Shipped", "Out for Delivery", "Delivered", "Returned"):
            try:
                from src.services.email_service import send_order_status_update_email
                email_res = send_order_status_update_email(
                    customer_name=updated.get("customer_name") or "Valued Customer",
                    customer_email=customer_email,
                    order_id=order_id,
                    new_status=target_status,
                    total=float(updated.get("total") or 0.0),
                    product_name=updated.get("product_name") or "Order Item",
                    quantity=int(updated.get("quantity") or 1)
                )
                updated["email_notification_status"] = email_res.get("status")
                updated["email_notification_message"] = email_res.get("message")
                logger.info(f"📧 Status update email for #{order_id} ({target_status}) to {customer_email}: {email_res.get('status')}")
            except Exception as email_err:
                logger.error(f"⚠️ Failed to send status update email for #{order_id}: {email_err}")
                updated["email_notification_status"] = "error"
                updated["email_notification_message"] = str(email_err)

        return updated
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(ve)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to update status for order '{order_id}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database transaction error: {str(e)}"
        )


@router.get("/products", response_model=List[AdminProductResponse], summary="List all products for inventory management")
async def list_admin_products():
    """Retrieves all product records from PostgreSQL for the manager inventory interface."""
    try:
        return get_admin_products()
    except Exception as e:
        logger.error(f"❌ Failed to fetch inventory products: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database query failed: {str(e)}"
        )


@router.post("/upload-image", summary="Upload product image file")
async def upload_product_image(file: UploadFile = File(...)):
    """Uploads an image file and stores it in the static /uploads folder."""
    try:
        backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        uploads_dir = os.path.abspath(os.path.join(backend_dir, "..", "frontend", "uploads"))
        os.makedirs(uploads_dir, exist_ok=True)

        orig_filename = file.filename or "image.jpg"
        ext = os.path.splitext(orig_filename)[1].lower()
        if ext not in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}:
            ext = ".jpg"

        # Safe filename
        base_clean = "".join(c for c in os.path.splitext(orig_filename)[0] if c.isalnum() or c in ("-", "_")).strip() or "product"
        clean_name = f"{base_clean}{ext}"
        dest_path = os.path.join(uploads_dir, clean_name)

        with open(dest_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "status": "success",
            "image_url": f"/uploads/{clean_name}",
            "filename": clean_name
        }
    except Exception as e:
        logger.error(f"❌ Failed to save uploaded product image: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save image file: {str(e)}"
        )


@router.post("/products", response_model=AdminProductResponse, status_code=status.HTTP_201_CREATED, summary="Add new product to catalog")
async def create_admin_product(payload: CreateProductRequest):
    """Inserts a new product into PostgreSQL with server-side Pydantic validation."""
    try:
        new_prod = create_product(
            name=payload.name,
            price=payload.price,
            description=payload.description,
            stock=payload.stock or 0,
            image_url=payload.image_url
        )
        return new_prod
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(ve)
        )
    except Exception as e:
        logger.error(f"❌ Failed to create product in PostgreSQL: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error creating product: {str(e)}"
        )


@router.delete("/products/{product_id}", summary="Delete or deactivate product")
async def delete_admin_product(
    product_id: int = Path(..., description="ID of product to remove or deactivate")
):
    """Safely soft-deactivates or deletes product while preserving historical order records."""
    try:
        success = delete_or_deactivate_product(product_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product #{product_id} not found"
            )
        return {
            "status": "success",
            "message": f"Product #{product_id} has been deactivated and removed from storefront catalog."
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to deactivate product #{product_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error deleting product: {str(e)}"
        )


@router.get("/manager-stats", response_model=ManagerStatsResponse, summary="Get live manager dashboard metrics")
async def get_manager_dashboard_stats():
    """Returns database-derived metrics: total orders, active orders, total products, active products."""
    try:
        return get_manager_stats()
    except Exception as e:
        logger.error(f"❌ Failed to fetch manager metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database query failed: {str(e)}"
        )
