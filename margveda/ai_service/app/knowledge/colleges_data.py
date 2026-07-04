"""Indian colleges and universities knowledge base."""
from __future__ import annotations

COLLEGES = [
    # ── IITs ──────────────────────────────────────────────────────────────────
    {
        "id": "iit_bombay", "name": "IIT Bombay", "location": "Mumbai, Maharashtra",
        "state": "Maharashtra", "type": "Central/IIT", "tier": "Tier-1",
        "nirf_rank": 3, "naac_grade": "A++",
        "programs": ["B.Tech", "M.Tech", "M.Sc", "MBA (SJMSOM)", "PhD"],
        "popular_branches": ["Computer Science", "Electrical", "Mechanical", "Chemical Engineering"],
        "entrance_exams": ["JEE Advanced"],
        "cutoff_general": "JEE Advanced rank < 100 for CS; < 500 for other top branches",
        "cutoff_obc": "Approx 1.5× general rank cutoff",
        "cutoff_sc_st": "Approx 3–5× general rank cutoff",
        "annual_fees_inr": "₹2.3 lakh/year (B.Tech)",
        "placement_avg_lpa": 21.8, "placement_highest_lpa": 228.0,
        "top_recruiters": ["Google", "Microsoft", "Goldman Sachs", "McKinsey", "DE Shaw", "Tower Research"],
        "hostel": True,
        "description": (
            "IIT Bombay (IITB) is India's third-ranked engineering institution and one of Asia's premier "
            "research universities.  Located in Powai, Mumbai, it offers exceptional industry connections "
            "through its proximity to India's financial capital.  The institute has the best startup "
            "ecosystem among IITs with TechFest Asia's largest technical festival."
        ),
    },
    {
        "id": "iit_delhi", "name": "IIT Delhi", "location": "New Delhi",
        "state": "Delhi", "type": "Central/IIT", "tier": "Tier-1",
        "nirf_rank": 2, "naac_grade": "A++",
        "programs": ["B.Tech", "M.Tech", "MBA (DMS)", "PhD"],
        "popular_branches": ["Computer Science", "Electrical", "Mechanical", "Civil"],
        "entrance_exams": ["JEE Advanced"],
        "cutoff_general": "JEE Advanced rank < 80 for CS; < 300 for Electrical",
        "annual_fees_inr": "₹2.3 lakh/year (B.Tech)",
        "placement_avg_lpa": 23.5, "placement_highest_lpa": 200.0,
        "top_recruiters": ["Google", "Microsoft", "Amazon", "BCG", "DE Shaw", "Schlumberger"],
        "hostel": True,
        "description": (
            "IIT Delhi is India's second-ranked IIT, situated in South Delhi next to government ministries "
            "and the AIIMS medical complex.  Best placement record among all IITs; DMS MBA competes "
            "with top IIMs.  Strong research output in AI, semiconductors, and biomedical engineering."
        ),
    },
    {
        "id": "iit_madras", "name": "IIT Madras", "location": "Chennai, Tamil Nadu",
        "state": "Tamil Nadu", "type": "Central/IIT", "tier": "Tier-1",
        "nirf_rank": 1, "naac_grade": "A++",
        "programs": ["B.Tech", "M.Tech", "BS Research", "PhD"],
        "entrance_exams": ["JEE Advanced"],
        "cutoff_general": "JEE Advanced rank < 100 for CS; < 600 for other branches",
        "annual_fees_inr": "₹2.3 lakh/year",
        "placement_avg_lpa": 20.0, "placement_highest_lpa": 150.0,
        "top_recruiters": ["Microsoft", "Samsung", "Goldman Sachs", "Intel", "NVIDIA"],
        "hostel": True,
        "description": (
            "IIT Madras is India's #1 ranked engineering institution (NIRF 2024) and hosts India's "
            "first on-campus Research Park.  Best for core engineering research and manufacturing.  "
            "The campus is India's only urban national park with resident wildlife."
        ),
    },
    {
        "id": "iit_kanpur", "name": "IIT Kanpur", "location": "Kanpur, Uttar Pradesh",
        "state": "Uttar Pradesh", "type": "Central/IIT", "tier": "Tier-1",
        "nirf_rank": 5,
        "programs": ["B.Tech", "M.Tech", "MBA", "PhD"],
        "entrance_exams": ["JEE Advanced"],
        "cutoff_general": "JEE Advanced rank < 150 for CS",
        "annual_fees_inr": "₹2.3 lakh/year",
        "placement_avg_lpa": 18.5, "placement_highest_lpa": 160.0,
        "top_recruiters": ["Google", "Microsoft", "ISRO", "Intel", "D.E. Shaw"],
        "hostel": True,
        "description": (
            "IIT Kanpur is the birthplace of computer science education in India (first CS department, 1963). "
            "Known for academic rigour, strong research culture, and excellent alumni network in the USA.  "
            "Particularly strong in aerospace, materials science, and management (IIM Lucknow was conceived here)."
        ),
    },
    # ── NITs ──────────────────────────────────────────────────────────────────
    {
        "id": "nit_trichy", "name": "NIT Tiruchirappalli", "location": "Tiruchirappalli, Tamil Nadu",
        "state": "Tamil Nadu", "type": "Central/NIT", "tier": "Tier-1",
        "nirf_rank": 8,
        "programs": ["B.Tech", "M.Tech", "MBA", "PhD"],
        "entrance_exams": ["JEE Main (JoSAA counselling)"],
        "cutoff_general": "JEE Main rank ~1000–5000 (branch dependent)",
        "annual_fees_inr": "₹1.5 lakh/year",
        "placement_avg_lpa": 12.5, "placement_highest_lpa": 60.0,
        "top_recruiters": ["Samsung", "Amazon", "Accenture", "Tata Motors", "L&T"],
        "hostel": True,
        "description": (
            "NIT Trichy is the top-ranked NIT and a Tier-1 institution accessible via JEE Main.  "
            "Strong industry placement record, especially in manufacturing, FMCG, and IT.  "
            "Best choice for students who want a premier institution without clearing JEE Advanced."
        ),
    },
    {
        "id": "nit_warangal", "name": "NIT Warangal", "location": "Warangal, Telangana",
        "state": "Telangana", "type": "Central/NIT", "tier": "Tier-1",
        "nirf_rank": 21,
        "programs": ["B.Tech", "M.Tech", "MBA", "PhD"],
        "entrance_exams": ["JEE Main"],
        "cutoff_general": "JEE Main rank ~2000–8000",
        "annual_fees_inr": "₹1.5 lakh/year",
        "placement_avg_lpa": 11.0, "placement_highest_lpa": 55.0,
        "top_recruiters": ["Infosys", "TCS", "Wipro", "Amazon", "BHEL"],
        "hostel": True,
        "description": (
            "NIT Warangal was India's first NIT (originally Regional Engineering College Warangal, 1959). "
            "Strong in mechanical, civil, and computer science engineering.  Good placement rate of 85%+."
        ),
    },
    # ── IIMs ──────────────────────────────────────────────────────────────────
    {
        "id": "iim_ahmedabad", "name": "IIM Ahmedabad", "location": "Ahmedabad, Gujarat",
        "state": "Gujarat", "type": "Central/IIM", "tier": "Tier-1",
        "nirf_rank": 1,   # management ranking
        "programs": ["MBA (PGP)", "Executive MBA (PGPX)", "PhD (FPM)"],
        "entrance_exams": ["CAT (99.5+ percentile for shortlist)"],
        "cutoff_general": "CAT 99.5+ percentile; GMAT 730+ for PGPX",
        "annual_fees_inr": "₹14.5 lakh/year (PGP 2024-26 total ~₹29 lakh)",
        "placement_avg_lpa": 34.3, "placement_highest_lpa": 200.0,
        "top_recruiters": ["McKinsey", "BCG", "Bain", "Goldman Sachs", "Amazon", "Aditya Birla"],
        "hostel": True,
        "description": (
            "IIM Ahmedabad (IIMA) is India's premier business school and consistently ranked #1 in management. "
            "Produces CEOs of marquee Indian and global companies.  Case-based pedagogy, MBB consulting "
            "placements, and an alumni network that leads major industries.  The PGPX (1-year MBA for "
            "executives with 5+ years experience) has a GMAT average of 720+."
        ),
    },
    {
        "id": "iim_bangalore", "name": "IIM Bangalore", "location": "Bangalore, Karnataka",
        "state": "Karnataka", "type": "Central/IIM", "tier": "Tier-1",
        "nirf_rank": 2,
        "programs": ["MBA (PGP)", "Executive MBA (EPGP)", "PhD (FPM)", "PGPEM"],
        "entrance_exams": ["CAT (99+ percentile)"],
        "annual_fees_inr": "₹13 lakh/year",
        "placement_avg_lpa": 30.5, "placement_highest_lpa": 142.0,
        "top_recruiters": ["Amazon", "McKinsey", "BCG", "Flipkart", "Goldman Sachs"],
        "hostel": True,
        "description": (
            "IIM Bangalore (IIMB) is India's #2 business school and the best for technology-sector placements. "
            "Located in India's Silicon Valley, it leads in entrepreneurship (NR Narayana Murthy of Infosys is "
            "an alum).  Particularly strong in strategy, finance, and consulting."
        ),
    },
    # ── Medical Colleges ──────────────────────────────────────────────────────
    {
        "id": "aiims_delhi", "name": "AIIMS Delhi", "location": "New Delhi",
        "state": "Delhi", "type": "Central/AIIMS", "tier": "Tier-1",
        "nirf_rank": 1,   # medical ranking
        "programs": ["MBBS", "MD/MS (residency)", "PhD", "BSc Nursing"],
        "entrance_exams": ["NEET-UG (MBBS); NEET-PG (MD/MS)"],
        "cutoff_general": "NEET-UG rank < 50 (General) for MBBS",
        "annual_fees_inr": "₹1,628/year (MBBS — one of the cheapest premier institutions)",
        "placement_avg_lpa": 20.0,
        "hostel": True,
        "description": (
            "AIIMS New Delhi is India's foremost medical institution and a world-class healthcare complex. "
            "MBBS admissions require a NEET rank in the top 50 (General category).  Known for "
            "exceptional clinical training, strong residency programmes, and world-class faculty.  "
            "AIIMS produces India's best specialist doctors; government hospital setting with "
            "India's most complex patient cases."
        ),
    },
    # ── Law Schools ───────────────────────────────────────────────────────────
    {
        "id": "nlsiu_bangalore", "name": "NLSIU Bangalore", "location": "Bangalore, Karnataka",
        "state": "Karnataka", "type": "State/NLU", "tier": "Tier-1",
        "nirf_rank": 1,   # law ranking
        "programs": ["BA LLB (5-year integrated)", "LLM", "PhD"],
        "entrance_exams": ["CLAT (top 70 rank for General category)"],
        "cutoff_general": "CLAT rank < 70 for General",
        "annual_fees_inr": "₹2.8 lakh/year",
        "placement_avg_lpa": 25.0, "placement_highest_lpa": 90.0,
        "top_recruiters": ["AZB & Partners", "Cyril Amarchand", "Khaitan & Co", "JSA", "Trilegal"],
        "hostel": True,
        "description": (
            "NLSIU Bangalore (National Law School) is India's top law school and the pioneer of "
            "the 5-year BA LLB integrated programme.  Placement at top-tier Indian and international "
            "law firms, investment banks, and consulting firms.  CLAT rank < 70 required for General category."
        ),
    },
    # ── Central Universities ───────────────────────────────────────────────────
    {
        "id": "du_colleges", "name": "Delhi University (Colleges)", "location": "New Delhi",
        "state": "Delhi", "type": "Central University", "tier": "Tier-1",
        "programs": ["BA (Hons)", "BCom (Hons)", "BSc (Hons)", "MA", "MCom", "MSc"],
        "entrance_exams": ["CUET-UG (Common University Entrance Test)"],
        "cutoff_general": "CUET score 700+ for top colleges like SRCC, Hindu, Miranda House",
        "annual_fees_inr": "₹15,000–50,000/year (very affordable)",
        "placement_avg_lpa": 8.5,
        "hostel": True,
        "description": (
            "Delhi University (DU) comprises 90+ colleges with over 3 lakh students.  Top colleges: "
            "SRCC (BCom), Miranda House (arts/science), St. Stephen's (arts), Kirori Mal (science), "
            "Hindu College (arts/science), Hansraj College.  Best for humanities, economics, and commerce "
            "at a very affordable price.  Admission through CUET-UG score since 2022."
        ),
    },
    {
        "id": "bits_pilani", "name": "BITS Pilani", "location": "Pilani, Rajasthan (+ Goa, Hyderabad campuses)",
        "state": "Rajasthan", "type": "Deemed University", "tier": "Tier-1",
        "nirf_rank": 24,
        "programs": ["B.E.", "M.Sc (dual)", "M.E.", "PhD"],
        "entrance_exams": ["BITSAT (own entrance exam, not JEE)"],
        "cutoff_general": "BITSAT score 340+ for CS at Pilani campus",
        "annual_fees_inr": "₹5.5 lakh/year (private, no government subsidy)",
        "placement_avg_lpa": 16.0, "placement_highest_lpa": 120.0,
        "top_recruiters": ["Google", "Microsoft", "Goldman Sachs", "Amazon", "Uber", "Qualcomm"],
        "hostel": True,
        "description": (
            "BITS Pilani is India's best private engineering university.  Unique Practice School (PS) "
            "programme: students work at companies like Google, Goldman, Samsung during their degree. "
            "No JEE needed — BITSAT is a separate online exam.  Campuses in Pilani, Goa, and Hyderabad. "
            "Strong US graduate school admissions and Silicon Valley presence."
        ),
    },
    # ── Arts/Humanities/Design ─────────────────────────────────────────────────
    {
        "id": "nid_ahmedabad", "name": "National Institute of Design (NID)", "location": "Ahmedabad, Gujarat",
        "state": "Gujarat", "type": "Central/Design", "tier": "Tier-1",
        "programs": ["B.Des (4 years)", "M.Des (2.5 years)"],
        "entrance_exams": ["NID DAT (Design Aptitude Test) — Prelim + Mains"],
        "cutoff_general": "Top 200 out of ~10,000 applicants",
        "annual_fees_inr": "₹3 lakh/year",
        "placement_avg_lpa": 12.0, "placement_highest_lpa": 35.0,
        "top_recruiters": ["Apple", "Samsung", "Tata Motors", "design studios", "own practice"],
        "hostel": True,
        "description": (
            "NID Ahmedabad is India's premier design school, often called the IIT of design.  "
            "Specialisations: Product Design, Communication Design, Textile, Furniture.  "
            "Strong alumni base in global design firms, automotive companies, and independent studios. "
            "Admission through NID DAT (aptitude + portfolio), NOT board marks."
        ),
    },
]


