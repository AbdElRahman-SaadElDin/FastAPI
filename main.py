from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json
import os
from models import Doctor, Patient, PatientDoctor, Diagnosis, Case, PatientInfo, CreateDoctor, CreatePatient, UpdateDoctor, UpdatePatient, UpdatePatientInfo

app = FastAPI(
    title="Medical Reminder API",
    description="A FastAPI server for managing doctors, patients, and medical records",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory data storage (for Vercel serverless environment)
# Note: This data will be reset on each deployment
_in_memory_data = {
  "doctors": [
    {
      "code": "EGP12Hop676",
      "name": "AbdElRahman Mohamed Saad-ElDin",
      "Age": 24,
      "phone": "+201119944899",
      "profession": "Software Engineer",
      "specialty": "Data Science",
      "gender": "male",
      "email": "abdelrahmansaad@gmail.com",
      "password": "SaadSaadSaad@@777",
      "country": "Egypt",
      "city": "Alexandria",
      "patient": [
        {
          "id": "141516",
          "name": "Mazen Ahmed",
          "dateOfAdmission": "2025-08-20T10:30:00Z",
          "phone": "+201205621566",
          "country": "Egypt",
          "gender": "male",
          "profession": "frontend",
          "age": 23,
          "cases": [
            {
              "diagnosis": [
                {
                  "diagnosis": "Type 2 Diabetes Mellitus",
                  "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control and prevent long-term complications.",
                  "medical-report": "Patient exhibits elevated fasting blood glucose levels over the past 3 months. HbA1c is 7.5%. No signs of diabetic retinopathy. Blood pressure is within normal range.",
                  "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise, and quarterly check-ups.",
                  "schedule": "2025-08-20T10:30:00Z",
                  "complaint": "Frequent urination, increased thirst, and fatigue."
                },
                {
                  "diagnosis": "Acute Bronchitis",
                  "prognosis": "Condition is self-limiting in most cases and expected to improve within 1–3 weeks with treatment and rest. Low risk of complications if managed appropriately.",
                  "medical-report": "Patient presents with persistent cough for the past 10 days, mild fever (37.8°C), and chest congestion. No signs of pneumonia on chest X-ray. Oxygen saturation at 98%.",
                  "medical-treatment": "Prescribed Amoxicillin 500mg three times daily for 7 days, increased fluid intake, and rest.",
                  "schedule": "2025-08-22T09:15:00Z",
                  "complaint": "Persistent cough, mild fever, and difficulty breathing during physical activity."
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "code": "EGP45Med123",
      "name": "Dr. Salma Hassan",
      "Age": 35,
      "phone": "+201224587412",
      "profession": "Doctor",
      "specialty": "Cardiology",
      "gender": "female",
      "email": "salma.hassan@hospital.com",
      "password": "SalmaCardio@@2025",
      "country": "Egypt",
      "city": "Cairo",
      "patient": [
        {
          "id": "202589",
          "name": "Omar Ali",
          "dateOfAdmission": "2025-07-10T11:00:00Z",
          "phone": "+201005698741",
          "country": "Egypt",
          "gender": "male",
          "profession": "Teacher",
          "age": 40,
          "cases": [
            {
              "diagnosis": [
                {
                  "diagnosis": "Hypertension",
                  "prognosis": "With proper lifestyle modifications and regular medication adherence, blood pressure can be controlled and cardiovascular risk reduced.",
                  "medical-report": "Patient has recorded consistent BP readings of 150/95 mmHg over the last month. ECG shows no abnormalities. Cholesterol levels slightly elevated.",
                  "medical-treatment": "Prescribed Amlodipine 5mg daily, dietary salt reduction, and daily 30-min walks.",
                  "schedule": "2025-07-15T09:00:00Z",
                  "complaint": "Headaches, dizziness, occasional blurred vision."
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "code": "EGP78Derm999",
      "name": "Dr. Karim El-Sayed",
      "Age": 42,
      "phone": "+201334785215",
      "profession": "Doctor",
      "specialty": "Dermatology",
      "gender": "male",
      "email": "karim.derma@hospital.com",
      "password": "DermaKarim@@2025",
      "country": "Egypt",
      "city": "Giza",
      "patient": [
        {
          "id": "304522",
          "name": "Sara Mohamed",
          "dateOfAdmission": "2025-06-05T08:45:00Z",
          "phone": "+201114785236",
          "country": "Egypt",
          "gender": "female",
          "profession": "Designer",
          "age": 29,
          "cases": [
            {
              "diagnosis": [
                {
                  "diagnosis": "Eczema",
                  "prognosis": "Condition can be managed with topical treatment and lifestyle adjustments. Recurrence possible with triggers.",
                  "medical-report": "Patient presents with itchy, red patches on forearm and neck. No infection signs. Family history of allergies noted.",
                  "medical-treatment": "Topical corticosteroid cream twice daily, avoid allergens and harsh soaps.",
                  "schedule": "2025-06-08T14:20:00Z",
                  "complaint": "Persistent itching, redness, skin dryness."
                }
              ]
            }
          ]
        }
      ]
    }
  ],
  "patients": [
    {
      "email": "mazen@gmail.com",
      "name": "Mazen Ahmed",
      "age": 23,
      "phone": "+201205621566",
      "password": "SaadSaadSaad@@777",
      "country": "Egypt",
      "drCodes": ["EGP12Hop676"]
    },
    {
      "email": "omar.ali@gmail.com",
      "name": "Omar Ali",
      "age": 40,
      "phone": "+201005698741",
      "password": "OmarAli123@@",
      "country": "Egypt",
      "drCodes": ["EGP45Med123"]
    },
    {
      "email": "sara.mohamed@gmail.com",
      "name": "Sara Mohamed",
      "age": 29,
      "phone": "+201114785236",
      "password": "SaraDerma2025@@",
      "country": "Egypt",
      "drCodes": ["EGP78Derm999"]
    }
  ],
  "patient-doctor": [
    {
      "doctor-code": "EGP12Hop676",
      "patient-phone": "+201205621566"
    },
    {
      "doctor-code": "EGP45Med123",
      "patient-phone": "+201005698741"
    },
    {
      "doctor-code": "EGP78Derm999",
      "patient-phone": "+201114785236"
    }
  ]
}


def load_data():
    """Load data from in-memory storage"""
    return _in_memory_data.copy()

def save_data(data):
    """Save data to in-memory storage"""
    global _in_memory_data
    _in_memory_data = data.copy()

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Medical Reminder API is running"}

@app.get("/status")
async def get_status():
    """Get current data status"""
    data = load_data()
    return {
        "message": "Data status",
        "doctors_count": len(data.get("doctors", [])),
        "patients_count": len(data.get("patients", [])),
        "relationships_count": len(data.get("patient-doctor", [])),
        "data_source": "In-memory (no database configured)"
    }

# Doctor endpoints
@app.get("/doctors", response_model=List[Doctor])
async def get_doctors():
    """Get all doctors"""
    data = load_data()
    return data["doctors"]

@app.get("/doctors/{doctor_code}", response_model=Doctor)
async def get_doctor(doctor_code: str):
    """Get a specific doctor by code"""
    data = load_data()
    doctor = next((d for d in data["doctors"] if d["code"] == doctor_code), None)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@app.post("/doctors", response_model=Doctor, status_code=status.HTTP_201_CREATED)
async def create_doctor(doctor: CreateDoctor):
    """Create a new doctor"""
    data = load_data()
    
    # Check if doctor code already exists
    if any(d["code"] == doctor.code for d in data["doctors"]):
        raise HTTPException(status_code=400, detail="Doctor code already exists")
    
    # Check if email already exists
    if any(d["email"] == doctor.email for d in data["doctors"]):
        raise HTTPException(status_code=400, detail="Doctor email already exists")
    
    # Create new doctor with empty patient list
    new_doctor = doctor.dict()
    new_doctor["patient"] = []
    
    data["doctors"].append(new_doctor)
    save_data(data)
    return new_doctor

@app.put("/doctors/{doctor_code}", response_model=Doctor)
async def update_doctor(doctor_code: str, doctor_update: UpdateDoctor):
    """Update a doctor"""
    data = load_data()
    
    doctor_index = next((i for i, d in enumerate(data["doctors"]) if d["code"] == doctor_code), None)
    if doctor_index is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # Update only provided fields
    doctor_dict = doctor_update.dict(exclude_unset=True)
    data["doctors"][doctor_index].update(doctor_dict)
    
    save_data(data)
    return data["doctors"][doctor_index]

# Note: More specific routes should come before general ones to avoid routing conflicts
# This endpoint is moved after the more specific doctor-patient endpoints

# Patient endpoints
@app.get("/patients", response_model=List[Patient])
async def get_patients():
    """Get all patients"""
    data = load_data()
    return data["patients"]

@app.get("/doctor")
async def check_doctor(email: str, password: str):
    """Check if a doctor exists with the given email and password"""
    data = load_data()
    doctor = next((d for d in data["doctors"] if d["email"] == email), None)
    if not doctor:
        return {"exists": False}
    if doctor["password"] != password:
        return {"exists": False}
    return {"exists": True}

@app.get("/patient")
async def check_patient(email: str, password: str):
    """Check if a patient exists with the given email and password"""
    data = load_data()
    patient = next((p for p in data["patients"] if p["email"] == email), None)
    if not patient:
        return {"exists": False}
    if patient["password"] == password:
        return {"exists": True}
    return {"exists": False}

@app.get("/patients/{patient_email}", response_model=Patient)
async def get_patient(patient_email: str):
    """Get a specific patient by email"""
    data = load_data()
    patient = next((p for p in data["patients"] if p["email"] == patient_email), None)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.post("/patients", response_model=Patient, status_code=status.HTTP_201_CREATED)
async def create_patient(patient: CreatePatient):
    """Create a new patient"""
    data = load_data()
    
    # Check if patient email already exists
    if any(p["email"] == patient.email for p in data["patients"]):
        raise HTTPException(status_code=400, detail="Patient email already exists")
    
    new_patient = patient.dict()
    data["patients"].append(new_patient)
    save_data(data)
    return new_patient

@app.put("/patients/{patient_email}", response_model=Patient)
async def update_patient(patient_email: str, patient_update: UpdatePatient):
    """Update a patient"""
    data = load_data()
    
    patient_index = next((i for i, p in enumerate(data["patients"]) if p["email"] == patient_email), None)
    if patient_index is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Update only provided fields
    patient_dict = patient_update.dict(exclude_unset=True)
    data["patients"][patient_index].update(patient_dict)
    
    save_data(data)
    return data["patients"][patient_index]

@app.delete("/patients/{patient_email}")
async def delete_patient(patient_email: str):
    """Delete a patient"""
    data = load_data()
    
    patient_index = next((i for i, p in enumerate(data["patients"]) if p["email"] == patient_email), None)
    if patient_index is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Remove patient
    deleted_patient = data["patients"].pop(patient_index)
    
    # Remove related patient-doctor relationships
    # Note: We need to find the patient by phone in patient-doctor relationships
    patient_phone = None
    # Find patient phone from doctor's patient list
    for doctor in data["doctors"]:
        for patient_info in doctor["patient"]:
            if patient_info["name"] == deleted_patient["name"]:
                patient_phone = patient_info["phone"]
                break
        if patient_phone:
            break
    
    if patient_phone:
        data["patient-doctor"] = [pd for pd in data["patient-doctor"] if pd["patient-phone"] != patient_phone]
    
    # Remove patient from doctor's patient lists
    for doctor in data["doctors"]:
        doctor["patient"] = [p for p in doctor["patient"] if p["name"] != deleted_patient["name"]]
    
    save_data(data)
    return {"message": "Patient deleted successfully", "deleted_patient": deleted_patient}

# Patient endpoints using phone number as identifier
@app.get("/patients/phone/{patient_phone}", response_model=Patient)
async def get_patient_by_phone(patient_phone: str):
    """Get a specific patient by phone number"""
    data = load_data()
    patient = next((p for p in data["patients"] if p["phone"] == patient_phone), None)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.post("/patients/phone/{patient_phone}", response_model=Patient, status_code=status.HTTP_201_CREATED)
async def create_patient_by_phone(patient_phone: str, patient: CreatePatient):
    """Create a new patient with specified phone number"""
    data = load_data()
    
    # Check if patient phone already exists
    if any(p["phone"] == patient_phone for p in data["patients"]):
        raise HTTPException(status_code=400, detail="Patient phone already exists")
    
    # Check if patient email already exists
    if any(p["email"] == patient.email for p in data["patients"]):
        raise HTTPException(status_code=400, detail="Patient email already exists")
    
    new_patient = patient.dict()
    new_patient["phone"] = patient_phone  # Override phone with the path parameter
    data["patients"].append(new_patient)
    save_data(data)
    return new_patient

@app.put("/patients/phone/{patient_phone}", response_model=Patient)
async def update_patient_by_phone(patient_phone: str, patient_update: UpdatePatient):
    """Update a patient by phone number"""
    data = load_data()
    
    patient_index = next((i for i, p in enumerate(data["patients"]) if p["phone"] == patient_phone), None)
    if patient_index is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Update only provided fields
    patient_dict = patient_update.dict(exclude_unset=True)
    data["patients"][patient_index].update(patient_dict)
    
    save_data(data)
    return data["patients"][patient_index]

@app.delete("/patients/phone/{patient_phone}")
async def delete_patient_by_phone(patient_phone: str):
    """Delete a patient by phone number"""
    data = load_data()
    
    patient_index = next((i for i, p in enumerate(data["patients"]) if p["phone"] == patient_phone), None)
    if patient_index is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Remove patient
    deleted_patient = data["patients"].pop(patient_index)
    
    # Remove related patient-doctor relationships
    data["patient-doctor"] = [pd for pd in data["patient-doctor"] if pd["patient-phone"] != patient_phone]
    
    # Remove patient from doctor's patient lists
    for doctor in data["doctors"]:
        doctor["patient"] = [p for p in doctor["patient"] if p["phone"] != patient_phone]
    
    save_data(data)
    return {"message": "Patient deleted successfully", "deleted_patient": deleted_patient}

# Patient-Doctor relationship endpoints
@app.get("/patient-doctor", response_model=List[PatientDoctor])
async def get_patient_doctor_relationships():
    """Get all patient-doctor relationships"""
    data = load_data()
    return data["patient-doctor"]

@app.post("/patient-doctor", response_model=PatientDoctor, status_code=status.HTTP_201_CREATED)
async def create_patient_doctor_relationship(relationship: PatientDoctor):
    """Create a patient-doctor relationship"""
    data = load_data()
    
    # Check if doctor exists
    doctor = next((d for d in data["doctors"] if d["code"] == relationship.doctor_code), None)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # Check if relationship already exists
    if any(pd["doctor-code"] == relationship.doctor_code and pd["patient-phone"] == relationship.patient_phone 
           for pd in data["patient-doctor"]):
        raise HTTPException(status_code=400, detail="Relationship already exists")
    
    new_relationship = relationship.dict()
    new_relationship["doctor-code"] = relationship.doctor_code
    new_relationship["patient-phone"] = relationship.patient_phone
    
    data["patient-doctor"].append(new_relationship)
    save_data(data)
    return new_relationship

@app.delete("/patient-doctor/{doctor_code}/{patient_phone}")
async def delete_patient_doctor_relationship(doctor_code: str, patient_phone: str):
    """Delete a patient-doctor relationship"""
    data = load_data()
    
    relationship_index = next((i for i, pd in enumerate(data["patient-doctor"]) 
                              if pd["doctor-code"] == doctor_code and pd["patient-phone"] == patient_phone), None)
    if relationship_index is None:
        raise HTTPException(status_code=404, detail="Relationship not found")
    
    deleted_relationship = data["patient-doctor"].pop(relationship_index)
    save_data(data)
    return {"message": "Relationship deleted successfully", "deleted_relationship": deleted_relationship}

# Additional endpoints for patient management within doctor records
import uuid

@app.post("/doctors/{doctor_code}/patients", status_code=status.HTTP_201_CREATED)
async def add_patient_to_doctor(doctor_code: str, patient_info: PatientInfo):
    """Add a patient to a doctor's patient list"""
    data = load_data()

    doctor_index = next((i for i, d in enumerate(data["doctors"]) if d["code"] == doctor_code), None)
    if doctor_index is None:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Generate a unique id for the new patient
    generated_id = str(uuid.uuid4())

    # Check if patient already exists in doctor's list by phone (since id is now generated)
    if any(p["phone"] == patient_info.phone for p in data["doctors"][doctor_index]["patient"]):
        raise HTTPException(status_code=400, detail="Patient already exists in doctor's list")

    new_patient_info = patient_info.dict()
    new_patient_info["id"] = generated_id
    data["doctors"][doctor_index]["patient"].append(new_patient_info)
    save_data(data)
    return {"message": "Patient added to doctor successfully", "patient": new_patient_info}

@app.get("/doctors/{doctor_code}/patients", response_model=List[PatientInfo])
async def get_doctor_patients(doctor_code: str):
    """Get all patients for a specific doctor"""
    data = load_data()
    
    doctor = next((d for d in data["doctors"] if d["code"] == doctor_code), None)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    return doctor["patient"]

# Individual patient management within doctor records
@app.get("/doctors/{doctor_code}/patients/{patient_phone}")
async def get_doctor_patient(doctor_code: str, patient_phone: str):
    """Get a specific patient from a doctor's patient list"""
    data = load_data()
    
    doctor = next((d for d in data["doctors"] if d["code"] == doctor_code), None)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    patient = next((p for p in doctor["patient"] if p["phone"] == patient_phone), None)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found in doctor's list")
    
    return patient

@app.put("/doctors/{doctor_code}/patients/{patient_phone}")
async def update_doctor_patient(doctor_code: str, patient_phone: str, patient_update: UpdatePatientInfo):
    """Update a specific patient in a doctor's patient list"""
    data = load_data()
    
    doctor_index = next((i for i, d in enumerate(data["doctors"]) if d["code"] == doctor_code), None)
    if doctor_index is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    patient_index = next((i for i, p in enumerate(data["doctors"][doctor_index]["patient"]) 
                         if p["phone"] == patient_phone), None)
    if patient_index is None:
        raise HTTPException(status_code=404, detail="Patient not found in doctor's list")
    
    # Update only provided fields
    patient_dict = patient_update.dict(exclude_unset=True)
    data["doctors"][doctor_index]["patient"][patient_index].update(patient_dict)
    
    save_data(data)
    return {"message": "Patient updated successfully", "patient": data["doctors"][doctor_index]["patient"][patient_index]}

@app.delete("/doctors/{doctor_code}/patients/{patient_phone}")
async def delete_doctor_patient(doctor_code: str, patient_phone: str):
    """Delete a specific patient from a doctor's patient list"""
    data = load_data()
    
    doctor_index = next((i for i, d in enumerate(data["doctors"]) if d["code"] == doctor_code), None)
    if doctor_index is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    patient_index = next((i for i, p in enumerate(data["doctors"][doctor_index]["patient"]) 
                         if p["phone"] == patient_phone), None)
    if patient_index is None:
        raise HTTPException(status_code=404, detail="Patient not found in doctor's list")
    
    deleted_patient = data["doctors"][doctor_index]["patient"].pop(patient_index)
    
    data["patient-doctor"] = [pd for pd in data["patient-doctor"] 
                             if not (pd["doctor-code"] == doctor_code and pd["patient-phone"] == patient_phone)]
    
    save_data(data)
    return {"message": "Patient removed from doctor successfully", "deleted_patient": deleted_patient}

# Diagnosis management for specific patients
@app.get("/doctors/{doctor_code}/patients/{patient_phone}/diagnosis")
async def get_patient_diagnosis(doctor_code: str, patient_phone: str):
    """Get all diagnoses for a specific patient"""
    data = load_data()
    
    doctor = next((d for d in data["doctors"] if d["code"] == doctor_code), None)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    patient = next((p for p in doctor["patient"] if p["phone"] == patient_phone), None)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found in doctor's list")
    
    # Return all diagnoses from all cases
    all_diagnoses = []
    for case in patient["cases"]:
        all_diagnoses.extend(case["diagnosis"])
    
    return {"patient_name": patient["name"], "diagnoses": all_diagnoses}

@app.post("/doctors/{doctor_code}/patients/{patient_phone}/diagnosis", status_code=status.HTTP_201_CREATED)
async def add_patient_diagnosis(doctor_code: str, patient_phone: str, diagnosis: Diagnosis):
    """Add a new diagnosis to a specific patient"""
    data = load_data()
    
    doctor_index = next((i for i, d in enumerate(data["doctors"]) if d["code"] == doctor_code), None)
    if doctor_index is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    patient_index = next((i for i, p in enumerate(data["doctors"][doctor_index]["patient"]) 
                         if p["phone"] == patient_phone), None)
    if patient_index is None:
        raise HTTPException(status_code=404, detail="Patient not found in doctor's list")
    
    # Add diagnosis to the first case (or create a new case if none exists)
    patient = data["doctors"][doctor_index]["patient"][patient_index]
    
    if not patient["cases"]:
        # Create a new case if patient has no cases
        patient["cases"] = [{"diagnosis": []}]
    
    # Add diagnosis to the first case
    new_diagnosis = diagnosis.dict()
    patient["cases"][0]["diagnosis"].append(new_diagnosis)
    
    save_data(data)
    return {"message": "Diagnosis added successfully", "diagnosis": new_diagnosis}

@app.delete("/doctors/{doctor_code}/patients/{patient_phone}/diagnosis")
async def delete_patient_diagnosis(doctor_code: str, patient_phone: str, diagnosis_name: str):
    """Delete a specific diagnosis from a patient"""
    data = load_data()
    
    doctor_index = next((i for i, d in enumerate(data["doctors"]) if d["code"] == doctor_code), None)
    if doctor_index is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    patient_index = next((i for i, p in enumerate(data["doctors"][doctor_index]["patient"]) 
                         if p["phone"] == patient_phone), None)
    if patient_index is None:
        raise HTTPException(status_code=404, detail="Patient not found in doctor's list")
    
    patient = data["doctors"][doctor_index]["patient"][patient_index]
    deleted_diagnosis = None
    
    for case in patient["cases"]:
        for i, diagnosis in enumerate(case["diagnosis"]):
            if diagnosis["diagnosis"] == diagnosis_name:
                deleted_diagnosis = case["diagnosis"].pop(i)
                break
        if deleted_diagnosis:
            break
    
    if not deleted_diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    
    save_data(data)
    return {"message": "Diagnosis deleted successfully", "deleted_diagnosis": deleted_diagnosis}

# Patient Doctor Codes Management Endpoints
@app.get("/patients/{phone}/drCodes")
async def get_patient_doctor_codes(phone: str):
    """Get all doctor codes for a specific patient"""
    data = load_data()
    
    patient = next((p for p in data["patients"] if p["phone"] == phone), None)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return {"phone": phone, "drCodes": patient.get("drCodes", [])}

@app.post("/patients/{phone}/drCodes", status_code=status.HTTP_201_CREATED)
async def add_doctor_code_to_patient(phone: str, doctor_code: str):
    """Add a doctor code to a patient's drCodes list"""
    data = load_data()
    
    patient_index = next((i for i, p in enumerate(data["patients"]) if p["phone"] == phone), None)
    if patient_index is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Check if doctor exists
    doctor = next((d for d in data["doctors"] if d["code"] == doctor_code), None)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # Initialize drCodes list if it doesn't exist
    if "drCodes" not in data["patients"][patient_index]:
        data["patients"][patient_index]["drCodes"] = []
    
    # Check if doctor code already exists
    if doctor_code in data["patients"][patient_index]["drCodes"]:
        raise HTTPException(status_code=400, detail="Doctor code already exists for this patient")
    
    # Add doctor code
    data["patients"][patient_index]["drCodes"].append(doctor_code)
    
    # Also create patient-doctor relationship
    new_relationship = {
        "doctor-code": doctor_code,
        "patient-phone": phone
    }
    
    # Check if relationship already exists
    if not any(pd["doctor-code"] == doctor_code and pd["patient-phone"] == phone 
               for pd in data["patient-doctor"]):
        data["patient-doctor"].append(new_relationship)
    
    save_data(data)
    return {"message": "Doctor code added successfully", "phone": phone, "drCodes": data["patients"][patient_index]["drCodes"]}

@app.put("/patients/{phone}/drCodes")
async def update_patient_doctor_codes(phone: str, dr_codes: List[str]):
    """Replace all doctor codes for a patient"""
    data = load_data()
    
    patient_index = next((i for i, p in enumerate(data["patients"]) if p["phone"] == phone), None)
    if patient_index is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Validate that all doctor codes exist
    for doctor_code in dr_codes:
        doctor = next((d for d in data["doctors"] if d["code"] == doctor_code), None)
        if not doctor:
            raise HTTPException(status_code=404, detail=f"Doctor with code {doctor_code} not found")
    
    # Update drCodes
    data["patients"][patient_index]["drCodes"] = dr_codes
    
    # Update patient-doctor relationships
    # Remove existing relationships for this patient
    data["patient-doctor"] = [pd for pd in data["patient-doctor"] if pd["patient-phone"] != phone]
    
    # Add new relationships
    for doctor_code in dr_codes:
        new_relationship = {
            "doctor-code": doctor_code,
            "patient-phone": phone
        }
        data["patient-doctor"].append(new_relationship)
    
    save_data(data)
    return {"message": "Doctor codes updated successfully", "phone": phone, "drCodes": dr_codes}

@app.delete("/patients/{phone}/drCodes")
async def delete_all_patient_doctor_codes(phone: str):
    """Delete all doctor codes for a patient"""
    data = load_data()
    
    patient_index = next((i for i, p in enumerate(data["patients"]) if p["phone"] == phone), None)
    if patient_index is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Get current drCodes before deletion
    current_dr_codes = data["patients"][patient_index].get("drCodes", [])
    
    # Remove all drCodes
    data["patients"][patient_index]["drCodes"] = []
    
    # Remove all patient-doctor relationships for this patient
    data["patient-doctor"] = [pd for pd in data["patient-doctor"] if pd["patient-phone"] != phone]
    
    save_data(data)
    return {"message": "All doctor codes deleted successfully", "phone": phone, "deleted_drCodes": current_dr_codes}

@app.delete("/patients/{phone}/drCodes/{doctor_code}")
async def delete_specific_patient_doctor_code(phone: str, doctor_code: str):
    """Delete a specific doctor code from a patient"""
    data = load_data()
    
    patient_index = next((i for i, p in enumerate(data["patients"]) if p["phone"] == phone), None)
    if patient_index is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Check if drCodes exists and contains the doctor code
    if "drCodes" not in data["patients"][patient_index] or doctor_code not in data["patients"][patient_index]["drCodes"]:
        raise HTTPException(status_code=404, detail="Doctor code not found for this patient")
    
    # Remove the specific doctor code
    data["patients"][patient_index]["drCodes"].remove(doctor_code)
    
    # Remove the specific patient-doctor relationship
    data["patient-doctor"] = [pd for pd in data["patient-doctor"] 
                             if not (pd["doctor-code"] == doctor_code and pd["patient-phone"] == phone)]
    
    save_data(data)
    return {"message": "Doctor code deleted successfully", "phone": phone, "drCodes": data["patients"][patient_index]["drCodes"]}

# General doctor deletion endpoint (moved to end to avoid routing conflicts)
@app.delete("/doctors/{doctor_code}")
async def delete_doctor(doctor_code: str):
    """Delete a doctor"""
    data = load_data()
    
    doctor_index = next((i for i, d in enumerate(data["doctors"]) if d["code"] == doctor_code), None)
    if doctor_index is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # Remove doctor
    deleted_doctor = data["doctors"].pop(doctor_index)
    
    # Remove related patient-doctor relationships
    data["patient-doctor"] = [pd for pd in data["patient-doctor"] if pd["doctor-code"] != doctor_code]
    
    save_data(data)
    return {"message": "Doctor deleted successfully", "deleted_doctor": deleted_doctor}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
