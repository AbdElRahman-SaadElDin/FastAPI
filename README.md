# Medical Reminder API

A FastAPI-based REST API for managing doctors, patients, and medical records.

## Features

- **Doctor Management**: Create, read, update, and delete doctor records
- **Patient Management**: Create, read, update, and delete patient records
- **Patient-Doctor Relationships**: Manage relationships between doctors and patients
- **Medical Records**: Store and manage patient diagnoses, treatments, and medical reports
- **Simple Authentication**: Basic email and password verification for doctors and patients
- **CORS Enabled**: Ready for frontend integration

## API Endpoints

### Doctors

- `GET /doctors` - Get all doctors
- `GET /doctors/{doctor_code}` - Get specific doctor
- `POST /doctors` - Create new doctor
- `PUT /doctors/{doctor_code}` - Update doctor
- `DELETE /doctors/{doctor_code}` - Delete doctor

### Patients

- `GET /patients` - Get all patients

- `GET /patients/{patient_email}` - Get specific patient by email
- `POST /patients` - Create new patient
- `PUT /patients/{patient_email}` - Update patient by email
- `DELETE /patients/{patient_email}` - Delete patient by email

- `GET /patients/phone/{patient_phone}` - Get specific patient by phone number
- `POST /patients/phone/{patient_phone}` - Create new patient with specified phone number
- `PUT /patients/phone/{patient_phone}` - Update patient by phone number
- `DELETE /patients/phone/{patient_phone}` - Delete patient by phone number

### Authentication Checks

- `GET /doctor?email={email}&password={password}` - Check if doctor exists
- `GET /patient?email={email}&password={password}` - Check if patient exists

### Patient-Doctor Relationships

- `GET /patient-doctor` - Get all relationships
- `POST /patient-doctor` - Create relationship
- `DELETE /patient-doctor/{doctor_code}/{patient_phone}` - Delete relationship

### Doctor's Patients

- `GET /doctors/{doctor_code}/patients` - Get doctor's patients
- `POST /doctors/{doctor_code}/patients` - Add patient to doctor
- `GET /doctors/{doctor_code}/patients/{patient_phone}` - Get specific patient from doctor's list
- `DELETE /doctors/{doctor_code}/patients/{patient_phone}` - Remove patient from doctor's list

### Patient Diagnoses

- `GET /doctors/{doctor_code}/patients/{patient_phone}/diagnosis` - Get all diagnoses for a patient
- `POST /doctors/{doctor_code}/patients/{patient_phone}/diagnosis` - Add new diagnosis to patient
- `DELETE /doctors/{doctor_code}/patients/{patient_phone}/diagnosis` - Delete specific diagnosis from patient

### Patient Doctor Codes

- `GET /patients/{phone}/drCodes` - Get all doctor codes for a specific patient
- `POST /patients/{phone}/drCodes` - Add a doctor code to a patient's drCodes list
- `PUT /patients/{phone}/drCodes` - Replace all doctor codes for a patient
- `DELETE /patients/{phone}/drCodes` - Delete all doctor codes for a patient
- `DELETE /patients/{phone}/drCodes/{doctor_code}` - Delete a specific doctor code from a patient

## Deployment to Vercel

### Prerequisites

