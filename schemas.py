from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import enum

# 1. DEFINE THE ENUM FIRST
class RoleEnum(str, enum.Enum):
    PATIENT = "patient"
    CAREGIVER = "caregiver"
    DOCTOR = "doctor"

# 2. THEN DEFINE THE MODEL THAT USES THE ENUM
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum  # Now Python knows what RoleEnum is!
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    specialization: Optional[str] = None
    license_number: Optional[str] = Field(None, alias="licenseNumber")
    linked_patient_id: Optional[str] = Field(None, alias="linkedPatientId")
    patient_id: Optional[str] = Field(None, alias="patientId")

    class Config:
        populate_by_name = True

# 3. DEFINE RESPONSE MODEL
class UserResponse(BaseModel):
    id: str
    email: EmailStr
    role: RoleEnum
    name: str
    patient_id: Optional[str] = None

    class Config:
        from_attributes = True