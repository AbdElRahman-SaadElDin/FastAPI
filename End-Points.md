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
