"""Entrance exam knowledge base — engineering, medical, management, law, civil services, international."""
from __future__ import annotations

EXAMS = [
    # ── Engineering ───────────────────────────────────────────────────────────
    {
        "id": "jee_main",
        "name": "JEE Main",
        "full_name": "Joint Entrance Examination – Main",
        "conducting_body": "National Testing Agency (NTA)",
        "applicable_for": ["B.Tech/B.E. at NITs, IIITs, CFTIs", "Eligibility for JEE Advanced (IITs)"],
        "frequency": "Twice a year (Session 1: January, Session 2: April)",
        "mode": "Online CBT",
        "eligibility": "Class 12 passed/appearing with PCM. No age limit as of 2024.",
        "subjects": "Physics, Chemistry, Mathematics (30 questions each, 90 total)",
        "total_marks": 300,
        "duration_minutes": 180,
        "marking_scheme": "+4 correct MCQ, −1 wrong MCQ; +4 numeric (no negative)",
        "registration_period": "November (Session 1), February (Session 2)",
        "exam_months": "January and April",
        "result_months": "February and May",
        "total_seats_approx": 23500,
        "cutoff_2024": "~90th percentile for top NIT CS; ~97th percentile for top NITs",
        "preparation_time_months": 12,
        "preparation_tips": [
            "Master NCERT Physics, Chemistry, Mathematics (Class 11-12) — 40% questions are NCERT-level",
            "Practice JEE Main previous papers 2015–2024 under timed conditions",
            "Focus on high-weightage chapters: Mechanics, Electrochemistry, Calculus, Algebra",
            "Attempt all 3 sessions of JEE Main mock tests on NTA Abhyas app (free)",
            "Target 250+ marks for top NIT; 270+ marks for NIT Trichy CS",
        ],
        "website": "jeemain.nta.nic.in",
    },
    {
        "id": "jee_advanced",
        "name": "JEE Advanced",
        "full_name": "Joint Entrance Examination – Advanced",
        "conducting_body": "One of 7 IIT zones (rotates each year)",
        "applicable_for": ["B.Tech at all 23 IITs", "B.Arch at IIT Kharagpur and Roorkee"],
        "frequency": "Once a year (May/June)",
        "mode": "Online CBT",
        "eligibility": "Top 2.5 lakh JEE Main qualifiers; max 2 attempts",
        "total_marks": "360 (Paper 1: 180, Paper 2: 180)",
        "duration_minutes": "3 hours per paper",
        "marking_scheme": "Variable — single correct, multi-correct, integer type; negative marking applies",
        "exam_months": "May",
        "result_months": "June",
        "total_seats_approx": 17385,
        "cutoff_2024": "Rank < 100 for IIT Bombay CS (General); rank < 5000 for guaranteed admission",
        "preparation_time_months": 24,
        "preparation_tips": [
            "Solve complete IIT JEE papers from 2000–2024 — conceptual depth matters more than speed",
            "Understand derivations, not just formulas — JEE Advanced tests application and reasoning",
            "Multi-correct questions: partial marking applies; attempt only if confident in all options",
            "Mock test strategy: simulate exam-day stress with 3-hour timed attempts",
            "Focus on wave optics, coordination chemistry, permutations & combinations, integration",
        ],
        "website": "jeeadv.ac.in",
    },
    {
        "id": "bitsat",
        "name": "BITSAT",
        "full_name": "Birla Institute of Technology and Science Admission Test",
        "conducting_body": "BITS Pilani",
        "applicable_for": ["B.E./B.Pharm at BITS Pilani, Goa, Hyderabad campuses"],
        "frequency": "Once a year (May/June)",
        "mode": "Online CBT",
        "eligibility": "PCM with 75%+ in Class 12 (and English 60%+). Class 12 appearing/passed.",
        "total_marks": 450,
        "duration_minutes": 180,
        "marking_scheme": "+3 correct, −1 wrong; extra time bonus questions for 100% correct",
        "exam_months": "May–June",
        "cutoff_2024": "340+ for CS at Pilani; 315+ for CS at Goa/Hyderabad",
        "preparation_time_months": 12,
        "preparation_tips": [
            "BITSAT syllabus is Class 11-12 NCERT — no JEE Advanced-level depth required",
            "Speed is key: 150 questions in 180 minutes; practice timed mock tests",
            "Complete English proficiency section: 10 marks but easily scoreable",
            "Logical reasoning section: 10 questions, start practicing 2 months before",
            "Score 340+ at home mock tests before scheduling the real exam",
        ],
        "website": "bitsadmission.com",
    },
    # ── Medical ───────────────────────────────────────────────────────────────
    {
        "id": "neet_ug",
        "name": "NEET-UG",
        "full_name": "National Eligibility cum Entrance Test – Undergraduate",
        "conducting_body": "National Testing Agency (NTA)",
        "applicable_for": ["MBBS", "BDS", "BAMS (Ayurveda)", "BHMS (Homeopathy)", "BSMS", "Veterinary (BVSc)"],
        "frequency": "Once a year (May)",
        "mode": "Offline (OMR pen-paper)",
        "eligibility": "Class 12 with PCB + English; min 50% PCB (45% for PwD; 40% for SC/ST/OBC)",
        "subjects": "Physics (45Q), Chemistry (45Q), Biology: Botany+Zoology (90Q) = 180 questions",
        "total_marks": 720,
        "duration_minutes": 200,
        "marking_scheme": "+4 correct, −1 wrong",
        "exam_months": "May",
        "total_seats_approx": 107000,
        "cutoff_2024": "720–715 for AIIMS Delhi; ~660+ for government medical college (General)",
        "preparation_time_months": 24,
        "preparation_tips": [
            "NCERT Biology (Class 11-12) is the bible — 90%+ questions are NCERT-based",
            "Read NCERT line by line; memorise tables, diagrams, and exceptions",
            "Biology weightage is highest (360 marks) — score 340+ in Biology for top rank",
            "Physics: focus on mechanics, optics, modern physics (fewer chapters, high marks)",
            "Take full 180-question mocks weekly from November before May exam",
        ],
        "website": "neet.nta.nic.in",
    },
    # ── Management ────────────────────────────────────────────────────────────
    {
        "id": "cat",
        "name": "CAT",
        "full_name": "Common Admission Test",
        "conducting_body": "IIMs (one IIM is the convener each year, rotates)",
        "applicable_for": ["MBA/PGDM at all 20 IIMs", "Accepted at 1200+ B-schools in India"],
        "frequency": "Once a year (November)",
        "mode": "Online CBT",
        "eligibility": "Bachelor's degree with 50% marks (45% for SC/ST). Final year students may apply.",
        "sections": "VARC (Verbal Ability & Reading Comprehension), DILR (Data Interpretation & LR), QA (Quantitative Ability)",
        "total_questions": 66,
        "duration_minutes": 120,
        "marking_scheme": "+3 correct MCQ, −1 wrong MCQ; +3 TITA (no negative for TITA)",
        "exam_months": "November",
        "result_months": "January",
        "cutoff_2024": "99.5+ percentile for IIM ABC shortlist; 99+ percentile for new IIMs; 95+ for tier-2 IIMs",
        "preparation_time_months": 12,
        "preparation_tips": [
            "Start with QA fundamentals: Number System, Algebra, Geometry, Permutations",
            "VARC: Read 1 editorial + 1 RC passage daily from CAT-level sources (Hindu, Economist)",
            "DILR: Solve 3 sets per day — practice more than theory here",
            "Sectional time limits: VARC 40 min, DILR 40 min, QA 40 min — practice under time",
            "Analyse mock CATs question-by-question; understand why you got wrong answers",
        ],
        "website": "iimcat.ac.in",
    },
    {
        "id": "gmat",
        "name": "GMAT",
        "full_name": "Graduate Management Admission Test",
        "conducting_body": "Graduate Management Admission Council (GMAC)",
        "applicable_for": ["MBA at global top-100 B-schools (Harvard, Wharton, INSEAD, IIM PGPX, ISB)"],
        "frequency": "Year-round (upto 5 times per year)",
        "mode": "Online or test centre CBT",
        "eligibility": "Bachelor's degree; no age limit",
        "sections": "Quantitative Reasoning, Verbal Reasoning, Data Insights",
        "total_score_range": "205–805",
        "duration_minutes": 135,
        "cutoff_global_top": "740+ for Harvard/Wharton; 720+ for INSEAD; 700+ for top-20",
        "cutoff_india": "720+ for IIM PGPX; 700+ for ISB",
        "preparation_time_months": 4,
        "preparation_tips": [
            "GMAT Focus Edition (2024): 3 sections, 64 questions total, 2h 15m",
            "Official GMAT prep materials (mba.com) are the most representative",
            "Target Quant 85th percentile + Verbal 85th percentile for 720+ total",
            "Sentence Correction is no longer tested (GMAT Focus) — focus on Reading Comprehension",
        ],
        "website": "mba.com/exams/gmat",
    },
    # ── Law ───────────────────────────────────────────────────────────────────
    {
        "id": "clat",
        "name": "CLAT",
        "full_name": "Common Law Admission Test",
        "conducting_body": "Consortium of NLUs",
        "applicable_for": ["5-year BA LLB / BBA LLB at 24 National Law Universities (NLUs)"],
        "frequency": "Once a year (December)",
        "mode": "Online CBT",
        "eligibility": "Class 12 passed/appearing with 45% (40% for SC/ST).  Age limit: no upper limit",
        "sections": "English, GK & Current Affairs, Legal Reasoning, Logical Reasoning, Quantitative Techniques",
        "total_questions": 120,
        "duration_minutes": 120,
        "marking_scheme": "+1 correct, −0.25 wrong",
        "exam_months": "December",
        "total_seats_approx": 3400,
        "cutoff_2024": "Rank < 70 for NLSIU Bangalore (General); < 300 for top 5 NLUs",
        "preparation_time_months": 12,
        "preparation_tips": [
            "Read The Hindu daily for current affairs and legal news (2-3 months before exam)",
            "Legal reasoning: no prior law knowledge needed — read passages and apply logic",
            "Quantitative: Class 10-level maths — don't ignore this section (10 marks)",
            "Attempt full-length CLAT mocks from October onwards",
            "Focus on accuracy not speed — 120 questions in 120 minutes allows re-reading",
        ],
        "website": "consortiumofnlus.ac.in",
    },
    # ── Civil Services ────────────────────────────────────────────────────────
    {
        "id": "upsc_cse",
        "name": "UPSC CSE",
        "full_name": "Union Public Service Commission Civil Services Examination",
        "conducting_body": "Union Public Service Commission (UPSC)",
        "applicable_for": ["IAS (Indian Administrative Service)", "IPS (Indian Police Service)",
                           "IFS (Indian Foreign Service)", "IRS", "100+ other Group A and B services"],
        "frequency": "Once a year",
        "mode": "Offline (OMR Prelims; handwritten Mains)",
        "eligibility": "Bachelor's degree from recognised university.  Age: 21-32 (General), up to 37 (SC/ST)",
        "stages": "Prelims (GS Paper 1 + CSAT) → Mains (9 papers) → Personality Test (interview)",
        "total_posts_2024": 1056,
        "success_rate": "~0.1–0.2% of applicants",
        "exam_months": "Prelims: May/June; Mains: September/October; Interview: March-April",
        "preparation_time_months": 18,
        "preparation_tips": [
            "Phase 1: Complete NCERT books (Class 6-12) for History, Geography, Polity, Economics, Science",
            "Phase 2: Standard references — Laxmikanth (Polity), Ramesh Singh (Economy), Nitin Singhania (Culture)",
            "Phase 3: Current affairs — The Hindu editorial + PIB + Yojana + Kurukshetra (6 months before Prelims)",
            "Optional subject: Choose based on background + scoring potential (Sociology, Anthropology, PSIR popular)",
            "Mains answer writing: practice 15-mark and 10-mark answers daily from April of preparation year",
        ],
        "website": "upsc.gov.in",
    },
    # ── Research / Postgraduate ────────────────────────────────────────────────
    {
        "id": "gate",
        "name": "GATE",
        "full_name": "Graduate Aptitude Test in Engineering",
        "conducting_body": "IITs + IISc (rotates each year)",
        "applicable_for": ["M.Tech/M.E. at IITs, NITs, CFTIs", "PSU jobs (BHEL, ONGC, DRDO, NTPC, etc.)", "Research programmes"],
        "frequency": "Once a year (February)",
        "mode": "Online CBT",
        "eligibility": "B.Tech/B.E./B.Sc (Research)/B.Arch in final year or completed",
        "total_marks": 100,
        "duration_minutes": 180,
        "marking_scheme": "MSQ (+1/+2, no negative), NAT (no negative), MCQ (+1/+2, −1/3 negative)",
        "exam_months": "February",
        "cutoff_2024": "GATE score 750+ for IIT M.Tech; 500+ for NIT; specific PSU cutoffs vary",
        "preparation_time_months": 6,
        "preparation_tips": [
            "GATE CS: Focus on Algorithms, OS, DBMS, CN, Digital Logic — these are 70% of the paper",
            "Practice previous 15 years GATE papers — question patterns repeat",
            "GATE score is valid for 3 years — useful for PSU applications even without M.Tech",
            "For PSU jobs (BHEL, ONGC, DRDO): GATE score 600+ typically enough for shortlisting",
        ],
        "website": "gate.iitm.ac.in",
    },
    # ── International ────────────────────────────────────────────────────────
    {
        "id": "gre",
        "name": "GRE",
        "full_name": "Graduate Record Examination",
        "conducting_body": "Educational Testing Service (ETS)",
        "applicable_for": ["MS/PhD at US/Canada/Australia/Europe universities"],
        "frequency": "Year-round (5 times per year)",
        "mode": "Online or test centre",
        "eligibility": "No formal requirement; typically undergraduate degree holders",
        "sections": "Verbal Reasoning (130-170), Quantitative Reasoning (130-170), Analytical Writing (0-6)",
        "total_score_range": "260–340 (Verbal + Quant)",
        "duration_minutes": 225,
        "cutoff_global_top": "325+ for MIT/Stanford/CMU CS; 315+ for top-50 US universities",
        "preparation_time_months": 3,
        "preparation_tips": [
            "GRE Quant (170) is achievable — Indian students score high here; do not neglect Verbal",
            "Vocabulary: Learn 3000 GRE words via Magoosh or ETS Official word lists",
            "Analytical Writing: Practice Issue + Argument essays with official scoring guides",
            "Many top US CS programmes no longer require GRE as of 2023-24 — verify individual program policy",
        ],
        "website": "ets.org/gre",
    },
    {
        "id": "ielts",
        "name": "IELTS",
        "full_name": "International English Language Testing System",
        "conducting_body": "British Council / IDP / Cambridge Assessment English",
        "applicable_for": ["UK universities", "Canada (study/work/PR)", "Australia/NZ", "Some US universities"],
        "frequency": "Year-round (multiple dates per month)",
        "mode": "Paper-based or Computer-based",
        "sections": "Listening, Reading, Writing, Speaking (each 0-9)",
        "overall_band_range": "0–9",
        "cutoff_uk": "6.5 overall (no band below 6.0) for most UK universities",
        "cutoff_canada_pr": "6.0 overall for Express Entry immigration",
        "preparation_time_months": 2,
        "preparation_tips": [
            "Band 7.0 is achievable in 2 months of focused preparation for educated Indians",
            "Speaking: practice with a partner or record yourself; fluency matters more than accent",
            "Writing Task 2 (essay): learn 5-6 essay structures; practice 3 essays per week",
            "Reading: don't read the passage first — scan questions, then read strategically",
            "Use Cambridge IELTS Official Practice Test books (Cambridge 1-18) for full mocks",
        ],
        "website": "ielts.org",
    },
    # ── Finance ───────────────────────────────────────────────────────────────
    {
        "id": "ca_foundation",
        "name": "CA Foundation",
        "full_name": "Chartered Accountancy Foundation Examination",
        "conducting_body": "Institute of Chartered Accountants of India (ICAI)",
        "applicable_for": ["Entry into CA qualification pathway — leads to CA Intermediate and Final"],
        "frequency": "Twice a year (May and November)",
        "mode": "Offline (OMR + descriptive)",
        "eligibility": "Class 12 passed (can register after Class 10, appear after Class 12)",
        "papers": "Paper 1: Accounting (100), Paper 2: Business Laws (100), Paper 3: Maths/LR/Stats (100), Paper 4: Business Economics (100)",
        "total_marks": 400,
        "passing_criteria": "Aggregate 50% (200/400) with no paper below 30%",
        "exam_months": "May and November",
        "preparation_time_months": 4,
        "preparation_tips": [
            "Register with ICAI immediately after Class 10 to complete 4-month study period",
            "Paper 1 Accounting: ICAI study material is sufficient; practice journal entries daily",
            "Paper 3 Maths: Class 11-12 level — students with PCM background find this easy",
            "Attempt ICAI mock papers from 2019–2024 to calibrate preparation",
            "Target 55+ per paper to have buffer against passing criteria",
        ],
        "website": "icai.org",
    },
]


