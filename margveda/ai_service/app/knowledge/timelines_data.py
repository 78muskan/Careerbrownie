"""Admission timelines and preparation roadmaps for major Indian career paths."""
from __future__ import annotations

TIMELINES = [
    {
        "id": "jee_timeline",
        "title": "JEE (IIT/NIT Admission) Timeline",
        "target": "B.Tech at IITs/NITs/IIITs via JEE Main + JEE Advanced",
        "total_duration": "2 years (Class 11 + Class 12)",
        "phases": [
            {
                "phase": "Class 11 — Foundation (June–March)",
                "milestones": [
                    "Join reputed coaching (ALLEN/Resonance/Fiitjee/Aakash) or self-study with online resources",
                    "Complete Class 11 NCERT and coaching study material by March",
                    "Focus on building conceptual clarity — do NOT rush to solve JEE papers yet",
                    "Physics: Mechanics (most important chapter), Heat & Thermodynamics",
                    "Chemistry: Physical Chemistry (Mole Concept, Thermodynamics), Organic reaction basics",
                    "Maths: Algebra, Coordinate Geometry, Trigonometry, Limits & Derivatives",
                    "Start solving NCERT Exemplar problems for all 3 subjects",
                ],
            },
            {
                "phase": "Class 12 — July to November",
                "milestones": [
                    "Complete Class 12 syllabus by November (2 months ahead of board exams)",
                    "Physics: Electrodynamics, Optics, Modern Physics",
                    "Chemistry: Electrochemistry, Coordination Compounds, Organic Chemistry (reactions)",
                    "Maths: Calculus (Differentiation + Integration), 3D Geometry, Probability",
                    "Start JEE Main mock tests from September — minimum 2 full mocks per month",
                    "NTA Abhyas app: attempt all previous JEE Main chapters",
                ],
            },
            {
                "phase": "Class 12 — December to January",
                "milestones": [
                    "JEE Main Session 1 registration: November",
                    "Board exam preparation alongside JEE prep — 40% overlap in syllabus",
                    "Take 1 full JEE Main mock test per week under exam conditions",
                    "Revise all Class 11 chapters (very important — 50% JEE syllabus is Class 11)",
                    "JEE Main Session 1: January 22–31 approximately",
                ],
            },
            {
                "phase": "February to April — Advanced Prep",
                "milestones": [
                    "Board exams: February–March",
                    "JEE Main Session 2: April (attempt if Session 1 score was below target)",
                    "JEE Advanced shortlisting: top 2.5 lakh JEE Main qualifiers",
                    "JEE Advanced preparation: solve 2000–2020 IIT JEE papers (pre-2006 also valuable)",
                    "Focus on multi-correct and integer-type questions",
                ],
            },
            {
                "phase": "May–June — Exam & Counselling",
                "milestones": [
                    "JEE Advanced: late May",
                    "JEE Advanced results: mid-June",
                    "JoSAA counselling rounds: June–July (for IITs, NITs, IIITs)",
                    "Institute-specific counselling for BITS (BITSAT usually April–May)",
                    "Admission and hostel reporting: July",
                ],
            },
        ],
        "key_dates_approximate": {
            "JEE Main Session 1": "January 22–31",
            "JEE Main Session 2": "April 1–15",
            "JEE Advanced": "May 26 (approximate)",
            "JoSAA Counselling Starts": "Mid-June",
            "Hostel Reporting": "Late July",
        },
    },
    {
        "id": "neet_timeline",
        "title": "NEET-UG (MBBS Admission) Timeline",
        "target": "MBBS/BDS at government and private medical colleges",
        "total_duration": "2 years (Class 11 + Class 12)",
        "phases": [
            {
                "phase": "Class 11 (June–March) — Foundation",
                "milestones": [
                    "Register with NCERT Biology as the primary resource — every word counts",
                    "Physics: focus on Mechanics, Ray Optics, Modern Physics (high NEET weightage)",
                    "Chemistry: Mole Concept, Redox, Chemical Bonding — master Physical Chemistry first",
                    "Biology: Complete NCERT Class 11 Chapters (1-22) — read 3 times minimum",
                    "Make handwritten notes for Biology — diagrams and tables are frequently tested",
                    "Enroll in Aakash/Allen/Motion/Unacademy for structured coaching or use PW/YouTube",
                ],
            },
            {
                "phase": "Class 12 (June–December) — Completion",
                "milestones": [
                    "Complete NCERT Class 12 Biology (Chapters 1-16) by December",
                    "Revision: re-read Class 11 NCERT Biology chapters simultaneously",
                    "Chemistry: Biomolecules, Polymers, Chemistry in Everyday Life (Class 12 organic)",
                    "Physics: Electrostatics, Magnetism, Dual Nature of Matter, Semiconductors",
                    "Start weekly 180-question full mock tests from October",
                ],
            },
            {
                "phase": "January–May — Final Push",
                "milestones": [
                    "NEET registration: usually February-March",
                    "Revision cycle: NCERT Bio → Physics formula sheets → Organic reactions",
                    "Solve NEET papers from 2005-2024 (available free on NTA/Allen websites)",
                    "3 full mock tests per week in the final 2 months",
                    "Focus on improving Biology from 300 to 340+ marks (highest ROI)",
                    "Board exams: February-March (NEET syllabus = board syllabus, dual preparation efficient)",
                ],
            },
            {
                "phase": "May–September — Results & Counselling",
                "milestones": [
                    "NEET exam: first Sunday of May",
                    "NEET results: June",
                    "MCC counselling (for government quota seats): 4 rounds",
                    "State counselling (for state quota seats): varies by state",
                    "Private college admissions: July–September",
                ],
            },
        ],
        "key_dates_approximate": {
            "NEET-UG Exam": "First Sunday of May",
            "NEET Results": "Mid-June",
            "MCC Counselling Round 1": "Late June",
            "MCC Counselling Round 4 (Mop-Up)": "August",
            "College Joining": "September–October",
        },
    },
    {
        "id": "cat_mba_timeline",
        "title": "CAT / MBA Admission Timeline",
        "target": "MBA at IIMs via CAT; also covers XAT (XLRI), SNAP (Symbiosis), NMAT",
        "total_duration": "12–18 months",
        "phases": [
            {
                "phase": "Month 1–3 — Foundations",
                "milestones": [
                    "QA: Start with Number System, Percentages, Profit & Loss, Ratios",
                    "VARC: Begin reading 1 article from Hindu/Mint editorial daily (30 min)",
                    "DILR: Solve 1 set per day (tables, bar charts, caselets)",
                    "Choose study resources: TIME/IMS study material, CAT Question Bank (2IIM), CATKing",
                ],
            },
            {
                "phase": "Month 4–6 — Intermediate",
                "milestones": [
                    "QA: Algebra, Geometry, Modern Maths, Speed-Time-Distance",
                    "VARC: Para-jumbles, Sentence Completion, Critical Reasoning",
                    "DILR: Advance set types — binary logic, scheduling, seating arrangements",
                    "Take first diagnostic mock test (don't worry about score yet)",
                ],
            },
            {
                "phase": "Month 7–9 — Intensive",
                "milestones": [
                    "Complete all QA chapters; solve 100+ questions per chapter",
                    "VARC: 2 RC passages + 2 VA sets daily",
                    "CAT notification released: August (registration window)",
                    "Begin weekly full-length CAT mocks from September",
                ],
            },
            {
                "phase": "Month 10–12 — Final",
                "milestones": [
                    "CAT exam: last Sunday of November",
                    "Analyse every mock: identify weak areas; stop learning new topics after October",
                    "Parallel preparation for XAT (January), SNAP (December), NMAT (October-December)",
                    "Update SOP and interview preparation profiles",
                ],
            },
            {
                "phase": "Post-CAT — Selection Rounds",
                "milestones": [
                    "CAT results: January 2nd week",
                    "IIM shortlist calls: February",
                    "WAT-PI preparation: group discussion, essay writing, HR questions, PI practice",
                    "IIM final results: March–April",
                    "MBA programme begins: June",
                ],
            },
        ],
        "key_dates_approximate": {
            "CAT Registration": "August–September",
            "CAT Admit Card": "October",
            "CAT Exam": "Last Sunday of November",
            "CAT Results": "2nd week of January",
            "IIM WAT-PI": "February–March",
            "Final Admission Offers": "April–May",
        },
    },
    {
        "id": "upsc_timeline",
        "title": "UPSC Civil Services (IAS/IPS) Timeline",
        "target": "IAS, IPS, IFS and allied services",
        "total_duration": "18–24 months of dedicated preparation",
        "phases": [
            {
                "phase": "Months 1–6 — Foundation",
                "milestones": [
                    "Read all NCERT books: Polity (6-12), History (6-12), Geography (6-12), Economics (9-12), Science (6-10)",
                    "Start standard reference texts: Laxmikanth Polity, Majid Husain Geography",
                    "Current affairs: Subscribe to The Hindu + PIB; maintain a daily 1-page notes habit",
                    "Choose optional subject — start preliminary reading",
                    "Understand UPSC pattern: Prelims GS 1 + CSAT, Mains 9 papers, Interview",
                ],
            },
            {
                "phase": "Months 7–12 — Core Subjects",
                "milestones": [
                    "Complete all standard references for GS: Economy (Ramesh Singh), Environment, Governance",
                    "Optional subject: Complete syllabus once with standard textbooks",
                    "Answer writing practice: 2 mains-style answers per day",
                    "Take first Prelims mock test series (Insights/Vision/ForumIAS)",
                ],
            },
            {
                "phase": "Months 13–18 — Pre-Prelims",
                "milestones": [
                    "UPSC notification: February (apply online)",
                    "Prelims revision: 3 complete revision rounds of all subjects",
                    "Current affairs: compile notes for last 12 months",
                    "Mock tests: minimum 30 full Prelims mocks before exam",
                    "CSAT: ensure CSAT paper cleared (qualifying 33%); don't over-invest time here",
                    "Prelims exam: May/June",
                ],
            },
            {
                "phase": "Post-Prelims — Mains Preparation",
                "milestones": [
                    "Prelims result: August",
                    "Mains prep: intensive answer writing for 8 weeks (Oct-Nov)",
                    "Essay: practice 5 essays under timed conditions",
                    "Mains exam: September–October",
                    "Mains result: January (following year)",
                    "Interview preparation: February-March",
                    "Final result: April–May",
                    "Training at LBSNAA Mussoorie: August (IAS) / SVP NPA Hyderabad (IPS)",
                ],
            },
        ],
    },
    {
        "id": "study_abroad_timeline",
        "title": "Study Abroad (US/UK/Canada) Timeline",
        "target": "Undergraduate or Masters admission at foreign universities",
        "total_duration": "2 years before intended start",
        "phases": [
            {
                "phase": "2 Years Before — Research",
                "milestones": [
                    "Research target countries and universities (US: QS/US News rankings; UK: Times; Canada: Macleans)",
                    "Identify 10-12 target programs (2-3 reach, 4-5 match, 3-4 safety)",
                    "Understand admission requirements for each program: GPA, test scores, essays, recommendations",
                    "Start extracurricular activities that demonstrate leadership and impact",
                ],
            },
            {
                "phase": "18 Months Before — Test Preparation",
                "milestones": [
                    "UG admissions: SAT (1400+ for mid-tier US; 1500+ for top-50) or ACT",
                    "PG admissions: GRE (320+ for STEM), GMAT (700+ for MBA), or no test required (2024 trend)",
                    "English proficiency: IELTS (7.0+) or TOEFL (100+)",
                    "Appear for test; re-take if score is below target",
                ],
            },
            {
                "phase": "12 Months Before — Application Prep",
                "milestones": [
                    "Request Letters of Recommendation from professors/supervisors (3 months advance notice)",
                    "Draft Statement of Purpose (SOP) / Personal Statement",
                    "Update CV/Resume",
                    "Get transcripts attested from university registrar",
                    "Research scholarship options: Chevening (UK), Fulbright (US), DAAD (Germany)",
                ],
            },
            {
                "phase": "Sept–December — Applications",
                "milestones": [
                    "US UG: Common Application opens August 1; Regular Decision deadline January 1",
                    "US graduate: most deadlines December 1 – January 15",
                    "UK (UCAS): application deadline January 31 for most courses",
                    "Canada: rolling admissions; apply November–February",
                    "Pay application fees ($75–$125 per university)",
                ],
            },
            {
                "phase": "Feb–May — Results & Visa",
                "milestones": [
                    "Decisions arrive: US UG March 31; US grad: February–April; UK: March–May",
                    "Compare financial aid packages; negotiate if necessary",
                    "Accept offer by May 1 (US); July (UK)",
                    "Apply for student visa: F-1 (US), Student Route (UK), Study Permit (Canada)",
                    "Book accommodation, flights, travel SIM card",
                ],
            },
        ],
    },
]


def get_timeline_documents() -> list[dict]:
    docs = []
    for t in TIMELINES:
        text = _timeline_to_text(t)
        docs.append({
            "id": f"timeline::{t['id']}",
            "text": text,
            "domain": "timeline",
            "title": t["title"],
            "metadata": {
                "domain": "timeline",
                "timeline_id": t["id"],
                "title": t["title"],
            },
        })
    return docs


def _timeline_to_text(t: dict) -> str:
    lines = [
        f"Timeline: {t['title']}",
        f"Target: {t.get('target', '')}",
        f"Total duration: {t.get('total_duration', '')}",
    ]
    for phase in t.get("phases", []):
        lines.append(f"\n=== {phase['phase']} ===")
        for milestone in phase.get("milestones", []):
            lines.append(f"  • {milestone}")
    if t.get("key_dates_approximate"):
        lines.append("\nKey approximate dates:")
        for event, date in t["key_dates_approximate"].items():
            lines.append(f"  {event}: {date}")
    return "\n".join(lines)
