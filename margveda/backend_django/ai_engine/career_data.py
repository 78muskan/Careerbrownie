"""
Career intelligence data: RIASEC mappings, career database, assessment questions,
roadmap templates, and India-specific market data.
"""

# ---------------------------------------------------------------------------
# Assessment Questions
# ---------------------------------------------------------------------------

INTEREST_QUESTIONS = [
    {
        "id": 1, "text": "I enjoy working with tools, machines, or building things.",
        "options": [
            {"text": "Strongly Agree", "value": 4, "riasec": "R"},
            {"text": "Agree", "value": 3, "riasec": "R"},
            {"text": "Neutral", "value": 2, "riasec": None},
            {"text": "Disagree", "value": 1, "riasec": None},
        ]
    },
    {
        "id": 2, "text": "I like solving complex puzzles and analysing data.",
        "options": [
            {"text": "Strongly Agree", "value": 4, "riasec": "I"},
            {"text": "Agree", "value": 3, "riasec": "I"},
            {"text": "Neutral", "value": 2, "riasec": None},
            {"text": "Disagree", "value": 1, "riasec": None},
        ]
    },
    {
        "id": 3, "text": "I express myself through art, music, writing, or design.",
        "options": [
            {"text": "Strongly Agree", "value": 4, "riasec": "A"},
            {"text": "Agree", "value": 3, "riasec": "A"},
            {"text": "Neutral", "value": 2, "riasec": None},
            {"text": "Disagree", "value": 1, "riasec": None},
        ]
    },
    {
        "id": 4, "text": "I enjoy helping, teaching, or counselling other people.",
        "options": [
            {"text": "Strongly Agree", "value": 4, "riasec": "S"},
            {"text": "Agree", "value": 3, "riasec": "S"},
            {"text": "Neutral", "value": 2, "riasec": None},
            {"text": "Disagree", "value": 1, "riasec": None},
        ]
    },
    {
        "id": 5, "text": "I like leading projects, persuading people, or starting businesses.",
        "options": [
            {"text": "Strongly Agree", "value": 4, "riasec": "E"},
            {"text": "Agree", "value": 3, "riasec": "E"},
            {"text": "Neutral", "value": 2, "riasec": None},
            {"text": "Disagree", "value": 1, "riasec": None},
        ]
    },
    {
        "id": 6, "text": "I prefer organised, structured tasks with clear rules and procedures.",
        "options": [
            {"text": "Strongly Agree", "value": 4, "riasec": "C"},
            {"text": "Agree", "value": 3, "riasec": "C"},
            {"text": "Neutral", "value": 2, "riasec": None},
            {"text": "Disagree", "value": 1, "riasec": None},
        ]
    },
    {
        "id": 7, "text": "I am curious about how technology and computers work.",
        "options": [
            {"text": "Strongly Agree", "value": 4, "riasec": "I"},
            {"text": "Agree", "value": 3, "riasec": "I"},
            {"text": "Neutral", "value": 2, "riasec": None},
            {"text": "Disagree", "value": 1, "riasec": None},
        ]
    },
    {
        "id": 8, "text": "I enjoy outdoor activities, sports, or working with nature.",
        "options": [
            {"text": "Strongly Agree", "value": 4, "riasec": "R"},
            {"text": "Agree", "value": 3, "riasec": "R"},
            {"text": "Neutral", "value": 2, "riasec": None},
            {"text": "Disagree", "value": 1, "riasec": None},
        ]
    },
    {
        "id": 9, "text": "I like managing finances, budgets, or business operations.",
        "options": [
            {"text": "Strongly Agree", "value": 4, "riasec": "C"},
            {"text": "Agree", "value": 3, "riasec": "C"},
            {"text": "Neutral", "value": 2, "riasec": None},
            {"text": "Disagree", "value": 1, "riasec": None},
        ]
    },
    {
        "id": 10, "text": "I enjoy public speaking, debates, or presenting ideas.",
        "options": [
            {"text": "Strongly Agree", "value": 4, "riasec": "E"},
            {"text": "Agree", "value": 3, "riasec": "E"},
            {"text": "Neutral", "value": 2, "riasec": None},
            {"text": "Disagree", "value": 1, "riasec": None},
        ]
    },
    {
        "id": 11, "text": "I like designing websites, apps, or visual content.",
        "options": [
            {"text": "Strongly Agree", "value": 4, "riasec": "A"},
            {"text": "Agree", "value": 3, "riasec": "A"},
            {"text": "Neutral", "value": 2, "riasec": None},
            {"text": "Disagree", "value": 1, "riasec": None},
        ]
    },
    {
        "id": 12, "text": "I am interested in medicine, healthcare, or helping people's health.",
        "options": [
            {"text": "Strongly Agree", "value": 4, "riasec": "S"},
            {"text": "Agree", "value": 3, "riasec": "S"},
            {"text": "Neutral", "value": 2, "riasec": None},
            {"text": "Disagree", "value": 1, "riasec": None},
        ]
    },
]

