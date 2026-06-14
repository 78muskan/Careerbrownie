# MargVedA

MargVedA is an AI-powered career counselling and guidance platform for students.

It is built with Python only:

- Backend: FastAPI
- Frontend: Reflex
- AI service: FastAPI + Python AI modules
- Database: SQLite for local beginner use, PostgreSQL-ready through Docker Compose

## What The Product Does

MargVedA supports:

- Student registration and login
- Counsellor registration and login
- Admin dashboard
- JWT authentication
- Role-based access control
- Student profile management
- Counsellor dashboard
- Session booking APIs
- AI chatbot
- Career recommendations
- Skill gap analysis
- College prediction
- Career roadmap generation

## Project Structure

```text
margveda/
├── backend/
│   ├── app/
│   │   ├── api/routes/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   └── main.py
│   ├── alembic/
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env
├── ai_service/
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── pages/
│   ├── components/
│   ├── states/
│   ├── services/
│   ├── assets/
│   ├── margveda_frontend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── rxconfig.py
├── docker-compose.yml
├── README.md
└── .gitignore
```

## Easiest Way To Run Everything

Use Docker Desktop. This is the easiest option if you have no technical experience.

### Step 1: Install Docker Desktop

Install Docker Desktop from:

```text
https://www.docker.com/products/docker-desktop/
```

Open Docker Desktop after installation.

### Step 2: Open Terminal In Project Folder

Open PowerShell and run:

```powershell
cd "D:\Margveda final\margveda"
```

### Step 3: Start The Whole Project

```powershell
docker compose up --build
```

Wait until the logs stop moving quickly.

### Step 4: Open The App

Frontend:

```text
http://localhost:3000
```

Backend API docs:

```text
http://localhost:8000/docs
```

AI service docs:

```text
http://localhost:9000/docs
```

### Step 5: Create Accounts

Open `http://localhost:3000/register`.

Create one account for each role:

- student
- counsellor
- admin

Then log in and test the dashboards.

## Run Without Docker

Use this only if Docker is not available.

### Backend

```powershell
cd "D:\Margveda final\margveda\backend"
..\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### AI Service

Open another PowerShell window:

```powershell
cd "D:\Margveda final\margveda\ai_service"
..\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 9000
```

### Frontend

Open another PowerShell window:

```powershell
cd "D:\Margveda final\margveda\frontend"
pip install -r requirements.txt
reflex run
```

Then open:

```text
http://localhost:3000
```

## Environment Variables

Backend variables:

| Variable | Meaning |
|---|---|
| `DATABASE_URL` | SQLite or PostgreSQL database URL |
| `AI_SERVICE_URL` | URL of the AI service |
| `SECRET_KEY` | JWT secret key |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Login token lifetime |
| `BACKEND_CORS_ORIGINS` | Frontend URLs allowed to call backend |

Frontend variable:

| Variable | Meaning |
|---|---|
| `BACKEND_API_URL` | Backend API URL used by Reflex state handlers |

## API Endpoints

Backend:

- `GET /health`
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/token`
- `GET /api/v1/auth/me`
- `GET /api/v1/students/dashboard`
- `GET /api/v1/students/me`
- `PUT /api/v1/students/me`
- `POST /api/v1/students/sessions`
- `GET /api/v1/counsellors/dashboard`
- `GET /api/v1/counsellors/me`
- `PUT /api/v1/counsellors/me`
- `GET /api/v1/counsellors/sessions`
- `PATCH /api/v1/counsellors/sessions/{session_id}`
- `POST /api/v1/chatbot/message`
- `POST /api/v1/recommendations/careers`
- `POST /api/v1/recommendations/skill-gap`
- `POST /api/v1/recommendations/colleges`
- `POST /api/v1/recommendations/roadmaps`
- `GET /api/v1/recommendations/roadmaps`
- `GET /api/v1/admin/dashboard`
- `GET /api/v1/admin/users`
- `PATCH /api/v1/admin/users/{user_id}/active`

AI service:

- `GET /health`
- `POST /chatbot/chat`
- `POST /recommendations/careers`
- `POST /recommendations/skill-gap`
- `POST /recommendations/colleges`
- `POST /roadmaps/generate`

## File-by-File Documentation

### Backend Core

- `backend/app/main.py`: Creates the FastAPI app, registers middleware and routers, creates database tables.
- `backend/app/core/config.py`: Loads `.env` values and exposes app settings.
- `backend/app/core/database.py`: Builds the SQLAlchemy engine, session factory, and base model class.
- `backend/app/core/security.py`: Handles password hashing, password verification, JWT creation, and JWT decoding.
- `backend/app/core/logging.py`: Configures backend logging.

### Backend Routes

- `auth.py`: Register, login, Swagger token endpoint, and current-user endpoint.
- `students.py`: Student profile, dashboard, and session booking.
- `counsellors.py`: Counsellor profile, dashboard, session list, and session status update.
- `chatbot.py`: Protected chatbot API route.
- `recommendations.py`: Career recommendation, skill gap, college prediction, and roadmap APIs.
- `admin.py`: Admin statistics, user list, and user activation control.

### Backend Models

- `User`: Login account with role and active status.
- `StudentProfile`: Student academic profile, interests, skills, goals, and preferences.
- `CounsellorProfile`: Counsellor specialization, bio, experience, rating, and availability.
- `College`: College catalog model for future database-backed prediction.
- `GuidanceSession`: Session booking between student and counsellor.
- `CareerRoadmap`: Saved AI-generated roadmap for a student.

