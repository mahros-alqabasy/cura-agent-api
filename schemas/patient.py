from pydantic import BaseModel
from datetime import date

class PatientCreate(BaseModel):
    full_name: str
    date_of_birth: date | None = None
    gender: str | None = None
    phone: str | None = None
    address: str | None = None
    emergency_contact: str | None = None

class PatientUpdate(BaseModel):
    full_name: str | None = None
    date_of_birth: date | None = None
    gender: str | None = None
    phone: str | None = None
    address: str | None = None
    emergency_contact: str | None = None

class PatientOut(BaseModel):
    id: int
    full_name: str
    date_of_birth: date | None
    gender: str | None
    phone: str | None
    address: str | None
    emergency_contact: str | None

    class Config:
        orm_mode = True
