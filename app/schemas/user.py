from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role_id: int

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role_id: int

    class Config:
      model_config = {
          "from_attributes": True
      }

class UserLogin(BaseModel):
    email: str
    password: str

class UserCreateInternal(BaseModel):
    name: str
    email: EmailStr
    password: str
    role_id: int

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role_id: int | None = None

class UserOutInternal(BaseModel):
    id: int
    name: str
    email: EmailStr
    role_id: int

    class Config:
        orm_mode = True
