"""Scholarship knowledge base — government, private, and international scholarships for Indian students."""
from __future__ import annotations

SCHOLARSHIPS = [
    # ── Government of India ───────────────────────────────────────────────────
    {
        "id": "central_sector_scholarship",
        "name": "Central Sector Scheme of Scholarships",
        "provider": "Ministry of Education, Government of India",
        "type": "Merit + Need",
        "amount": "₹10,000/year (Freshers) to ₹20,000/year (PG students)",
        "eligibility_category": ["All"],
        "min_marks_percent": 80.0,
        "max_family_income": 800000.0,
        "applicable_streams": ["All streams (Science, Arts, Commerce)"],
        "applicable_for": "Class 12 toppers — 82,000 new scholarships per year",
        "application_url": "scholarships.gov.in (NSP portal)",
        "renewable": True,
        "description": (
            "India's largest scholarship programme for meritorious students from modest families. "
            "82,000 scholarships per cohort.  Eligible students must be in the top 20th percentile "
            "of their board exam AND have family income below ₹8 lakh/year.  "
            "Scholarship is for full degree duration (3-year UG = 3 years of support)."
        ),
    },
    {
        "id": "pm_scholarship_scheme",
        "name": "Prime Minister's Scholarship Scheme (PMSS)",
        "provider": "Ministry of Home Affairs, Government of India",
        "type": "Category-specific",
        "amount": "₹2,500/month (girls), ₹2,000/month (boys)",
        "eligibility_category": ["Wards of Central Armed Police Forces & Railway Protection Force"],
        "min_marks_percent": 60.0,
        "applicable_streams": ["B.Tech", "MBBS", "BDS", "MBA", "BCA", "B.Pharm", "BBA"],
        "renewable": True,
        "description": (
            "For wards and widows of ex-servicemen/ex-Coast Guard personnel.  "
            "Covers professional degree programmes only (not BA/BCom/BSc).  "
            "Apply via Kendriya Sainik Board portal (ksb.gov.in).  "
            "Enhanced: ₹3,000/month (girls) and ₹2,500/month (boys) from 2023-24."
        ),
    },
    {
        "id": "inspire_scholarship",
        "name": "INSPIRE Scholarship (SHE)",
        "provider": "Department of Science & Technology (DST), Government of India",
        "type": "Merit-based / Science",
        "amount": "₹80,000/year (₹60,000 scholarship + ₹20,000 mentorship grant)",
        "eligibility_category": ["All categories"],
        "min_marks_percent": None,
        "applicable_streams": ["B.Sc", "Integrated M.Sc", "B.Sc-M.Sc — Natural Sciences only"],
        "renewable": True,
        "description": (
            "INSPIRE SHE (Scholarship for Higher Education) is for top 1% students from each board "
            "who choose natural sciences (Physics, Chemistry, Maths, Biology, Statistics) for UG. "
            "10,000 scholarships per year.  Mentorship of ₹20,000/year connects scholars to "
            "scientists/faculty.  Encourages India's best minds to pursue basic science research."
        ),
    },
    {
        "id": "post_matric_scholarship_sc_st",
        "name": "Post-Matric Scholarship for SC/ST Students",
        "provider": "Ministry of Social Justice / Ministry of Tribal Affairs",
        "type": "Category-based",
        "amount": "Maintenance allowance + tuition fee reimbursement (varies by course)",
        "eligibility_category": ["SC", "ST"],
        "max_family_income": 250000.0,
        "applicable_streams": ["All streams"],
        "renewable": True,
        "description": (
            "One of India's largest scholarship programmes covering over 60 lakh SC/ST students annually. "
            "Covers full tuition fee for government colleges and maintenance allowance for living expenses. "
            "Amount varies: ₹120–550/month maintenance + actual tuition fees (government institution). "
            "Apply through NSP portal before the state deadline (usually October-November)."
        ),
    },
    {
        "id": "merit_cum_means_scholarship",
        "name": "Merit-cum-Means (MCM) Scholarship for Professional/Technical Courses",
        "provider": "Ministry of Minority Affairs, Government of India",
        "type": "Merit + Need",
        "amount": "Course fee up to ₹20,000/year + maintenance ₹10,000/year",
        "eligibility_category": ["Muslim", "Christian", "Sikh", "Buddhist", "Zoroastrian", "Jain minorities"],
        "min_marks_percent": 50.0,
        "max_family_income": 250000.0,
        "applicable_streams": ["Technical (B.Tech/BE)", "Professional (MBBS/MBA/MCA)"],
        "renewable": True,
        "description": (
            "For students from minority communities pursuing professional and technical courses.  "
            "30% of MCM scholarships reserved for girls.  "
            "Apply through NSP portal.  30,000 fresh scholarships per year."
        ),
    },
    # ── Private / Corporate ───────────────────────────────────────────────────
    {
        "id": "reliance_foundation_scholarship",
        "name": "Reliance Foundation Scholarships",
        "provider": "Reliance Foundation",
        "type": "Merit + Need",
        "amount": "Up to ₹6 lakh (PG) or ₹4 lakh (UG) for the full programme",
        "eligibility_category": ["All"],
        "min_marks_percent": 60.0,
        "max_family_income": 1500000.0,
        "applicable_streams": ["STEM (B.Tech, B.Sc, M.Tech, M.Sc)", "Humanities (BA, MA)", "Management"],
        "renewable": True,
        "description": (
            "One of India's most generous private scholarships covering tuition fees and living expenses. "
            "UG programme: 100 scholarships; PG programme: 100 scholarships per year. "
            "Selection includes academic performance, financial need, and social contribution. "
            "Scholars get mentoring by industry professionals and Reliance leadership. "
            "Apply at reliancefoundation.org/scholarships."
        ),
    },
    {
        "id": "tata_scholarship_cornell",
        "name": "Tata Scholarship for Cornell University",
        "provider": "Tata Education and Development Trust",
        "type": "Need-based",
        "amount": "Full tuition + fees + living expenses at Cornell (value: ~$80,000/year)",
        "eligibility_category": ["All — Indian citizens only"],
        "min_marks_percent": None,
        "applicable_streams": ["All undergraduate programmes at Cornell University (USA)"],
        "renewable": True,
        "description": (
            "Full scholarship at Cornell University (Ivy League, USA) for Indian students with "
            "financial need.  One of the very few full-ride scholarships for Indians at a top "
            "US university.  Apply through Cornell's financial aid process during Common App. "
            "Covers 4 years of undergraduate education including living expenses and return airfare."
        ),
    },
    {
        "id": "dr_reddy_foundation_scholarship",
        "name": "Dr. Reddy's Foundation Scholarship (DARE)",
        "provider": "Dr. Reddy's Foundation",
        "type": "Merit + Entrepreneurship",
        "amount": "₹50,000–₹1 lakh",
        "eligibility_category": ["All"],
        "applicable_streams": ["Students pursuing careers in science, social entrepreneurship"],
        "renewable": False,
        "description": (
            "DARE (Drug and Applied Research Education) scholarship for students showing "
            "exceptional academic merit and entrepreneurial initiative.  "
            "Focus areas: pharmaceutical sciences, public health, and social innovation."
        ),
    },
    # ── International ─────────────────────────────────────────────────────────
    {
        "id": "chevening_scholarship",
        "name": "Chevening Scholarship",
        "provider": "UK Foreign, Commonwealth & Development Office",
        "type": "Merit + Leadership",
        "amount": "Full tuition + living expenses + flights (1-year Master's in UK) — ~£30,000 value",
        "eligibility_category": ["All — Indian citizens only"],
        "min_marks_percent": None,
        "applicable_streams": ["All Master's programmes at any UK university"],
        "renewable": False,
        "description": (
            "UK Government's flagship scholarship for future global leaders.  "
            "Open to Indian citizens with 2+ years of work experience.  "
            "Covers full tuition at any UK university + monthly stipend + return flights + visa.  "
            "Selection criteria: academic excellence + leadership potential + networking ability. "
            "Apply September–November for studies starting the following September. "
            "~100 Chevening scholars from India each year."
        ),
    },
    {
        "id": "fulbright_nehru",
        "name": "Fulbright-Nehru Fellowships",
        "provider": "US-India Educational Foundation (USIEF) / US State Department",
        "type": "Merit + Research",
        "amount": "Full funding — tuition, living, health insurance, round-trip airfare (US$25,000–50,000 value)",
        "eligibility_category": ["All — Indian citizens only"],
        "applicable_streams": ["Master's, PhD, Research, Teaching — all subjects"],
        "renewable": False,
        "description": (
            "Prestigious US Government scholarship for Indian students and professionals.  "
            "Multiple categories: Fulbright-Nehru Master's Fellowships, Research Fellowships, "
            "Doctoral Research Awards, Teaching Fellowships.  "
            "Students apply for Master's/PhD programmes at US universities.  "
            "2-year post-study home-return requirement applies.  "
            "Apply through usief.org — deadline is usually July for following academic year."
        ),
    },
    {
        "id": "daad_scholarship",
        "name": "DAAD Scholarship (Germany)",
        "provider": "Deutscher Akademischer Austauschdienst (DAAD) — German Academic Exchange Service",
        "type": "Merit-based",
        "amount": "€850–1,200/month stipend + health insurance + travel allowance",
        "eligibility_category": ["All — Indian citizens only"],
        "applicable_streams": ["Engineering, Natural Sciences, Arts, Humanities — Master's and PhD"],
        "renewable": True,
        "description": (
            "DAAD offers scholarships for studying in Germany — which has PUBLIC universities with "
            "near-zero tuition (€150–300/semester) for all international students.  "
            "DAAD stipend covers living costs for 12-24 months.  "
            "Requires German language proficiency for many programmes (B2 level); "
            "many engineering/science programmes are taught in English.  "
            "Germany is the most cost-effective study-abroad destination for Indian students."
        ),
    },
    {
        "id": "commonwealth_scholarship",
        "name": "Commonwealth Scholarship",
        "provider": "Commonwealth Scholarship Commission (CSC), UK",
        "type": "Development-focused",
        "amount": "Full tuition + stipend + airfare (UK universities, ~£30,000 value)",
        "eligibility_category": ["All — Indian citizens only"],
        "applicable_streams": ["Priority subjects: Science/technology, Healthcare, Education, Social work"],
        "renewable": True,
        "description": (
            "UK Government scholarship for students from developing Commonwealth nations.  "
            "Priority given to students committed to contributing to India's development.  "
            "Covers 1-year Master's or 3-year PhD at any UK university.  "
            "Apply through cscuk.fcdo.gov.uk — Indian applications managed by Association of Indian Universities."
        ),
    },
]


