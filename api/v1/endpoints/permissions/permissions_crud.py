from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import SessionLocal
from api.v1.endpoints.auth.guards import get_current_user
from db.models.permission import Permission
from schemas.permission import PermissionCreate, PermissionUpdate, PermissionOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PermissionOut)
def create_permission(permission_in: PermissionCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] not in ["manager", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create permissions",
        )

    permission = Permission(name=permission_in.name)
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission

@router.get("/", response_model=list[PermissionOut])
def list_permissions(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    permissions = db.query(Permission).all()
    return permissions

@router.put("/{permission_id}", response_model=PermissionOut)
def update_permission(permission_id: int, permission_in: PermissionUpdate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] not in ["manager", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update permissions",
        )

    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    permission.name = permission_in.name
    db.commit()
    db.refresh(permission)
    return permission

@router.delete("/{permission_id}")
def delete_permission(permission_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] not in ["manager", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete permissions",
        )

    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    db.delete(permission)
    db.commit()
    return {"message": "Permission deleted successfully"}
