from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import SessionLocal
from api.v1.endpoints.auth.guards import get_current_user
from db.models.user import User
from db.models.role import Role
from schemas.user import UserCreateInternal, UserUpdate, UserOutInternal
from core.security import get_password_hash

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserOutInternal)
def create_user(user_in: UserCreateInternal, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] not in ["manager", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create users",
        )

    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    role = db.query(Role).filter(Role.id == user_in.role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    user = User(
        name=user_in.name,
        email=user_in.email,
        password=get_password_hash(user_in.password),
        role_id=user_in.role_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/", response_model=list[UserOutInternal])
def list_users(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] not in ["manager", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    users = db.query(User).all()
    return users

@router.put("/{user_id}", response_model=UserOutInternal)
def update_user(user_id: int, user_in: UserUpdate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] not in ["manager", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_in.name:
        user.name = user_in.name
    if user_in.email:
        user.email = user_in.email
    if user_in.password:
        user.password = get_password_hash(user_in.password)
    if user_in.role_id:
        role = db.query(Role).filter(Role.id == user_in.role_id).first()
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        user.role_id = user_in.role_id

    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] not in ["manager", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
