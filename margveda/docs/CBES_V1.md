# CareerBrownie Engineering Specification (CBES)
## Volume 1 — AI Architecture
### Version 1.0 | 2026-07-06

---

## 1. Vision

CareerBrownie is an **AI-Native Career Counselling Platform**.

It combines AI, Human Counsellors, Admission Guidance, Knowledge Graph, Recommendation Engine,
CRM, and Marketing Automation into one platform.

**Objective:** Help every student make the right education and career decision using AI.

---

## 2. Core Philosophy

CareerBrownie is NOT:
- ❌ ChatGPT Wrapper
- ❌ College Listing Website
- ❌ CRM
- ❌ LMS

CareerBrownie IS:
- ✅ AI Operating System for Education

Everything revolves around one central intelligence.

---

## 3. CareerBrain

```
CareerBrain
```

CareerBrain is the central AI orchestrator. It controls:
- AI Counsellor
- Marketing
- Research
- CRM
- Booking
- Analytics
- Founder Assistant
- Knowledge Base

**CareerBrain is NOT an LLM.** It is an orchestrator.

---

## 4. Core Architecture

```
Frontend (Next.js)
        │
Backend (Django)
        │
AI Gateway
        │
CareerBrain
        │
RAG Engine
        │
Knowledge Base
        │
PostgreSQL  |  ChromaDB/Qdrant  |  Redis
        │
Automation (n8n)
        │
Monitoring (Grafana + Prometheus)
        │
Deployment (Docker + Railway + Cloudflare)
```

---

## 5. AI Gateway

CareerBrain never talks directly to models. Instead:

```
CareerBrain → AI Gateway → Ollama (Qwen) → Response
                         → Anthropic (Claude) [fallback]
                         → Rule-based [fallback]
```

**Why:** Any provider (DeepSeek, Llama, Mistral, Gemma) can be swapped
without changing business logic.

---

## 6. Memory System

| Type       | Storage    | Scope                                      |
|------------|------------|--------------------------------------------|
| Short-term | Redis      | Conversation turns (session-scoped)        |
| Long-term  | PostgreSQL | Student profile, history, goals, style     |

---

## 7. Knowledge Sources (RAG Domains)

Career Database, Course Database, College Database, Scholarships, Exams,
Government Notifications, Blogs, Career Roadmaps, Admission Rules, Cutoffs,
Placements, Salary Data, FAQs, Government Jobs.

All indexed inside ChromaDB (Vector Store via FastAPI ai_service microservice).

---

## 8. Retrieval Pipeline

```
Student Question
      ↓
Intent Detection
      ↓
Query Rewrite
      ↓
Hybrid Search (ChromaDB)
      ↓
Re-Ranking
      ↓
Context Compression
      ↓
Prompt Builder
      ↓
LLM (via AI Gateway)
      ↓
Answer + Citations
      ↓
Memory Update
```

---

## 9. Agent Framework

Every agent has:
- **Goal** — what it exists to accomplish
- **Tools** — what it can invoke
- **Memory** — its memory scope
- **Permissions** — what data it can access
- **Knowledge** — which RAG domains it queries
- **Output** — standardized AgentResult

No duplicated logic between agents.

---

## 10. AI Agents (16 Total)

| Agent            | Purpose                                      |
|------------------|----------------------------------------------|
| CareerAgent      | Career guidance, exams, colleges             |
| CRMAgent         | Lead management, student follow-up           |
| BookingAgent     | Session scheduling, calendar management      |
| MarketingAgent   | Campaign automation, email sequences         |
| ResearchAgent    | Web research, data gathering                 |
| SEOAgent         | Content optimization, keyword research       |
| AnalyticsAgent   | Platform metrics, student insights           |
| FounderAssistant | Founder-facing queries and reports           |
| ScholarshipAgent | Scholarship discovery and matching           |
| CollegeAgent     | College comparison, cutoffs, admissions      |
| AdmissionAgent   | Application strategy, SOP assistance         |
| ResumeAgent      | Resume review and improvement                |
| InterviewAgent   | Mock interview preparation                   |
| ParentAgent      | Parent-specific guidance and communication   |
| NotificationAgent| Push notifications, reminders                |
| KnowledgeAgent   | Knowledge base management and updates        |

---

## 11. Shared Services

Every agent uses — and NEVER owns:
- Authentication
- Authorization
- Logging
- Memory
- RAG
- Prompt Templates
- Analytics
- Database
- Notifications
- Payments
- Scheduling

---

## 12. Folder Structure

```
backend_django/
└── apps/
    └── ai/
        ├── careerbrain/      # Main orchestrator
        ├── gateway/          # LLM provider abstraction
        ├── agents/           # All 16 agents
        │   ├── career/
        │   ├── crm/
        │   ├── booking/
        │   └── ...
        ├── memory/           # Short-term (Redis) + Long-term (PG)
        ├── rag/              # RAG client → FastAPI ai_service
        ├── prompts/          # Prompt templates (no hardcoded prompts)
        ├── tools/            # Tool base class
        └── services/         # Shared services container
```

---

## 13. Coding Standards

Every module must:
- Use Clean Architecture
- Repository Pattern
- Service Layer
- Type Hints throughout
- Unit Tests
- Integration Tests
- No duplicated logic
- No hardcoded values
- No secrets in code

---

## 14. Development Rules

Claude Code must:
- Inspect project, reuse existing code
- Never rewrite working modules
- Keep changes isolated
- Write migrations for DB changes
- Write tests
- Keep APIs, frontend, backend, Docker in sync

---

## Volume Roadmap

| Vol | Title                          | Status      |
|-----|-------------------------------|-------------|
| 1   | AI Architecture               | ✅ Implemented |
| 2   | Database Design               | Pending     |
| 3   | Knowledge Base Architecture   | Pending     |
| 4   | RAG Pipeline (detailed)       | Pending     |
| 5   | Career Agent                  | Pending     |
| 6   | CRM Agent                     | Pending     |
| 7   | Booking Agent                 | Pending     |
| 8   | Marketing Agent               | Pending     |
| 9   | Research Agent                | Pending     |
| 10  | Analytics Agent               | Pending     |
| 11  | Founder Assistant             | Pending     |
| 12  | Frontend Architecture         | Pending     |
| 13  | Authentication & RBAC         | Pending     |
| 14  | Payments & Subscriptions      | Pending     |
| 15  | n8n Automation                | Pending     |
| 16  | Railway Deployment            | Pending     |
| 17  | Security                      | Pending     |
| 18  | Testing & QA                  | Pending     |
| 19  | Monitoring & Observability    | Pending     |
| 20  | Scaling & Multi-Tenant SaaS   | Pending     |