def get_exam_documents() -> list[dict]:
    docs = []
    for exam in EXAMS:
        text = _exam_to_text(exam)
        docs.append({
            "id": f"exam::{exam['id']}",
            "text": text,
            "domain": "exam",
            "title": exam["name"],
            "metadata": {
                "domain": "exam",
                "exam_id": exam["id"],
                "title": exam["name"],
                "full_name": exam.get("full_name", ""),
            },
        })
    return docs


def _exam_to_text(e: dict) -> str:
    lines = [
        f"Exam: {e['name']} ({e.get('full_name', '')})",
        f"Conducted by: {e.get('conducting_body', '')}",
        f"Purpose: {', '.join(e.get('applicable_for', []))}",
        f"Frequency: {e.get('frequency', '')}",
        f"Mode: {e.get('mode', '')}",
        f"Eligibility: {e.get('eligibility', '')}",
    ]
    if e.get("total_marks"):
        lines.append(f"Total marks: {e['total_marks']}")
    if e.get("duration_minutes"):
        lines.append(f"Duration: {e['duration_minutes']} minutes")
    if e.get("marking_scheme"):
        lines.append(f"Marking scheme: {e['marking_scheme']}")
    if e.get("exam_months"):
        lines.append(f"Exam held in: {e['exam_months']}")
    if e.get("cutoff_2024"):
        lines.append(f"2024 cutoff: {e['cutoff_2024']}")
    if e.get("total_seats_approx"):
        lines.append(f"Approximate seats: {e['total_seats_approx']}")
    if e.get("preparation_time_months"):
        lines.append(f"Recommended preparation time: {e['preparation_time_months']} months")
    tips = e.get("preparation_tips", [])
    if tips:
        lines.append("Preparation tips:")
        for tip in tips:
            lines.append(f"  - {tip}")
    if e.get("website"):
        lines.append(f"Official website: {e['website']}")
    return "\n".join(lines)