def get_scholarship_documents() -> list[dict]:
    docs = []
    for s in SCHOLARSHIPS:
        text = _scholarship_to_text(s)
        docs.append({
            "id": f"scholarship::{s['id']}",
            "text": text,
            "domain": "scholarship",
            "title": s["name"],
            "metadata": {
                "domain": "scholarship",
                "scholarship_id": s["id"],
                "title": s["name"],
                "provider": s.get("provider", ""),
                "type": s.get("type", ""),
            },
        })
    return docs


def _scholarship_to_text(s: dict) -> str:
    lines = [
        f"Scholarship: {s['name']}",
        f"Provider: {s.get('provider', '')}",
        f"Type: {s.get('type', '')}",
        f"Amount: {s.get('amount', '')}",
        f"Eligible categories: {', '.join(s.get('eligibility_category', []))}",
    ]
    if s.get("min_marks_percent"):
        lines.append(f"Minimum marks required: {s['min_marks_percent']}%")
    if s.get("max_family_income"):
        lines.append(f"Maximum family income: ₹{s['max_family_income']:,.0f}/year")
    if s.get("applicable_streams"):
        lines.append(f"Applicable to: {', '.join(s['applicable_streams'])}")
    if s.get("application_url"):
        lines.append(f"Apply at: {s['application_url']}")
    lines.append(f"Renewable: {'Yes' if s.get('renewable') else 'No'}")
    if s.get("description"):
        lines.append(f"\n{s['description']}")
    return "\n".join(lines)
