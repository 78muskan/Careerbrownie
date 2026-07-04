"""Government jobs & public sector career knowledge base for India.

Covers: UPSC, SSC, Banking, Defence, Railways, Teaching, Insurance, State PSC.
Data sourced from official websites, DOPT reports, UPSC annual reports (2024-25).
"""
from __future__ import annotations

GOVT_JOB_PROFILES = [
    # ── UPSC Civil Services ────────────────────────────────────────────────────
    {
        "id": "upsc_civil_services",
        "title": "UPSC Civil Services (IAS / IPS / IFS)",
        "domain": "govt_jobs",
        "content": """
UPSC Civil Services Examination is India's most prestigious and competitive exam.

**Services offered**: IAS (Indian Administrative Service), IPS (Indian Police Service),
IFS (Indian Foreign Service), IRS (Revenue), and 20+ other Group A & B central services.

**Eligibility**: Graduate in any stream | Age: 21–32 years (General); relaxed for SC/ST/OBC/PwD
**Attempts**: General - 6 attempts; OBC - 9 attempts; SC/ST - unlimited till age limit

**Three-stage selection process**:
1. Prelims (GS Paper 1 + CSAT) — qualifying, objective
2. Mains (9 descriptive papers: GS1-4, Essay, Optional subject ×2, Language papers)
3. Personality Test (Interview) — 275 marks

**Vacancies**: ~1,000–1,100 total annually; IAS ~180, IPS ~200, IFS ~30 approx.

**Salary (7th Pay Commission)**:
- IAS/IPS starting: ₹56,100/month + DA + HRA + perks (worth ₹1.5–2L/month effective)
- Cabinet Secretary (top IAS): ₹2.5 lakh/month
- With allowances + perks + subsidised housing: effective CTC ₹30–40 LPA entry-level

**Preparation time**: 12–24 months dedicated; most toppers prepare for 2–3 years.

**Key resources**: NCERT books (6–12), The Hindu, Laxmikanth Polity, Bipin Chandra History,
Ramesh Singh Economy, Majid Husain Geography, Vision IAS/ForumIAS test series.

**Coaching**: Optional but helpful. Delhi coaching hubs: Old Rajinder Nagar, Mukherjee Nagar.
Online alternatives: Unacademy IAS, StudyIQ, InsightIAS (free content available).

**Reality check**: Selection rate ~0.1–0.2%. Requires 8–10 hours/day sustained study.
Most successful candidates have engineering/science backgrounds but arts students equally succeed.
""",
    },

    # ── SSC CGL ───────────────────────────────────────────────────────────────
    {
        "id": "ssc_cgl",
        "title": "SSC CGL (Staff Selection Commission – Combined Graduate Level)",
        "domain": "govt_jobs",
        "content": """
SSC CGL is the most popular government exam for graduates seeking Group B and C central government jobs.

**Posts offered**: Income Tax Inspector, Excise Inspector, Assistant Section Officer (MEA, CSS),
Statistical Investigator, Auditor, Accountant, Sub-Inspector (CBI/NIA), Tax Assistant, UDC.

**Eligibility**: Graduate in any stream | Age: 18–32 years (varies by post)
**Posts**: ~10,000–20,000 vacancies annually

**Selection process**:
1. Tier 1: 200 marks CBT — General Intelligence, GK, Quantitative Aptitude, English
2. Tier 2: 300 marks CBT — Maths/Reasoning/English (compulsory) + module papers by post
3. Document verification and medical

**Salary**:
- Grade Pay 4200: ₹29,200–92,300 (Income Tax Inspector, Excise Inspector)
- Grade Pay 4600: ₹35,400–1,12,400 (Assistant Section Officer)
- After 7th Pay: effective in-hand ₹45,000–75,000/month with DA+HRA+TA

**Preparation**: 4–8 months. Focus on: Quantitative Aptitude (CAT-level), Reasoning, English.
Books: Rakesh Yadav Maths, R.S. Aggarwal, Wren & Martin.

**Posting**: Pan-India; many posts in Delhi/metro cities. Transfers are part of the job.

**Best suited for**: Commerce/Science graduates wanting stable income, perks, and pension.
SSC CGL Inspector posts are among the best non-UPSC government jobs available.
""",
    },

    # ── Banking (IBPS PO) ──────────────────────────────────────────────────────
    {
        "id": "ibps_po",
        "title": "IBPS PO / SBI PO (Bank Probationary Officer)",
        "domain": "govt_jobs",
        "content": """
Bank PO (Probationary Officer) is one of the most sought-after government jobs in India,
combining job security with competitive salary and rapid promotion track.

**Conducting bodies**:
- IBPS PO: Institute of Banking Personnel Selection — for 11 public sector banks
  (Punjab National Bank, Bank of Baroda, Canara Bank, Union Bank, etc.)
- SBI PO: State Bank of India conducts its own exam separately

**Vacancies**: IBPS PO ~3,000–5,000/year; SBI PO ~2,000/year

**Eligibility**: Graduate in any stream | Age: 20–30 years
**Exam pattern**:
1. Prelims: English Language (30), Quantitative Aptitude (35), Reasoning Ability (35) — 60 min
2. Mains: Reasoning+Computer (45), General/Economy/Banking (40), English (35), Data Analysis (35)
   + Descriptive Paper (English Letter/Essay)
3. Interview (SBI PO) / Group Discussion + Interview (IBPS)

**Salary (after 11th Bipartite Settlement)**:
- Starting basic: ₹41,960/month
- Gross with HRA+DA+other: ₹62,000–72,000/month in metros
- After 2–3 promotions (5–7 years): Deputy Manager/Branch Manager ₹85,000–1.2L/month

**Career growth**: PO → Assistant Manager → Deputy Manager → Branch Manager → Chief Manager
Scale 1 to Scale 7 promotions based on performance + JAIIB/CAIIB certifications.

**Preparation**: 3–6 months. Quantitative Aptitude (speed math), Reasoning, English grammar.
Platforms: Oliveboard, Testbook, Adda247 for mock tests.

**RBI Grade B**: Separate prestigious exam by RBI. Higher salary (₹1.17L/month gross),
requires 2 years of experience or postgraduate degree. Covers Economics + Finance deeply.
""",
    },

    # ── NDA ───────────────────────────────────────────────────────────────────
    {
        "id": "nda_exam",
        "title": "NDA (National Defence Academy) — Army / Navy / Air Force Officer",
        "domain": "govt_jobs",
        "content": """
NDA is the gateway to becoming an officer in the Indian Army, Navy, or Air Force after Class 12.
It is among the most prestigious career paths in India — combining national service, adventure,
leadership, and excellent compensation.

**Conducting body**: Union Public Service Commission (UPSC)
**Eligibility**: Male and female candidates | Class 12 passed/appearing
  - Army: Any stream (PCM preferred)
  - Navy & Air Force: Class 12 PCM mandatory

**Age**: 16.5–19.5 years at time of commencement of course

**Selection process**:
1. Written exam: Maths (300 marks) + General Ability Test (600 marks) = 900 total
2. SSB (Services Selection Board): 5-day psychological + physical assessment in Bangalore/Bhopal/Allahabad
3. Medical examination

**Training**: 3-year NDA training in Pune (joint), then 1-year service academy training.

**Post-NDA career**:
- Lieutenant (entry) → Captain → Major → Colonel → Brigadier → Major General → Lieutenant General → General
- Navy: Sub-Lieutenant → Lieutenant → Lieutenant Commander → Commander → Captain → Rear Admiral → Admiral

**Salary**:
- Lieutenant: ₹56,100–1,77,500 + MSP ₹15,500 + allowances = ₹80,000–1.1L/month effective
- Colonel: ₹1,30,600 + allowances = ₹2.5–3L/month
- Risk & Hardship allowance, free housing, medical coverage for family, 60 days annual leave.

**Perks beyond salary**: Subsidised canteen (CSD), low-cost housing (military colonies),
free schooling for children at Kendriya Vidyalayas, golf/sports club memberships, resorts.

**CDS (Combined Defence Services)**: For graduates (22–27 years). Entry as Lieutenant directly
without NDA training. Conducted by UPSC twice yearly. IMA Dehradun, OTA Chennai, Naval Academy Goa.

**AFCAT (Air Force Common Admission Test)**: Entry to Air Force for graduates as Flying Officer.
Includes Flying Branch (pilot), Ground Duty Technical, and Administrative branches.
""",
    },

    # ── Railways ──────────────────────────────────────────────────────────────
    {
        "id": "rrb_ntpc",
        "title": "RRB NTPC / RRB Group D (Indian Railways)",
        "domain": "govt_jobs",
        "content": """
Indian Railways is the world's fourth-largest railway network and one of India's biggest employers.
RRB (Railway Recruitment Board) conducts multiple exams for different levels.

**RRB NTPC (Non-Technical Popular Categories)**:
Posts: Station Master, Junior Account Assistant, Commercial Clerk, Traffic Assistant, Goods Guard
Eligibility: Graduate or 12th pass (depending on post) | Age: 18–33 years
Vacancies: 35,000+ in large recruitment cycles

**RRB Group D**:
Posts: Helper, Porter, Track Maintainer, Gateman, Assistant Pointsman
Eligibility: 10th pass (Matric) + ITI Certificate | Age: 18–36 years
Vacancies: 1,00,000+ in mega recruitment drives

**Selection Process (NTPC)**:
1. CBT Stage 1: 100 questions — General Awareness (40), Maths (30), General Intelligence (30)
2. CBT Stage 2: 120 questions — subject-specific based on post
3. Typing Test (for clerical posts) or Skill Test
4. Document Verification

**Salary**:
- RRB NTPC Graduate Posts: ₹35,400–1,12,400 (Level 6)
- RRB NTPC 12th Pass: ₹19,900–63,200 (Level 3)
- RRB Group D: ₹18,000–56,900 (Level 1)
- After 7th CPC: effective take-home ₹32,000–55,000/month with allowances

**Perks**: Free travel passes (self + family), medical benefits, subsidised housing,
Privilege Leave, railway township facilities.

**Best suited for**: Candidates from smaller towns, ITI graduates, those wanting
posting near home state (Railway zones are region-specific).
""",
    },

    # ── Teaching (CTET / UGC NET) ─────────────────────────────────────────────
    {
        "id": "teaching_career",
        "title": "Teaching Career — CTET, UGC NET, TGT/PGT, Professor",
        "domain": "govt_jobs",
        "content": """
Teaching is a respected and stable government career in India with multiple pathways
from primary school to university professor.

**Pathways by level**:

**Primary Teacher (PRT)**:
Qualification: D.El.Ed (Diploma in Elementary Education) or B.Ed | Pass CTET Paper 1 or State TET
Salary: ₹28,000–60,000/month (government school, 7th CPC)

**Trained Graduate Teacher (TGT) — Classes 6-10**:
Qualification: Bachelor's in relevant subject + B.Ed | Pass CTET Paper 2 or State TET
Salary: ₹35,400–67,000/month (Central Government schools / KVS / NVS)

**Post Graduate Teacher (PGT) — Classes 11-12**:
Qualification: Master's in relevant subject + B.Ed
Salary: ₹44,900–1,42,400/month (KVS/NVS) + DA + HRA + academic grade pay

**KVS (Kendriya Vidyalaya Sangathan)**: Most prestigious teaching service; pan-India postings,
national curriculum, excellent salary, DCRG pension. Exams: KVS PRT/TGT/PGT (direct recruitment).

**NVS (Navodaya Vidyalaya Samiti)**: Residential schools for rural students. Similar pay to KVS.

**UGC NET (National Eligibility Test)**:
- Qualifying exam for Assistant Professor in Indian colleges and universities
- Also awards JRF (Junior Research Fellowship) for PhD funding: ₹31,000–35,000/month stipend
- Eligibility: Master's degree with 55% marks | Conducted by NTA
- Assistant Professor salary: ₹57,700–1,82,400/month (7th Pay + Academic Grade Pay ₹6,000)

**Professor career path**: Asst. Professor → Associate Professor → Professor → Dean → Vice Chancellor
Top IIT/IIM professor salary: ₹1.5–2.5 lakh/month

**Why choose teaching**: Job security, 2-month vacation annually, national pension scheme,
high social respect, intellectual fulfilment, housing allowance.
""",
    },

    # ── State PSC ─────────────────────────────────────────────────────────────
    {
        "id": "state_psc",
        "title": "State PSC (Public Service Commission) Exams — State Civil Services",
        "domain": "govt_jobs",
        "content": """
Every Indian state has its own Public Service Commission that recruits state-level civil servants —
State Administrative Service (SAS), State Police Service (SPS), and dozens of departmental services.

**Major State PSCs and their equivalents**:
- MPSC (Maharashtra) → Maharashtra Administrative Service, Maharashtra Police Service
- UPPSC (Uttar Pradesh) → UP PCS, SDM, Deputy SP, Block Development Officer
- BPSC (Bihar) → Bihar Administrative Service, Bihar Police Service
- RPSC (Rajasthan) → Rajasthan Administrative Service
- TNPSC (Tamil Nadu) → Tamil Nadu Civil Service, Group 1/2/4
- KPSC (Karnataka), APPSC (Andhra Pradesh), TSPSC (Telangana), MPPSC (Madhya Pradesh)

**Eligibility**: Graduate in any stream | Age: 21–40 years (varies by state + category)

**Selection process**: Similar to UPSC — Prelims (GS + optional CSAT) → Mains (descriptive) → Interview

**Posts**: SDM (Sub-Divisional Magistrate), DSP (Deputy Superintendent of Police),
BDO (Block Development Officer), CDPO, Tehsildar, State Tax Officer, etc.

**Salary (State Level)**:
- Entry level (State Administrative Service): ₹40,000–75,000/month (varies by state)
- Senior IAS/IPS equivalent positions: ₹1.5–2.5L/month
- Maharashtra ADO: ₹38,600–1,22,000/month; UP PCS: ₹47,600–1,51,100/month

**Advantage over UPSC**: State-specific posting (stay in home state), lower competition than UPSC,
faster promotions in smaller cadre, regional language allowed in Mains.

**Preparation**: 12–18 months; use UPSC preparation resources as base +
state-specific current affairs, geography, history, and polity of the state.
""",
    },

    # ── SSC CHSL ─────────────────────────────────────────────────────────────
    {
        "id": "ssc_chsl",
        "title": "SSC CHSL (Combined Higher Secondary Level) — 12th Pass Government Jobs",
        "domain": "govt_jobs",
        "content": """
SSC CHSL is the premier government exam for Class 12 pass candidates seeking central government jobs.

**Posts**: Lower Division Clerk (LDC), Junior Secretariat Assistant (JSA), Postal/Sorting Assistant,
Data Entry Operator (DEO) in various ministries, departments, and central government offices.

**Eligibility**: Class 12 passed | Age: 18–27 years

**Vacancies**: 3,000–7,000 annually

**Selection process**:
1. Tier 1 CBT: 200 marks — English (25), Reasoning (25), Quantitative Aptitude (25), GK (25)
2. Tier 2: Descriptive Paper (English/Hindi Essay + Letter)
3. Skill Test (Typing Test 35 wpm English / 30 wpm Hindi)

**Salary**:
- LDC/JSA: ₹19,900–63,200 (Level 2) → effective ₹26,000–35,000/month
- Postal/Sorting Assistant: ₹25,500–81,100 (Level 4) → effective ₹35,000–42,000/month
- DEO Grade A: ₹25,500 (Level 4)
- After promotions: reach Assistant/UDC level ₹29,200–35,400/month over 3–5 years

**Best suited for**: Students who completed 12th and want to secure government employment
quickly; can pursue graduation simultaneously while working.

**Combine with**: SSC CGL preparation (same aptitude topics), IBPS Clerk, RRB NTPC 12th level.
""",
    },

    # ── LIC / Insurance ────────────────────────────────────────────────────────
    {
        "id": "lic_career",
        "title": "LIC AAO / Development Officer — Insurance Sector Government Jobs",
        "domain": "govt_jobs",
        "content": """
Life Insurance Corporation of India (LIC) is India's largest public sector insurer.
Government insurance careers offer excellent salary, benefits, and job security.

**LIC AAO (Assistant Administrative Officer)**:
Eligibility: Graduate with 60% marks | Age: 21–30 years
Exam: Prelims (60 min) + Mains (2 hrs) + Interview
Salary: ₹44,000–1,37,700 (IDA pay scale) → effective CTC ₹65,000–80,000/month with all benefits

**LIC Development Officer**:
Promoted from LIC Agent or direct recruitment in some cycles
Manages insurance agents in a territory; performance-based income

**NIACL (New India Assurance), UIIC, Oriental Insurance, NICL**:
Similar AAO exams conducted by respective PSU insurers
Salary: ₹32,795–62,315 (entry level)

**Why LIC/Insurance**:
- Excellent non-contributory pension (defined benefit scheme)
- Medical benefits for self and family
- Annual bonus (LIC declares bonus at valuation)
- Transferable but mostly metro/city postings
- Work-life balance better than banking

**Career path**: AAO → AO → Administrative Officer → Sr. Divisional Manager → Zonal Manager → ED → MD
""",
    },

    # ── Government Jobs overview ──────────────────────────────────────────────
    {
        "id": "govt_jobs_overview",
        "title": "Government Jobs in India — Complete Overview and Comparison",
        "domain": "govt_jobs",
        "content": """
Government jobs in India are categorised into Groups based on grade pay and responsibility:

**Group A (Gazetted officers)**: IAS, IPS, IRS, IBPS PO (after confirmation), SSC CGL Grade B posts
Salary range: ₹56,100–2,50,000/month | Requires: Graduate + competitive exam

**Group B (Gazetted/Non-Gazetted)**: SSC CGL Inspector posts, RRB NTPC Officer-level
Salary range: ₹35,400–1,12,400/month | Requires: Graduate + exam

**Group C**: SSC CHSL (LDC/Postal Assistant), RRB NTPC Clerk-level
Salary range: ₹18,000–63,200/month | Requires: 10th/12th + exam

**Group D**: RRB Group D Helper/Track Maintainer
Salary range: ₹18,000–56,900/month | Requires: 10th pass

**Government vs Private sector comparison**:
| Factor | Government Job | Private Sector |
|---|---|---|
| Job security | Very high (near-permanent) | Moderate |
| Starting salary | ₹30,000–60,000 | ₹25,000–60,000 (varies widely) |
| Growth ceiling | Defined (promotions by seniority) | Uncapped (merit-based) |
| Pension | Defined benefit (old) / NPS (new) | NPS/EPFO only |
| Work-life balance | Generally better | Depends on company |
| Relocation risk | Yes (transfers) | Yes (office shifts) |
| Lateral entry | Difficult | Easy |

**Top exams by difficulty** (hardest to easiest):
1. UPSC Civil Services — 0.1% selection rate
2. UPSC NDA/CDS — 2–5% selection rate
3. SSC CGL — ~1% selection rate (lakhs apply)
4. IBPS PO — ~1.5% selection rate
5. RBI Grade B — 0.5% selection rate (but fewer applicants)
6. SSC CHSL — 2% selection rate
7. RRB NTPC — 1–2% selection rate

**Preparation calendar for multiple exams**:
April–August: Focus on SSC CGL Tier 1 / IBPS PO Prelims
September–November: CAT, NDA, IBPS Mains
December–February: RRB NTPC, SSC CHSL
March: State PSC results + UPSC Prelims preparation
""",
    },
]


def get_govt_job_documents() -> list[dict]:
    docs = []
    for item in GOVT_JOB_PROFILES:
        docs.append({
            "id": f"govt_jobs::{item['id']}",
            "text": item["title"] + "\n\n" + item["content"].strip(),
            "domain": "govt_jobs",
            "title": item["title"],
            "metadata": {
                "domain": "govt_jobs",
                "job_id": item["id"],
                "title": item["title"],
            },
        })
    return docs
