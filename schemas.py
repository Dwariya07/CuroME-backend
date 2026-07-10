from pydantic import BaseModel, EmailStr
from typing import Optional
import enum

class RoleEnum(str, enum.Enum):
    PATIENT = "patient"
    CAREGIVER = "caregiver"
    DOCTOR = "doctor"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    specialization: Optional[str] = None
    license_number: Optional[str] = None
    linked_patient_id: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    role: RoleEnum
    name: str
    patient_id: Optional[str] = None

    class Config:
        from_attributes = True