### Backend Schemas

- `auth.py`: Register/login/token/user response schemas.
- `student.py`: Student profile, dashboard, session booking, and session response schemas.
- `counsellor.py`: Counsellor profile and dashboard schemas.
- `chatbot.py`: Chatbot request and response schemas.
- `recommendation.py`: Career, skill gap, college, roadmap, and saved roadmap schemas.

### Backend Services

- `AuthService`: Registers users, creates profiles, authenticates users, builds JWT responses.
- `StudentService`: Creates/updates student profiles, returns dashboards, books sessions.
- `CounsellorService`: Creates/updates counsellor profiles and manages counsellor sessions.
- `AdminService`: Returns platform statistics and user records.
- `ChatbotService`: Calls the AI service chatbot and provides fallback replies.
- `RecommendationService`: Calls AI recommendation endpoints and provides fallback guidance.
- `RoadmapService`: Calls AI roadmap endpoint and saves generated roadmaps.
- `AIServiceClient`: Sends JSON requests from backend to the AI service.

### Backend Utils

- `helpers.py`: Shared date and comma-separated text helpers.
- `validators.py`: Ownership and role helper validation.
- `email.py`: Email queue placeholder ready for provider integration.

### AI Service

- `ai_service/app/main.py`: AI FastAPI app and AI endpoints.
- `models/schemas.py`: AI request and response schemas.
- `recommender/engine.py`: Deterministic career recommendation engine.
- `pipelines/skill_gap.py`: Skill gap analysis logic.
- `pipelines/college_prediction.py`: College prediction logic.
- `roadmap/generator.py`: Career roadmap generator.
- `chatbot/bot.py`: AI chatbot response logic.
- `embeddings/pipeline.py`: Deterministic local embedding helper for future semantic search.

### Frontend Components

- `components/theme.py`: Dark AI dashboard colors and common styles.
- `components/navigation.py`: Top navigation bar and links.
- `components/layout.py`: Page shell and page headers.
- `components/cards.py`: Metric cards and feature cards.
- `components/forms.py`: Reusable inputs, text areas, and buttons.
- `components/chatbot.py`: Chatbot panel component.
- `components/roadmap.py`: Roadmap stage card component.

### Frontend State Classes

- `AuthState`: Login, register, load user, logout, JWT storage.
- `StudentState`: Student dashboard and profile update state.
- `CounsellorState`: Counsellor dashboard and profile update state.
- `AdminState`: Admin metrics and user list state.
- `ChatbotState`: Chatbot message and response state.
- `RecommendationState`: Recommendations, skill gap, college prediction, and roadmap state.

### Frontend Pages

- `landing.py`: Landing page.
- `login.py`: Login page.
- `register.py`: Register page.
- `student_dashboard.py`: Student dashboard.
- `counsellor_dashboard.py`: Counsellor dashboard.
- `admin_dashboard.py`: Admin dashboard.
- `chatbot.py`: AI chatbot page.
- `roadmap.py`: Career roadmap page.
- `recommendations.py`: Recommendation page.

## How The Services Integrate

1. User opens Reflex frontend.
2. Frontend state calls FastAPI backend using `BACKEND_API_URL`.
3. Backend validates JWT and role permissions.
4. Backend calls AI service using `AI_SERVICE_URL`.
5. AI service returns recommendations, chat replies, skill gaps, colleges, or roadmaps.
6. Backend returns clean response models to the frontend.

## Deployment Guide

The easiest production path is a Docker-based platform with managed PostgreSQL.

### Recommended Beginner Platform: Railway

Railway supports Dockerfile-based deployments. Each service should point to its own Dockerfile:

- Backend service: `backend/Dockerfile`
- AI service: `ai_service/Dockerfile`
- Frontend service: `frontend/Dockerfile`
- Database service: PostgreSQL

Set environment variables:

Backend:

```text
DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DB
AI_SERVICE_URL=https://YOUR_AI_SERVICE_URL
SECRET_KEY=make-a-long-random-secret
BACKEND_CORS_ORIGINS=https://YOUR_FRONTEND_URL
```

Frontend:

```text
BACKEND_API_URL=https://YOUR_BACKEND_URL/api/v1
```

### Fly.io Option

Fly.io also supports Dockerfile deployment. Deploy backend, AI service, and frontend as separate apps, then connect them using environment variables.

### Simple Deployment Checklist

1. Push this project to GitHub.
2. Create PostgreSQL database on your platform.
3. Create backend service from `backend/Dockerfile`.
4. Create AI service from `ai_service/Dockerfile`.
5. Create frontend service from `frontend/Dockerfile`.
6. Add environment variables.
7. Deploy AI service first.
8. Deploy backend second.
9. Deploy frontend last.
10. Open frontend public URL and register your first admin account.

## Important Security Notes

- Replace `SECRET_KEY` before deployment.
- Do not commit real `.env` secrets.
- Use PostgreSQL in production.
- Add email verification before real public launch.
- Add payments, rate limiting, audit logs, and monitoring before charging users.

## Current Status

This is a runnable startup-grade foundation. It includes real authentication, roles, APIs, Reflex screens, AI-service integration, Docker files, and beginner-friendly run instructions.
