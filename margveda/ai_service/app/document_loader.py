"""Document loading and the built-in CareerBrownie knowledge base.

Converts structured knowledge (career profiles, FAQs, custom records) into
:class:`Document` objects.  Each Document is chunked by :mod:`chunking` and
its pieces are stored in the vector store on first startup.

The built-in knowledge covers 20 India-focused careers and 8 FAQ entries.
Additional documents can be ingested at runtime via the ``/ingest`` endpoint.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)


# ── Data model ────────────────────────────────────────────────────────────────

@dataclass
class Document:
    id: str
    text: str
    domain: str       # career | faq | college | exam | general
    title: str = ""
    metadata: dict = field(default_factory=dict)


# ── Built-in career knowledge base ───────────────────────────────────────────
# Each entry is a rich profile for one career path relevant to Indian students.

_CAREERS: dict[str, dict[str, Any]] = {
    "software_engineer": {
        "title": "Software Engineer",
        "description": (
            "Software engineers design, develop, and maintain software systems — from "
            "mobile apps to large-scale distributed platforms.  India's tech ecosystem "
            "generates 200 000+ software engineering roles every year across IT services, "
            "product companies, and startups."
        ),
        "education": "B.Tech/B.E. in Computer Science, IT, or related.  MCA/M.Tech optional.",
        "top_skills": ["Python", "JavaScript", "Data Structures & Algorithms", "System Design", "SQL", "Git", "REST APIs"],
        "entry_salary_lpa": "4–10",
        "senior_salary_lpa": "25–80",
        "growth": "Very High",
        "top_companies": ["Google", "Microsoft", "Flipkart", "Zomato", "Infosys", "TCS", "funded startups"],
        "roadmap": [
            "Master programming fundamentals in Python or Java",
            "Practice Data Structures & Algorithms daily on LeetCode",
            "Build and deploy 3-5 full-stack projects",
            "Study system design: load balancers, databases, caches",
            "Prepare for campus/off-campus placements with mock interviews",
        ],
    },
    "data_scientist": {
        "title": "Data Scientist",
        "description": (
            "Data scientists extract business insights from large datasets using statistics, "
            "machine learning, and visualisation.  India's data economy is growing at 35% "
            "annually, with demand from fintech, healthtech, e-commerce, and consulting."
        ),
        "education": "B.Tech CS/IT/ECE, B.Sc Statistics, or any degree + PG diploma in Data Science.",
        "top_skills": ["Python", "SQL", "Machine Learning", "Statistics", "Pandas", "Scikit-learn", "Power BI / Tableau"],
        "entry_salary_lpa": "5–12",
        "senior_salary_lpa": "20–60",
        "growth": "Very High",
        "top_companies": ["Amazon", "Swiggy", "Paytm", "McKinsey", "EY", "KPMG", "analytics boutiques"],
        "roadmap": [
            "Learn Python + probability/statistics foundations",
            "Complete a structured ML course (fast.ai, deeplearning.ai)",
            "Build 3-4 end-to-end projects and publish on GitHub",
            "Compete on Kaggle to build ranking and learn from top solutions",
            "Apply for Data Analyst roles first, then transition to Data Scientist",
        ],
    },
    "ai_ml_engineer": {
        "title": "AI / ML Engineer",
        "description": (
            "AI/ML engineers design, train, and deploy machine learning models in production. "
            "Generative AI has dramatically accelerated demand in 2024-25.  India-specific "
            "opportunities at Sarvam AI, Krutrim, and dozens of funded AI startups."
        ),
        "education": "B.Tech CS/IT, M.Tech in AI/ML, or strong self-study portfolio with deployed projects.",
        "top_skills": ["Python", "PyTorch / TensorFlow", "LLMs & Transformers", "MLOps", "Docker", "AWS / GCP", "Statistics"],
        "entry_salary_lpa": "8–18",
        "senior_salary_lpa": "30–100",
        "growth": "Extremely High",
        "top_companies": ["Google DeepMind India", "Microsoft Research", "Amazon", "Sarvam AI", "Ola Krutrim", "AI startups"],
        "roadmap": [
            "Master Python + linear algebra + statistics",
            "Study deep learning: CNNs, RNNs, Transformer architecture",
            "Fine-tune open-source LLMs and build RAG applications",
            "Practice MLOps: model serving, monitoring, CI/CD for ML pipelines",
            "Participate in Kaggle NLP / vision competitions",
        ],
    },
    "product_manager": {
        "title": "Product Manager",
        "description": (
            "Product managers own the vision, strategy, and execution roadmap of software "
            "products.  India's startup boom created massive PM demand at all experience levels. "
            "PMs sit at the intersection of business, design, and technology."
        ),
        "education": "Any bachelor's degree. MBA from IIM/ISB preferred for senior roles. APM programmes also available.",
        "top_skills": ["Product Thinking", "Data Analysis", "Roadmapping", "Stakeholder Management", "SQL basics", "User Research"],
        "entry_salary_lpa": "8–18",
        "senior_salary_lpa": "35–100",
        "growth": "High",
        "top_companies": ["Meesho", "Razorpay", "CRED", "Flipkart", "Ola", "Byju's", "MNCs with India product centres"],
        "roadmap": [
            "Read 'Inspired' by Marty Cagan; study CIRCLES, RICE, jobs-to-be-done frameworks",
            "Build a personal side project and document every product decision",
            "Take PM School or Reforge programme; practice PM interview cases",
            "Start as a Business Analyst or Associate PM (APM) at a startup",
            "Build domain expertise in one vertical: fintech, edtech, or SaaS",
        ],
    },
    "cloud_devops_engineer": {
        "title": "Cloud / DevOps Engineer",
        "description": (
            "Cloud and DevOps engineers build and maintain infrastructure, CI/CD pipelines, "
            "and scalable deployment platforms.  India has a severe shortage of DevOps talent, "
            "making it one of the best-paying entry-level technology career paths in 2024-25."
        ),
        "education": "B.Tech CS/IT or equivalent.  AWS/Azure/GCP certifications highly valued.",
        "top_skills": ["Linux", "Docker", "Kubernetes", "Terraform", "CI/CD (GitHub Actions / Jenkins)", "AWS / Azure / GCP"],
        "entry_salary_lpa": "5–12",
        "senior_salary_lpa": "20–60",
        "growth": "Very High",
        "top_companies": ["AWS India", "Microsoft", "Google Cloud", "Wipro", "Accenture", "cloud-native startups"],
        "roadmap": [
            "Learn Linux administration and Bash scripting",
            "Master Docker; build and push multi-stage container images",
            "Deploy applications on Kubernetes (Minikube locally, then EKS/GKE)",
            "Write Terraform configs for a multi-region cloud environment",
            "Earn AWS Solutions Architect Associate or CKA certification",
        ],
    },
    "cybersecurity_analyst": {
        "title": "Cybersecurity Analyst",
        "description": (
            "Cybersecurity analysts protect organisations from breaches, ransomware, and data "
            "theft.  India's digital banking and government digitalisation programmes are driving "
            "25-30% annual growth in security hiring."
        ),
        "education": "B.Tech CS/IT/ECE.  Certifications: CEH, CISSP, CompTIA Security+, OSCP for advanced roles.",
        "top_skills": ["Network Security", "Ethical Hacking", "SIEM Tools", "Vulnerability Assessment", "Incident Response", "Linux"],
        "entry_salary_lpa": "4–9",
        "senior_salary_lpa": "18–50",
        "growth": "High",
        "top_companies": ["IBM Security", "Wipro CyberDefense", "HCL", "Deloitte", "CERT-In (Government)", "banking sector SOCs"],
        "roadmap": [
            "Learn networking: TCP/IP, OSI model, subnetting, DNS, HTTP",
            "Practice ethical hacking on TryHackMe and HackTheBox platforms",
            "Earn CEH or CompTIA Security+ certification",
            "Build a home lab: simulate phishing, MITM, and brute-force scenarios",
            "Apply for SOC Analyst Tier-1 roles; progress to pentester or DFIR",
        ],
    },
    "chartered_accountant": {
        "title": "Chartered Accountant (CA)",
        "description": (
            "Chartered Accountants certified by ICAI work in audit, taxation, financial "
            "advisory, and corporate finance.  CA is one of the most prestigious professional "
            "qualifications in India with near-guaranteed employment."
        ),
        "education": "CA Foundation → CA Intermediate → CA Final (ICAI).  Eligible after Class 12 or graduation.",
        "top_skills": ["Accounting", "Direct & Indirect Taxation", "Audit", "GST", "Financial Reporting", "Tally / SAP"],
        "entry_salary_lpa": "6–12",
        "senior_salary_lpa": "20–60+",
        "growth": "Stable High",
        "top_companies": ["Big 4: Deloitte, EY, KPMG, PwC", "Banks", "Corporates (TCS, Infosys)", "PSUs", "Own practice"],
        "roadmap": [
            "Register for CA Foundation after Class 12 and clear 4 papers",
            "Begin 3-year articleship with a registered CA firm after Intermediate Group 1",
            "Pass CA Intermediate (2 groups) — aim within 2-3 attempts",
            "Clear CA Final while completing articleship",
            "Consider DISA for IT audit or CPA for international practice",
        ],
    },
    "investment_banker": {
        "title": "Investment Banker",
        "description": (
            "Investment bankers advise corporations on IPOs, M&A, and capital raising. "
            "India's record IPO pipeline and M&A activity make this one of the highest-paying "
            "finance careers.  Entry is highly competitive — typically via IIM or CFA."
        ),
        "education": "MBA from IIM/ISB/top B-school, or CFA + strong finance undergrad.  Engineering + MBA (IIT-IIM) common.",
        "top_skills": ["Financial Modelling (Excel)", "DCF / Comps Valuation", "Pitchbooks", "M&A Process", "Capital Markets", "Bloomberg"],
        "entry_salary_lpa": "15–30",
        "senior_salary_lpa": "50–200+",
        "growth": "High",
        "top_companies": ["Goldman Sachs", "Morgan Stanley", "JP Morgan India", "Kotak IB", "Axis Capital", "IIFL"],
        "roadmap": [
            "Build a strong GPA and leadership profile in undergrad",
            "Intern at a boutique IB or Big 4 transaction advisory team",
            "Self-study financial modelling (WSP or CFI certification)",
            "Crack MBA at top IIM/ISB or earn CFA Level 1-3",
            "Network through alumni, LinkedIn, and IB club events",
        ],
    },
    "management_consultant": {
        "title": "Management Consultant",
        "description": (
            "Management consultants solve complex strategic and operational problems for "
            "organisations.  India's MBB (McKinsey, BCG, Bain) offices recruit heavily from "
            "top IIMs.  Considered one of the best-exit-opportunity careers globally."
        ),
        "education": "MBA from IIM A/B/C or ISB.  IIT/NIT undergrad for non-MBA analyst roles.",
        "top_skills": ["Problem Structuring", "Case Solving", "Excel / PowerPoint", "Hypothesis-driven Analysis", "Industry Research"],
        "entry_salary_lpa": "18–35",
        "senior_salary_lpa": "50–150+",
        "growth": "High",
        "top_companies": ["McKinsey", "BCG", "Bain (MBB)", "EY-Parthenon", "Deloitte", "KPMG Advisory", "Roland Berger"],
        "roadmap": [
            "Target top IIM through CAT (99th percentile+)",
            "Practice 100+ structured case interviews using CaseCoach or Case in Point",
            "Intern at a consulting firm during MBA summer",
            "Build deep expertise in one sector (FMCG, tech, pharma)",
            "Earn PPO from summer internship or apply through campus placement",
        ],
    },
    "doctor_mbbs": {
        "title": "Doctor (MBBS / MD)",
        "description": (
            "Medical doctors diagnose and treat illness.  MBBS (5.5 years + 1-year internship) "
            "is the entry degree.  MD/MS specialisation adds 3 more years.  India's expanding "
            "private healthcare sector ensures sustained demand."
        ),
        "education": "MBBS (NEET-UG mandatory) → MD/MS/DNB via NEET-PG for specialisation.",
        "top_skills": ["Clinical Diagnosis", "Anatomy", "Pharmacology", "Patient Communication", "Surgical Skills (for surgeons)"],
        "entry_salary_lpa": "6–15 (government), 12–25 (private hospital)",
        "senior_salary_lpa": "30–100+ (specialist / consultant)",
        "growth": "Stable High",
        "top_companies": ["AIIMS", "Fortis", "Apollo Hospitals", "Max Healthcare", "Government health services"],
        "roadmap": [
            "Score 600+ in NEET-UG for a government medical college seat",
            "Complete MBBS with strong rotations in medicine, surgery, ob-gyn, paediatrics",
            "Clear NEET-PG for MD/MS specialisation (score 700+ for top seats)",
            "Consider USMLE / PLAB for USA / UK practice",
            "Pursue DM / MCh superspecialisation for highest salaries",
        ],
    },
    "lawyer": {
        "title": "Lawyer / Advocate",
        "description": (
            "Lawyers provide legal advice, represent clients, and draft contracts.  India has "
            "one of the world's largest legal markets.  Corporate law, IP, and dispute "
            "resolution are the fastest-growing specialisations."
        ),
        "education": "LLB 3-year (after graduation) or BA/BBA LLB 5-year integrated.  CLAT for NLUs.",
        "top_skills": ["Legal Research", "Drafting & Pleading", "Contract Law", "Negotiation", "Litigation"],
        "entry_salary_lpa": "3–12 (junior associate)",
        "senior_salary_lpa": "25–100+ (equity partner at top firm)",
        "growth": "Moderate High",
        "top_companies": ["AZB & Partners", "Cyril Amarchand Mangaldas", "Khaitan & Co", "JSA", "Trilegal", "global law firm India offices"],
        "roadmap": [
            "Clear CLAT for NLU Delhi, NLSIU Bangalore, or equivalent NLU",
            "Intern at top law firms every semester to build a network",
            "Publish research in law journals for academic credibility",
            "Sit the bar exam and enroll with the Bar Council of India",
            "Specialise early: M&A / corporate, IP, tax litigation, or arbitration",
        ],
    },
    "ux_ui_designer": {
        "title": "UX / UI Designer",
        "description": (
            "UX/UI designers create user-friendly digital experiences.  As India's product "
            "ecosystem matures, design has become a highly valued discipline complementing "
            "engineering teams in every funded startup."
        ),
        "education": "Any degree.  Specialised courses: Interaction Design Foundation, Google UX Certificate, NID, or self-study.",
        "top_skills": ["Figma", "User Research", "Wireframing", "Prototyping", "Design Systems", "Accessibility"],
        "entry_salary_lpa": "4–10",
        "senior_salary_lpa": "20–60",
        "growth": "High",
        "top_companies": ["Flipkart", "CRED", "PhonePe", "Meesho", "design agencies", "product startups"],
        "roadmap": [
            "Learn Figma (free Figma Academy or YouTube crash course)",
            "Study UX principles: usability heuristics, cognitive load, accessibility",
            "Complete 3 UX case studies with user research and iteration rounds",
            "Build a Figma + Behance portfolio; contribute to open-source design projects",
            "Apply for junior designer or UX intern roles at product companies",
        ],
    },
    "ias_civil_services": {
        "title": "IAS / IPS / Civil Services Officer",
        "description": (
            "Civil services officers run India's administrative, police, and foreign service "
            "machinery.  The UPSC Civil Services Exam has a ~0.1% selection rate but offers "
            "immense social impact and job security."
        ),
        "education": "Any bachelor's degree from a recognised university.  Age limit: 21–32 (General), 21–35 (OBC), 21–37 (SC/ST).",
        "top_skills": ["General Studies", "Current Affairs", "Essay Writing", "Optional Subject Mastery", "Interview Skills"],
        "entry_salary_lpa": "7–9 basic + allowances (~12–15 CTC equivalent)",
        "senior_salary_lpa": "18–28 (Cabinet Secretary level) + non-monetary perks",
        "growth": "Hierarchical (very stable)",
        "top_companies": ["Government of India", "State governments", "PSUs", "International organisations (via IFS)"],
        "roadmap": [
            "Complete graduation; begin UPSC prep 2 years before first attempt",
            "Finish NCERT books (6-12) for all subjects → standard texts",
            "Maintain a current affairs diary: The Hindu editorial + PIB daily",
            "Choose a scoring optional subject aligned with your background",
            "Practice mains answer writing daily; join a mock interview programme",
        ],
    },
    "teacher_professor": {
        "title": "Teacher / Professor",
        "description": (
            "Teachers educate students at schools, colleges, and universities.  EdTech platforms "
            "(Unacademy, Vedantu, BYJU'S) have created hybrid opportunities paying well for "
            "subject-matter experts."
        ),
        "education": "B.Ed for school teaching. NET/SET for college. Ph.D. for university faculty.",
        "top_skills": ["Subject Expertise", "Communication", "Curriculum Design", "Assessment", "Digital Tools"],
        "entry_salary_lpa": "3–8 (school), 8–20 (college / EdTech)",
        "senior_salary_lpa": "15–40 (professor), up to 60 (EdTech star educator)",
        "growth": "Moderate",
        "top_companies": ["CBSE schools", "IITs / IIMs", "BYJU'S", "Unacademy", "Vedantu", "government colleges"],
        "roadmap": [
            "Specialise in your subject at postgraduate level",
            "Clear B.Ed for school; NET/SET for college/university teaching",
            "Create YouTube or online course content to build a teaching portfolio",
            "Apply for government positions or EdTech platforms",
            "Pursue Ph.D. for tenure-track academic positions",
        ],
    },
    "marketing_professional": {
        "title": "Marketing Professional",
        "description": (
            "Marketing professionals build brand awareness and drive customer acquisition. "
            "India's digital advertising market crossed ₹40 000 crore in 2024, creating massive "
            "demand for performance marketers, content strategists, and brand managers."
        ),
        "education": "MBA Marketing, BBA, or any degree with digital marketing certifications.",
        "top_skills": ["Digital Marketing", "SEO / SEM", "Social Media", "Content Marketing", "Google Analytics", "Meta Ads"],
        "entry_salary_lpa": "4–10",
        "senior_salary_lpa": "20–60 (CMO / VP Marketing)",
        "growth": "High",
        "top_companies": ["FMCG companies (HUL, ITC)", "e-commerce", "D2C brands", "SaaS startups", "digital agencies"],
        "roadmap": [
            "Earn Google Ads and Meta Blueprint certifications (free)",
            "Run a real experiment: grow a page/blog from 0 and document the results",
            "Complete MBA Marketing or a 3-month digital marketing bootcamp",
            "Specialise in one channel: SEO, performance marketing, or content",
            "Build a portfolio showing campaigns with measured ROAS / organic traffic growth",
        ],
    },
    "psychologist_counsellor": {
        "title": "Psychologist / Career Counsellor",
        "description": (
            "Psychologists study human behaviour and provide therapeutic support.  Career "
            "counsellors help students and professionals with education and career planning. "
            "India's mental health awareness is rising, creating new service demand."
        ),
        "education": "BA/MA Psychology. M.Phil Clinical Psychology (RCI-recognised) for clinical practice.",
        "top_skills": ["Counselling Techniques", "Psychometric Assessment", "Empathy", "Report Writing", "Career Assessment Tools"],
        "entry_salary_lpa": "3–8",
        "senior_salary_lpa": "12–35 (private practice or hospital consultant)",
        "growth": "Growing",
        "top_companies": ["Hospitals", "NGOs", "Schools (counsellor)", "Corporate HR wellness", "Online therapy platforms"],
        "roadmap": [
            "Complete BA/MA in Psychology from a UGC-recognised university",
            "Gain supervised clinical hours through hospital or NGO internships",
            "Register with RCI (Rehabilitation Council of India) for clinical practice",
            "Earn certified career counsellor credentials (GCDF, NCC)",
            "Build caseload through schools, hospitals, or online therapy platforms",
        ],
    },
    "architect": {
        "title": "Architect",
        "description": (
            "Architects design buildings, spaces, and urban environments.  India's "
            "infrastructure boom, smart city projects, and luxury real estate growth drive "
            "consistent demand for registered architects."
        ),
        "education": "B.Arch (5 years) from Council of Architecture-recognised institution.  NATA for admission.",
        "top_skills": ["AutoCAD", "Revit", "SketchUp", "Structural Knowledge", "Urban Planning", "Sustainable Design"],
        "entry_salary_lpa": "3–8",
        "senior_salary_lpa": "15–40+ (principal or own firm)",
        "growth": "Moderate",
        "top_companies": ["HCP Design", "Morphogenesis", "real estate companies", "government PWD", "own studio"],
        "roadmap": [
            "Clear NATA for B.Arch at SPA Delhi, CEPT Ahmedabad, or top NIT",
            "Build a design portfolio across all studio projects in college",
            "Intern at a registered architect firm in the 5th year",
            "Register with the Council of Architecture after B.Arch",
            "Develop a niche: sustainable design, interior design, or urban planning",
        ],
    },
    "pharmacist": {
        "title": "Pharmacist",
        "description": (
            "Pharmacists dispense medications and work in pharma R&D, regulatory affairs, and "
            "quality assurance.  India is the world's largest generic drug manufacturer, "
            "creating strong domestic and export-focused career demand."
        ),
        "education": "B.Pharm (4 years) or D.Pharm (2 years).  M.Pharm for R&D.  PharmD for clinical pharmacy.",
        "top_skills": ["Pharmacology", "Drug Formulation", "Regulatory Affairs", "Quality Control", "Patient Counselling"],
        "entry_salary_lpa": "3–8",
        "senior_salary_lpa": "12–30",
        "growth": "Moderate",
        "top_companies": ["Sun Pharma", "Cipla", "Dr. Reddy's", "Apollo hospital chains", "retail pharmacy chains"],
        "roadmap": [
            "Complete B.Pharm with strong chemistry and pharmacology foundation",
            "Pursue M.Pharm specialisation: Pharmacognosy, Pharma Chemistry, or Clinical",
            "Get RA-Pharm certification for regulatory affairs roles",
            "Target USFDA or EMA-focused roles for international opportunities",
        ],
    },
    "journalist": {
        "title": "Journalist / Media Professional",
        "description": (
            "Journalists research, write, and broadcast news.  Digital media has disrupted "
            "print but created new opportunities in data journalism, video storytelling, and "
            "independent media in India."
        ),
        "education": "BA/MA Journalism and Mass Communication from IIMC, Symbiosis, ACJ, or top university.",
        "top_skills": ["Investigative Reporting", "Writing", "Video Editing", "Social Media", "Data Journalism", "Interviewing"],
        "entry_salary_lpa": "2–6",
        "senior_salary_lpa": "12–30 (senior editor / anchor)",
        "growth": "Moderate (digital growing, print declining)",
        "top_companies": ["The Hindu", "NDTV", "Economic Times", "The Wire", "HT Media", "digital news startups"],
        "roadmap": [
            "Join BA Mass Communication at IIMC, ACJ, or a reputed college",
            "Intern at a local newspaper / TV channel every semester",
            "Build a portfolio of published articles and video reports",
            "Learn data journalism: Flourish, Datawrapper, Excel pivot tables",
            "Specialise: business journalism, investigations, or sports media",
        ],
    },
    "hr_professional": {
        "title": "HR Professional",
        "description": (
            "HR professionals manage talent acquisition, employee relations, training, and "
            "compensation.  As India's organised sector grows, HR as a strategic function is "
            "gaining importance across technology companies, FMCG, and consulting."
        ),
        "education": "MBA HR from a recognised institute.  BBA/BA also accepted with relevant experience.",
        "top_skills": ["Talent Acquisition", "HR Analytics", "HRIS (Workday / SAP)", "Labour Law", "Performance Management"],
        "entry_salary_lpa": "4–9",
        "senior_salary_lpa": "18–50 (CHRO / VP HR at large companies)",
        "growth": "Moderate High",
        "top_companies": ["IT companies (TCS, Infosys)", "FMCG (HUL, ITC)", "e-commerce (Amazon, Flipkart)", "HR consulting (Aon, Mercer)"],
        "roadmap": [
            "Complete MBA HR or PGDM in HRM from a recognised institution",
            "Get certified on SAP SuccessFactors or Workday HRIS",
            "Intern in an HR generalist or talent acquisition role",
            "Learn employment law: ID Act, Factories Act, POSH",
            "Build expertise in one vertical: TA, L&D, or total rewards",
        ],
    },
}


_FAQS: list[dict[str, str]] = [
    {
        "id": "faq_001",
        "question": "What is the best career after Class 12 in India?",
        "answer": (
            "The best career depends on your stream and interests.  For Science PCM: "
            "engineering (JEE), defence, merchant navy.  For Science PCB: medicine (NEET), "
            "pharmacy, biotech.  For Commerce: CA, MBA, finance, banking.  For Arts/Humanities: "
            "law (CLAT), civil services (UPSC), media, psychology, design.  Take an aptitude "
            "and interest assessment before choosing — a career counsellor can administer tools "
            "like Holland Code or DMIT to guide you."
        ),
    },
    {
        "id": "faq_002",
        "question": "How much salary can I expect as a fresher in India?",
        "answer": (
            "Fresher salaries in India (2025) vary by role and company tier.  "
            "Engineering/Tech: ₹4–18 LPA at product companies, ₹3–5 LPA at IT services.  "
            "MBA roles: ₹8–35 LPA (top IIMs), ₹5–12 LPA (tier-2 B-schools).  "
            "Government jobs: ₹4–8 LPA consolidated.  CA: ₹7–12 LPA at Big 4.  "
            "Focus on skill-building and the right company over salary in the first 2 years; "
            "high earners at 5 years almost always started with strong foundations, not high packages."
        ),
    },
    {
        "id": "faq_003",
        "question": "Is JEE mandatory for a good engineering career?",
        "answer": (
            "JEE is NOT mandatory for a good engineering career.  JEE Advanced is only for IIT "
            "admission.  Many state universities, NITs, IIITs, and deemed universities offer "
            "excellent programmes without JEE.  Successful engineers at top companies "
            "graduated from state colleges.  Skills, projects, and communication matter more "
            "than college brand for mid-career growth."
        ),
    },
    {
        "id": "faq_004",
        "question": "What are the highest-paying fresher careers in India?",
        "answer": (
            "Highest-paying fresher roles in India (2025): "
            "1. Software Engineer at top product companies: ₹10–25 LPA.  "
            "2. Investment Banking Analyst: ₹15–30 LPA.  "
            "3. Management Consultant (MBB via IIM): ₹18–35 LPA.  "
            "4. AI/ML Engineer at funded startups: ₹12–22 LPA.  "
            "5. Data Scientist: ₹8–18 LPA.  "
            "6. Chartered Accountant (Big 4): ₹8–12 LPA.  "
            "High-paying jobs require proportionally high skill, preparation, and competition."
        ),
    },
    {
        "id": "faq_005",
        "question": "How do I study abroad after Class 12 from India?",
        "answer": (
            "Steps to study abroad after Class 12: "
            "1. Choose country: USA (SAT/ACT), UK (A-levels/UCAS), Canada, Germany (mostly free tuition), Australia.  "
            "2. English proficiency: IELTS 6.5+, TOEFL 90+, or Duolingo English Test.  "
            "3. Start applications 2 years before joining; USA uses Common App + essays + LoRs.  "
            "4. Scholarships: Chevening (UK), Commonwealth, institution need-based aid.  "
            "5. Annual budget: USA ₹40–80 LPA, UK ₹25–60 LPA, Canada ₹15–40 LPA, Germany ₹3–5 LPA (public university)."
        ),
    },
    {
        "id": "faq_006",
        "question": "What exams are needed for a medical career in India?",
        "answer": (
            "Key medical exams in India: "
            "NEET-UG: Mandatory for MBBS/BDS/BAMS; score 600+ for government college seats.  "
            "NEET-PG: After MBBS internship, required for MD/MS specialisation.  "
            "USMLE Steps 1, 2, 3: For practice in the USA.  "
            "PLAB 1 & 2: For practice in the UK.  "
            "FMGE: For graduates of foreign medical colleges to practice in India.  "
            "Timeline: MBBS 5.5 years + 1-year internship = 6.5 years total before PG entrance."
        ),
    },
    {
        "id": "faq_007",
        "question": "How do I switch careers from engineering to a non-tech field?",
        "answer": (
            "Engineering-to-non-tech career switches are very common in India: "
            "Engineering → Management Consulting: MBA at top IIM (CAT 99 percentile).  "
            "Engineering → Product Management: PM bootcamp / APM programme / MBA.  "
            "Engineering → Investment Banking: CFA + Excel modelling + networking.  "
            "Engineering → Data Science: Upskill in Python, ML, statistics + portfolio.  "
            "Engineering → Teaching / EdTech: Subject expertise + B.Ed or online course creation.  "
            "Key: identify transferable skills (analytical thinking, problem solving), build domain knowledge, "
            "and network in the target industry before applying."
        ),
    },
    {
        "id": "faq_008",
        "question": "What is the scope of an MBA in India?",
        "answer": (
            "MBA scope in India (2025): Top IIM (A/B/C) averages ₹24–33 LPA placements.  "
            "Tier-2 IIMs: ₹12–20 LPA.  Best-ROI specialisations: Finance (IB, PE, VC), "
            "Consulting, Marketing (FMCG), and Analytics.  "
            "CAT score needed: 99+ percentile for IIM ABC, 95+ for newer IIMs.  "
            "MBA adds most value when combined with 2-3 years of prior work experience and a clear goal.  "
            "Executive MBA from IIM (PGPX / EPGP) for 5+ year professionals delivers strong ROI."
        ),
    },
]


# ── Public loading functions ──────────────────────────────────────────────────

def load_career_documents() -> list[Document]:
    """Return one Document per career from the built-in knowledge base."""
    docs: list[Document] = []
    for key, career in _CAREERS.items():
        docs.append(
            Document(
                id=f"career::{key}",
                text=_career_to_text(career),
                domain="career",
                title=career["title"],
                metadata={"domain": "career", "key": key, "title": career["title"]},
            )
        )
    return docs


def load_faq_documents() -> list[Document]:
    """Return one Document per FAQ entry from the built-in knowledge base."""
    docs: list[Document] = []
    for faq in _FAQS:
        docs.append(
            Document(
                id=f"faq::{faq['id']}",
                text=f"Q: {faq['question']}\nA: {faq['answer']}",
                domain="faq",
                title=faq["question"][:80],
                metadata={"domain": "faq"},
            )
        )
    return docs


def load_from_dicts(records: list[dict], domain: str = "general") -> list[Document]:
    """Create Documents from arbitrary dicts (used by the /ingest endpoint).

    Each record must have a ``text`` or ``content`` key.  ``id`` and ``title``
    are optional; a positional id is generated if omitted.
    """
    docs: list[Document] = []
    for i, record in enumerate(records):
        text = record.get("text") or record.get("content", "")
        if not isinstance(text, str) or not text.strip():
            log.warning("Skipping record %d — missing or empty text field", i)
            continue
        doc_id = str(record.get("id") or f"{domain}::{i}")
        docs.append(
            Document(
                id=doc_id,
                text=text.strip(),
                domain=domain,
                title=str(record.get("title", "")),
                metadata={k: v for k, v in record.items() if k not in ("text", "content")},
            )
        )
    return docs


def load_from_jsonl(path: str | Path, domain: str = "general") -> list[Document]:
    """Load Documents from a newline-delimited JSON file."""
    docs: list[Document] = []
    p = Path(path)
    if not p.exists():
        log.warning("JSONL path not found: %s", p)
        return docs
    with p.open(encoding="utf-8") as fh:
        for i, line in enumerate(fh):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                docs.extend(load_from_dicts([record], domain=domain))
            except json.JSONDecodeError:
                log.warning("Malformed JSON at line %d — skipped", i + 1)
    return docs


# ── Internal helpers ──────────────────────────────────────────────────────────

def _career_to_text(career: dict[str, Any]) -> str:
    """Render a career dict into a rich prose block optimised for embedding."""
    lines = [
        f"Career: {career['title']}",
        f"Description: {career['description']}",
        f"Education required: {career.get('education', 'N/A')}",
        f"Key skills: {', '.join(career.get('top_skills', []))}",
        f"Entry salary (India): ₹{career.get('entry_salary_lpa', 'N/A')} LPA",
        f"Senior salary (India): ₹{career.get('senior_salary_lpa', 'N/A')} LPA",
        f"Growth outlook: {career.get('growth', 'N/A')}",
        f"Top companies / employers: {', '.join(career.get('top_companies', []))}",
    ]
    roadmap = career.get("roadmap", [])
    if roadmap:
        lines.append("Step-by-step career roadmap:")
        for step in roadmap:
            lines.append(f"  - {step}")
    return "\n".join(lines)
