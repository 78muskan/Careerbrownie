# MargVedA — Quick Start Guide

## Start Both Servers

**Frontend (Next.js):**
```powershell
cd "d:\Margveda final\margveda\frontend-next"
npm run dev
```
Opens at: http://localhost:3000

**Backend (Django):**
```powershell
cd "d:\Margveda final\margveda\backend_django"
python manage.py runserver
```
Opens at: http://localhost:8000
Admin panel: http://localhost:8000/admin/
- Email: admin@margveda.com
- Password: Admin@1234

---

## Phase 1 — Marketing Website

### Pages
| URL | Description |
|-----|-------------|
| / | Landing page (10 sections) |
| /about | About MargVedA |
| /services | All services |
| /services/career-counselling | Career Counselling |
| /services/university-admissions | University Admissions |
| /services/study-abroad | Study Abroad |
| /services/career-intelligence | Career Intelligence |
| /services/ai-career-guidance | AI Career Guidance |
| /book-consultation | Book free session |
| /contact | Contact form |
| /blog | Blog listing |
| /blog/[slug] | Blog post detail |
| /faq | FAQ |
| /privacy-policy | Privacy Policy |
| /terms-conditions | Terms & Conditions |
| /refund-policy | Refund Policy |
| /sitemap.xml | Auto-generated sitemap |
| /robots.txt | Auto-generated robots |

### Marketing API Endpoints
| Method | URL | Description |
|--------|-----|-------------|
| POST | /api/v1/leads/contact/ | Contact form |
| POST | /api/v1/leads/consultation/ | Book consultation |
| POST | /api/v1/leads/newsletter/ | Newsletter signup |
| GET | /api/v1/blog/ | Blog posts |
| GET | /api/v1/counsellors/ | Counsellors |
| GET | /api/v1/health/ | Health check |

---

## Phase 2 — Platform MVP

### Auth Pages
| URL | Description |
|-----|-------------|
| /login | Sign in |
| /register | Create account |
| /forgot-password | Request password reset |
| /reset-password?token=XXX | Set new password |
| /verify-email?token=XXX | Verify email |

### Student Dashboard
| URL | Description |
|-----|-------------|
| /student/dashboard | Main dashboard |
| /student/profile | View profile |
| /student/profile/build | Multi-step profile builder |
| /student/sessions | My sessions |
| /student/goals | Career goals |

### Counsellor Dashboard
| URL | Description |
|-----|-------------|
| /counsellor/dashboard | Sessions overview |

### Admin Dashboard
| URL | Description |
|-----|-------------|
| /admin/dashboard | Admin overview (links to Django admin) |

### Phase 2 Auth API
| Method | URL | Description |
|--------|-----|-------------|
| POST | /api/v1/auth/register/ | Register new user |
| POST | /api/v1/auth/login/ | Login, get JWT tokens |
| POST | /api/v1/auth/logout/ | Logout (blacklist refresh token) |
| GET/PATCH | /api/v1/auth/me/ | Get/update current user |
| POST | /api/v1/auth/token/refresh/ | Refresh access token |
| GET | /api/v1/auth/verify-email/?token=X | Verify email |
| POST | /api/v1/auth/resend-verification/ | Resend verification email |
| POST | /api/v1/auth/forgot-password/ | Send password reset email |
| POST | /api/v1/auth/reset-password/ | Reset password with token |
| POST | /api/v1/auth/change-password/ | Change password (authenticated) |
| POST | /api/v1/auth/google/ | Google OAuth login |

### Student Profile API
| Method | URL | Description |
|--------|-----|-------------|
| GET/PATCH | /api/v1/student/profile/ | Get/update student profile |
| GET | /api/v1/student/dashboard/ | Dashboard data aggregate |
| GET/POST | /api/v1/student/goals/ | List/create goals |
| PATCH/DELETE | /api/v1/student/goals/<id>/ | Update/delete goal |

### Sessions API
| Method | URL | Description |
|--------|-----|-------------|
| POST | /api/v1/sessions/book/ | Book a session |
| GET | /api/v1/sessions/my/ | Student's sessions |
| GET/PATCH | /api/v1/sessions/<uuid>/ | Session detail/update |
| GET | /api/v1/sessions/counsellor/ | Counsellor's sessions |
| PATCH | /api/v1/sessions/counsellor/<uuid>/ | Counsellor update session |

### Notifications API
| Method | URL | Description |
|--------|-----|-------------|
| GET | /api/v1/notifications/ | List notifications |
| POST | /api/v1/notifications/mark-read/ | Mark as read |

---

## Test Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@margveda.com | Admin@1234 |

To create a test student:
```
POST /api/v1/auth/register/
{
  "email": "student@test.com",
  "full_name": "Test Student",
  "password": "Test@1234",
  "role": "student"
}
```

