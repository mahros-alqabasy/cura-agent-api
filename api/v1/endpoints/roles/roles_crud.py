from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import SessionLocal
from api.v1.endpoints.auth.guards import get_current_user
from db.models.role import Role
from schemas.role import RoleCreate, RoleUpdate, RoleOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=RoleOut)
def create_role(role_in: RoleCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] not in ["manager", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create roles",
        )

    role = Role(name=role_in.name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

@router.get("/", response_model=list[RoleOut])
def list_roles(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    return roles

@router.put("/{role_id}", response_model=RoleOut)
def update_role(role_id: int, role_in: RoleUpdate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] not in ["manager", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update roles",
        )

    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    role.name = role_in.name
    db.commit()
    db.refresh(role)
    return role

@router.delete("/{role_id}")
def delete_role(role_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] not in ["manager", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete roles",
        )

    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    db.delete(role)
    db.commit()
    return {"message": "Role deleted successfully"}
