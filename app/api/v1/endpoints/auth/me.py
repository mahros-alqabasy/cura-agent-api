from fastapi import APIRouter, Depends
from app.api.v1.endpoints.auth.guards import get_current_user

router = APIRouter()

@router.get("/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
