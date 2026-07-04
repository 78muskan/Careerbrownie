"""Salary benchmarks by role, experience, city, and industry — India 2024-25."""
from __future__ import annotations

# Format: each entry covers a role across experience bands and cities
SALARY_DATA = [
    {
        "role": "Software Engineer",
        "domain": "technology",
        "description": (
            "Software engineers write, test, and maintain code.  "
            "Salaries vary enormously between IT services firms (TCS, Infosys) and "
            "product/startup companies."
        ),
        "by_experience": {
            "fresher_0_2yr": {"range_lpa": "3.5–18", "median_lpa": 7.5,
                              "note": "Product companies: ₹12–18 LPA; IT services: ₹3.5–5 LPA"},
            "mid_2_5yr": {"range_lpa": "8–35", "median_lpa": 18,
                          "note": "Senior engineer at startup/MNC; team lead at IT services"},
            "senior_5_10yr": {"range_lpa": "18–80", "median_lpa": 35,
                              "note": "Staff engineer at top product company; principal/architect"},
            "lead_10yr_plus": {"range_lpa": "35–200", "median_lpa": 60,
                               "note": "Engineering manager, VP Engineering at funded startups"},
        },
        "by_city": {
            "Bangalore": "+15% vs national median (India's tech capital)",
            "Mumbai": "+10% vs national median",
            "Hyderabad": "+12% vs national median",
            "Pune": "+5% vs national median",
            "Delhi/NCR": "+8% vs national median",
            "Chennai": "+5% vs national median",
        },
        "top_paying_companies": ["Google India", "Microsoft", "Amazon", "Flipkart", "Goldman Sachs tech"],
        "skills_for_max_pay": ["System Design", "Distributed Systems", "ML/AI", "Cloud (AWS/GCP)"],
    },
    {
        "role": "Data Scientist / ML Engineer",
        "domain": "data_ai",
        "description": "Extract insights from data; build and deploy ML models.",
        "by_experience": {
            "fresher_0_2yr": {"range_lpa": "5–18", "median_lpa": 10,
                              "note": "Often titled Data Analyst at fresher level"},
            "mid_2_5yr": {"range_lpa": "14–40", "median_lpa": 22,
                          "note": "Significant jump with 2+ years real ML experience"},
            "senior_5_10yr": {"range_lpa": "25–90", "median_lpa": 45,
                              "note": "ML research scientist, senior DS at FAANG"},
            "lead_10yr_plus": {"range_lpa": "50–200", "median_lpa": 80,
                               "note": "Head of Data Science; AI/ML Director"},
        },
        "by_city": {
            "Bangalore": "+20% (most ML jobs in India)",
            "Hyderabad": "+10%",
            "Mumbai": "+5% (fintech ML)",
        },
        "top_paying_companies": ["Amazon", "Google", "Microsoft Research", "Flipkart", "Meesho"],
        "skills_for_max_pay": ["LLMs/Fine-tuning", "MLOps", "PyTorch", "Spark", "A/B Testing"],
    },
    {
        "role": "Product Manager",
        "domain": "product",
        "description": "Owns product vision, roadmap, and execution at technology companies.",
        "by_experience": {
            "fresher_apm": {"range_lpa": "8–22", "median_lpa": 14,
                            "note": "APM (Associate PM) at funded startup; typically MBA/IIT graduates"},
            "mid_2_5yr": {"range_lpa": "18–50", "median_lpa": 28,
                          "note": "PM at growth-stage startup; Senior PM at IT services"},
            "senior_5_10yr": {"range_lpa": "35–100", "median_lpa": 60,
                              "note": "Senior PM at FAANG; Group PM at Series B+ startup"},
            "lead_10yr_plus": {"range_lpa": "60–150", "median_lpa": 90,
                               "note": "Director of Product, VP Product at tech unicorn"},
        },
        "by_city": {
            "Bangalore": "+25% (India's product hub)",
            "Delhi/NCR": "+10%",
            "Mumbai": "+8%",
        },
        "top_paying_companies": ["Amazon", "Flipkart", "Google", "Microsoft", "CRED", "Razorpay"],
        "skills_for_max_pay": ["Data Analysis (SQL)", "Product Strategy", "A/B Testing", "Roadmapping"],
    },
    {
        "role": "Investment Banker",
        "domain": "finance",
        "description": "Advises on M&A, IPOs, and capital markets transactions.",
        "by_experience": {
            "analyst_0_3yr": {"range_lpa": "12–35", "median_lpa": 22,
                              "note": "Analyst level at domestic or foreign IB; after IIM/CFA"},
            "associate_3_6yr": {"range_lpa": "30–80", "median_lpa": 50,
                                "note": "Associate post-MBA; significant bonus potential"},
            "vp_6_10yr": {"range_lpa": "60–150", "median_lpa": 90,
                          "note": "Vice President at Tier 1 IB; bonus can equal base"},
            "md_director": {"range_lpa": "100–500+", "median_lpa": 180,
                            "note": "Managing Director; bonus-heavy; deal-dependent"},
        },
        "by_city": {
            "Mumbai": "IB hub of India; +40% vs other cities",
            "Delhi/NCR": "+10%",
        },
        "top_paying_companies": ["Goldman Sachs", "Morgan Stanley", "JP Morgan", "Kotak IB", "Axis Capital"],
        "skills_for_max_pay": ["Financial Modelling", "DCF", "LBO Modelling", "Client Management"],
    },
    {
        "role": "Management Consultant",
        "domain": "consulting",
        "description": "Solves strategic business problems for large organisations.",
        "by_experience": {
            "analyst_0_3yr": {"range_lpa": "15–30", "median_lpa": 22,
                              "note": "Business Analyst at top firm post-IIT undergrad"},
            "associate_3_6yr": {"range_lpa": "25–60", "median_lpa": 40,
                                "note": "Post-MBA Associate at MBB via IIM ABC"},
            "manager_6_10yr": {"range_lpa": "50–120", "median_lpa": 75,
                               "note": "Manager/Project Leader; leads case teams"},
            "partner_10yr_plus": {"range_lpa": "150–500+", "median_lpa": 220,
                                  "note": "Partner level; profit sharing; highly variable"},
        },
        "by_city": {
            "Mumbai": "+15% vs Delhi/Bangalore (most consulting offices)",
            "Delhi/NCR": "Base",
            "Bangalore": "+5%",
        },
        "top_paying_companies": ["McKinsey India", "BCG India", "Bain India", "EY-Parthenon", "Deloitte"],
        "skills_for_max_pay": ["Problem Structuring", "Financial Modelling", "Client Communication"],
    },
    {
        "role": "Chartered Accountant",
        "domain": "finance",
        "description": "Audit, tax, and financial advisory professional certified by ICAI.",
        "by_experience": {
            "fresher_ca": {"range_lpa": "6–14", "median_lpa": 9,
                           "note": "Big 4 starting salary: ₹7-12 LPA; industry: ₹6-9 LPA"},
            "mid_3_6yr": {"range_lpa": "15–35", "median_lpa": 22,
                          "note": "Senior Associate/Manager at Big 4; Finance Manager at corporate"},
            "senior_6_10yr": {"range_lpa": "25–60", "median_lpa": 40,
                              "note": "Senior Manager Big 4; CFO at mid-size company"},
            "partner_director": {"range_lpa": "50–200+", "median_lpa": 80,
                                 "note": "Big 4 partner; CFO at large company; own practice"},
        },
        "top_paying_companies": ["Deloitte", "EY", "KPMG", "PwC", "large corporates (TCS, HDFC)"],
        "skills_for_max_pay": ["US GAAP/IFRS", "Transfer Pricing", "M&A Advisory", "SAP Finance"],
    },
    {
        "role": "Doctor (MBBS/Specialist)",
        "domain": "healthcare",
        "description": "Medical practitioner; salary depends heavily on specialisation and setting.",
        "by_experience": {
            "mbbs_intern": {"range_lpa": "0.6–1.2", "median_lpa": 0.9,
                            "note": "Government internship stipend ₹5,000-10,000/month"},
            "mbbs_resident_pg": {"range_lpa": "1.5–4", "median_lpa": 2.5,
                                 "note": "PG residency stipend"},
            "specialist_0_5yr": {"range_lpa": "12–30", "median_lpa": 20,
                                 "note": "MD/MS specialist at private hospital; 1-2 years post-residency"},
            "senior_specialist": {"range_lpa": "25–100+", "median_lpa": 50,
                                  "note": "Senior consultant at Apollo/Fortis; own clinic in metro"},
        },
        "by_city": {
            "Mumbai/Delhi": "+30% vs smaller cities (private hospitals)",
            "Bangalore": "+20%",
            "Tier-3 cities": "−30% but higher local purchasing power",
        },
        "skills_for_max_pay": ["DM/MCh superspecialisation", "Robotic Surgery", "Oncology", "Cardiology"],
    },
    {
        "role": "Civil Services Officer (IAS/IPS)",
        "domain": "government",
        "description": "Government administrative service officers; salary includes multiple allowances.",
        "by_experience": {
            "entry_level_7th_cpc": {"range_lpa": "8–12", "median_lpa": 10,
                                    "note": "Basic pay ₹56,100 + DA + HRA + transport; all-in ₹80,000-1L/month"},
            "joint_secretary": {"range_lpa": "15–18", "median_lpa": 16,
                                 "note": "15+ years service; Pay Level 14"},
            "additional_secretary": {"range_lpa": "18–22", "median_lpa": 19},
            "secretary_cabinet": {"range_lpa": "22–28", "median_lpa": 25,
                                  "note": "Cabinet Secretary: ₹2.5 lakh/month + perks"},
        },
        "non_monetary_benefits": [
            "Subsidised housing (government bungalows)",
            "Chauffeur-driven vehicle",
            "Domestic help allowance",
            "Security (IPS/IAS)",
            "Heavily subsidised utilities",
            "Pension (defined benefit)",
            "Medical benefits (CGHS)",
        ],
        "note": "IAS/IPS salary is lower than equivalent private sector but total compensation including perks is substantial.",
    },
    {
        "role": "UX/UI Designer",
        "domain": "design",
        "description": "Designs digital product interfaces and user experiences.",
        "by_experience": {
            "fresher_0_2yr": {"range_lpa": "3–10", "median_lpa": 6,
                              "note": "Junior designer at agency or startup"},
            "mid_2_5yr": {"range_lpa": "10–25", "median_lpa": 16,
                          "note": "Product designer at funded startup; design lead at agency"},
            "senior_5_10yr": {"range_lpa": "20–50", "median_lpa": 32,
                              "note": "Senior product designer, design systems lead"},
            "lead_10yr_plus": {"range_lpa": "40–80", "median_lpa": 55,
                               "note": "Head of Design, Design Director"},
        },
        "top_paying_companies": ["Flipkart", "CRED", "Meesho", "PhonePe", "Google India"],
        "skills_for_max_pay": ["Design Systems", "Figma", "User Research", "Motion Design"],
    },
    {
        "role": "Marketing Manager (Digital)",
        "domain": "marketing",
        "description": "Manages brand presence, campaigns, and customer acquisition.",
        "by_experience": {
            "fresher_0_2yr": {"range_lpa": "3–8", "median_lpa": 5,
                              "note": "Digital marketing executive; SEO/SEM/content"},
            "mid_2_5yr": {"range_lpa": "8–20", "median_lpa": 13,
                          "note": "Senior digital marketer; performance marketing manager"},
            "senior_5_10yr": {"range_lpa": "18–40", "median_lpa": 28,
                              "note": "Marketing Director at FMCG/D2C brand; Head of Growth at startup"},
            "lead_10yr_plus": {"range_lpa": "35–80", "median_lpa": 50,
                               "note": "CMO, VP Marketing at large company"},
        },
        "skills_for_max_pay": ["Performance Marketing", "Attribution Modelling", "Product-led Growth", "CRM"],
    },
]


