from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import SessionLocal
from schemas.user import UserCreate, UserOut
from db.models.user import User
from db.models.role import Role
from core.security import get_password_hash

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserOut)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    role = db.query(Role).filter(Role.id == user_in.role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role ID does not exist",
        )

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
