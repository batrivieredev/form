from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import json
from datetime import datetime
import os

from ..database import get_db
from ..models import User, Form, FormResponse, UploadedFile, UserRole
from ..schemas import (
    FormCreate,
    FormUpdate,
    FormResponse as FormResponseSchema,
    FormSubmissionResponse,
    UploadedFileResponse
)
from ..auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=FormResponseSchema)
async def create_form(
    form_data: FormCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new form (site admin only)."""
    if current_user.role != UserRole.SITE_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only site admins can create forms"
        )

    # Validate that the form belongs to the admin's site
    if form_data.site_id != current_user.site_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create form for another site"
        )

    # Create new form
    new_form = Form(
        title=form_data.title,
        description=form_data.description,
        fields=json.dumps(form_data.fields),
        site_id=form_data.site_id
    )

    db.add(new_form)
    db.commit()
    db.refresh(new_form)

    return new_form

@router.get("/", response_model=List[FormResponseSchema])
async def list_forms(
    site_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List forms for a site."""
    query = db.query(Form)

    if current_user.role == UserRole.SUPER_ADMIN:
        if site_id:
            query = query.filter(Form.site_id == site_id)
    elif current_user.role == UserRole.SITE_ADMIN:
        query = query.filter(Form.site_id == current_user.site_id)
    else:
        query = query.filter(Form.site_id == current_user.site_id)

    forms = query.offset(skip).limit(limit).all()
    return forms

@router.get("/{form_id}", response_model=FormResponseSchema)
async def get_form(
    form_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific form."""
    form = db.query(Form).filter(Form.id == form_id).first()
    if not form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form not found"
        )

    # Check permissions
    if current_user.role != UserRole.SUPER_ADMIN:
        if form.site_id != current_user.site_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot access form from another site"
            )

    return form

@router.put("/{form_id}", response_model=FormResponseSchema)
async def update_form(
    form_id: int,
    form_data: FormUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a form (site admin only)."""
    if current_user.role != UserRole.SITE_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only site admins can update forms"
        )

    form = db.query(Form).filter(Form.id == form_id).first()
    if not form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form not found"
        )

    # Check if form belongs to admin's site
    if form.site_id != current_user.site_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update form from another site"
        )

    # Update form fields
    for field, value in form_data.dict(exclude_unset=True).items():
        if field == "fields" and value is not None:
            setattr(form, field, json.dumps(value))
        else:
            setattr(form, field, value)

    db.commit()
    db.refresh(form)

    return form

@router.delete("/{form_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_form(
    form_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a form (site admin only)."""
    if current_user.role != UserRole.SITE_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only site admins can delete forms"
        )

    form = db.query(Form).filter(Form.id == form_id).first()
    if not form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form not found"
        )

    # Check if form belongs to admin's site
    if form.site_id != current_user.site_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete form from another site"
        )

    db.delete(form)
    db.commit()
    return None

@router.post("/{form_id}/submit", response_model=FormSubmissionResponse)
async def submit_form(
    form_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Submit a form response."""
    form = db.query(Form).filter(Form.id == form_id).first()
    if not form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form not found"
        )

    # Validate that user belongs to the correct site
    if current_user.site_id != form.site_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot submit form for another site"
        )

    # Create form response
    form_response = FormResponse(
        form_id=form_id,
        user_id=current_user.id,
        data=json.dumps(data)
    )

    db.add(form_response)
    db.commit()
    db.refresh(form_response)

    return form_response

@router.post("/{form_id}/upload", response_model=UploadedFileResponse)
async def upload_file(
    form_id: int,
    response_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Upload a file for a form response."""
    form_response = db.query(FormResponse).filter(
        FormResponse.id == response_id,
        FormResponse.form_id == form_id
    ).first()

    if not form_response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form response not found"
        )

    # Check permissions
    if current_user.id != form_response.user_id and current_user.role not in [UserRole.SUPER_ADMIN, UserRole.SITE_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot upload file for another user's response"
        )

    # Create upload directory if it doesn't exist
    upload_dir = os.getenv("UPLOAD_DIR", "./uploads")
    os.makedirs(upload_dir, exist_ok=True)

    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(upload_dir, filename)

    # Save file
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # Create file record
    uploaded_file = UploadedFile(
        filename=filename,
        original_filename=file.filename,
        file_path=file_path,
        form_response_id=response_id
    )

    db.add(uploaded_file)
    db.commit()
    db.refresh(uploaded_file)

    return uploaded_file
