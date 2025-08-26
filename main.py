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
    allow_origins=[
        "http://localhost:3000", 
        "https://localhost:3000", 
        "http://127.0.0.1:3000", 
        "https://127.0.0.1:3000",
        "http://localhost:3001", 
        "https://localhost:3001", 
        "http://127.0.0.1:3001", 
        "https://127.0.0.1:3001",
        "http://localhost:5173",
        "https://localhost:5173",
        "http://127.0.0.1:5173",
        "https://127.0.0.1:5173",
        "https://fast-api-dnk5.vercel.app",
        "https://*.vercel.app",
        "http://192.168.1.5:3000",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Handle OPTIONS requests for CORS preflight
@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    return {"message": "OK"}

# In-memory data storage (for Vercel serverless environment)
# Note: This data will be reset on each deployment
_in_memory_data = {
  "doctors": [
    {
      "code": "EGP12Hop676",
      "name": "AbdElRahman Saad",
      "Age": 24,
      "phone": "+201119944899",
      "profession": "Physician",
      "specialty": "Orthopedics",
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
            },
			  {
  "diagnosis": [
    {
      "diagnosis": "Hypertension (High Blood Pressure)",
      "prognosis": "With consistent medication use, low-sodium diet, and stress management, blood pressure can remain under control and reduce the risk of cardiovascular complications.",
      "medical-report": "Patient shows elevated blood pressure readings over multiple visits (average 150/95 mmHg). No signs of hypertensive retinopathy. Kidney function tests within normal limits.",
      "medical-treatment": "Amlodipine 5mg once daily, reduction of salt intake, weight management, and monthly blood pressure monitoring.",
      "schedule": "2025-08-26T09:00:00Z",
      "complaint": "Persistent headaches, occasional dizziness, and blurred vision."
    }
  ]
}
          ]
        },
  {
    "id": "141517",
    "name": "Layla Hassan",
    "dateOfAdmission": "2025-08-19T14:15:00Z",
    "phone": "+201155478932",
    "country": "Egypt",
    "gender": "female",
    "profession": "ux designer",
    "age": 28,
      "cases": [
		   {
  "diagnosis": [
    {
      "diagnosis": "Hypertension (High Blood Pressure)",
      "prognosis": "With consistent medication use, low-sodium diet, and stress management, blood pressure can remain under control and reduce the risk of cardiovascular complications.",
      "medical-report": "Patient shows elevated blood pressure readings over multiple visits (average 150/95 mmHg). No signs of hypertensive retinopathy. Kidney function tests within normal limits.",
      "medical-treatment": "Amlodipine 5mg once daily, reduction of salt intake, weight management, and monthly blood pressure monitoring.",
      "schedule": "2025-08-26T12:15:00Z",
      "complaint": "Persistent headaches, occasional dizziness, and blurred vision."
    }
  ]
}
	  ]
  },
  {
    "id": "141518",
    "name": "Omar Khalid",
    "dateOfAdmission": "2025-08-18T09:45:00Z",
    "phone": "+201098765432",
    "country": "Egypt",
    "gender": "male",
    "profession": "backend",
    "age": 32,
      "cases": [
		  {
  "diagnosis": [
    {
      "diagnosis": "Asthma (Chronic Respiratory Condition)",
      "prognosis": "With proper inhaler use, allergen avoidance, and routine follow-ups, the patient can maintain good lung function and minimize asthma attacks.",
      "medical-report": "Patient reports shortness of breath and wheezing episodes, especially at night. Pulmonary function test (FEV1) indicates mild obstruction. Chest X-ray is clear. No evidence of infection.",
      "medical-treatment": "Salbutamol inhaler as needed, Fluticasone inhaler twice daily, avoidance of dust and smoke, annual flu vaccination.",
      "schedule": "2025-08-26T14:15:00Z",
      "complaint": "Shortness of breath, chest tightness, and wheezing during exertion and at night."
    }
  ]
}
	  ]
  },
  {
    "id": "141519",
    "name": "Nour ElDin",
    "dateOfAdmission": "2025-08-17T16:20:00Z",
    "phone": "+201212345678",
    "country": "Egypt",
    "gender": "male",
    "profession": "fullstack",
    "age": 26,
      "cases": [
		  {
  "diagnosis": [
    {
      "diagnosis": "Iron Deficiency Anemia",
      "prognosis": "With proper iron supplementation, dietary changes, and monitoring, hemoglobin levels are expected to return to normal within 3–6 months.",
      "medical-report": "Patient presents with low hemoglobin (10.2 g/dL), low ferritin levels, and pale conjunctiva. No signs of active bleeding. Stool occult blood test negative.",
      "medical-treatment": "Oral ferrous sulfate 325mg once daily, vitamin C supplementation to improve absorption, dietary advice to include iron-rich foods, follow-up blood tests every 3 months.",
      "schedule": "2025-08-26T11:45:00Z",
      "complaint": "Fatigue, weakness, pale skin, and shortness of breath on exertion."
    }
  ]
}
	  ]
  },
  {
    "id": "141520",
    "name": "Yasmin Saleh",
    "dateOfAdmission": "2025-08-16T11:10:00Z",
    "phone": "+201287654321",
    "country": "Egypt",
    "gender": "female",
    "profession": "frontend",
    "age": 24,
      "cases": [
		  {
  "diagnosis": [
    {
      "diagnosis": "Gastritis",
      "prognosis": "With medication adherence, dietary changes, and stress management, symptoms are expected to improve significantly within weeks, reducing the risk of ulcers.",
      "medical-report": "Patient reports epigastric pain and nausea. Endoscopy reveals mild gastric mucosal inflammation. H. pylori test is negative. No evidence of bleeding.",
      "medical-treatment": "Omeprazole 20mg once daily for 6 weeks, avoidance of spicy and acidic foods, reduction of caffeine and alcohol intake, stress management techniques.",
      "schedule": "2025-08-26T16:00:00Z",
      "complaint": "Burning stomach pain after meals, bloating, nausea, and occasional loss of appetite."
    }
  ]
}
	  ]
  },
  {
    "id": "141521",
    "name": "Ahmed Mahmoud",
    "dateOfAdmission": "2025-08-15T13:25:00Z",
    "phone": "+201376543219",
    "country": "Egypt",
    "gender": "male",
    "profession": "devops",
    "age": 30,
      "cases": [
		  {
  "diagnosis": [
    {
      "diagnosis": "Migraine Headache",
      "prognosis": "With preventive therapy, lifestyle modifications, and trigger avoidance, migraine frequency and intensity can be significantly reduced.",
      "medical-report": "Patient experiences recurrent unilateral throbbing headaches accompanied by nausea and photophobia. Neurological exam is normal. MRI brain shows no abnormalities.",
      "medical-treatment": "Sumatriptan 50mg as needed during attacks, prophylactic propranolol 40mg twice daily, avoidance of known triggers such as caffeine and irregular sleep, regular hydration.",
      "schedule": "2025-08-26T13:30:00Z",
      "complaint": "Severe headache episodes with nausea, sensitivity to light, and occasional vomiting."
    }
  ]
}
	  ]
  },
  {
    "id": "141522",
    "name": "Fatima Zahra",
    "dateOfAdmission": "2025-08-14T15:40:00Z",
    "phone": "+201465432187",
    "country": "Egypt",
    "gender": "female",
    "profession": "data scientist",
    "age": 27,
      "cases": [
		  {
  "diagnosis": [
    {
      "diagnosis": "Stable Angina Pectoris",
      "prognosis": "With consistent medication, risk factor control, and regular cardiology follow-ups, the patient can maintain good quality of life and reduce the risk of heart attack.",
      "medical-report": "Patient reports chest discomfort on exertion, relieved by rest. ECG shows ST-segment depression during stress test. Lipid profile indicates elevated LDL cholesterol.",
      "medical-treatment": "Aspirin 75mg once daily, Atorvastatin 20mg once daily, Nitroglycerin sublingual as needed for chest pain, advice on regular exercise and low-fat diet.",
      "schedule": "2025-08-26T15:00:00Z",
      "complaint": "Chest pain during physical activity, shortness of breath on exertion, and occasional fatigue."
    }
  ]
}
	  ]
  },
  {
    "id": "141523",
    "name": "Karim Abdul",
    "dateOfAdmission": "2025-08-13T08:55:00Z",
    "phone": "+201554321876",
    "country": "Egypt",
    "gender": "male",
    "profession": "backend",
    "age": 29,
      "cases": [
		  {
  "diagnosis": [
    {
      "diagnosis": "Osteoarthritis of the Knee",
      "prognosis": "With regular physiotherapy, weight management, and pain control, the patient can maintain mobility and delay disease progression.",
      "medical-report": "Patient complains of chronic knee pain, stiffness in the morning, and reduced range of motion. X-ray shows joint space narrowing and mild osteophyte formation.",
      "medical-treatment": "Paracetamol 1g as needed, physiotherapy sessions twice weekly, weight reduction program, use of supportive knee brace, follow-up every 6 months.",
      "schedule": "2025-08-26T10:15:00Z",
      "complaint": "Knee pain worsening with activity, stiffness after rest, and occasional swelling."
    }
  ]
}
	  ]
  },
  {
    "id": "141524",
    "name": "Sara Mohamed",
    "dateOfAdmission": "2025-08-12T12:30:00Z",
    "phone": "+201643218765",
    "country": "Egypt",
    "gender": "female",
    "profession": "frontend",
    "age": 25,
      "cases": [
		  {
  "diagnosis": [
    {
      "diagnosis": "Eczema (Atopic Dermatitis)",
      "prognosis": "With regular skin care, trigger avoidance, and prescribed medication, flare-ups can be minimized and the patient can maintain good skin health.",
      "medical-report": "Patient presents with itchy, dry, and inflamed patches on the forearms and behind the knees. No signs of infection. Family history of allergic conditions noted.",
      "medical-treatment": "Topical corticosteroid cream twice daily for 2 weeks, emollient moisturizers applied frequently, antihistamine at night for itching, follow-up in 1 month.",
      "schedule": "2025-08-26T12:30:00Z",
      "complaint": "Intense itching, redness, and dry skin patches worsening at night."
    }
  ]
}
	  ]
  },
  {
    "id": "141525",
    "name": "Tariq Nasser",
    "dateOfAdmission": "2025-08-11T17:05:00Z",
    "phone": "+201732187654",
    "country": "Egypt",
    "gender": "male",
    "profession": "mobile developer",
    "age": 31,
      "cases": [
		  {
  "diagnosis": [
    {
      "diagnosis": "Chronic Kidney Disease (Stage 2)",
      "prognosis": "With controlled blood pressure, dietary modifications, and regular nephrology follow-ups, kidney function can be preserved and progression slowed.",
      "medical-report": "Patient shows an eGFR of 75 mL/min/1.73m² with mild proteinuria. Blood pressure slightly elevated (145/90 mmHg). Electrolytes within normal limits. No evidence of edema.",
      "medical-treatment": "Lisinopril 10mg once daily, low-salt and low-protein diet, regular monitoring of kidney function every 3 months, lifestyle modifications for blood pressure control.",
      "schedule": "2025-08-26T17:00:00Z",
      "complaint": "Occasional fatigue, mild swelling around ankles, and increased nighttime urination."
    }
  ]
}
	  ]
  },
  {
    "id": "141526",
    "name": "Rana Ali",
    "dateOfAdmission": "2025-08-10T10:50:00Z",
    "phone": "+201821876543",
    "country": "Egypt",
    "gender": "female",
    "profession": "ux designer",
    "age": 26,
      "cases": []
  },
  {
    "id": "141527",
    "name": "Hassan Ibrahim",
    "dateOfAdmission": "2025-08-09T14:15:00Z",
    "phone": "+201910987654",
    "country": "Egypt",
    "gender": "male",
    "profession": "backend",
    "age": 33,
      "cases": []
  },
  {
    "id": "141528",
    "name": "Dalia Samir",
    "dateOfAdmission": "2025-08-08T09:20:00Z",
    "phone": "+202012345678",
    "country": "Egypt",
    "gender": "female",
    "profession": "frontend",
    "age": 24,
      "cases": [
		  {
  "diagnosis": [
    {
      "diagnosis": "Chronic Kidney Disease (Stage 2)",
      "prognosis": "With controlled blood pressure, dietary modifications, and regular nephrology follow-ups, kidney function can be preserved and progression slowed.",
      "medical-report": "Patient shows an eGFR of 75 mL/min/1.73m² with mild proteinuria. Blood pressure slightly elevated (145/90 mmHg). Electrolytes within normal limits. No evidence of edema.",
      "medical-treatment": "Lisinopril 10mg once daily, low-salt and low-protein diet, regular monitoring of kidney function every 3 months, lifestyle modifications for blood pressure control.",
      "schedule": "2025-08-28T17:00:00Z",
      "complaint": "Occasional fatigue, mild swelling around ankles, and increased nighttime urination."
    }
  ]
}
	  ]
  },
  {
    "id": "141529",
    "name": "Amir Farouk",
    "dateOfAdmission": "2025-08-07T16:45:00Z",
    "phone": "+202098765432",
    "country": "Egypt",
    "gender": "male",
    "profession": "fullstack",
    "age": 28,
      "cases": [
		  {
  "diagnosis": [
    {
      "diagnosis": "Chronic Kidney Disease (Stage 2)",
      "prognosis": "With controlled blood pressure, dietary modifications, and regular nephrology follow-ups, kidney function can be preserved and progression slowed.",
      "medical-report": "Patient shows an eGFR of 75 mL/min/1.73m² with mild proteinuria. Blood pressure slightly elevated (145/90 mmHg). Electrolytes within normal limits. No evidence of edema.",
      "medical-treatment": "Lisinopril 10mg once daily, low-salt and low-protein diet, regular monitoring of kidney function every 3 months, lifestyle modifications for blood pressure control.",
      "schedule": "2025-08-29T17:00:00Z",
      "complaint": "Occasional fatigue, mild swelling around ankles, and increased nighttime urination."
    }
  ]
}
	  ]
  },
  {
    "id": "141530",
    "name": "Lina Ashraf",
    "dateOfAdmission": "2025-08-06T11:30:00Z",
    "phone": "+202112345678",
    "country": "Egypt",
    "gender": "female",
    "profession": "data analyst",
    "age": 26,
      "cases": [
		  {
  "diagnosis": [
    {
      "diagnosis": "Chronic Kidney Disease (Stage 2)",
      "prognosis": "With controlled blood pressure, dietary modifications, and regular nephrology follow-ups, kidney function can be preserved and progression slowed.",
      "medical-report": "Patient shows an eGFR of 75 mL/min/1.73m² with mild proteinuria. Blood pressure slightly elevated (145/90 mmHg). Electrolytes within normal limits. No evidence of edema.",
      "medical-treatment": "Lisinopril 10mg once daily, low-salt and low-protein diet, regular monitoring of kidney function every 3 months, lifestyle modifications for blood pressure control.",
      "schedule": "2025-08-30T17:00:00Z",
      "complaint": "Occasional fatigue, mild swelling around ankles, and increased nighttime urination."
    }
  ]
}
	  ]
  },
  {
    "id": "141531",
    "name": "Youssef Hamdi",
    "dateOfAdmission": "2025-08-05T13:50:00Z",
    "phone": "+202223456789",
    "country": "Egypt",
    "gender": "male",
    "profession": "devops",
    "age": 32,
      "cases": [
		  {
  "diagnosis": [
    {
      "diagnosis": "Chronic Kidney Disease (Stage 2)",
      "prognosis": "With controlled blood pressure, dietary modifications, and regular nephrology follow-ups, kidney function can be preserved and progression slowed.",
      "medical-report": "Patient shows an eGFR of 75 mL/min/1.73m² with mild proteinuria. Blood pressure slightly elevated (145/90 mmHg). Electrolytes within normal limits. No evidence of edema.",
      "medical-treatment": "Lisinopril 10mg once daily, low-salt and low-protein diet, regular monitoring of kidney function every 3 months, lifestyle modifications for blood pressure control.",
      "schedule": "2025-08-12T17:00:00Z",
      "complaint": "Occasional fatigue, mild swelling around ankles, and increased nighttime urination."
    }
  ]
}
	  ]
  },
  {
    "id": "141532",
    "name": "Mona Tarek",
    "dateOfAdmission": "2025-08-04T15:15:00Z",
    "phone": "+202334567890",
    "country": "Egypt",
    "gender": "female",
    "profession": "frontend",
    "age": 23,
      "cases": [
		  {
  "diagnosis": [
    {
      "diagnosis": "Chronic Kidney Disease (Stage 2)",
      "prognosis": "With controlled blood pressure, dietary modifications, and regular nephrology follow-ups, kidney function can be preserved and progression slowed.",
      "medical-report": "Patient shows an eGFR of 75 mL/min/1.73m² with mild proteinuria. Blood pressure slightly elevated (145/90 mmHg). Electrolytes within normal limits. No evidence of edema.",
      "medical-treatment": "Lisinopril 10mg once daily, low-salt and low-protein diet, regular monitoring of kidney function every 3 months, lifestyle modifications for blood pressure control.",
      "schedule": "2025-08-18T17:00:00Z",
      "complaint": "Occasional fatigue, mild swelling around ankles, and increased nighttime urination."
    }
  ]
}
	  ]
  },
  {
    "id": "141533",
    "name": "Khaled Samy",
    "dateOfAdmission": "2025-08-03T08:40:00Z",
    "phone": "+202445678901",
    "country": "Egypt",
    "gender": "male",
    "profession": "backend",
    "age": 29,
      "cases": [
		  {
  "diagnosis": [
    {
      "diagnosis": "Chronic Kidney Disease (Stage 2)",
      "prognosis": "With controlled blood pressure, dietary modifications, and regular nephrology follow-ups, kidney function can be preserved and progression slowed.",
      "medical-report": "Patient shows an eGFR of 75 mL/min/1.73m² with mild proteinuria. Blood pressure slightly elevated (145/90 mmHg). Electrolytes within normal limits. No evidence of edema.",
      "medical-treatment": "Lisinopril 10mg once daily, low-salt and low-protein diet, regular monitoring of kidney function every 3 months, lifestyle modifications for blood pressure control.",
      "schedule": "2025-08-08T17:00:00Z",
      "complaint": "Occasional fatigue, mild swelling around ankles, and increased nighttime urination."
    }
  ]
}
	  ]
  },
  {
    "id": "141534",
    "name": "Jana Wael",
    "dateOfAdmission": "2025-08-02T12:05:00Z",
    "phone": "+202556789012",
    "country": "Egypt",
    "gender": "female",
    "profession": "ux designer",
    "age": 27,
      "cases": []
  },
  {
    "id": "141535",
    "name": "Ziad Rashad",
    "dateOfAdmission": "2025-08-01T16:30:00Z",
    "phone": "+202667890123",
    "country": "Egypt",
    "gender": "male",
    "profession": "fullstack",
    "age": 30,
      "cases": []
  },
  {
    "id": "141536",
    "name": "Hana Essam",
    "dateOfAdmission": "2025-07-31T10:55:00Z",
    "phone": "+202778901234",
    "country": "Egypt",
    "gender": "female",
    "profession": "frontend",
    "age": 25,
      "cases": []
  },
  {
    "id": "141537",
    "name": "Samir Fathi",
    "dateOfAdmission": "2025-07-30T14:20:00Z",
    "phone": "+202889012345",
    "country": "Egypt",
    "gender": "male",
    "profession": "mobile developer",
    "age": 31,
      "cases": []
  },
  {
    "id": "141538",
    "name": "Nada Hisham",
    "dateOfAdmission": "2025-07-29T09:45:00Z",
    "phone": "+202990123456",
    "country": "Egypt",
    "gender": "female",
    "profession": "data scientist",
    "age": 28,
      "cases": []
  },
  {
    "id": "141539",
    "name": "Fadi Gamal",
    "dateOfAdmission": "2025-07-28T17:10:00Z",
    "phone": "+203001234567",
    "country": "Egypt",
    "gender": "male",
    "profession": "backend",
    "age": 33,
      "cases": []
  },
  {
    "id": "141540",
    "name": "Rania Osman",
    "dateOfAdmission": "2025-07-27T11:35:00Z",
    "phone": "+203112345678",
    "country": "Egypt",
    "gender": "female",
    "profession": "frontend",
    "age": 24,
      "cases": []
  },
  {
    "id": "141541",
    "name": "Bassem Adel",
    "dateOfAdmission": "2025-07-26T13:00:00Z",
    "phone": "+203223456789",
    "country": "Egypt",
    "gender": "male",
    "profession": "devops",
    "age": 32,
      "cases": []
  },
  {
    "id": "141542",
    "name": "Salma Karim",
    "dateOfAdmission": "2025-07-25T15:25:00Z",
    "phone": "+203334567890",
    "country": "Egypt",
    "gender": "female",
    "profession": "ux designer",
    "age": 26,
      "cases": []
  },
  {
    "id": "141543",
    "name": "Waleed Magdy",
    "dateOfAdmission": "2025-07-24T08:50:00Z",
    "phone": "+203445678901",
    "country": "Egypt",
    "gender": "male",
    "profession": "fullstack",
    "age": 29,
      "cases": []
  },
  {
    "id": "141544",
    "name": "Aya Sobhy",
    "dateOfAdmission": "2025-07-23T12:15:00Z",
    "phone": "+203556789012",
    "country": "Egypt",
    "gender": "female",
    "profession": "frontend",
    "age": 23,
      "cases": []
  },
  {
    "id": "141545",
    "name": "Kareem Tawfik",
    "dateOfAdmission": "2025-07-22T16:40:00Z",
    "phone": "+203667890123",
    "country": "Egypt",
    "gender": "male",
    "profession": "backend",
    "age": 30,
      "cases": []
  },
  {
    "id": "141546",
    "name": "Farida Nabil",
    "dateOfAdmission": "2025-07-21T10:05:00Z",
    "phone": "+203778901234",
    "country": "Egypt",
    "gender": "female",
    "profession": "data analyst",
    "age": 27,
      "cases": []
  },
  {
    "id": "141547",
    "name": "Hisham Raafat",
    "dateOfAdmission": "2025-07-20T14:30:00Z",
    "phone": "+203889012345",
    "country": "Egypt",
    "gender": "male",
    "profession": "mobile developer",
    "age": 31,
      "cases": []
  },
  {
    "id": "141548",
    "name": "Soha Ayman",
    "dateOfAdmission": "2025-07-19T09:55:00Z",
    "phone": "+203990123456",
    "country": "Egypt",
    "gender": "female",
    "profession": "frontend",
    "age": 25,
      "cases": []
  },
  {
    "id": "141549",
    "name": "Nader Lotfy",
    "dateOfAdmission": "2025-07-18T17:20:00Z",
    "phone": "+204001234567",
    "country": "Egypt",
    "gender": "male",
    "profession": "backend",
    "age": 33,
      "cases": []
  },
  {
    "id": "141550",
    "name": "Mai Hesham",
    "dateOfAdmission": "2025-07-17T11:45:00Z",
    "phone": "+204112345678",
    "country": "Egypt",
    "gender": "female",
    "profession": "ux designer",
    "age": 26,
      "cases": []
  },
  {
    "id": "141551",
    "name": "Adel Sabry",
    "dateOfAdmission": "2025-07-16T13:10:00Z",
    "phone": "+204223456789",
    "country": "Egypt",
    "gender": "male",
    "profession": "fullstack",
    "age": 28,
      "cases": []
  },
  {
    "id": "141552",
    "name": "Reem Ashraf",
    "dateOfAdmission": "2025-07-15T15:35:00Z",
    "phone": "+204334567890",
    "country": "Egypt",
    "gender": "female",
    "profession": "frontend",
    "age": 24,
      "cases": []
  },
  {
    "id": "141553",
    "name": "Tamer Naguib",
    "dateOfAdmission": "2025-07-14T08:00:00Z",
    "phone": "+204445678901",
    "country": "Egypt",
    "gender": "male",
    "profession": "devops",
    "age": 32,
      "cases": []
  },
  {
    "id": "141554",
    "name": "Dina Sherif",
    "dateOfAdmission": "2025-07-13T12:25:00Z",
    "phone": "+204556789012",
    "country": "Egypt",
    "gender": "female",
    "profession": "data scientist",
    "age": 29,
      "cases": []
  },
  {
    "id": "141555",
    "name": "Sherif Galal",
    "dateOfAdmission": "2025-07-12T16:50:00Z",
    "phone": "+204667890123",
    "country": "Egypt",
    "gender": "male",
    "profession": "backend",
    "age": 30,
      "cases": []
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
    },
            {
            "code": "EGP31Hop402",
            "name": "Lisa Smith",
            "Age": 52,
            "phone": "(009)735-4731",
            "profession": "Doctor",
            "specialty": "Cardiology",
            "gender": "female",
            "email": "norma25@george-zimmerman.biz",
            "password": "Q4%06GAy%J",
            "country": "Colombia",
            "city": "South Christinemouth",
            "patient": [
                {
                    "id": "220700",
                    "name": "Angela Collins",
                    "dateOfAdmission": "2000-04-27T01:27:01",
                    "phone": "001-855-391-3058",
                    "country": "Martinique",
                    "gender": "male",
                    "profession": "Occupational hygienist",
                    "age": 20,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "1979-09-29T06:35:49",
                                    "complaint": "Cough, fever, and chest discomfort."
                                },
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "2022-12-19T01:41:23",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP19Hop748",
            "name": "Andrea Peterson",
            "Age": 49,
            "phone": "+1-365-100-2689x21509",
            "profession": "Doctor",
            "specialty": "Cardiology",
            "gender": "male",
            "email": "obrown@hamilton-curtis.com",
            "password": "&i9Vo7@Ts+",
            "country": "Uzbekistan",
            "city": "Port Amymouth",
            "patient": [
                {
                    "id": "149441",
                    "name": "Eric Williams",
                    "dateOfAdmission": "1990-06-29T10:39:21",
                    "phone": "+1-575-304-6120",
                    "country": "Korea",
                    "gender": "male",
                    "profession": "Operations geologist",
                    "age": 29,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "1992-12-22T04:11:37",
                                    "complaint": "Headaches and dizziness."
                                },
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "1970-04-22T13:11:56",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                }
                            ]
                        }
                    ]
                },
                {
					"id": "141d3211156516",
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
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Condition can be well-controlled with consistent treatment and lifestyle adjustments, reducing long-term cardiovascular risk.",
                                    "medical-report": "Blood pressure readings averaged 150/95 mmHg over the past month. No hypertensive retinopathy. ECG shows no acute changes.",
                                    "medical-treatment": "Amlodipine 5mg once daily, reduced salt intake, weight management, and monthly monitoring.",
                                    "schedule": "2025-08-25T11:00:00Z",
                                    "complaint": "Occasional headaches and dizziness."
                                },
                                {
                                    "diagnosis": "Hyperlipidemia",
                                    "prognosis": "With appropriate treatment, cholesterol levels can be normalized, lowering risk of cardiovascular disease.",
                                    "medical-report": "LDL cholesterol: 165 mg/dL, HDL: 38 mg/dL, Triglycerides: 200 mg/dL. No history of myocardial infarction.",
                                    "medical-treatment": "Atorvastatin 20mg daily, low-fat diet, regular physical activity.",
                                    "schedule": "2025-09-01T09:45:00Z",
                                    "complaint": "No specific symptoms, detected during routine check-up."
                                }
							]
						}
					]
				}
            ]
        },
        {
            "code": "EGP96Hop267",
            "name": "Amy Young",
            "Age": 42,
            "phone": "745-133-1377",
            "profession": "Doctor",
            "specialty": "Pediatrics",
            "gender": "female",
            "email": "robert40@russell.net",
            "password": "s_E*Z8nmDE",
            "country": "Lesotho",
            "city": "Lloydtown",
            "patient": [
                {
                    "id": "687228",
                    "name": "Jeremy Mitchell",
                    "dateOfAdmission": "1977-06-24T03:44:35",
                    "phone": "001-851-200-8252x904",
                    "country": "Niger",
                    "gender": "female",
                    "profession": "Town planner",
                    "age": 27,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "1982-10-04T03:15:52",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                },
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "2017-11-14T11:05:58",
                                    "complaint": "Headaches and dizziness."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP99Hop495",
            "name": "Jenny Glass",
            "Age": 36,
            "phone": "+1-006-741-9535",
            "profession": "Doctor",
            "specialty": "Data Science",
            "gender": "male",
            "email": "blakerobert@james.biz",
            "password": "AG1FduQQ3^",
            "country": "San Marino",
            "city": "New Lauren",
            "patient": [
                {
                    "id": "88240466542",
                    "name": "Fernando Baker",
                    "dateOfAdmission": "1981-02-25T14:53:40",
                    "phone": "997.722.7589",
                    "country": "Saudi Arabia",
                    "gender": "male",
                    "profession": "Operations geologist",
                    "age": 44,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "1983-04-18T21:11:13",
                                    "complaint": "Headaches and dizziness."
                                },
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "1993-05-11T12:19:48",
                                    "complaint": "Cough, fever, and chest discomfort."
                                }
                            ]
                        }
                    ]
                },
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
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting in most cases and expected to improve within 1–3 weeks with treatment and rest. Low risk of complications if managed appropriately.",
                                    "medical-report": "Patient presents with persistent cough for the past 10 days, mild fever (37.8°C), and chest congestion. No signs of pneumonia on chest X-ray. Oxygen saturation at 98%.",
                                    "medical-treatment": "Prescribed Amoxicillin 500mg three times daily for 7 days, increased fluid intake, and rest.",
                                    "schedule": "2025-08-22T09:15:00Z",
                                    "complaint": "Persistent cough, mild fever, and difficulty breathing during physical activity."
                                },
                                {
                                    "diagnosis": "Seasonal Allergic Rhinitis",
                                    "prognosis": "Symptoms are expected to improve with treatment and allergen avoidance, though recurrence during pollen seasons is likely.",
                                    "medical-report": "Patient experiences nasal congestion, sneezing, and itchy eyes during spring. Allergy test positive for pollen sensitivity.",
                                    "medical-treatment": "Antihistamines once daily, nasal corticosteroid spray, and avoidance of allergen exposure.",
                                    "schedule": "2025-08-28T08:30:00Z",
                                    "complaint": "Sneezing, runny nose, and itchy eyes."
                                },
                                {
                                    "diagnosis": "Iron Deficiency Anemia",
                                    "prognosis": "Condition improves significantly with iron supplementation and dietary adjustments within a few months.",
                                    "medical-report": "Hemoglobin: 9.5 g/dL, MCV: 72 fL. Ferritin levels low. No signs of bleeding on stool test.",
                                    "medical-treatment": "Ferrous sulfate 325mg daily, iron-rich diet, recheck hemoglobin in 6 weeks.",
                                    "schedule": "2025-09-05T14:00:00Z",
                                    "complaint": "Fatigue, pale skin, and shortness of breath on exertion."
                                },
                                {
                                    "diagnosis": "Gastroesophageal Reflux Disease (GERD)",
                                    "prognosis": "Condition is manageable with lifestyle changes and medication, preventing progression to complications like Barrett’s esophagus.",
                                    "medical-report": "Patient reports heartburn 3–4 times per week. Endoscopy shows mild esophagitis, no ulcers.",
                                    "medical-treatment": "Omeprazole 20mg daily, avoid spicy foods, elevate head during sleep.",
                                    "schedule": "2025-09-10T10:00:00Z",
                                    "complaint": "Burning sensation in chest, especially after meals."
                                }
							]
						}
					]
				}
            ]
        },
        {
            "code": "EGP59Hop513",
            "name": "Sarah Velez",
            "Age": 52,
            "phone": "(301)235-5015x13994",
            "profession": "Doctor",
            "specialty": "Neurology",
            "gender": "male",
            "email": "carlosmorris@yahoo.com",
            "password": "NllrXffu+8",
            "country": "Dominica",
            "city": "Port David",
            "patient": [
                {
                    "id": "772819",
                    "name": "Rhonda Watts",
                    "dateOfAdmission": "1987-05-08T12:59:32",
                    "phone": "952.512.0541x469",
                    "country": "Turkmenistan",
                    "gender": "male",
                    "profession": "Systems developer",
                    "age": 69,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "1991-01-27T16:37:37",
                                    "complaint": "Headaches and dizziness."
                                },
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "2002-02-28T08:02:25",
                                    "complaint": "Cough, fever, and chest discomfort."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP52Hop393",
            "name": "Elizabeth Roberts",
            "Age": 58,
            "phone": "001-954-204-2619",
            "profession": "Doctor",
            "specialty": "Data Science",
            "gender": "female",
            "email": "tonya86@yahoo.com",
            "password": "dR3JBFl9_(",
            "country": "Haiti",
            "city": "Lewismouth",
            "patient": [
                {
                    "id": "8482132172",
                    "name": "Colleen Carter",
                    "dateOfAdmission": "2017-05-14T10:54:45",
                    "phone": "(415)588-6259",
                    "country": "Myanmar",
                    "gender": "male",
                    "profession": "Banker",
                    "age": 50,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "1995-11-28T21:13:15",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                },
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "2024-07-13T18:57:27",
                                    "complaint": "Cough, fever, and chest discomfort."
                                }
                            ]
                        }
                    ]
                },
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
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting in most cases and expected to improve within 1–3 weeks with treatment and rest. Low risk of complications if managed appropriately.",
                                    "medical-report": "Patient presents with persistent cough for the past 10 days, mild fever (37.8°C), and chest congestion. No signs of pneumonia on chest X-ray. Oxygen saturation at 98%.",
                                    "medical-treatment": "Prescribed Amoxicillin 500mg three times daily for 7 days, increased fluid intake, and rest.",
                                    "schedule": "2025-08-22T09:15:00Z",
                                    "complaint": "Persistent cough, mild fever, and difficulty breathing during physical activity."
                                },
                                {
                                    "diagnosis": "Seasonal Allergic Rhinitis",
                                    "prognosis": "Symptoms are expected to improve with treatment and allergen avoidance, though recurrence during pollen seasons is likely.",
                                    "medical-report": "Patient experiences nasal congestion, sneezing, and itchy eyes during spring. Allergy test positive for pollen sensitivity.",
                                    "medical-treatment": "Antihistamines once daily, nasal corticosteroid spray, and avoidance of allergen exposure.",
                                    "schedule": "2025-08-28T08:30:00Z",
                                    "complaint": "Sneezing, runny nose, and itchy eyes."
                                },
                                {
                                    "diagnosis": "Iron Deficiency Anemia",
                                    "prognosis": "Condition improves significantly with iron supplementation and dietary adjustments within a few months.",
                                    "medical-report": "Hemoglobin: 9.5 g/dL, MCV: 72 fL. Ferritin levels low. No signs of bleeding on stool test.",
                                    "medical-treatment": "Ferrous sulfate 325mg daily, iron-rich diet, recheck hemoglobin in 6 weeks.",
                                    "schedule": "2025-09-05T14:00:00Z",
                                    "complaint": "Fatigue, pale skin, and shortness of breath on exertion."
                                },
                                {
                                    "diagnosis": "Gastroesophageal Reflux Disease (GERD)",
                                    "prognosis": "Condition is manageable with lifestyle changes and medication, preventing progression to complications like Barrett’s esophagus.",
                                    "medical-report": "Patient reports heartburn 3–4 times per week. Endoscopy shows mild esophagitis, no ulcers.",
                                    "medical-treatment": "Omeprazole 20mg daily, avoid spicy foods, elevate head during sleep.",
                                    "schedule": "2025-09-10T10:00:00Z",
                                    "complaint": "Burning sensation in chest, especially after meals."
                                }
							]
						}
					]
				}
            ]
        },
        {
            "code": "EGP21Hop955",
            "name": "Jodi Hernandez",
            "Age": 42,
            "phone": "7758416688",
            "profession": "Doctor",
            "specialty": "Data Science",
            "gender": "male",
            "email": "dpittman@hotmail.com",
            "password": "&R20hSayle",
            "country": "Cyprus",
            "city": "West Matthewland",
            "patient": [
                {
                    "id": "537140",
                    "name": "Tony Ramirez",
                    "dateOfAdmission": "1975-11-23T20:14:12",
                    "phone": "001-586-275-3487x8664",
                    "country": "Malaysia",
                    "gender": "male",
                    "profession": "Holiday representative",
                    "age": 42,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "2001-09-23T10:11:22",
                                    "complaint": "Cough, fever, and chest discomfort."
                                },
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "1999-10-18T07:14:13",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP41Hop268",
            "name": "Brian Thompson",
            "Age": 46,
            "phone": "929.544.6801",
            "profession": "Doctor",
            "specialty": "Data Science",
            "gender": "female",
            "email": "patriciataylor@johnson.com",
            "password": "%4#AU&Dd1C",
            "country": "United States of America",
            "city": "East John",
            "patient": [
                {
                    "id": "769560",
                    "name": "Kelly Ford",
                    "dateOfAdmission": "2007-07-30T10:03:56",
                    "phone": "904.625.6542x632",
                    "country": "United States of America",
                    "gender": "male",
                    "profession": "Radiographer, therapeutic",
                    "age": 57,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "2024-06-21T20:09:50",
                                    "complaint": "Cough, fever, and chest discomfort."
                                },
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "1975-05-25T23:30:16",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP58Hop163",
            "name": "Daniel Dudley",
            "Age": 54,
            "phone": "+1-120-390-9852x6897",
            "profession": "Doctor",
            "specialty": "Data Science",
            "gender": "male",
            "email": "ericmcgee@yahoo.com",
            "password": "ZcM6)QtM@N",
            "country": "Serbia",
            "city": "Pamelaland",
            "patient": [
                {
                    "id": "768672",
                    "name": "Nathaniel Hunt",
                    "dateOfAdmission": "2017-09-26T05:20:30",
                    "phone": "258-014-2249",
                    "country": "Burundi",
                    "gender": "female",
                    "profession": "Chief Technology Officer",
                    "age": 22,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "1970-12-08T22:28:42",
                                    "complaint": "Headaches and dizziness."
                                },
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "1991-12-14T12:26:52",
                                    "complaint": "Cough, fever, and chest discomfort."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP15Hop905",
            "name": "Kelly Powell",
            "Age": 48,
            "phone": "869.125.1356x7579",
            "profession": "Doctor",
            "specialty": "Orthopedics",
            "gender": "male",
            "email": "nicholas53@hotmail.com",
            "password": "*dJepUj*&3",
            "country": "Falkland Islands (Malvinas)",
            "city": "New Aliciaton",
            "patient": [
                {
                    "id": "962605",
                    "name": "Felicia Bailey",
                    "dateOfAdmission": "1996-06-30T16:48:06",
                    "phone": "(665)028-5186x471",
                    "country": "Cayman Islands",
                    "gender": "male",
                    "profession": "Administrator, education",
                    "age": 69,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "2024-01-06T17:41:15",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                },
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "2018-12-12T08:57:00",
                                    "complaint": "Headaches and dizziness."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP27Hop282",
            "name": "Megan Williams",
            "Age": 31,
            "phone": "502.989.1851x068",
            "profession": "Doctor",
            "specialty": "Data Science",
            "gender": "male",
            "email": "lydia22@richards.biz",
            "password": "5iZTmG6t_T",
            "country": "Cambodia",
            "city": "Port Micheleburgh",
            "patient": [
                {
                    "id": "327519",
                    "name": "Stacey Roberts",
                    "dateOfAdmission": "1988-06-15T23:58:46",
                    "phone": "(311)710-0723x949",
                    "country": "Chad",
                    "gender": "male",
                    "profession": "Ceramics designer",
                    "age": 65,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "2016-02-09T16:31:58",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                },
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "1996-05-03T05:42:06",
                                    "complaint": "Headaches and dizziness."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP36Hop831",
            "name": "Ashlee Matthews",
            "Age": 33,
            "phone": "0599469441",
            "profession": "Doctor",
            "specialty": "Orthopedics",
            "gender": "male",
            "email": "heather16@yahoo.com",
            "password": "@2_f69Rp0i",
            "country": "South Georgia and the South Sandwich Islands",
            "city": "Hayesberg",
            "patient": [
                {
                    "id": "974696",
                    "name": "Nicole Melton",
                    "dateOfAdmission": "1989-10-17T22:58:08",
                    "phone": "468.771.9649",
                    "country": "Mali",
                    "gender": "female",
                    "profession": "Professor Emeritus",
                    "age": 36,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "1977-06-08T23:28:29",
                                    "complaint": "Cough, fever, and chest discomfort."
                                },
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "1974-12-16T15:43:42",
                                    "complaint": "Headaches and dizziness."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP73Hop965",
            "name": "Julian Davies",
            "Age": 38,
            "phone": "578-317-1269x53936",
            "profession": "Doctor",
            "specialty": "Neurology",
            "gender": "male",
            "email": "cindy05@gmail.com",
            "password": "P4qzHN(k#c",
            "country": "Holy See (Vatican City State)",
            "city": "Jamiefort",
            "patient": [
                {
                    "id": "991908",
                    "name": "Matthew Morris",
                    "dateOfAdmission": "2000-02-02T19:01:31",
                    "phone": "(192)087-6317x5948",
                    "country": "Kiribati",
                    "gender": "male",
                    "profession": "Interior and spatial designer",
                    "age": 58,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "2003-12-09T04:56:47",
                                    "complaint": "Cough, fever, and chest discomfort."
                                },
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "2010-10-29T20:16:40",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP26Hop257",
            "name": "John Barton",
            "Age": 49,
            "phone": "990-222-9090",
            "profession": "Doctor",
            "specialty": "Orthopedics",
            "gender": "female",
            "email": "andrewvelasquez@hotmail.com",
            "password": "8*48N6veg)",
            "country": "Saint Kitts and Nevis",
            "city": "East Alexis",
            "patient": [
                {
                    "id": "238817",
                    "name": "David Chang",
                    "dateOfAdmission": "2019-12-21T20:45:27",
                    "phone": "895.667.7718x75828",
                    "country": "Czech Republic",
                    "gender": "male",
                    "profession": "Aid worker",
                    "age": 34,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "2000-05-07T21:23:51",
                                    "complaint": "Cough, fever, and chest discomfort."
                                },
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "1986-11-29T14:11:27",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP21Hop668",
            "name": "Anthony Conrad",
            "Age": 39,
            "phone": "(249)972-5762",
            "profession": "Doctor",
            "specialty": "Orthopedics",
            "gender": "male",
            "email": "iwhite@hotmail.com",
            "password": "w_jG4G8x_Q",
            "country": "Luxembourg",
            "city": "Port Aaronfort",
            "patient": [
                {
                    "id": "247360",
                    "name": "Adam Henderson",
                    "dateOfAdmission": "2025-02-13T06:56:42",
                    "phone": "001-182-174-2989x49387",
                    "country": "United Kingdom",
                    "gender": "female",
                    "profession": "Presenter, broadcasting",
                    "age": 64,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "1981-10-02T23:51:08",
                                    "complaint": "Cough, fever, and chest discomfort."
                                },
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "1972-04-30T08:53:23",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP61Hop420",
            "name": "Amber Baker",
            "Age": 60,
            "phone": "751-811-1647x3318",
            "profession": "Doctor",
            "specialty": "Pediatrics",
            "gender": "female",
            "email": "kimberlysanchez@little.com",
            "password": "Go2QKYTc(h",
            "country": "Jordan",
            "city": "West Markfort",
            "patient": [
                {
                    "id": "352493",
                    "name": "Frank Fuller",
                    "dateOfAdmission": "2024-05-17T17:31:21",
                    "phone": "016.104.6068",
                    "country": "Gambia",
                    "gender": "female",
                    "profession": "Corporate treasurer",
                    "age": 25,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "2011-12-24T11:00:48",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                },
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "2010-01-04T13:55:04",
                                    "complaint": "Cough, fever, and chest discomfort."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP41Hop696",
            "name": "Tara Wilson",
            "Age": 48,
            "phone": "+1-668-839-2860",
            "profession": "Doctor",
            "specialty": "Neurology",
            "gender": "male",
            "email": "martinezangel@hotmail.com",
            "password": "#8X%GxNHt0",
            "country": "San Marino",
            "city": "Lake Diane",
            "patient": [
                {
                    "id": "842166",
                    "name": "Paul Potter",
                    "dateOfAdmission": "2019-10-07T19:29:01",
                    "phone": "+1-953-123-0275",
                    "country": "Togo",
                    "gender": "male",
                    "profession": "Risk manager",
                    "age": 38,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "1991-08-11T18:49:08",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                },
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "2002-10-22T00:08:54",
                                    "complaint": "Headaches and dizziness."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP18Hop751",
            "name": "Holly Weiss",
            "Age": 54,
            "phone": "001-990-454-6393x363",
            "profession": "Doctor",
            "specialty": "Cardiology",
            "gender": "male",
            "email": "michaelmendoza@hanna-mccoy.com",
            "password": "PhuVZw%I*9",
            "country": "Uruguay",
            "city": "East Jasmine",
            "patient": [
                {
                    "id": "102860",
                    "name": "John Davis",
                    "dateOfAdmission": "2023-11-17T13:23:30",
                    "phone": "974.220.4628x524",
                    "country": "Gambia",
                    "gender": "male",
                    "profession": "Seismic interpreter",
                    "age": 55,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "2011-03-19T21:41:19",
                                    "complaint": "Cough, fever, and chest discomfort."
                                },
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "2008-12-01T09:08:07",
                                    "complaint": "Headaches and dizziness."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP54Hop762",
            "name": "Erica Williams",
            "Age": 52,
            "phone": "(288)450-2480x70231",
            "profession": "Doctor",
            "specialty": "Neurology",
            "gender": "female",
            "email": "william69@hotmail.com",
            "password": "l8PUSDGg$H",
            "country": "Norway",
            "city": "New Jonathan",
            "patient": [
                {
                    "id": "398370",
                    "name": "Mr. Kevin Wilson DDS",
                    "dateOfAdmission": "2024-06-25T09:58:52",
                    "phone": "392-854-3373x69627",
                    "country": "Wallis and Futuna",
                    "gender": "female",
                    "profession": "Catering manager",
                    "age": 22,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "2001-10-08T22:19:36",
                                    "complaint": "Cough, fever, and chest discomfort."
                                },
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "2012-08-20T03:00:52",
                                    "complaint": "Headaches and dizziness."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP34Hop148",
            "name": "Justin Bradford",
            "Age": 35,
            "phone": "064-686-8005",
            "profession": "Doctor",
            "specialty": "Neurology",
            "gender": "male",
            "email": "thomasmichael@yahoo.com",
            "password": "^0$OJUiXpn",
            "country": "Kenya",
            "city": "Copelandmouth",
            "patient": [
                {
                    "id": "611401",
                    "name": "Michael Parker",
                    "dateOfAdmission": "2009-03-16T04:33:40",
                    "phone": "(765)146-9652x9310",
                    "country": "Djibouti",
                    "gender": "male",
                    "profession": "Solicitor",
                    "age": 34,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "2007-02-26T22:45:56",
                                    "complaint": "Headaches and dizziness."
                                },
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "1974-07-16T02:50:01",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP99Hop303",
            "name": "Michael Murphy",
            "Age": 45,
            "phone": "(605)762-9953x9421",
            "profession": "Doctor",
            "specialty": "Neurology",
            "gender": "female",
            "email": "schmittyolanda@gmail.com",
            "password": "+(3Eo*NcIQ",
            "country": "Aruba",
            "city": "Howellstad",
            "patient": [
                {
                    "id": "601517",
                    "name": "Sharon Mora",
                    "dateOfAdmission": "2014-05-25T02:34:47",
                    "phone": "885-250-4097x562",
                    "country": "Montserrat",
                    "gender": "male",
                    "profession": "Learning mentor",
                    "age": 24,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "2017-04-19T23:36:17",
                                    "complaint": "Cough, fever, and chest discomfort."
                                },
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "1972-10-09T06:13:10",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP91Hop885",
            "name": "Meghan Zavala",
            "Age": 32,
            "phone": "057.464.3392x029",
            "profession": "Doctor",
            "specialty": "Orthopedics",
            "gender": "male",
            "email": "vjohnson@long-martinez.com",
            "password": "+3@sNZAz40",
            "country": "Turkey",
            "city": "South Joel",
            "patient": [
                {
                    "id": "845289",
                    "name": "Samantha Robinson",
                    "dateOfAdmission": "2022-07-31T14:06:52",
                    "phone": "(512)449-8184x8520",
                    "country": "United States Virgin Islands",
                    "gender": "male",
                    "profession": "Retail manager",
                    "age": 28,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "1971-02-06T03:18:31",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                },
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "2017-12-28T02:56:40",
                                    "complaint": "Headaches and dizziness."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP93Hop340",
            "name": "Randy Knapp",
            "Age": 55,
            "phone": "+1-319-911-7358x2263",
            "profession": "Doctor",
            "specialty": "Neurology",
            "gender": "female",
            "email": "noblebrandon@gmail.com",
            "password": "(cMbMn0Y61",
            "country": "Peru",
            "city": "Jonathanburgh",
            "patient": [
                {
                    "id": "273811",
                    "name": "Steven Serrano",
                    "dateOfAdmission": "1996-12-24T22:41:29",
                    "phone": "4803939487",
                    "country": "Brunei Darussalam",
                    "gender": "female",
                    "profession": "Animator",
                    "age": 68,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "2014-03-05T03:33:21",
                                    "complaint": "Cough, fever, and chest discomfort."
                                },
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "2011-11-12T17:23:37",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP45Hop621",
            "name": "Mark Gomez",
            "Age": 32,
            "phone": "001-499-230-8377x1559",
            "profession": "Doctor",
            "specialty": "Cardiology",
            "gender": "male",
            "email": "silvatravis@rodriguez.com",
            "password": "@54NH1rEgk",
            "country": "Tajikistan",
            "city": "Lake Janice",
            "patient": [
                {
                    "id": "410183",
                    "name": "Matthew Shepard",
                    "dateOfAdmission": "1987-07-18T22:36:44",
                    "phone": "259.785.9651x36698",
                    "country": "Norfolk Island",
                    "gender": "female",
                    "profession": "Food technologist",
                    "age": 66,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "2001-12-24T03:23:23",
                                    "complaint": "Headaches and dizziness."
                                },
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "1989-01-12T21:03:39",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP17Hop369",
            "name": "Nancy Fisher",
            "Age": 55,
            "phone": "(483)154-8131",
            "profession": "Doctor",
            "specialty": "Data Science",
            "gender": "male",
            "email": "jason57@hotmail.com",
            "password": "(yI8Ojnrs^",
            "country": "Tonga",
            "city": "Lake Normanfort",
            "patient": [
                {
                    "id": "490082",
                    "name": "Bridget Davis",
                    "dateOfAdmission": "2018-04-05T16:13:59",
                    "phone": "+1-189-216-7088",
                    "country": "Barbados",
                    "gender": "male",
                    "profession": "Editor, film/video",
                    "age": 70,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "1995-12-11T15:30:54",
                                    "complaint": "Headaches and dizziness."
                                },
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "1971-04-02T21:50:27",
                                    "complaint": "Cough, fever, and chest discomfort."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP85Hop182",
            "name": "Amy Nichols",
            "Age": 49,
            "phone": "(305)140-1620x385",
            "profession": "Doctor",
            "specialty": "Data Science",
            "gender": "female",
            "email": "benjaminmejia@gmail.com",
            "password": "^^0%HsCj3(",
            "country": "Zimbabwe",
            "city": "Pottsmouth",
            "patient": [
                {
                    "id": "944752",
                    "name": "Andrea Young",
                    "dateOfAdmission": "2009-10-17T09:20:43",
                    "phone": "001-281-476-7086x322",
                    "country": "Kenya",
                    "gender": "female",
                    "profession": "Consulting civil engineer",
                    "age": 56,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "2013-03-30T00:50:01",
                                    "complaint": "Cough, fever, and chest discomfort."
                                },
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "1979-02-18T18:48:09",
                                    "complaint": "Headaches and dizziness."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP44Hop184",
            "name": "Regina Davis",
            "Age": 37,
            "phone": "(039)118-7943x6255",
            "profession": "Doctor",
            "specialty": "Data Science",
            "gender": "female",
            "email": "cjohnson@oneal-johnson.com",
            "password": "Hc0KN6nd#t",
            "country": "France",
            "city": "Cynthiahaven",
            "patient": [
                {
                    "id": "266864",
                    "name": "Beth Brown",
                    "dateOfAdmission": "2000-05-18T17:37:00",
                    "phone": "130.462.3369x3463",
                    "country": "Liechtenstein",
                    "gender": "male",
                    "profession": "Research scientist (medical)",
                    "age": 27,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "1995-09-30T13:18:12",
                                    "complaint": "Cough, fever, and chest discomfort."
                                },
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "2010-02-03T02:13:18",
                                    "complaint": "Headaches and dizziness."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP91Hop420",
            "name": "Mrs. Cynthia Marquez DDS",
            "Age": 33,
            "phone": "(037)697-4085",
            "profession": "Doctor",
            "specialty": "Neurology",
            "gender": "male",
            "email": "morrisoncarrie@wagner.com",
            "password": "_E70KN+b7%",
            "country": "Niger",
            "city": "Lake Roberto",
            "patient": [
                {
                    "id": "255068",
                    "name": "Timothy Frost",
                    "dateOfAdmission": "1991-03-10T22:24:55",
                    "phone": "+1-270-846-7257",
                    "country": "Costa Rica",
                    "gender": "male",
                    "profession": "Environmental education officer",
                    "age": 26,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "2005-09-28T04:49:23",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                },
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "2021-11-15T01:28:58",
                                    "complaint": "Headaches and dizziness."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP73Hop529",
            "name": "Maria Ford",
            "Age": 55,
            "phone": "(034)773-9416x0289",
            "profession": "Doctor",
            "specialty": "Pediatrics",
            "gender": "female",
            "email": "cwhite@ross.com",
            "password": "n9tQ#LtJ*f",
            "country": "Singapore",
            "city": "Martinfort",
            "patient": [
                {
                    "id": "111091",
                    "name": "Christopher Ramirez",
                    "dateOfAdmission": "2018-10-25T08:33:57",
                    "phone": "(316)998-0483x4973",
                    "country": "Madagascar",
                    "gender": "male",
                    "profession": "Warden/ranger",
                    "age": 35,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "2024-12-22T09:06:55",
                                    "complaint": "Cough, fever, and chest discomfort."
                                },
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "2013-08-08T02:57:39",
                                    "complaint": "Headaches and dizziness."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP38Hop744",
            "name": "Shirley King",
            "Age": 34,
            "phone": "(054)236-1376",
            "profession": "Doctor",
            "specialty": "Cardiology",
            "gender": "female",
            "email": "darius94@hotmail.com",
            "password": "G^O#7Lwrvz",
            "country": "Tuvalu",
            "city": "Davisview",
            "patient": [
                {
                    "id": "956629",
                    "name": "Kayla Gomez",
                    "dateOfAdmission": "2006-07-03T18:37:56",
                    "phone": "001-342-910-2087x2206",
                    "country": "Anguilla",
                    "gender": "female",
                    "profession": "Radio producer",
                    "age": 57,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "2019-12-12T00:41:29",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                },
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "2019-10-14T07:11:43",
                                    "complaint": "Cough, fever, and chest discomfort."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP91Hop921",
            "name": "James Melton",
            "Age": 32,
            "phone": "119-690-0106",
            "profession": "Doctor",
            "specialty": "Orthopedics",
            "gender": "male",
            "email": "fred55@griffin.net",
            "password": "T5e7A!aq*P",
            "country": "Netherlands",
            "city": "Lake Jamesport",
            "patient": [
                {
                    "id": "671640",
                    "name": "Holly Hogan",
                    "dateOfAdmission": "2018-09-16T14:50:46",
                    "phone": "+1-451-648-0312",
                    "country": "Rwanda",
                    "gender": "male",
                    "profession": "Diagnostic radiographer",
                    "age": 38,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "1994-01-18T01:31:49",
                                    "complaint": "Cough, fever, and chest discomfort."
                                },
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "2010-07-27T18:25:34",
                                    "complaint": "Headaches and dizziness."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP50Hop208",
            "name": "James Taylor",
            "Age": 60,
            "phone": "923-774-9173",
            "profession": "Doctor",
            "specialty": "Data Science",
            "gender": "female",
            "email": "francissalinas@yahoo.com",
            "password": "gCU&1CpJ9O",
            "country": "Indonesia",
            "city": "Lake Jessica",
            "patient": [
                {
                    "id": "614393",
                    "name": "William Lowery",
                    "dateOfAdmission": "1989-09-09T05:37:38",
                    "phone": "+1-678-420-1021x486",
                    "country": "Burkina Faso",
                    "gender": "female",
                    "profession": "English as a second language teacher",
                    "age": 53,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "2015-05-26T01:20:49",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                },
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "2006-11-26T10:56:14",
                                    "complaint": "Cough, fever, and chest discomfort."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP59Hop373",
            "name": "Joseph Blanchard",
            "Age": 48,
            "phone": "902-134-4700",
            "profession": "Doctor",
            "specialty": "Data Science",
            "gender": "male",
            "email": "hjuarez@hotmail.com",
            "password": ")l%R9NrpXf",
            "country": "Armenia",
            "city": "Matthewmouth",
            "patient": [
                {
                    "id": "923900",
                    "name": "Connor Long",
                    "dateOfAdmission": "1990-06-25T10:47:19",
                    "phone": "828.169.7638",
                    "country": "Marshall Islands",
                    "gender": "male",
                    "profession": "Marketing executive",
                    "age": 48,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "1971-10-26T22:40:13",
                                    "complaint": "Cough, fever, and chest discomfort."
                                },
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "2021-12-08T05:11:17",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP36Hop614",
            "name": "Thomas York",
            "Age": 34,
            "phone": "001-300-009-1721x234",
            "profession": "Doctor",
            "specialty": "Pediatrics",
            "gender": "male",
            "email": "douglas22@vance.com",
            "password": "*389yYb#3a",
            "country": "Marshall Islands",
            "city": "Hodgesport",
            "patient": [
                {
                    "id": "963030",
                    "name": "Clarence Gibbs",
                    "dateOfAdmission": "2011-05-01T18:31:23",
                    "phone": "(333)107-8036x84277",
                    "country": "Montenegro",
                    "gender": "female",
                    "profession": "Engineer, building services",
                    "age": 25,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "1974-12-06T01:29:22",
                                    "complaint": "Headaches and dizziness."
                                },
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "1999-10-03T06:52:08",
                                    "complaint": "Cough, fever, and chest discomfort."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP25Hop765",
            "name": "Stephanie Coleman",
            "Age": 47,
            "phone": "135-790-0047x80139",
            "profession": "Doctor",
            "specialty": "Cardiology",
            "gender": "male",
            "email": "valeriemarsh@moss.com",
            "password": "*C8H93Ab4z",
            "country": "Mauritius",
            "city": "Lake Jennifermouth",
            "patient": [
                {
                    "id": "307054",
                    "name": "Molly Ryan",
                    "dateOfAdmission": "2004-01-01T08:53:01",
                    "phone": "001-493-238-8429x874",
                    "country": "French Guiana",
                    "gender": "male",
                    "profession": "Teacher, secondary school",
                    "age": 32,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "1984-09-11T09:11:26",
                                    "complaint": "Headaches and dizziness."
                                },
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "2016-02-02T11:30:40",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP62Hop120",
            "name": "Tommy Rogers",
            "Age": 58,
            "phone": "(310)583-0298x187",
            "profession": "Doctor",
            "specialty": "Pediatrics",
            "gender": "male",
            "email": "georgewilliams@yahoo.com",
            "password": "6^L5XQq%!b",
            "country": "Guinea-Bissau",
            "city": "Port Ian",
            "patient": [
                {
                    "id": "772331",
                    "name": "Alice Mckinney",
                    "dateOfAdmission": "1985-01-14T12:15:36",
                    "phone": "1189471178",
                    "country": "Argentina",
                    "gender": "female",
                    "profession": "Scientist, audiological",
                    "age": 27,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "2024-05-27T02:47:13",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                },
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "1980-02-26T10:17:03",
                                    "complaint": "Cough, fever, and chest discomfort."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP46Hop395",
            "name": "Joseph Ayala",
            "Age": 50,
            "phone": "003-136-4537x75653",
            "profession": "Doctor",
            "specialty": "Orthopedics",
            "gender": "female",
            "email": "evega@yahoo.com",
            "password": "_88TI0k!X8",
            "country": "Bermuda",
            "city": "Kleinville",
            "patient": [
                {
                    "id": "565671",
                    "name": "Nicole Griffith",
                    "dateOfAdmission": "2018-05-04T19:49:13",
                    "phone": "(267)916-7904x64241",
                    "country": "Swaziland",
                    "gender": "female",
                    "profession": "Clinical molecular geneticist",
                    "age": 31,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "1973-07-22T20:54:49",
                                    "complaint": "Headaches and dizziness."
                                },
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "2016-09-08T06:47:58",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP91Hop350",
            "name": "Sharon Ayala",
            "Age": 58,
            "phone": "+1-415-792-0611x577",
            "profession": "Doctor",
            "specialty": "Cardiology",
            "gender": "male",
            "email": "doris37@gmail.com",
            "password": "*w1H3jz!ss",
            "country": "Uzbekistan",
            "city": "Dawsonburgh",
            "patient": [
                {
                    "id": "656830",
                    "name": "Alexis Taylor",
                    "dateOfAdmission": "2000-11-29T18:38:14",
                    "phone": "988.961.0068",
                    "country": "Mongolia",
                    "gender": "male",
                    "profession": "Television floor manager",
                    "age": 58,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "1977-10-04T11:03:36",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                },
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "1989-07-26T23:32:11",
                                    "complaint": "Cough, fever, and chest discomfort."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP55Hop970",
            "name": "Amy Thornton",
            "Age": 41,
            "phone": "632.352.5823x88701",
            "profession": "Doctor",
            "specialty": "Data Science",
            "gender": "female",
            "email": "cburke@gmail.com",
            "password": "f9SzA7uN$C",
            "country": "Mali",
            "city": "Timothyborough",
            "patient": [
                {
                    "id": "772869",
                    "name": "Teresa Hart",
                    "dateOfAdmission": "1971-10-05T10:23:03",
                    "phone": "+1-001-495-2796x783",
                    "country": "Kiribati",
                    "gender": "male",
                    "profession": "Printmaker",
                    "age": 28,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Type 2 Diabetes Mellitus",
                                    "prognosis": "With adherence to medication, lifestyle modifications, and regular follow-ups, the patient can maintain good glycemic control.",
                                    "medical-report": "Elevated fasting blood glucose levels. HbA1c is 7.5%. No signs of complications yet.",
                                    "medical-treatment": "Metformin 500mg twice daily, dietary modifications, regular exercise.",
                                    "schedule": "2020-07-12T07:16:39",
                                    "complaint": "Frequent urination, increased thirst, and fatigue."
                                },
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "2011-01-21T09:21:25",
                                    "complaint": "Headaches and dizziness."
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "code": "EGP21Hop737",
            "name": "Raymond Brooks",
            "Age": 50,
            "phone": "151.994.7508x029",
            "profession": "Doctor",
            "specialty": "Pediatrics",
            "gender": "female",
            "email": "rothemily@gardner.com",
            "password": "x)^a6wIn*%",
            "country": "New Caledonia",
            "city": "Port Hannahstad",
            "patient": [
                {
                    "id": "343014",
                    "name": "Philip Williams",
                    "dateOfAdmission": "1997-07-15T10:50:19",
                    "phone": "507-196-2589x19136",
                    "country": "Ireland",
                    "gender": "female",
                    "profession": "Learning mentor",
                    "age": 48,
                    "cases": [
                        {
                            "diagnosis": [
                                {
                                    "diagnosis": "Acute Bronchitis",
                                    "prognosis": "Condition is self-limiting and expected to improve within 1\u20133 weeks with treatment and rest.",
                                    "medical-report": "Persistent cough, mild fever, and chest congestion. No pneumonia detected.",
                                    "medical-treatment": "Amoxicillin 500mg three times daily for 7 days, fluids, rest.",
                                    "schedule": "1978-08-14T22:59:23",
                                    "complaint": "Cough, fever, and chest discomfort."
                                },
                                {
                                    "diagnosis": "Hypertension",
                                    "prognosis": "Manageable with medications and lifestyle changes, risk of complications if uncontrolled.",
                                    "medical-report": "Blood pressure consistently 150/95 mmHg, no organ damage signs.",
                                    "medical-treatment": "Amlodipine 5mg daily, reduced salt intake, exercise.",
                                    "schedule": "1980-02-02T13:06:11",
                                    "complaint": "Headaches and dizziness."
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
    },
            {
            "email": "craigashley@yahoo.com",
            "name": "Angela Collins",
            "age": 20,
            "phone": "001-855-391-3058",
            "password": "v+Gw3GO$Ax",
            "country": "Martinique",
            "drCodes": [
                "EGP31Hop402"
            ]
        },
        {
            "email": "brian24@washington-marshall.com",
            "name": "Eric Williams",
            "age": 29,
            "phone": "+1-575-304-6120",
            "password": "K&1TWPkvJy",
            "country": "Korea",
            "drCodes": [
                "EGP19Hop748"
            ]
        },
        {
            "email": "yflores@yahoo.com",
            "name": "Jeremy Mitchell",
            "age": 27,
            "phone": "001-851-200-8252x904",
            "password": "f!Le0mE3Vu",
            "country": "Niger",
            "drCodes": [
                "EGP96Hop267"
            ]
        },
        {
            "email": "jflores@hotmail.com",
            "name": "Fernando Baker",
            "age": 44,
            "phone": "997.722.7589",
            "password": "Tmi%3RAjJl",
            "country": "Saudi Arabia",
            "drCodes": [
                "EGP99Hop495"
            ]
        },
        {
            "email": "lauraanthony@gmail.com",
            "name": "Rhonda Watts",
            "age": 69,
            "phone": "952.512.0541x469",
            "password": "e2fETnOR+L",
            "country": "Turkmenistan",
            "drCodes": [
                "EGP59Hop513"
            ]
        },
        {
            "email": "lopezreginald@lamb.org",
            "name": "Colleen Carter",
            "age": 50,
            "phone": "(415)588-6259",
            "password": "%57EdBxkpz",
            "country": "Myanmar",
            "drCodes": [
                "EGP52Hop393"
            ]
        },
        {
            "email": "cookelizabeth@gmail.com",
            "name": "Tony Ramirez",
            "age": 42,
            "phone": "001-586-275-3487x8664",
            "password": "f+1dRpi2f#",
            "country": "Malaysia",
            "drCodes": [
                "EGP21Hop955"
            ]
        },
        {
            "email": "htaylor@ortiz-mullins.com",
            "name": "Kelly Ford",
            "age": 57,
            "phone": "904.625.6542x632",
            "password": "k2_iAr3N)h",
            "country": "United States of America",
            "drCodes": [
                "EGP41Hop268"
            ]
        },
        {
            "email": "cantrellchad@bell-ferguson.biz",
            "name": "Nathaniel Hunt",
            "age": 22,
            "phone": "258-014-2249",
            "password": "#5FZ7zemOS",
            "country": "Burundi",
            "drCodes": [
                "EGP58Hop163"
            ]
        },
        {
            "email": "jessica83@gmail.com",
            "name": "Felicia Bailey",
            "age": 69,
            "phone": "(665)028-5186x471",
            "password": "^0A4EIqv74",
            "country": "Cayman Islands",
            "drCodes": [
                "EGP15Hop905"
            ]
        },
        {
            "email": "bsmith@butler-diaz.net",
            "name": "Stacey Roberts",
            "age": 65,
            "phone": "(311)710-0723x949",
            "password": "RM%VzNp1%4",
            "country": "Chad",
            "drCodes": [
                "EGP27Hop282"
            ]
        },
        {
            "email": "jeremywilkinson@yahoo.com",
            "name": "Nicole Melton",
            "age": 36,
            "phone": "468.771.9649",
            "password": "&4TbzHaI56",
            "country": "Mali",
            "drCodes": [
                "EGP36Hop831"
            ]
        },
        {
            "email": "juliehardy@morris-phillips.com",
            "name": "Matthew Morris",
            "age": 58,
            "phone": "(192)087-6317x5948",
            "password": "!2DDE8a3SA",
            "country": "Kiribati",
            "drCodes": [
                "EGP73Hop965"
            ]
        },
        {
            "email": "vturner@hotmail.com",
            "name": "David Chang",
            "age": 34,
            "phone": "895.667.7718x75828",
            "password": "P&8K+ZRua9",
            "country": "Czech Republic",
            "drCodes": [
                "EGP26Hop257"
            ]
        },
        {
            "email": "thomasanthony@collier-sullivan.com",
            "name": "Adam Henderson",
            "age": 64,
            "phone": "001-182-174-2989x49387",
            "password": "%8QnsCQAT^",
            "country": "United Kingdom",
            "drCodes": [
                "EGP21Hop668"
            ]
        },
        {
            "email": "mvalencia@mcclure.biz",
            "name": "Frank Fuller",
            "age": 25,
            "phone": "016.104.6068",
            "password": "j*yd9KennL",
            "country": "Gambia",
            "drCodes": [
                "EGP61Hop420"
            ]
        },
        {
            "email": "edwinpowers@hotmail.com",
            "name": "Paul Potter",
            "age": 38,
            "phone": "+1-953-123-0275",
            "password": "jdjU7CDSu#",
            "country": "Togo",
            "drCodes": [
                "EGP41Hop696"
            ]
        },
        {
            "email": "asingleton@hotmail.com",
            "name": "John Davis",
            "age": 55,
            "phone": "974.220.4628x524",
            "password": "_MhLi^)A$6",
            "country": "Gambia",
            "drCodes": [
                "EGP18Hop751"
            ]
        },
        {
            "email": "salexander@hotmail.com",
            "name": "Mr. Kevin Wilson DDS",
            "age": 22,
            "phone": "392-854-3373x69627",
            "password": "dQ*t8KDvPl",
            "country": "Wallis and Futuna",
            "drCodes": [
                "EGP54Hop762"
            ]
        },
        {
            "email": "porterwilliam@parker.com",
            "name": "Michael Parker",
            "age": 34,
            "phone": "(765)146-9652x9310",
            "password": "%u50xqJu5+",
            "country": "Djibouti",
            "drCodes": [
                "EGP34Hop148"
            ]
        },
        {
            "email": "mdunn@hotmail.com",
            "name": "Sharon Mora",
            "age": 24,
            "phone": "885-250-4097x562",
            "password": "9M(i6%Xfze",
            "country": "Montserrat",
            "drCodes": [
                "EGP99Hop303"
            ]
        },
        {
            "email": "mmitchell@gmail.com",
            "name": "Samantha Robinson",
            "age": 28,
            "phone": "(512)449-8184x8520",
            "password": "*ZZEs4Ikss",
            "country": "United States Virgin Islands",
            "drCodes": [
                "EGP91Hop885"
            ]
        },
        {
            "email": "nelsonelizabeth@yahoo.com",
            "name": "Steven Serrano",
            "age": 68,
            "phone": "4803939487",
            "password": "$F9NJjdx%3",
            "country": "Brunei Darussalam",
            "drCodes": [
                "EGP93Hop340"
            ]
        },
        {
            "email": "nkoch@goodman.com",
            "name": "Matthew Shepard",
            "age": 66,
            "phone": "259.785.9651x36698",
            "password": "%I2wOCi!7(",
            "country": "Norfolk Island",
            "drCodes": [
                "EGP45Hop621"
            ]
        },
        {
            "email": "hendrixjanice@crawford-yates.org",
            "name": "Bridget Davis",
            "age": 70,
            "phone": "+1-189-216-7088",
            "password": "F8uxKeBH)3",
            "country": "Barbados",
            "drCodes": [
                "EGP17Hop369"
            ]
        },
        {
            "email": "hayessylvia@may-tucker.com",
            "name": "Andrea Young",
            "age": 56,
            "phone": "001-281-476-7086x322",
            "password": "@mTugpyNh1",
            "country": "Kenya",
            "drCodes": [
                "EGP85Hop182"
            ]
        },
        {
            "email": "christie51@gmail.com",
            "name": "Beth Brown",
            "age": 27,
            "phone": "130.462.3369x3463",
            "password": "x@4^juGkNU",
            "country": "Liechtenstein",
            "drCodes": [
                "EGP44Hop184"
            ]
        },
        {
            "email": "markchandler@marquez.net",
            "name": "Timothy Frost",
            "age": 26,
            "phone": "+1-270-846-7257",
            "password": "Nn7GXdXq&m",
            "country": "Costa Rica",
            "drCodes": [
                "EGP91Hop420"
            ]
        },
        {
            "email": "mary82@garcia-hill.com",
            "name": "Christopher Ramirez",
            "age": 35,
            "phone": "(316)998-0483x4973",
            "password": "ZOi7WEEp+0",
            "country": "Madagascar",
            "drCodes": [
                "EGP73Hop529"
            ]
        },
        {
            "email": "pearsonmelody@yahoo.com",
            "name": "Kayla Gomez",
            "age": 57,
            "phone": "001-342-910-2087x2206",
            "password": "#g2@KocXU9",
            "country": "Anguilla",
            "drCodes": [
                "EGP38Hop744"
            ]
        },
        {
            "email": "smithcassandra@gmail.com",
            "name": "Holly Hogan",
            "age": 38,
            "phone": "+1-451-648-0312",
            "password": "hqxWtB@h)3",
            "country": "Rwanda",
            "drCodes": [
                "EGP91Hop921"
            ]
        },
        {
            "email": "carrielewis@richmond-evans.com",
            "name": "William Lowery",
            "age": 53,
            "phone": "+1-678-420-1021x486",
            "password": "!@i3qTqG(I",
            "country": "Burkina Faso",
            "drCodes": [
                "EGP50Hop208"
            ]
        },
        {
            "email": "lisasmith@campbell.org",
            "name": "Connor Long",
            "age": 48,
            "phone": "828.169.7638",
            "password": "gB4M7Sfd!4",
            "country": "Marshall Islands",
            "drCodes": [
                "EGP59Hop373"
            ]
        },
        {
            "email": "mcintoshjoseph@gomez.com",
            "name": "Clarence Gibbs",
            "age": 25,
            "phone": "(333)107-8036x84277",
            "password": "@2GE%j@O@$",
            "country": "Montenegro",
            "drCodes": [
                "EGP36Hop614"
            ]
        },
        {
            "email": "tryan@gmail.com",
            "name": "Molly Ryan",
            "age": 32,
            "phone": "001-493-238-8429x874",
            "password": "gyr26Q(k^I",
            "country": "French Guiana",
            "drCodes": [
                "EGP25Hop765"
            ]
        },
        {
            "email": "loribell@hotmail.com",
            "name": "Alice Mckinney",
            "age": 27,
            "phone": "1189471178",
            "password": "6qQy#TLt^Y",
            "country": "Argentina",
            "drCodes": [
                "EGP62Hop120"
            ]
        },
        {
            "email": "thomasmorgan@buck-schmidt.com",
            "name": "Nicole Griffith",
            "age": 31,
            "phone": "(267)916-7904x64241",
            "password": "_@!8rQata2",
            "country": "Swaziland",
            "drCodes": [
                "EGP46Hop395"
            ]
        },
        {
            "email": "juliestewart@yahoo.com",
            "name": "Alexis Taylor",
            "age": 58,
            "phone": "988.961.0068",
            "password": "FgOZM@5J$4",
            "country": "Mongolia",
            "drCodes": [
                "EGP91Hop350"
            ]
        },
        {
            "email": "brooksandrew@diaz-watson.com",
            "name": "Teresa Hart",
            "age": 28,
            "phone": "+1-001-495-2796x783",
            "password": "_8chCV4aXz",
            "country": "Kiribati",
            "drCodes": [
                "EGP55Hop970"
            ]
        },
        {
            "email": "kevinsmith@gmail.com",
            "name": "Philip Williams",
            "age": 48,
            "phone": "507-196-2589x19136",
            "password": "+$8Vj9Jc!c",
            "country": "Ireland",
            "drCodes": [
                "EGP21Hop737"
            ]
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
    },
    {
            "doctor-code": "EGP31Hop402",
            "patient-phone": "001-855-391-3058"
        },
        {
            "doctor-code": "EGP19Hop748",
            "patient-phone": "+1-575-304-6120"
        },
        {
            "doctor-code": "EGP96Hop267",
            "patient-phone": "001-851-200-8252x904"
        },
        {
            "doctor-code": "EGP99Hop495",
            "patient-phone": "997.722.7589"
        },
        {
            "doctor-code": "EGP59Hop513",
            "patient-phone": "952.512.0541x469"
        },
        {
            "doctor-code": "EGP52Hop393",
            "patient-phone": "(415)588-6259"
        },
        {
            "doctor-code": "EGP21Hop955",
            "patient-phone": "001-586-275-3487x8664"
        },
        {
            "doctor-code": "EGP41Hop268",
            "patient-phone": "904.625.6542x632"
        },
        {
            "doctor-code": "EGP58Hop163",
            "patient-phone": "258-014-2249"
        },
        {
            "doctor-code": "EGP15Hop905",
            "patient-phone": "(665)028-5186x471"
        },
        {
            "doctor-code": "EGP27Hop282",
            "patient-phone": "(311)710-0723x949"
        },
        {
            "doctor-code": "EGP36Hop831",
            "patient-phone": "468.771.9649"
        },
        {
            "doctor-code": "EGP73Hop965",
            "patient-phone": "(192)087-6317x5948"
        },
        {
            "doctor-code": "EGP26Hop257",
            "patient-phone": "895.667.7718x75828"
        },
        {
            "doctor-code": "EGP21Hop668",
            "patient-phone": "001-182-174-2989x49387"
        },
        {
            "doctor-code": "EGP61Hop420",
            "patient-phone": "016.104.6068"
        },
        {
            "doctor-code": "EGP41Hop696",
            "patient-phone": "+1-953-123-0275"
        },
        {
            "doctor-code": "EGP18Hop751",
            "patient-phone": "974.220.4628x524"
        },
        {
            "doctor-code": "EGP54Hop762",
            "patient-phone": "392-854-3373x69627"
        },
        {
            "doctor-code": "EGP34Hop148",
            "patient-phone": "(765)146-9652x9310"
        },
        {
            "doctor-code": "EGP99Hop303",
            "patient-phone": "885-250-4097x562"
        },
        {
            "doctor-code": "EGP91Hop885",
            "patient-phone": "(512)449-8184x8520"
        },
        {
            "doctor-code": "EGP93Hop340",
            "patient-phone": "4803939487"
        },
        {
            "doctor-code": "EGP45Hop621",
            "patient-phone": "259.785.9651x36698"
        },
        {
            "doctor-code": "EGP17Hop369",
            "patient-phone": "+1-189-216-7088"
        },
        {
            "doctor-code": "EGP85Hop182",
            "patient-phone": "001-281-476-7086x322"
        },
        {
            "doctor-code": "EGP44Hop184",
            "patient-phone": "130.462.3369x3463"
        },
        {
            "doctor-code": "EGP91Hop420",
            "patient-phone": "+1-270-846-7257"
        },
        {
            "doctor-code": "EGP73Hop529",
            "patient-phone": "(316)998-0483x4973"
        },
        {
            "doctor-code": "EGP38Hop744",
            "patient-phone": "001-342-910-2087x2206"
        },
        {
            "doctor-code": "EGP91Hop921",
            "patient-phone": "+1-451-648-0312"
        },
        {
            "doctor-code": "EGP50Hop208",
            "patient-phone": "+1-678-420-1021x486"
        },
        {
            "doctor-code": "EGP59Hop373",
            "patient-phone": "828.169.7638"
        },
        {
            "doctor-code": "EGP36Hop614",
            "patient-phone": "(333)107-8036x84277"
        },
        {
            "doctor-code": "EGP25Hop765",
            "patient-phone": "001-493-238-8429x874"
        },
        {
            "doctor-code": "EGP62Hop120",
            "patient-phone": "1189471178"
        },
        {
            "doctor-code": "EGP46Hop395",
            "patient-phone": "(267)916-7904x64241"
        },
        {
            "doctor-code": "EGP91Hop350",
            "patient-phone": "988.961.0068"
        },
        {
            "doctor-code": "EGP55Hop970",
            "patient-phone": "+1-001-495-2796x783"
        },
        {
            "doctor-code": "EGP21Hop737",
            "patient-phone": "507-196-2589x19136"
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
    new_doctor = doctor.model_dump()
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
    doctor_dict = doctor_update.model_dump(exclude_unset=True)
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
    
    new_patient = patient.model_dump()
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
    patient_dict = patient_update.model_dump(exclude_unset=True)
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
    
    new_patient = patient.model_dump()
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
    patient_dict = patient_update.model_dump(exclude_unset=True)
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
    
    new_relationship = relationship.model_dump()
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

    new_patient_info = patient_info.model_dump()
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
    patient_dict = patient_update.model_dump(exclude_unset=True)
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
    new_diagnosis = diagnosis.model_dump()
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