1. Install [Vercel CLI](https://vercel.com/docs/cli):

   ```bash
   npm i -g vercel
   ```

2. Make sure you have a Vercel account

### Deployment Steps

1. **Login to Vercel**:

   ```bash
   vercel login
   ```

2. **Deploy the application**:

   ```bash
   vercel
   ```

3. **Follow the prompts**:

   - Set up and deploy: `Y`
   - Which scope: Select your account
   - Link to existing project: `N`
   - Project name: `medical-reminder-api` (or your preferred name)
   - Directory: `./` (current directory)
   - Override settings: `N`

4. **Your API will be deployed** to a URL like: `https://your-project-name.vercel.app`

### Important Notes for Vercel Deployment

⚠️ **Data Persistence**: This deployment uses in-memory storage, which means:

- Data will be reset on each deployment
- Data is not persistent between serverless function invocations
- For production use, consider integrating with a database (MongoDB, PostgreSQL, etc.)

### Environment Variables (Optional)

You can set environment variables in Vercel dashboard:

- Go to your project settings
- Navigate to "Environment Variables"
- Add any configuration variables you need

## Local Development

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server**:

   ```bash
   python main.py
   ```

3. **Access the API**:
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Testing Authentication

### Using HTML Test Page

1. Open `auth_test.html` in your browser
2. Use the test credentials:
   - Email: `abdelrahmansaad@gmail.com`
   - Password: `SaadSaadSaad@@777`
3. Click "Login" to test the authentication

### Using cURL

```bash
# Check doctor authentication
curl "http://localhost:8000/doctor?email=abdelrahmansaad@gmail.com&password=SaadSaadSaad@@777"

# Check patient authentication
curl "http://localhost:8000/patient?email=mazen&password=SaadSaadSaad@@777"
```

## API Documentation

Once deployed, you can access:

- **Interactive API docs**: `https://your-domain.vercel.app/docs`
- **ReDoc documentation**: `https://your-domain.vercel.app/redoc`

## Data Models

### Doctor

```json
{
  "code": "string",
  "name": "string",
  "Age": "integer",
  "phone": "string",
  "profession": "string",
  "specialty": "string",
  "gender": "string",
  "email": "string",
  "password": "string",
  "country": "string",
  "city": "string",
  "patient": []
}
```

### Patient

```json
{
  "email": "string",
  "name": "string",
  "age": "integer",
  "phone": "string",
  "password": "string",
  "country": "string",
  "drCodes": ["string"]
}
```

## Example Usage

### Check Doctor Authentication

```bash
curl "https://your-domain.vercel.app/doctor?email=abdelrahmansaad@gmail.com&password=SaadSaadSaad@@777"
```

Response:

```json
{
  "exists": true
}
```

### Create a Doctor

```bash
curl -X POST "https://your-domain.vercel.app/doctors" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "DOC123",
    "name": "Dr. John Doe",
    "Age": 35,
    "phone": "+1234567890",
    "profession": "Cardiologist",
    "specialty": "Cardiology",
    "gender": "male",
    "email": "john.doe@example.com",
    "password": "securepassword",
    "country": "USA",
    "city": "New York"
  }'
```

### Get All Doctors

```bash
curl "https://your-domain.vercel.app/doctors"
```

### Get Specific Doctor

```bash
curl "https://your-domain.vercel.app/doctors/EGP12Hop676"
```

### Get Specific Patient from Doctor's List

```bash
curl "https://your-domain.vercel.app/doctors/EGP12Hop676/patients/+201205621566"
```

### Get Patient by Phone Number

```bash
curl "https://your-domain.vercel.app/patients/phone/+201205621566"
```

### Create Patient with Phone Number

```bash
curl -X POST "https://your-domain.vercel.app/patients/phone/+201234567890" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newpatient@example.com",
    "name": "John Smith",
    "age": 30,
    "phone": "+201234567890",
    "password": "securepassword",
    "country": "Egypt"
  }'
```

### Update Patient by Phone Number

```bash
curl -X PUT "https://your-domain.vercel.app/patients/phone/+201205621566" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "age": 25,
    "country": "Egypt"
  }'
```

### Delete Patient by Phone Number

```bash
curl -X DELETE "https://your-domain.vercel.app/patients/phone/+201205621566"
```

### Get Patient Diagnoses

```bash
curl "https://your-domain.vercel.app/doctors/EGP12Hop676/patients/+201205621566/diagnosis"
```

### Add Diagnosis to Patient

```bash
curl -X POST "https://your-domain.vercel.app/doctors/EGP12Hop676/patients/+201205621566/diagnosis" \
  -H "Content-Type: application/json" \
  -d '{
    "diagnosis": "Hypertension",
    "prognosis": "With proper medication and lifestyle changes, blood pressure can be controlled effectively.",
    "medical-report": "Patient shows elevated blood pressure readings over the past month. Systolic consistently above 140 mmHg.",
    "medical-treatment": "Lisinopril 10mg daily, reduced salt intake, regular exercise, monthly check-ups.",
    "schedule": "2025-01-15T14:00:00Z",
    "complaint": "Headaches and dizziness"
  }'
```

### Delete Diagnosis from Patient

```bash
curl -X DELETE "https://your-domain.vercel.app/doctors/EGP12Hop676/patients/+201205621566/diagnosis?diagnosis_name=Hypertension"
```

### Remove Patient from Doctor's List

```bash
curl -X DELETE "https://your-domain.vercel.app/doctors/EGP12Hop676/patients/+201205621566"
```

### Get Patient Doctor Codes

```bash
curl "https://your-domain.vercel.app/patients/+201205621566/drCodes"
```

Response:

```json
{
  "phone": "+201205621566",
  "drCodes": ["EGP12Hop676"]
}
```

### Add Doctor Code to Patient

```bash
curl -X POST "https://your-domain.vercel.app/patients/+201205621566/drCodes" \
  -H "Content-Type: application/json" \
  -d '"EGP12Hop676"'
```

Response:

```json
{
  "message": "Doctor code added successfully",
  "phone": "+201205621566",
  "drCodes": ["EGP12Hop676"]
}
```

### Update All Doctor Codes for Patient

```bash
curl -X PUT "https://your-domain.vercel.app/patients/+201205621566/drCodes" \
  -H "Content-Type: application/json" \
  -d '["EGP12Hop676", "NEWDOC123"]'
```

Response:

```json
{
  "message": "Doctor codes updated successfully",
  "phone": "+201205621566",
  "drCodes": ["EGP12Hop676", "NEWDOC123"]
}
```

### Delete All Doctor Codes for Patient

```bash
curl -X DELETE "https://your-domain.vercel.app/patients/+201205621566/drCodes"
```

Response:

```json
{
  "message": "All doctor codes deleted successfully",
  "phone": "+201205621566",
  "deleted_drCodes": ["EGP12Hop676", "NEWDOC123"]
}
```

### Delete Specific Doctor Code from Patient

```bash
curl -X DELETE "https://your-domain.vercel.app/patients/+201205621566/drCodes/EGP12Hop676"
```

Response:

```json
{
  "message": "Doctor code deleted successfully",
  "phone": "+201205621566",
  "drCodes": ["NEWDOC123"]
}
```

## Support

For issues or questions:

1. Check the API documentation at `/docs`
2. Review the error messages in the response
3. Ensure all required fields are provided in requests

## License

This project is open source and available under the MIT License.

---

# Frontend Integration Guide

## Overview

This API provides simple authentication endpoints for doctors and patients in a medical reminder system. The API includes simple GET endpoints to check if users exist with their email and password credentials.

## Base URL

```
http://localhost:8000
```

## Authentication Endpoints

### 1. Check Doctor Authentication

**Endpoint:** `GET /doctor`

**Parameters:**

- `email` (string): Doctor's email address
- `password` (string): Doctor's password

**Response:**

```json
{
  "exists": true // or false
}
```

**Example Usage:**

#### Using Fetch API (JavaScript)

```javascript
// Check if doctor exists
async function checkDoctor(email, password) {
  try {
    const response = await fetch(
      `http://localhost:8000/doctor?email=${encodeURIComponent(
        email
      )}&password=${encodeURIComponent(password)}`
    );
    const data = await response.json();

    if (data.exists) {
      console.log("Doctor authenticated successfully");
      // Redirect to doctor dashboard or set authentication state
      return true;
    } else {
      console.log("Invalid credentials");
      // Show error message to user
      return false;
    }
  } catch (error) {
    console.error("Error checking doctor:", error);
    return false;
  }
}

// Usage
checkDoctor("abdelrahmansaad@gmail.com", "SaadSaadSaad@@777");
```