PERSONALITY_QUESTIONS = [
    {"id": 101, "text": "I feel energised by social interactions and meeting new people.", "trait": "extraversion"},
    {"id": 102, "text": "I prefer to plan ahead rather than be spontaneous.", "trait": "conscientiousness"},
    {"id": 103, "text": "I enjoy learning about new ideas, even unrelated to my work.", "trait": "openness"},
    {"id": 104, "text": "I tend to stay calm even in stressful situations.", "trait": "stability"},
    {"id": 105, "text": "I often put others' needs before my own.", "trait": "agreeableness"},
    {"id": 106, "text": "I like to take charge and lead in group settings.", "trait": "extraversion"},
    {"id": 107, "text": "I am detail-oriented and like completing tasks thoroughly.", "trait": "conscientiousness"},
    {"id": 108, "text": "I think creatively and come up with original solutions.", "trait": "openness"},
]

APTITUDE_QUESTIONS = [
    {
        "id": 201,
        "text": "If a train travels at 60 km/h for 2.5 hours, what distance does it cover?",
        "type": "numerical",
        "options": ["120 km", "150 km", "180 km", "100 km"],
        "correct": 1,
    },
    {
        "id": 202,
        "text": "Choose the word that means the OPPOSITE of 'Eloquent'.",
        "type": "verbal",
        "options": ["Fluent", "Inarticulate", "Articulate", "Expressive"],
        "correct": 1,
    },
    {
        "id": 203,
        "text": "What comes next in the series: 2, 6, 12, 20, 30, ?",
        "type": "logical",
        "options": ["40", "42", "44", "36"],
        "correct": 1,
    },
    {
        "id": 204,
        "text": "If P = Q + 5 and Q = 10, what is 2P + Q?",
        "type": "numerical",
        "options": ["40", "45", "50", "35"],
        "correct": 1,
    },
    {
        "id": 205,
        "text": "Find the odd one out: Cricket, Football, Chess, Swimming, Tennis.",
        "type": "logical",
        "options": ["Cricket", "Chess", "Tennis", "Football"],
        "correct": 1,
    },
    {
        "id": 206,
        "text": "Rearrange: 'NGEENIR' to find a profession.",
        "type": "verbal",
        "options": ["ENGINEER", "GREENING", "ERRINGEN", "REIGNING"],
        "correct": 0,
    },
]

READINESS_QUESTIONS = [
    {"id": 301, "text": "I have a clear idea of the career I want to pursue.", "category": "self_awareness"},
    {"id": 302, "text": "I know the key skills required for my target career.", "category": "market_knowledge"},
    {"id": 303, "text": "I have spoken to professionals in my target field.", "category": "networking"},
    {"id": 304, "text": "I have taken relevant courses or certifications.", "category": "skills"},
    {"id": 305, "text": "I have researched the job market demand for my career.", "category": "market_knowledge"},
    {"id": 306, "text": "I have a written career action plan.", "category": "planning"},
    {"id": 307, "text": "I know my key strengths and weaknesses.", "category": "self_awareness"},
    {"id": 308, "text": "I have a strong online presence (LinkedIn/portfolio).", "category": "networking"},
]

# ---------------------------------------------------------------------------
# Career Database — 50+ careers with full metadata
# ---------------------------------------------------------------------------

