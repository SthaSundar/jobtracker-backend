# JobTracker — Backend

REST API for a personal job application tracker — built with Django REST Framework, JWT auth, and MySQL.

**Frontend repo:** [jobtracker-frontend](https://github.com/SthaSundar/jobtracker-frontend)

## Tech Stack
- Django 6.0 + Django REST Framework
- MySQL
- JWT Auth (djangorestframework-simplejwt)

## Features
- Full CRUD for job applications (company, role, status, dates, notes, resume upload)
- JWT authentication (register, login, token refresh)
- Per-user data isolation — each user only sees their own applications
- File upload support for resumes

## Setup

1. Clone the repo
2. Create and activate a virtual environment:

```
   python -m venv venv
   venv\Scripts\activate
```
3. Install dependencies:
```
   pip install -r requirements.txt
```
4. Copy `.env.example` to `.env` and fill in your own values (DB credentials, secret key)
5. Run migrations:
```
   python manage.py migrate
```
6. Start the dev server:
```
   python manage.py runserver
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Create a new user |
| POST | `/api/auth/login/` | Log in, get access + refresh tokens |
| POST | `/api/auth/login/refresh/` | Refresh an expired access token |
| GET | `/api/applications/` | List your job applications |
| POST | `/api/applications/` | Create a new job application |
| GET | `/api/applications/{id}/` | Retrieve a single application |
| PATCH | `/api/applications/{id}/` | Update an application |
| DELETE | `/api/applications/{id}/` | Delete an application |