#### Using Axios (JavaScript)

```javascript
import axios from "axios";

async function checkDoctor(email, password) {
  try {
    const response = await axios.get("http://localhost:8000/doctor", {
      params: {
        email: email,
        password: password,
      },
    });

    if (response.data.exists) {
      console.log("Doctor authenticated successfully");
      return true;
    } else {
      console.log("Invalid credentials");
      return false;
    }
  } catch (error) {
    console.error("Error checking doctor:", error);
    return false;
  }
}
```

#### Using React Hook

```javascript
import { useState } from "react";

function useDoctorAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const checkDoctor = async (email, password) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `http://localhost:8000/doctor?email=${encodeURIComponent(
          email
        )}&password=${encodeURIComponent(password)}`
      );
      const data = await response.json();

      setIsAuthenticated(data.exists);
      return data.exists;
    } catch (err) {
      setError("Authentication failed");
      setIsAuthenticated(false);
      return false;
    } finally {
      setLoading(false);
    }
  };

  return { isAuthenticated, loading, error, checkDoctor };
}
```

### 2. Check Patient Authentication

**Endpoint:** `GET /patient`

**Parameters:**

- `email` (string): Patient's email address
- `password` (string): Patient's password

**Response:**

```json
{
  "exists": true // or false
}
```

**Example Usage:**

