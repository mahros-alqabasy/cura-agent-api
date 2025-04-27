from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.token import Token
from app.schemas.user import UserLogin
from app.db.models.user import User
from app.db.models.role import Role
from app.db.models.permission import Permission
from app.db.models.role_permission import RolePermission
from app.core.security import verify_password, create_access_token
from datetime import timedelta

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(user_in.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    role = db.query(Role).filter(Role.id == user.role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role not assigned correctly"
        )

    permission_links = db.query(RolePermission).filter(RolePermission.role_id == role.id).all()
    permissions = []
    for link in permission_links:
        perm = db.query(Permission).filter(Permission.id == link.permission_id).first()
        if perm:
            permissions.append(perm.name)

    token_data = {
        "user_id": user.id,
        "role": role.name,
        "permissions": permissions
    }

    access_token = create_access_token(
        data=token_data,
        expires_delta=timedelta(minutes=60)
    )

    return Token(access_token=access_token, token_type="bearer")