CAREERS = {
    # Technology
    "software_engineer": {
        "title": "Software Engineer",
        "domain": "Technology",
        "riasec": ["I", "R", "C"],
        "description": "Design, develop, and maintain software systems and applications.",
        "avg_salary_india": "₹6–25 LPA",
        "growth_rate": "22%",
        "education": ["B.Tech/BE (CS/IT)", "BCA + MCA", "BSc CS"],
        "key_skills": ["Python", "Java", "Data Structures", "Algorithms", "System Design"],
        "top_companies": ["TCS", "Infosys", "Wipro", "Google", "Microsoft", "Amazon"],
        "difficulty": "medium",
        "demand": "very_high",
    },
    "data_scientist": {
        "title": "Data Scientist",
        "domain": "Technology",
        "riasec": ["I", "C", "R"],
        "description": "Analyse complex data to derive insights and build predictive models.",
        "avg_salary_india": "₹8–30 LPA",
        "growth_rate": "36%",
        "education": ["B.Tech CS/Stats", "MSc Statistics", "MBA Analytics"],
        "key_skills": ["Python", "Machine Learning", "SQL", "Statistics", "Tableau"],
        "top_companies": ["Flipkart", "Paytm", "Mu Sigma", "Fractal Analytics", "Amazon"],
        "difficulty": "high",
        "demand": "very_high",
    },
    "product_manager": {
        "title": "Product Manager",
        "domain": "Technology",
        "riasec": ["E", "I", "S"],
        "description": "Define product vision and drive execution across teams.",
        "avg_salary_india": "₹10–40 LPA",
        "growth_rate": "18%",
        "education": ["Any B.Tech/BE", "MBA (preferred)"],
        "key_skills": ["Product Strategy", "Data Analysis", "Stakeholder Management", "Agile"],
        "top_companies": ["Zomato", "Swiggy", "Flipkart", "Razorpay", "Google"],
        "difficulty": "high",
        "demand": "high",
    },
    "ui_ux_designer": {
        "title": "UI/UX Designer",
        "domain": "Design",
        "riasec": ["A", "I", "S"],
        "description": "Create intuitive and beautiful digital experiences for users.",
        "avg_salary_india": "₹4–18 LPA",
        "growth_rate": "23%",
        "education": ["BDes", "B.Tech + Design course", "BA Design"],
        "key_skills": ["Figma", "User Research", "Prototyping", "Adobe XD", "CSS"],
        "top_companies": ["Swiggy", "Dream11", "InMobi", "UrbanCompany", "Airbnb India"],
        "difficulty": "medium",
        "demand": "high",
    },
    "cybersecurity_analyst": {
        "title": "Cybersecurity Analyst",
        "domain": "Technology",
        "riasec": ["I", "R", "C"],
        "description": "Protect digital systems and networks from cyber threats.",
        "avg_salary_india": "₹5–20 LPA",
        "growth_rate": "31%",
        "education": ["B.Tech CS/IT", "BCA", "CEH/CISSP Certification"],
        "key_skills": ["Network Security", "Ethical Hacking", "SIEM", "Linux", "Python"],
        "top_companies": ["Wipro", "HCL", "IBM", "Deloitte", "PwC"],
        "difficulty": "high",
        "demand": "very_high",
    },
    # Business & Finance
    "investment_banker": {
        "title": "Investment Banker",
        "domain": "Finance",
        "riasec": ["E", "C", "I"],
        "description": "Advise companies on mergers, acquisitions, and capital raising.",
        "avg_salary_india": "₹8–50 LPA",
        "growth_rate": "14%",
        "education": ["CA", "MBA Finance", "CFA"],
        "key_skills": ["Financial Modelling", "Valuation", "Excel", "Pitching", "M&A"],
        "top_companies": ["Goldman Sachs", "JP Morgan", "Morgan Stanley", "ICICI Securities"],
        "difficulty": "very_high",
        "demand": "medium",
    },
    "marketing_manager": {
        "title": "Marketing Manager",
        "domain": "Business",
        "riasec": ["E", "A", "S"],
        "description": "Lead brand strategy, campaigns, and market growth.",
        "avg_salary_india": "₹6–22 LPA",
        "growth_rate": "10%",
        "education": ["MBA Marketing", "BBA", "BMM"],
        "key_skills": ["Digital Marketing", "Brand Strategy", "Analytics", "Content", "SEO"],
        "top_companies": ["HUL", "P&G", "Nestlé", "Flipkart", "Zomato"],
        "difficulty": "medium",
        "demand": "high",
    },
    "ca_chartered_accountant": {
        "title": "Chartered Accountant",
        "domain": "Finance",
        "riasec": ["C", "I", "E"],
        "description": "Handle audits, taxation, financial reporting, and advisory.",
        "avg_salary_india": "₹6–30 LPA",
        "growth_rate": "8%",
        "education": ["CA (ICAI)", "B.Com + CA"],
        "key_skills": ["Accounting", "Taxation", "Auditing", "Tally", "GST"],
        "top_companies": ["Big 4 (Deloitte/EY/PwC/KPMG)", "HDFC Bank", "Reliance", "TCS"],
        "difficulty": "very_high",
        "demand": "high",
    },
    # Healthcare
    "doctor_physician": {
        "title": "Doctor (MBBS/MD)",
        "domain": "Healthcare",
        "riasec": ["I", "S", "R"],
        "description": "Diagnose and treat patients in clinical or hospital settings.",
        "avg_salary_india": "₹6–30 LPA",
        "growth_rate": "15%",
        "education": ["MBBS", "MBBS + MD/MS"],
        "key_skills": ["Clinical Skills", "Diagnosis", "Patient Care", "Medical Knowledge"],
        "top_companies": ["AIIMS", "Apollo", "Fortis", "Max Healthcare", "Govt Hospitals"],
        "difficulty": "very_high",
        "demand": "very_high",
    },
    "clinical_psychologist": {
        "title": "Clinical Psychologist",
        "domain": "Healthcare",
        "riasec": ["S", "I", "A"],
        "description": "Assess, diagnose, and treat mental health conditions.",
        "avg_salary_india": "₹4–15 LPA",
        "growth_rate": "25%",
        "education": ["MA/MSc Psychology", "MPhil Clinical Psychology", "PhD"],
        "key_skills": ["Counselling", "Psychotherapy", "Assessment", "CBT"],
        "top_companies": ["NIMHANS", "Hospitals", "NGOs", "Private Practice"],
        "difficulty": "high",
        "demand": "high",
    },
    # Education
    "professor_educator": {
        "title": "Professor / Educator",
        "domain": "Education",
        "riasec": ["S", "I", "A"],
        "description": "Teach, research, and mentor students at academic institutions.",
        "avg_salary_india": "₹5–20 LPA",
        "growth_rate": "8%",
        "education": ["MA/MSc + BEd", "MTech + PhD", "PhD preferred"],
        "key_skills": ["Subject Expertise", "Communication", "Research", "Curriculum Design"],
        "top_companies": ["IITs", "NITs", "Private Universities", "EdTech Companies"],
        "difficulty": "high",
        "demand": "medium",
    },
    # Creative
    "content_creator": {
        "title": "Content Creator / YouTuber",
        "domain": "Creative",
        "riasec": ["A", "E", "S"],
        "description": "Create digital content for platforms like YouTube, Instagram, podcasts.",
        "avg_salary_india": "₹2–50 LPA (variable)",
        "growth_rate": "40%",
        "education": ["Any degree", "Media/Journalism preferred"],
        "key_skills": ["Video Editing", "Storytelling", "SEO", "Social Media", "Analytics"],
        "top_companies": ["Self-employed", "Media Houses", "Agencies"],
        "difficulty": "medium",
        "demand": "very_high",
    },
    "graphic_designer": {
        "title": "Graphic Designer",
        "domain": "Design",
        "riasec": ["A", "R", "I"],
        "description": "Create visual content for brands, marketing, and digital media.",
        "avg_salary_india": "₹2–12 LPA",
        "growth_rate": "12%",
        "education": ["BDes", "BFA", "Certificate in Graphic Design"],
        "key_skills": ["Adobe Illustrator", "Photoshop", "InDesign", "Typography", "Figma"],
        "top_companies": ["Ogilvy", "WPP", "Dentsu", "InMobi", "Freelance"],
        "difficulty": "medium",
        "demand": "high",
    },
    # Civil Services
    "ias_officer": {
        "title": "IAS / Civil Services Officer",
        "domain": "Government",
        "riasec": ["E", "S", "I"],
        "description": "Lead public administration and policy implementation across India.",
        "avg_salary_india": "₹6–20 LPA + perks",
        "growth_rate": "Stable",
        "education": ["Any Graduation (UPSC CSAT)"],
        "key_skills": ["General Knowledge", "Essay Writing", "Leadership", "Analytics"],
        "top_companies": ["Government of India", "State Governments"],
        "difficulty": "very_high",
        "demand": "stable",
    },
    # Law
    "lawyer": {
        "title": "Lawyer / Advocate",
        "domain": "Law",
        "riasec": ["E", "I", "S"],
        "description": "Represent clients, argue cases, and provide legal counsel.",
        "avg_salary_india": "₹4–25 LPA",
        "growth_rate": "15%",
        "education": ["LLB (3-year)", "BA LLB / BBA LLB (5-year)", "LLM"],
        "key_skills": ["Legal Research", "Argumentation", "Writing", "Negotiation"],
        "top_companies": ["Law Firms", "Corporate Legal Depts", "Courts"],
        "difficulty": "high",
        "demand": "high",
    },
    # Engineering
    "mechanical_engineer": {
        "title": "Mechanical Engineer",
        "domain": "Engineering",
        "riasec": ["R", "I", "C"],
        "description": "Design and build mechanical systems, machines, and infrastructure.",
        "avg_salary_india": "₹4–15 LPA",
        "growth_rate": "7%",
        "education": ["B.Tech/BE Mechanical"],
        "key_skills": ["CAD/CAM", "Thermodynamics", "Manufacturing", "AutoCAD", "SolidWorks"],
        "top_companies": ["L&T", "BHEL", "Tata Motors", "Mahindra", "DRDO"],
        "difficulty": "high",
        "demand": "medium",
    },
    # Management
    "entrepreneur": {
        "title": "Entrepreneur / Startup Founder",
        "domain": "Business",
        "riasec": ["E", "A", "I"],
        "description": "Build and scale your own business or startup.",
        "avg_salary_india": "Variable (₹0–unlimited)",
        "growth_rate": "N/A",
        "education": ["Any degree", "MBA helps", "Self-taught"],
        "key_skills": ["Leadership", "Sales", "Product Thinking", "Fundraising", "Resilience"],
        "top_companies": ["Self-founded", "Y Combinator", "Sequoia Backed"],
        "difficulty": "very_high",
        "demand": "high",
    },
    "hr_manager": {
        "title": "HR Manager",
        "domain": "Business",
        "riasec": ["S", "E", "C"],
        "description": "Manage talent acquisition, employee engagement, and HR strategy.",
        "avg_salary_india": "₹5–18 LPA",
        "growth_rate": "10%",
        "education": ["MBA HR", "BBA + MBA", "MSW"],
        "key_skills": ["Recruitment", "HRIS", "Labour Law", "Training & Development"],
        "top_companies": ["Infosys HR", "TCS", "HDFC Bank", "Deloitte"],
        "difficulty": "medium",
        "demand": "medium",
    },
}