---

---

## Phase 3 — AI Career Intelligence

### AI API Endpoints
| Method | URL | Description |
|--------|-----|-------------|
| GET | /api/v1/ai/assessment/{type}/questions/ | Get questions (interest/personality/aptitude/readiness) |
| POST | /api/v1/ai/assessment/{type}/submit/ | Submit responses, get scored results |
| GET | /api/v1/ai/assessment/{type}/result/ | Get a specific result |
| GET | /api/v1/ai/assessment/results/ | List all completed assessments |
| GET | /api/v1/ai/roadmap/ | Get career roadmap |
| POST | /api/v1/ai/roadmap/ | Generate roadmap for target career |
| GET | /api/v1/ai/advisor/ | AI advisor: career matches, gaps, trends, resources |
| GET | /api/v1/ai/careers/ | Career database list |
| GET | /api/v1/ai/careers/{key}/ | Career detail with skill gaps |

### AI Frontend Pages
| URL | Description |
|-----|-------------|
| /student/assessment | Assessment hub — 4 assessment types |
| /student/assessment/interest | RIASEC interest assessment |
| /student/assessment/personality | Big 5 personality assessment |
| /student/assessment/aptitude | Numerical/verbal/logical aptitude |
| /student/assessment/readiness | Career readiness check |
| /student/ai-advisor | AI career advisor — matches, gaps, trends, resources |
| /student/career-roadmap | Career roadmap generator — 3M/6M/1Y/3Y/5Y plans |

---

## Phase 4 — Counsellor Management System

### Counsellor Portal API
| Method | URL | Description |
|--------|-----|-------------|
| GET/PATCH | /api/v1/portal/profile/ | Counsellor profile |
| GET/POST | /api/v1/portal/slots/ | Availability time slots |
| PATCH/DELETE | /api/v1/portal/slots/{id}/ | Update/delete slot |
| GET | /api/v1/portal/calendar/ | Calendar view (filter by from/to date) |
| GET/PATCH | /api/v1/portal/appointments/{id}/ | Appointment detail/update |
| GET/POST | /api/v1/portal/appointments/{id}/notes/ | Session notes |
| GET | /api/v1/portal/reports/ | Revenue and session reports |
| POST | /api/v1/portal/booking/ | Student books appointment |
| GET | /api/v1/portal/booking/counsellors/ | Public counsellor list |
| GET | /api/v1/portal/booking/counsellors/{id}/ | Counsellor detail + slots |

### Counsellor Frontend Pages
| URL | Description |
|-----|-------------|
| /counsellor/dashboard | Sessions overview + stats |
| /counsellor/profile | Edit counsellor profile |
| /counsellor/availability | Manage weekly time slots |
| /counsellor/sessions/{id} | Session detail + notes |
| /counsellor/reports | Revenue + session analytics |

---

## Phase 5 — Employability Platform

### Resume & Interview API
| Method | URL | Description |
|--------|-----|-------------|
| GET | /api/v1/resume/ | List student's resumes |
| POST | /api/v1/resume/ | Create resume |
| GET/PATCH/DELETE | /api/v1/resume/{id}/ | Resume detail |
| POST | /api/v1/resume/{id}/sections/ | Add section |
| PATCH/DELETE | /api/v1/resume/{id}/sections/{sid}/ | Update/delete section |
| POST | /api/v1/resume/{id}/ats/ | Run ATS analysis |
| GET | /api/v1/resume/{id}/ats/ | Get past ATS analyses |
| GET | /api/v1/resume/templates/ | List resume templates |
| GET | /api/v1/interview/questions/?type=hr&domain=tech | Get interview questions |
| GET/POST | /api/v1/interview/sessions/ | List / create interview session |
| GET/POST/PATCH | /api/v1/interview/sessions/{id}/ | Session detail + submit answer |
| GET | /api/v1/interview/stats/ | Interview performance stats |

### Phase 5 Frontend Pages
| URL | Description |
|-----|-------------|
| /student/resume | Resume hub — list + manage resumes |
| /student/resume/builder?id=X | Resume builder — sections, personal info, summary |
| /student/resume/ats?id=X | ATS analyser — score, keywords, suggestions |
| /student/interview | Interview coach hub — type selector + stats |
| /student/interview/hr | HR interview practice |
| /student/interview/behavioural | Behavioural (STAR method) practice |
| /student/interview/technical | Technical interview (by domain) |
| /student/interview/mock | Full mock interview |
| /student/skill-gap | Skill gap analyser — career vs current skills |

---

## Phase 6 — University Consulting System

