from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import User, Ticket, TicketComment, UserRole
from ..schemas import TicketCreate, TicketResponse, TicketUpdate, TicketCommentCreate, TicketCommentResponse
from ..auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=TicketResponse)
async def create_ticket(
    ticket: TicketCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new ticket."""
    if current_user.role not in [UserRole.SITE_ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create tickets"
        )

    new_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority,
        status="open",
        created_by_id=current_user.id,
        site_id=current_user.site_id
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

@router.get("/", response_model=List[TicketResponse])
async def list_tickets(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List tickets based on user role."""
    if current_user.role == UserRole.SUPER_ADMIN:
        tickets = db.query(Ticket).all()
    elif current_user.role == UserRole.SITE_ADMIN:
        tickets = db.query(Ticket).filter(Ticket.site_id == current_user.site_id).all()
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view tickets"
        )
    return tickets

@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific ticket."""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    if current_user.role != UserRole.SUPER_ADMIN and ticket.site_id != current_user.site_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this ticket"
        )

    return ticket

@router.put("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: int,
    ticket_update: TicketUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a ticket's status."""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    if current_user.role != UserRole.SUPER_ADMIN and ticket.site_id != current_user.site_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this ticket"
        )

    for key, value in ticket_update.dict(exclude_unset=True).items():
        setattr(ticket, key, value)

    db.commit()
    db.refresh(ticket)
    return ticket

@router.post("/{ticket_id}/comments", response_model=TicketCommentResponse)
async def add_comment(
    ticket_id: int,
    comment: TicketCommentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add a comment to a ticket."""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    if current_user.role != UserRole.SUPER_ADMIN and ticket.site_id != current_user.site_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to comment on this ticket"
        )

    new_comment = TicketComment(
        content=comment.content,
        ticket_id=ticket_id,
        user_id=current_user.id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/{ticket_id}/comments", response_model=List[TicketCommentResponse])
async def list_comments(
    ticket_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all comments for a ticket."""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    if current_user.role != UserRole.SUPER_ADMIN and ticket.site_id != current_user.site_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view these comments"
        )

    return db.query(TicketComment).filter(TicketComment.ticket_id == ticket_id).all()
