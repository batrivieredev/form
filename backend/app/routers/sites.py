from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import User, Site, UserRole
from ..schemas import SiteCreate, SiteUpdate, SiteResponse
from ..auth import get_current_active_user, validate_super_admin

router = APIRouter()

@router.post("/", response_model=SiteResponse)
async def create_site(
    site_data: SiteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new site (super admin only)."""
    validate_super_admin(current_user)

    # Check if site with same name or subdomain exists
    if db.query(Site).filter(Site.name == site_data.name).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Site name already exists"
        )

    if db.query(Site).filter(Site.subdomain == site_data.subdomain).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subdomain already exists"
        )

    # Create new site
    new_site = Site(**site_data.dict())
    db.add(new_site)
    db.commit()
    db.refresh(new_site)

    return new_site

@router.get("/", response_model=List[SiteResponse])
async def list_sites(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all sites (super admin only)."""
    validate_super_admin(current_user)
    sites = db.query(Site).offset(skip).limit(limit).all()
    return sites

@router.get("/{site_id}", response_model=SiteResponse)
async def get_site(
    site_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific site."""
    # Super admin can access any site
    if current_user.role != UserRole.SUPER_ADMIN:
        # Site admin can only access their own site
        if current_user.role == UserRole.SITE_ADMIN and current_user.site_id != site_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )

    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )

    return site

@router.put("/{site_id}", response_model=SiteResponse)
async def update_site(
    site_id: int,
    site_data: SiteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a site (super admin only)."""
    validate_super_admin(current_user)

    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )

    # Check for name/subdomain conflicts if they are being updated
    if site_data.name and site_data.name != site.name:
        if db.query(Site).filter(Site.name == site_data.name).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Site name already exists"
            )

    if site_data.subdomain and site_data.subdomain != site.subdomain:
        if db.query(Site).filter(Site.subdomain == site_data.subdomain).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subdomain already exists"
            )

    # Update site
    for field, value in site_data.dict(exclude_unset=True).items():
        setattr(site, field, value)

    db.commit()
    db.refresh(site)

    return site

@router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_site(
    site_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a site (super admin only)."""
    validate_super_admin(current_user)

    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )

    # Delete site
    db.delete(site)
    db.commit()

    return None