### University & College Predictor API
| Method | URL | Description |
|--------|-----|-------------|
| GET | /api/v1/universities/ | University list (filter: type, country, q) |
| GET | /api/v1/universities/{slug}/ | University detail + suggested programs |
| GET | /api/v1/universities/programs/list/ | Program list (filter: level, domain) |
| GET | /api/v1/universities/scholarships/ | Scholarship list |
| GET | /api/v1/universities/scholarships/match/ | Personalised scholarship matches |
| GET/POST | /api/v1/universities/scholarships/my-applications/ | Track scholarship applications |
| GET | /api/v1/universities/scholarships/{slug}/ | Scholarship detail |
| GET | /api/v1/universities/cutoffs/ | Exam cutoff data |
| POST | /api/v1/predictor/predict/ | College predictor — input score, get matches |
| GET | /api/v1/predictor/exams/ | Supported exams list |
| GET | /api/v1/predictor/my-predictions/ | Past predictions |

### Phase 6 Frontend Pages
| URL | Description |
|-----|-------------|
| /universities | University explorer — search, filter, compare |
| /universities/{slug} | University detail page |
| /student/college-predictor | College predictor — enter score, see matches |
| /student/scholarships | Scholarship finder + save tracker |

---

## Phase 7 — School Ecosystem

### School API Endpoints
| Method | URL | Description |
|--------|-----|-------------|
| GET | /api/v1/school/dashboard/ | School admin dashboard |
| GET/POST | /api/v1/school/batches/ | List/create batches |
| GET/PATCH/DELETE | /api/v1/school/batches/{id}/ | Batch detail |
| POST/DELETE | /api/v1/school/batches/{id}/students/ | Add/remove students |
| GET | /api/v1/school/analytics/ | Student analytics across school |
| GET/POST | /api/v1/school/reports/ | School reports |
| GET/POST | /api/v1/school/parents/ | Parent portal |

### Phase 7 Frontend Pages
| URL | Description |
|-----|-------------|
| /school/dashboard | School admin dashboard |
| /school/batches | Batch management |
| /school/analytics | Student analytics |
| /school/reports | Career and assessment reports |

---

## Phase 8 — Recruiter & Placement Platform

### Recruiter / Jobs API
| Method | URL | Description |
|--------|-----|-------------|
| GET | /api/v1/jobs/jobs/ | Public job + internship board |
| GET | /api/v1/jobs/jobs/{id}/ | Job detail |
| GET | /api/v1/jobs/recruiter/dashboard/ | Recruiter dashboard |
| GET/POST | /api/v1/jobs/recruiter/jobs/ | Manage job postings |
| PATCH/DELETE | /api/v1/jobs/recruiter/jobs/{id}/ | Update/close job |
| GET/POST | /api/v1/jobs/recruiter/internships/ | Manage internships |
| GET | /api/v1/jobs/recruiter/candidates/ | Candidate search |
| GET/POST | /api/v1/jobs/applications/ | Student applications |
| PATCH | /api/v1/jobs/applications/{id}/ | Update status |
| GET | /api/v1/jobs/placement-readiness/ | Student placement score |
| GET | /api/v1/jobs/my-matches/ | Personalised job matches |

### Phase 8 Frontend Pages
| URL | Description |
|-----|-------------|
| /jobs | Public job board |
| /student/jobs | Personalised job matches |
| /student/applications | Application tracker |
| /student/placement | AI Placement Predictor |
| /recruiter/dashboard | Recruiter portal |
| /recruiter/candidates | Candidate search |

---

## Phase 9 — Enterprise & Advanced AI

### Enterprise / AI API
| Method | URL | Description |
|--------|-----|-------------|
| GET/POST | /api/v1/enterprise/clients/ | Enterprise clients (admin) |
| GET | /api/v1/enterprise/stats/ | Platform-wide stats (admin) |
| GET/POST | /api/v1/enterprise/ai-twin/ | AI Career Twin session |
| GET | /api/v1/enterprise/video-interview/questions/ | AI Video Interview questions |
| GET/POST | /api/v1/enterprise/placement-predictor/ | AI Placement Predictor |

### Phase 9 Frontend Pages
| URL | Description |
|-----|-------------|
| /student/ai-twin | AI Career Twin — personalised intelligence |
| /student/placement | AI Placement Predictor + company matches |
| /enterprise | Enterprise landing page + pricing |

---

## Google OAuth Setup (Phase 2)
1. Go to https://console.cloud.google.com/
2. Create OAuth 2.0 credentials
3. Set redirect URI: `http://localhost:3000/auth/google/callback`
4. Add to `.env`: `GOOGLE_CLIENT_ID=...` and `GOOGLE_CLIENT_SECRET=...`
5. In Django admin → Social Applications → Add Google app
