from fastapi import APIRouter, Depends
from app.api.v1.endpoints.auth.guards import get_current_user

router = APIRouter()

@router.post("/logout")
def logout(current_user: dict = Depends(get_current_user)):
    return {"message": "Logout successful."}
