# API Testing Guide

## Testing Your Medical Reminder API

### Prerequisites

- Your API is deployed and running
- You have a tool like Postman, curl, or any HTTP client

## 1. Test the Root Endpoint

```bash
curl https://your-domain.vercel.app/
```

**Expected Response:**

```json
{
  "message": "Medical Reminder API is running"
}
```

## 2. Test GET Endpoints

### Get All Doctors

```bash
curl https://your-domain.vercel.app/doctors
```

### Get All Patients

```bash
curl https://your-domain.vercel.app/patients
```

### Get All Patient-Doctor Relationships

```bash
curl https://your-domain.vercel.app/patient-doctor
```

## 3. Test POST Endpoints (The Important Part!)

### Create a New Doctor

```bash
curl -X POST "https://your-domain.vercel.app/doctors" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "DOC123",
    "name": "Dr. Sarah Johnson",
    "Age": 35,
    "phone": "+1234567890",
    "profession": "Cardiologist",
    "specialty": "Cardiology",
    "gender": "female",
    "email": "sarah.johnson@example.com",
    "password": "securepassword123",
    "country": "USA",
    "city": "New York"
  }'
```

### Create a New Patient

```bash
curl -X POST "https://your-domain.vercel.app/patients" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "name": "John Doe",
    "age": 28,
    "phone": "+1987654321",
    "password": "patientpass123",
    "country": "USA"
  }'
```

### Create a Patient-Doctor Relationship

```bash
curl -X POST "https://your-domain.vercel.app/patient-doctor" \
  -H "Content-Type: application/json" \
  -d '{
    "doctor_code": "DOC123",
    "patient_phone": "+1987654321"
  }'
```

### Add Patient to Doctor's List

```bash
curl -X POST "https://your-domain.vercel.app/doctors/DOC123/patients" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "PAT001",
    "name": "John Doe",
    "date of admission": "2025-01-15T10:30:00Z",
    "phone": "+1987654321",
    "country": "USA",
    "gender": "male",
    "profession": "Engineer",
    "age": 28,
    "cases": [
      {
        "diagnosis": [
          {
            "diagnosis": "Hypertension",
            "prognosis": "Controllable with medication and lifestyle changes",
            "medical-report": "Blood pressure consistently elevated at 140/90 mmHg",
            "medical-treatment": "Lisinopril 10mg daily, reduced salt intake, regular exercise",
            "schedule": "2025-01-15T10:30:00Z",
            "complaint": "Headaches and occasional dizziness"
          }
        ]
      }
    ]
  }'
```

## 4. Test PUT Endpoints

### Update a Doctor

```bash
curl -X PUT "https://your-domain.vercel.app/doctors/DOC123" \
  -H "Content-Type: application/json" \
  -d '{
    "specialty": "Pediatric Cardiology",
    "city": "Boston"
  }'
```

### Update a Patient

```bash
curl -X PUT "https://your-domain.vercel.app/patients/john.doe@example.com" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 29,
    "country": "Canada"
  }'
```

## 5. Test DELETE Endpoints

### Delete a Doctor

```bash
curl -X DELETE "https://your-domain.vercel.app/doctors/DOC123"
```

### Delete a Patient

```bash
curl -X DELETE "https://your-domain.vercel.app/patients/john.doe@example.com"
```

### Delete a Patient-Doctor Relationship

```bash
curl -X DELETE "https://your-domain.vercel.app/patient-doctor/DOC123/+1987654321"
```

## 6. Using Postman

If you're using Postman:

1. **Set the request method** to POST
2. **Set the URL** to your endpoint (e.g., `https://your-domain.vercel.app/doctors`)
3. **Go to the "Body" tab**
4. **Select "raw" and "JSON"**
5. **Add your JSON data** in the body field
6. **Click Send**

Example JSON body for creating a doctor:

```json
{
  "code": "DOC123",
  "name": "Dr. Sarah Johnson",
  "Age": 35,
  "phone": "+1234567890",
  "profession": "Cardiologist",
  "specialty": "Cardiology",
  "gender": "female",
  "email": "sarah.johnson@example.com",
  "password": "securepassword123",
  "country": "USA",
  "city": "New York"
}
```

## 7. Common Issues and Solutions

### Issue: "Field required" error

**Cause**: Missing request body or incorrect Content-Type header
**Solution**:

- Ensure you're sending JSON data in the request body
- Set Content-Type header to `application/json`

### Issue: "Validation error"

**Cause**: Missing required fields or incorrect data types
**Solution**: Check that all required fields are provided with correct data types

### Issue: "Doctor code already exists"

**Cause**: Trying to create a doctor with an existing code
**Solution**: Use a unique doctor code

## 8. Testing with JavaScript/Fetch

```javascript
// Create a new doctor
const createDoctor = async () => {
  const response = await fetch("https://your-domain.vercel.app/doctors", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      code: "DOC123",
      name: "Dr. Sarah Johnson",
      Age: 35,
      phone: "+1234567890",
      profession: "Cardiologist",
      specialty: "Cardiology",
      gender: "female",
      email: "sarah.johnson@example.com",
      password: "securepassword123",
      country: "USA",
      city: "New York",
    }),
  });

  const data = await response.json();
  console.log(data);
};

// Get all doctors
const getDoctors = async () => {
  const response = await fetch("https://your-domain.vercel.app/doctors");
  const data = await response.json();
  console.log(data);
};
```

## 9. API Documentation

Visit your API documentation at:

- **Interactive docs**: `https://your-domain.vercel.app/docs`
- **ReDoc**: `https://your-domain.vercel.app/redoc`

These provide interactive testing interfaces where you can test all endpoints directly in the browser.
