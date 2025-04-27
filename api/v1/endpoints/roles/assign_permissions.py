from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import SessionLocal
from api.v1.endpoints.auth.guards import get_current_user
from db.models.role import Role
from db.models.permission import Permission
from db.models.role_permission import RolePermission

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/assign-permissions/{role_id}")
def assign_permissions_to_role(
    role_id: int,
    permissions: list[int],
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] not in ["manager", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to assign permissions",
        )

    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    db.query(RolePermission).filter(RolePermission.role_id == role_id).delete()

    for permission_id in permissions:
        permission = db.query(Permission).filter(Permission.id == permission_id).first()
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Permission ID {permission_id} not found",
            )
        role_permission = RolePermission(role_id=role_id, permission_id=permission_id)
        db.add(role_permission)

    db.commit()

    return {"message": f"Permissions updated for role '{role.name}' successfully."}
