"""Database and API data models for Users, Chat History, and Tickets."""

from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class TicketStatus(str, Enum):
    """Status enumeration for in-house support tickets."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"


class UserBase(BaseModel):
    telegram_id: int
    name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime
    last_active_at: datetime

    class Config:
        from_attributes = True


class ChatMessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessageBase(BaseModel):
    user_id: int
    role: ChatMessageRole
    content: str


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessage(ChatMessageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TicketBase(BaseModel):
    user_id: int
    escalation_reason: str


class TicketCreate(TicketBase):
    pass


class Ticket(TicketBase):
    id: int
    status: TicketStatus = TicketStatus.OPEN
    created_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TicketStatusUpdate(BaseModel):
    status: TicketStatus = Field(..., description="New status for the ticket: open, in_progress, or resolved")


class AdminStats(BaseModel):
    total_users: int
    total_tickets: int
    open_tickets: int
    in_progress_tickets: int
    resolved_tickets: int


class UserHistoryResponse(BaseModel):
    user: User
    messages: List[ChatMessage]
