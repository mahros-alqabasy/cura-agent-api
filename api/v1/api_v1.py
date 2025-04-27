from fastapi import APIRouter

api_router = APIRouter()

@api_router.get("/healthcheck", tags=["healthcheck"])
async def healthcheck():
    return {"status": "ok"}

from fastapi import APIRouter
from api.v1.endpoints.auth import register
from api.v1.endpoints.auth import register, login
from api.v1.endpoints.auth import register, login, me

from api.v1.endpoints.auth import register, login, me, logout
from api.v1.endpoints.roles import roles_crud
from api.v1.endpoints.roles import assign_permissions
from api.v1.endpoints.permissions import permissions_crud
from api.v1.endpoints.users import users_crud
from api.v1.endpoints.patients import patients_crud

api_router = APIRouter()


api_router.include_router(register.router, prefix="/auth", tags=["auth"])
api_router.include_router(login.router, prefix="/auth", tags=["auth"])
api_router.include_router(me.router, prefix="/auth", tags=["auth"])
api_router.include_router(logout.router, prefix="/auth", tags=["auth"])
api_router.include_router(assign_permissions.router, prefix="/roles", tags=["roles"])

api_router.include_router(roles_crud.router, prefix="/roles", tags=["roles"])

api_router.include_router(permissions_crud.router, prefix="/permissions", tags=["permissions"])

api_router.include_router(users_crud.router, prefix="/users", tags=["users"])

api_router.include_router(patients_crud.router, prefix="/patients", tags=["patients"])