# Healthcare Backend API

A RESTful backend for a healthcare application built with **Django**, **Django REST Framework**, **PostgreSQL**, and **JWT authentication**.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Django 4.2 + Django REST Framework |
| Database | PostgreSQL |
| Auth | JWT via `djangorestframework-simplejwt` |
| Config | `python-decouple` for env variables |
| CORS | `django-cors-headers` |

---

## Local Setup

### 1. Clone & enter the project

```bash
git clone <your-repo-url>
cd healthcare_backend
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your actual values:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=your-postgres-password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Set up PostgreSQL

```sql
-- Run in psql as a superuser
CREATE DATABASE healthcare_db;
CREATE USER postgres WITH PASSWORD 'your-postgres-password';
GRANT ALL PRIVILEGES ON DATABASE healthcare_db TO postgres;
```

### 6. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a superuser (optional, for Django admin)

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

Server runs at: `http://127.0.0.1:8000/`

---

## API Endpoints

All protected endpoints require the header:
```
Authorization: Bearer <access_token>
```

---

### Authentication

#### POST `/api/auth/register/`
Register a new user.

**Request body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Response `201`:**
```json
{
  "message": "User registered successfully.",
  "user": { "id": "uuid", "name": "John Doe", "email": "john@example.com" },
  "tokens": { "access": "...", "refresh": "..." }
}
```

---

#### POST `/api/auth/login/`
Log in and receive JWT tokens.

**Request body:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Response `200`:**
```json
{
  "message": "Login successful.",
  "user": { "id": "uuid", "name": "John Doe", "email": "john@example.com" },
  "tokens": { "access": "...", "refresh": "..." }
}
```

---

### Patients *(Auth required — scoped to logged-in user)*

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/patients/` | Create a patient |
| `GET` | `/api/patients/` | List your patients |
| `GET` | `/api/patients/<id>/` | Get patient detail |
| `PUT` | `/api/patients/<id>/` | Update a patient |
| `DELETE` | `/api/patients/<id>/` | Delete a patient |

**Patient fields:**
```json
{
  "name": "Jane Smith",
  "age": 32,
  "gender": "Female",
  "blood_group": "O+",
  "address": "123 Main St, Delhi",
  "phone": "9876543210",
  "medical_history": "Diabetic"
}
```

---

### Doctors *(Auth required — globally visible)*

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/doctors/` | Create a doctor |
| `GET` | `/api/doctors/` | List all doctors |
| `GET` | `/api/doctors/<id>/` | Get doctor detail |
| `PUT` | `/api/doctors/<id>/` | Update a doctor |
| `DELETE` | `/api/doctors/<id>/` | Delete a doctor |

**Doctor fields:**
```json
{
  "name": "Dr. Arjun Mehta",
  "specialization": "Cardiology",
  "experience_years": 12,
  "email": "arjun.mehta@hospital.com",
  "phone": "9123456789",
  "hospital": "Apollo Hospital, Mumbai"
}
```

---

### Patient-Doctor Mappings *(Auth required)*

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/mappings/` | Assign a doctor to a patient |
| `GET` | `/api/mappings/` | List all mappings |
| `GET` | `/api/mappings/<patient_id>/` | Get all doctors for a patient |
| `DELETE` | `/api/mappings/remove/<id>/` | Remove a mapping by mapping ID |

**Assign doctor to patient:**
```json
{
  "patient": "<patient-uuid>",
  "doctor": "<doctor-uuid>"
}
```

---

## Error Responses

All errors return a consistent JSON structure:

```json
{ "error": "Human-readable message." }
```

Or for validation errors:
```json
{ "errors": { "field": ["error detail"] } }
```

| Status | Meaning |
|--------|---------|
| `400` | Validation error |
| `401` | Missing or invalid JWT token |
| `403` | Account deactivated |
| `404` | Resource not found |

---

## Project Structure

```
healthcare_backend/
├── healthcare_backend/      # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── authentication/      # User model, register, login
│   ├── patients/            # Patient CRUD
│   ├── doctors/             # Doctor CRUD
│   └── mappings/            # Patient-Doctor assignments
├── .env.example
├── requirements.txt
└── manage.py
```

---

## Django Admin

Visit `http://127.0.0.1:8000/admin/` with your superuser credentials to manage all records via the Django admin panel.
