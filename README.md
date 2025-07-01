# 🏥 Hospital Management API

A RESTful backend built with **Django** and **Django REST Framework (DRF)** that allows doctors to manage patients and their medical records securely.

---

## 🚀 Features

- ✅ User authentication using **JWT**
- ✅ Doctors can:
  - Register/Login
  - Create and manage their patients
  - Add/view medical records for their patients
- ✅ Admins can view all patients and records
- ✅ Proper permissions to restrict data access between doctors
- ✅ Health check & welcome endpoints
- ✅ Dockerized setup
- ✅ Unit test coverage

---

## 📦 Tech Stack

- Python 3.11+
- Django 4.x / 5.x
- Django REST Framework
- JWT Auth via `djangorestframework-simplejwt`
- PostgreSQL (via Docker)
- Docker & docker-compose

---

## 📁 API Endpoints

### 🔐 Auth
| Endpoint         | Method | Description          |
|------------------|--------|----------------------|
| `/api/signup/`   | POST   | Register doctor      |
| `/api/login/`    | POST   | Login and get tokens |
| `/api/token/refresh/` | POST | Refresh JWT token |

### 👨‍⚕️ Doctor APIs (Requires Auth)
| Endpoint                         | Method | Description                    |
|----------------------------------|--------|--------------------------------|
| `/api/patients/`                | GET/POST | List or create patients         |
| `/api/patients/records/add`     | POST   | Add medical record to patient |
| `/api/patients/<id>/records/`   | GET    | View records for a patient     |

### 🛠️ Utility
| Endpoint           | Method | Description      |
|--------------------|--------|------------------|
| `/api/health/`     | GET    | Health check     |
| `/api/welcome/`    | GET    | Welcome message  |

---

## 🐳 Running with Docker

### 1. Build & Run
Uncomment the `DATABASES` section in `settings.py` to use SQLite for local development, or configure PostgreSQL as needed.
```bash
docker-compose up --build
````

### 2. Create Superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

---

## 🧪 Running Tests

```bash
docker-compose exec web python manage.py test
```

Tests include:

* Patient creation
* Doctor-specific access control
* Record restrictions
* Login flow

---

## 🧠 Business Rules

* Doctors can only view/manage patients and records they created
* Superusers (admins) have access to all data
* Proper status codes and error handling implemented
* Token-based auth for secure APIs

---

## 📜 License

This project is open-sourced under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

**Nitin Chauhan**
Backend Developer – Django, Golang, Docker, DevOps