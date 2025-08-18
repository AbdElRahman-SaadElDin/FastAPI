from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

class Diagnosis(BaseModel):
    diagnosis: str
    prognosis: str
    medical_report: str = Field(..., alias="medical-report")
    medical_treatment: str = Field(..., alias="medical-treatment")
    schedule: str
    complaint: str

    class Config:
        allow_population_by_field_name = True

class Case(BaseModel):
    diagnosis: List[Diagnosis]

class PatientInfo(BaseModel):
    id: str
    name: str
    date_of_admission: str = Field(..., alias="date of admission")
    phone: str
    country: str
    gender: str
    profession: str
    age: int
    cases: List[Case] = []

    class Config:
        allow_population_by_field_name = True

class Doctor(BaseModel):
    code: str
    name: str
    Age: int
    phone: str
    profession: str
    specialty: str
    gender: str
    email: EmailStr
    password: str
    country: str
    city: str
    patient: List[PatientInfo] = []

class Patient(BaseModel):
    email: str
    name: str
    age: int
    phone: str
    password: str
    country: str
    drCodes: List[str]

class PatientDoctor(BaseModel):
    doctor_code: str = Field(..., alias="doctor-code")
    patient_phone: str = Field(..., alias="patient-phone")

    class Config:
        allow_population_by_field_name = True

# Create models (for POST requests)
class CreateDoctor(BaseModel):
    code: str
    name: str
    Age: int
    phone: str
    profession: str
    specialty: str
    gender: str
    email: EmailStr
    password: str
    country: str
    city: str

class CreatePatient(BaseModel):
    email: str
    name: str
    age: int
    phone: str
    password: str
    country: str

# Update models (for PUT requests - all fields optional)
class UpdateDoctor(BaseModel):
    name: Optional[str] = None
    Age: Optional[int] = None
    phone: Optional[str] = None
    profession: Optional[str] = None
    specialty: Optional[str] = None
    gender: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None

class UpdatePatient(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    country: Optional[str] = None

# Additional models for diagnosis and cases
class CreateDiagnosis(BaseModel):
    diagnosis: str
    prognosis: str
    medical_report: str = Field(..., alias="medical-report")
    medical_treatment: str = Field(..., alias="medical-treatment")
    schedule: str
    complaint: str

    class Config:
        allow_population_by_field_name = True

class CreateCase(BaseModel):
    diagnosis: List[CreateDiagnosis]

class CreatePatientInfo(BaseModel):
    id: str
    name: str
    date_of_admission: str = Field(..., alias="date of admission")
    phone: str
    country: str
    gender: str
    profession: str
    age: int
    cases: List[CreateCase] = []

    class Config:
        allow_population_by_field_name = True