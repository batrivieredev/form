from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    SITE_ADMIN = "site_admin"
    USER = "user"

class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"

# Base Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    role: Optional[UserRole] = UserRole.USER

class SiteBase(BaseModel):
    name: str
    subdomain: str

class FormBase(BaseModel):
    title: str
    description: Optional[str] = None
    fields: Dict[str, Any]

class MessageBase(BaseModel):
    subject: str
    content: str

class TicketBase(BaseModel):
    title: str
    description: str
    priority: TicketPriority

class TicketCommentBase(BaseModel):
    content: str

# Create/Update Schemas
class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class SiteCreate(SiteBase):
    pass

class SiteUpdate(BaseModel):
    name: Optional[str] = None
    subdomain: Optional[str] = None

class FormCreate(FormBase):
    site_id: int

class FormUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    fields: Optional[Dict[str, Any]] = None

class FormResponseCreate(BaseModel):
    form_id: int
    data: Dict[str, Any]

class MessageCreate(MessageBase):
    recipient_id: int

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None

class TicketCommentCreate(TicketCommentBase):
    pass

# Response Schemas
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    site_id: Optional[int]

    class Config:
        orm_mode = True

class SiteResponse(SiteBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class FormResponse(FormBase):
    id: int
    site_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class FormSubmissionResponse(BaseModel):
    id: int
    form_id: int
    user_id: int
    data: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class MessageResponse(MessageBase):
    id: int
    sender_id: int
    recipient_id: int
    is_read: bool
    created_at: datetime

    class Config:
        orm_mode = True

class TicketResponse(TicketBase):
    id: int
    status: TicketStatus
    created_at: datetime
    created_by_id: int
    site_id: int
    comments: List['TicketCommentResponse'] = []

    class Config:
        orm_mode = True

class TicketCommentResponse(TicketCommentBase):
    id: int
    ticket_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[UserRole] = None
    site_id: Optional[int] = None

# File Upload Schemas
class UploadedFileResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    created_at: datetime

    class Config:
        orm_mode = True

TicketResponse.update_forward_refs()