#### Using Fetch API (JavaScript)

```javascript
// Check if patient exists
async function checkPatient(email, password) {
  try {
    const response = await fetch(
      `http://localhost:8000/patient?email=${encodeURIComponent(
        email
      )}&password=${encodeURIComponent(password)}`
    );
    const data = await response.json();

    if (data.exists) {
      console.log("Patient authenticated successfully");
      // Redirect to patient dashboard or set authentication state
      return true;
    } else {
      console.log("Invalid credentials");
      // Show error message to user
      return false;
    }
  } catch (error) {
    console.error("Error checking patient:", error);
    return false;
  }
}

// Usage
checkPatient("mazen", "SaadSaadSaad@@777");
```

#### Using Axios (JavaScript)

```javascript
import axios from "axios";

async function checkPatient(email, password) {
  try {
    const response = await axios.get("http://localhost:8000/patient", {
      params: {
        email: email,
        password: password,
      },
    });

    if (response.data.exists) {
      console.log("Patient authenticated successfully");
      return true;
    } else {
      console.log("Invalid credentials");
      return false;
    }
  } catch (error) {
    console.error("Error checking patient:", error);
    return false;
  }
}
```

## Complete React Login Component Example

```jsx
import React, { useState } from "react";

function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [userType, setUserType] = useState("doctor"); // 'doctor' or 'patient'
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");

    try {
      const endpoint = userType === "doctor" ? "/doctor" : "/patient";
      const response = await fetch(
        `http://localhost:8000${endpoint}?email=${encodeURIComponent(
          email
        )}&password=${encodeURIComponent(password)}`
      );
      const data = await response.json();

      if (data.exists) {
        setSuccess(`${userType} authenticated successfully!`);
        // Store authentication state in localStorage or context
        localStorage.setItem("isAuthenticated", "true");
        localStorage.setItem("userType", userType);
        localStorage.setItem("userEmail", email);

        // Redirect to appropriate dashboard
        setTimeout(() => {
          window.location.href =
            userType === "doctor" ? "/doctor-dashboard" : "/patient-dashboard";
        }, 1000);
      } else {
        setError("Invalid email or password");
      }
    } catch (err) {
      setError("Login failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <h2>Medical Reminder Login</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>User Type:</label>
          <select
            value={userType}
            onChange={(e) => setUserType(e.target.value)}
          >
            <option value="doctor">Doctor</option>
            <option value="patient">Patient</option>
          </select>
        </div>

        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>

        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}
      </form>
    </div>
  );
}

export default LoginForm;
```

## Test Credentials

### Doctor

- **Email:** `abdelrahmansaad@gmail.com`
- **Password:** `SaadSaadSaad@@777`

### Patient

- **Email:** `mazen`
- **Password:** `SaadSaadSaad@@777`

## Error Handling

The API returns simple boolean responses. Here's how to handle different scenarios:

```javascript
// Handle network errors
try {
  const response = await fetch(
    "/doctor?email=test@example.com&password=password"
  );
  const data = await response.json();

  if (data.exists) {
    // User authenticated
  } else {
    // Invalid credentials
  }
} catch (error) {
  // Network error or server down
  console.error("Network error:", error);
}
```

## Security Notes

1. **HTTPS in Production:** Always use HTTPS in production environments
2. **Password Security:** Consider implementing rate limiting for failed login attempts
3. **Input Validation:** Always validate and sanitize user inputs on both frontend and backend

## CORS Configuration

The API is configured to allow requests from any origin (`*`). In production, you should restrict this to your specific domain:

```javascript
// Frontend - if you need to include credentials
fetch("/doctor?email=test@example.com&password=password", {
  credentials: "include",
});
```

## Getting Started

1. **Start the API server:**

   ```bash
   python main.py
   ```

2. **Test the endpoints:**

   ```bash
   # Test doctor authentication
   curl "http://localhost:8000/doctor?email=abdelrahmansaad@gmail.com&password=SaadSaadSaad@@777"

   # Test patient authentication
   curl "http://localhost:8000/patient?email=mazen&password=SaadSaadSaad@@777"
   ```

3. **Integrate with your frontend application** using the examples above.

## API Documentation

For complete API documentation, visit:

```
http://localhost:8000/docs
```

This will show the interactive Swagger UI with all available endpoints and their documentation.
