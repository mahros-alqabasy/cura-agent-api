from pydantic import BaseModel

class RoleCreate(BaseModel):
    name: str

class RoleUpdate(BaseModel):
    name: str

class RoleOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
