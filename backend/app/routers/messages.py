from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
import os
from datetime import datetime

from ..database import get_db
from ..models import User, Message, MessageAttachment, UserRole
from ..schemas import MessageCreate, MessageResponse, UploadedFileResponse
from ..auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=MessageResponse)
async def create_message(
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new message."""
    # Get recipient
    recipient = db.query(User).filter(User.id == message_data.recipient_id).first()
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipient not found"
        )

    # Validate messaging permissions
    if current_user.role == UserRole.USER:
        # Users can only message their site admin
        if recipient.role != UserRole.SITE_ADMIN or recipient.site_id != current_user.site_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Users can only message their site admin"
            )
    elif current_user.role == UserRole.SITE_ADMIN:
        # Site admins can message their users or super admin
        if (recipient.role == UserRole.USER and recipient.site_id != current_user.site_id) or \
           (recipient.role == UserRole.SITE_ADMIN):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid recipient"
            )
    # Super admins can message anyone

    # Create message
    new_message = Message(
        subject=message_data.subject,
        content=message_data.content,
        sender_id=current_user.id,
        recipient_id=message_data.recipient_id
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message

@router.get("/", response_model=List[MessageResponse])
async def list_messages(
    received: Optional[bool] = True,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List messages (received or sent)."""
    if received:
        messages = db.query(Message)\
            .filter(Message.recipient_id == current_user.id)\
            .order_by(Message.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
    else:
        messages = db.query(Message)\
            .filter(Message.sender_id == current_user.id)\
            .order_by(Message.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()

    return messages

@router.get("/{message_id}", response_model=MessageResponse)
async def get_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific message."""
    message = db.query(Message).filter(
        Message.id == message_id,
        or_(
            Message.sender_id == current_user.id,
            Message.recipient_id == current_user.id
        )
    ).first()

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found or access denied"
        )

    # Mark message as read if current user is recipient
    if message.recipient_id == current_user.id and not message.is_read:
        message.is_read = True
        db.commit()
        db.refresh(message)

    return message

@router.post("/{message_id}/attachment", response_model=UploadedFileResponse)
async def add_attachment(
    message_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Add an attachment to a message."""
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )

    # Only sender can add attachments
    if message.sender_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the sender can add attachments"
        )

    # Create upload directory if it doesn't exist
    upload_dir = os.getenv("UPLOAD_DIR", "./uploads")
    message_uploads = os.path.join(upload_dir, "messages", str(message_id))
    os.makedirs(message_uploads, exist_ok=True)

    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(message_uploads, filename)

    # Save file
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # Create attachment record
    attachment = MessageAttachment(
        filename=filename,
        original_filename=file.filename,
        file_path=file_path,
        message_id=message_id
    )

    db.add(attachment)
    db.commit()
    db.refresh(attachment)

    return attachment

@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a message."""
    message = db.query(Message).filter(
        Message.id == message_id,
        or_(
            Message.sender_id == current_user.id,
            Message.recipient_id == current_user.id
        )
    ).first()

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found or access denied"
        )

    # Delete all attachments first
    attachments = db.query(MessageAttachment).filter(
        MessageAttachment.message_id == message_id
    ).all()

    for attachment in attachments:
        # Delete file from filesystem
        try:
            os.remove(attachment.file_path)
        except OSError:
            pass  # Ignore if file doesn't exist
        db.delete(attachment)

    # Delete message
    db.delete(message)
    db.commit()

    return None
