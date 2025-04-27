from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.config import settings
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.db.models.role import Role
from app.db.models.permission import Permission
from app.db.models.role_permission import RolePermission

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise credentials_exception

    role = db.query(Role).filter(Role.id == user.role_id).first()
    permissions = []
    if role:
        permission_links = db.query(RolePermission).filter(RolePermission.role_id == role.id).all()
        for link in permission_links:
            perm = db.query(Permission).filter(Permission.id == link.permission_id).first()
            if perm:
                permissions.append(perm.name)

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": role.name if role else None,
        "permissions": permissions
    }
