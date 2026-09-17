"""Pydantic data models for Storefront products, carts, and order checkouts."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


class StoreProduct(BaseModel):
    """Product model for the storefront catalog."""
    id: int
    name: str = Field(..., description="Name of product")
    description: Optional[str] = Field(None, description="Detailed product description")
    price: float = Field(..., description="Unit price of product")
    image_url: Optional[str] = Field(None, description="Product image URL")
    stock: int = Field(..., description="Available inventory stock")
    status: str = Field("active", description="Product status: active or inactive")

    class Config:
        from_attributes = True


class CustomerInfo(BaseModel):
    """Customer checkout information."""
    name: str = Field(..., min_length=2, description="Customer full name")
    address: str = Field(..., min_length=5, description="Shipping street address")
    email: str = Field(..., description="Customer contact email address")
    phone: str = Field(..., min_length=7, description="Customer contact phone number")


class OrderItemRequest(BaseModel):
    """Single item request in order checkout payload."""
    product_id: int = Field(..., description="ID of product being purchased")
    quantity: int = Field(..., gt=0, description="Quantity to purchase (must be > 0)")


class CreateOrderRequest(BaseModel):
    """Order checkout payload submitted by customer storefront."""
    customer: CustomerInfo = Field(..., description="Customer contact and shipping details")
    items: List[OrderItemRequest] = Field(..., min_items=1, description="List of cart items being ordered")


class OrderItemResponse(BaseModel):
    """Detailed order item in checkout response."""
    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float


class OrderResponse(BaseModel):
    """Order confirmation response returned to storefront."""
    status: str = "success"
    order_id: str = Field(..., description="Unique generated order ID (e.g. ORD-XXXXX)")
    customer: CustomerInfo
    items: List[OrderItemResponse]
    total: float = Field(..., description="Server-calculated total price for order")
    created_at: str
