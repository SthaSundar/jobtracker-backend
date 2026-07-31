# JobTracker — Backend

REST API for a personal job application tracker — built with Django REST Framework, JWT auth, and MySQL.

**Frontend repo:** [jobtracker-frontend](https://github.com/SthaSundar/jobtracker-frontend)
**🔗 Live API docs (Swagger):** [jobtracker-backend-qv7a.onrender.com/api/docs/](https://jobtracker-backend-qv7a.onrender.com/api/docs/)

> This is an API-only backend — visiting the bare domain (`/`) returns a 404, since there's no root route defined. Use `/api/docs/` for the interactive Swagger UI, or `/admin/` for the Django admin panel.

## Tech Stack
- Django 6.0 + Django REST Framework
- MySQL (production database hosted on [Aiven](https://aiven.io))
- JWT Auth (djangorestframework-simplejwt)
- drf-spectacular (OpenAPI schema + Swagger UI)
- django-cors-headers
- WhiteNoise (static file serving in production)
- Gunicorn (production WSGI server)

## Features
- Full CRUD for job applications (company, role, status, dates, notes, resume upload)
- JWT authentication (register, login, token refresh)
- Per-user data isolation — each user only sees their own applications
- File upload support for resumes
- Auto-generated, interactive API documentation via Swagger

## Live Deployment

| | |
|---|---|
| **API docs (Swagger)** | [jobtracker-backend-qv7a.onrender.com/api/docs/](https://jobtracker-backend-qv7a.onrender.com/api/docs/) (Render, free tier) |
| **Database** | MySQL 8.4 on [Aiven](https://aiven.io) (free tier), SSL-required connection |
| **Frontend** | [jobtracker-frontend-one.vercel.app](https://jobtracker-frontend-one.vercel.app) (Vercel) |

**Deployment stack:** GitHub → Render (auto-deploys on push to `main`) → Gunicorn → Django → Aiven MySQL (SSL-encrypted connection via CA certificate).

> **Note:** the free Render instance spins down after ~15 minutes of inactivity. The first request after idle time may take 30–60 seconds while it wakes back up.

## Local Setup

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
4. Copy `.env.example` to `.env` and fill in your own values (DB credentials, secret key — see table below)
5. Run migrations:
   ```
   python manage.py migrate
   ```
6. Start the dev server:
   ```
   python manage.py runserver
   ```
7. Visit `http://127.0.0.1:8000/api/docs/` to explore the API via Swagger

## Environment Variables

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Django's cryptographic signing key | *(generate with `get_random_secret_key()`)* |
| `DEBUG` | Debug mode toggle — must be `False` in production | `True` (local) / `False` (production) |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames | `127.0.0.1,localhost` |
| `DB_NAME` | MySQL database name | `defaultdb` |
| `DB_USER` | MySQL username | `avnadmin` |
| `DB_PASSWORD` | MySQL password | *(secret)* |
| `DB_HOST` | MySQL host | `your-db.aivencloud.com` |
| `DB_PORT` | MySQL port | `21167` |
| `CORS_ALLOWED_ORIGINS` | Comma-separated list of allowed frontend origins | `http://localhost:5173` |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated list of trusted origins for CSRF | `https://your-frontend.vercel.app` |
| `RENDER_EXTERNAL_HOSTNAME` | Auto-injected by Render — no manual setup needed | *(set automatically)* |

Production database connections require SSL — a `ca.pem` CA certificate (downloaded from Aiven) must be present in the project root.

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
| GET | `/api/docs/` | Interactive Swagger API documentation |

Full request/response schemas are available live via the Swagger docs link above.

## Deployment Notes

- Hosted on **Render** (free tier), auto-deploys on push to `main`
- **Build command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- **Start command:** `gunicorn config.wsgi:application`
- Static files served via **WhiteNoise** (no separate static file host needed)
- Database is **MySQL on Aiven**, connected over a required SSL connection using a CA certificate
- `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` auto-include Render's own domain via the `RENDER_EXTERNAL_HOSTNAME` environment variable that Render injects automatically
- `SECURE_PROXY_SSL_HEADER` is set so Django correctly recognizes HTTPS requests behind Render's proxy

## Known Limitations

- **Ephemeral filesystem:** Render's free web services don't persist uploaded files (e.g. resumes) between deploys or restarts. A production fix would move file storage to S3 or Cloudinary.
- **Free-tier cold starts:** the API spins down after ~15 minutes idle; the first request afterward is slow (30–60s) while it restarts.