def get_college_documents() -> list[dict]:
    """Return college records ready for LlamaIndex Document creation."""
    docs = []
    for col in COLLEGES:
        text = _college_to_text(col)
        docs.append({
            "id": f"college::{col['id']}",
            "text": text,
            "domain": "college",
            "title": col["name"],
            "metadata": {
                "domain": "college",
                "college_id": col["id"],
                "title": col["name"],
                "state": col.get("state", ""),
                "type": col.get("type", ""),
                "tier": col.get("tier", ""),
                "nirf_rank": str(col.get("nirf_rank", "")),
            },
        })
    return docs


def _college_to_text(c: dict) -> str:
    lines = [
        f"Institution: {c['name']}",
        f"Location: {c['location']}",
        f"Type: {c['type']}  |  Tier: {c['tier']}",
    ]
    if c.get("nirf_rank"):
        lines.append(f"NIRF Ranking 2024: #{c['nirf_rank']}")
    if c.get("naac_grade"):
        lines.append(f"NAAC Grade: {c['naac_grade']}")
    lines.append(f"Programmes offered: {', '.join(c.get('programs', []))}")
    lines.append(f"Admission through: {', '.join(c.get('entrance_exams', []))}")
    if c.get("cutoff_general"):
        lines.append(f"General category cutoff: {c['cutoff_general']}")
    if c.get("cutoff_obc"):
        lines.append(f"OBC cutoff: {c['cutoff_obc']}")
    if c.get("cutoff_sc_st"):
        lines.append(f"SC/ST cutoff: {c['cutoff_sc_st']}")
    if c.get("annual_fees_inr"):
        lines.append(f"Annual fees: {c['annual_fees_inr']}")
    if c.get("placement_avg_lpa"):
        lines.append(f"Average placement package: ₹{c['placement_avg_lpa']} LPA")
    if c.get("placement_highest_lpa"):
        lines.append(f"Highest placement package: ₹{c['placement_highest_lpa']} LPA")
    if c.get("top_recruiters"):
        lines.append(f"Top recruiters: {', '.join(c['top_recruiters'])}")
    if c.get("description"):
        lines.append(f"\n{c['description']}")
    return "\n".join(lines)