# RIASEC code → top career matches
RIASEC_CAREER_MAP = {
    "R": ["mechanical_engineer", "software_engineer", "cybersecurity_analyst"],
    "I": ["data_scientist", "doctor_physician", "software_engineer", "cybersecurity_analyst"],
    "A": ["ui_ux_designer", "graphic_designer", "content_creator"],
    "S": ["clinical_psychologist", "professor_educator", "hr_manager", "doctor_physician"],
    "E": ["entrepreneur", "investment_banker", "marketing_manager", "ias_officer", "lawyer"],
    "C": ["ca_chartered_accountant", "data_scientist", "mechanical_engineer"],
}

# ---------------------------------------------------------------------------
# Roadmap Templates
# ---------------------------------------------------------------------------

ROADMAP_TEMPLATES = {
    "software_engineer": {
        "3_months": [
            {"title": "Master a programming language", "description": "Focus on Python or Java — complete an online course (Coursera / NPTEL).", "type": "learning"},
            {"title": "Build 2 portfolio projects", "description": "Create a web app and a CLI tool. Push to GitHub.", "type": "project"},
            {"title": "Learn Data Structures & Algorithms", "description": "Solve 50+ problems on LeetCode (Easy + Medium).", "type": "learning"},
        ],
        "6_months": [
            {"title": "Open Source Contribution", "description": "Make 3+ merged pull requests on GitHub.", "type": "project"},
            {"title": "System Design Basics", "description": "Study caching, load balancing, databases — read Designing Data-Intensive Apps.", "type": "learning"},
            {"title": "Internship / Freelance project", "description": "Apply for internships on Internshala / LinkedIn. Aim for 1 paid project.", "type": "career"},
        ],
        "1_year": [
            {"title": "Land a full-time position", "description": "Apply to 20+ companies with strong resume + GitHub profile.", "type": "career"},
            {"title": "Get AWS/GCP certification", "description": "AWS Cloud Practitioner or Google Associate Cloud Engineer.", "type": "certification"},
            {"title": "Build a SaaS project", "description": "Launch a small product — even if it earns ₹0, the learning is invaluable.", "type": "project"},
        ],
        "3_years": [
            {"title": "Senior Software Engineer", "description": "Lead a team, own a module, mentor juniors.", "type": "career"},
            {"title": "Specialise in an area", "description": "Pick: Backend, Frontend, ML, DevOps, Mobile — go deep.", "type": "learning"},
        ],
        "5_years": [
            {"title": "Tech Lead / Engineering Manager", "description": "Lead an engineering team of 5–10 people.", "type": "career"},
            {"title": "Consider FAANG / Startup CTO", "description": "Apply to top-tier companies or join an early-stage startup as CTO.", "type": "career"},
        ],
    },
    "data_scientist": {
        "3_months": [
            {"title": "Python for Data Science", "description": "Master NumPy, Pandas, Matplotlib, Scikit-learn.", "type": "learning"},
            {"title": "Statistics Foundation", "description": "Study probability, distributions, hypothesis testing.", "type": "learning"},
            {"title": "Kaggle beginner competitions", "description": "Complete 2 beginner competitions and publish notebooks.", "type": "project"},
        ],
        "6_months": [
            {"title": "Machine Learning fundamentals", "description": "Complete Andrew Ng's ML course. Implement 5 algorithms from scratch.", "type": "learning"},
            {"title": "SQL + Database skills", "description": "Master SQL queries and database design for analytics.", "type": "learning"},
            {"title": "End-to-end ML project", "description": "Build a deployed ML model (e.g., churn prediction). Host on Streamlit.", "type": "project"},
        ],
        "1_year": [
            {"title": "Deep Learning basics", "description": "TensorFlow or PyTorch — complete one specialisation.", "type": "learning"},
            {"title": "Data Science internship", "description": "Apply to analytics firms: Mu Sigma, Fractal, Latentview.", "type": "career"},
        ],
        "3_years": [
            {"title": "Data Science role at product company", "description": "Target Flipkart, Amazon, Ola, or BFSI firms.", "type": "career"},
        ],
        "5_years": [
            {"title": "Lead Data Scientist or ML Engineer", "description": "Own ML systems at scale, build data platforms.", "type": "career"},
        ],
    },
    "default": {
        "3_months": [
            {"title": "Research your target career deeply", "description": "Spend 30 minutes/day reading about job roles, skills, and companies.", "type": "learning"},
            {"title": "Identify 3 skill gaps", "description": "Compare your current skills to job descriptions. Start one online course.", "type": "learning"},
            {"title": "Update your LinkedIn profile", "description": "Add a strong headline, summary, and connect with 50+ professionals.", "type": "networking"},
        ],
        "6_months": [
            {"title": "Complete 2 relevant certifications", "description": "Choose industry-recognised certifications in your field.", "type": "certification"},
            {"title": "Informational interviews", "description": "Have conversations with 5+ professionals in your target field.", "type": "networking"},
            {"title": "Build a portfolio", "description": "Document your projects, skills, and achievements.", "type": "project"},
        ],
        "1_year": [
            {"title": "Apply for entry-level roles", "description": "Target 30+ companies with tailored applications.", "type": "career"},
            {"title": "Attend industry events", "description": "Join professional associations and attend 4+ events/meetups.", "type": "networking"},
        ],
        "3_years": [
            {"title": "Become a subject matter expert", "description": "Deepen expertise in 1–2 core areas of your field.", "type": "learning"},
            {"title": "Take on leadership responsibilities", "description": "Lead a small team, project, or initiative.", "type": "career"},
        ],
        "5_years": [
            {"title": "Senior / Manager level position", "description": "Position yourself for leadership or specialist roles.", "type": "career"},
            {"title": "Build your professional brand", "description": "Speak at conferences, write articles, mentor others.", "type": "networking"},
        ],
    }
}