def get_salary_documents() -> list[dict]:
    docs = []
    for s in SALARY_DATA:
        text = _salary_to_text(s)
        docs.append({
            "id": f"salary::{s['role'].lower().replace(' ', '_').replace('/', '_')}",
            "text": text,
            "domain": "salary",
            "title": f"Salary guide: {s['role']}",
            "metadata": {
                "domain": "salary",
                "role": s["role"],
                "industry": s.get("domain", ""),
            },
        })
    return docs


def _salary_to_text(s: dict) -> str:
    lines = [
        f"Salary guide: {s['role']}",
        f"Industry: {s.get('domain', '').replace('_', ' ').title()}",
        f"Description: {s.get('description', '')}",
        "",
        "Salary by experience level (India, 2024-25):",
    ]
    for band, data in s.get("by_experience", {}).items():
        label = band.replace("_", " ").title()
        lines.append(f"  {label}: ₹{data.get('range_lpa', 'N/A')} LPA (median ~₹{data.get('median_lpa', 'N/A')} LPA)")
        if data.get("note"):
            lines.append(f"    Note: {data['note']}")
    if s.get("by_city"):
        lines.append("\nCity-wise variation:")
        for city, note in s["by_city"].items():
            lines.append(f"  {city}: {note}")
    if s.get("top_paying_companies"):
        lines.append(f"\nTop paying companies: {', '.join(s['top_paying_companies'])}")
    if s.get("skills_for_max_pay"):
        lines.append(f"Skills to maximise pay: {', '.join(s['skills_for_max_pay'])}")
    if s.get("non_monetary_benefits"):
        lines.append("\nNon-monetary benefits:")
        for b in s["non_monetary_benefits"]:
            lines.append(f"  - {b}")
    if s.get("note"):
        lines.append(f"\nNote: {s['note']}")
    return "\n".join(lines)