# ---------------------------------------------------------------------------
# Learning Resources
# ---------------------------------------------------------------------------

LEARNING_RESOURCES = {
    "Python": [
        {"title": "Python for Everybody (Coursera)", "url": "https://coursera.org", "type": "course", "free": True},
        {"title": "NPTEL Python Programming", "url": "https://nptel.ac.in", "type": "course", "free": True},
        {"title": "Automate the Boring Stuff", "url": "https://automatetheboringstuff.com", "type": "book", "free": True},
    ],
    "Machine Learning": [
        {"title": "Andrew Ng's ML Course (Coursera)", "url": "https://coursera.org", "type": "course", "free": False},
        {"title": "Kaggle Learn", "url": "https://kaggle.com/learn", "type": "course", "free": True},
        {"title": "Fast.ai", "url": "https://fast.ai", "type": "course", "free": True},
    ],
    "Data Analysis": [
        {"title": "Google Data Analytics (Coursera)", "url": "https://coursera.org", "type": "course", "free": False},
        {"title": "IBM Data Science Professional", "url": "https://coursera.org", "type": "course", "free": False},
    ],
    "Digital Marketing": [
        {"title": "Google Digital Marketing (free)", "url": "https://grow.google", "type": "course", "free": True},
        {"title": "HubSpot Marketing Certification", "url": "https://hubspot.com/academy", "type": "course", "free": True},
    ],
    "Finance": [
        {"title": "Financial Markets (Coursera - Yale)", "url": "https://coursera.org", "type": "course", "free": False},
        {"title": "Zerodha Varsity", "url": "https://zerodha.com/varsity", "type": "course", "free": True},
    ],
    "Design": [
        {"title": "Google UX Design Certificate", "url": "https://coursera.org", "type": "course", "free": False},
        {"title": "Figma Tutorial (YouTube)", "url": "https://youtube.com", "type": "video", "free": True},
    ],
}

# Skill → learning resources mapping
SKILL_RESOURCES = {
    skill: LEARNING_RESOURCES.get(skill, [])
    for skill in ["Python", "Machine Learning", "Data Analysis", "Digital Marketing", "Finance", "Design"]
}

# Market trends (India-specific)
MARKET_TRENDS = [
    {"domain": "Technology", "trend": "AI/ML roles growing 40% YoY — highest demand in India", "impact": "positive"},
    {"domain": "Technology", "trend": "Cloud computing skills (AWS/Azure/GCP) commanding 30–50% salary premium", "impact": "positive"},
    {"domain": "Finance", "trend": "Fintech companies hiring 2x compared to traditional banks", "impact": "positive"},
    {"domain": "Healthcare", "trend": "Telemedicine and health-tech creating new hybrid roles", "impact": "positive"},
    {"domain": "Creative", "trend": "Creator economy projected to hit $104B globally; India is #2 market", "impact": "positive"},
    {"domain": "Government", "trend": "UPSC vacancies stable; digital governance creating new roles", "impact": "neutral"},
    {"domain": "Business", "trend": "MBA graduates with tech skills earning 40% more", "impact": "positive"},
]
