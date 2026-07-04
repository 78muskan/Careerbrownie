"""Skills database — technical and soft skills by domain, with learning resources."""
from __future__ import annotations

SKILL_CLUSTERS = [
    {
        "cluster": "Software Development & Engineering",
        "domain": "technology",
        "skills": [
            {"name": "Python", "level_needed": "Professional", "demand": "Very High",
             "learn_via": "Python.org docs, CS50P (Harvard, free), Automate the Boring Stuff",
             "time_to_learn": "3–6 months to job-ready",
             "why_matters": "Lingua franca of AI/ML, data science, backend, automation. Most in-demand language globally."},
            {"name": "Data Structures & Algorithms (DSA)", "level_needed": "Professional",
             "demand": "Essential for tech interviews",
             "learn_via": "LeetCode, NeetCode.io, Striver's A2Z Sheet (free), Abdul Bari YouTube",
             "time_to_learn": "3–6 months of consistent daily practice",
             "why_matters": "Mandatory for software engineering interviews at every product company."},
            {"name": "System Design", "level_needed": "Senior", "demand": "High for senior roles",
             "learn_via": "System Design Primer (GitHub, free), Grokking System Design, ByteByteGo",
             "time_to_learn": "2–4 months",
             "why_matters": "Determines salary tier at product companies. Required for staff engineer+ roles."},
            {"name": "SQL & Databases", "level_needed": "Professional", "demand": "Very High",
             "learn_via": "SQLZoo (free), Mode Analytics SQL Tutorial, PostgreSQL docs",
             "time_to_learn": "4–8 weeks",
             "why_matters": "Every data-touching role requires SQL proficiency."},
            {"name": "Git & Version Control", "level_needed": "Essential", "demand": "Universal",
             "learn_via": "Atlassian Git Tutorial (free), Oh My Git game",
             "time_to_learn": "1–2 weeks",
             "why_matters": "Non-negotiable for any software role."},
            {"name": "Docker & Kubernetes", "level_needed": "Professional", "demand": "High",
             "learn_via": "Docker official docs, TechWorld with Nana YouTube (free)",
             "time_to_learn": "4–8 weeks",
             "why_matters": "Container orchestration is required for all cloud-native roles."},
            {"name": "React / Next.js", "level_needed": "Professional", "demand": "Very High",
             "learn_via": "React official docs, Josh W. Comeau blog, Theo/t3 YouTube",
             "time_to_learn": "2–4 months",
             "why_matters": "Most in-demand frontend framework; required for frontend and full-stack roles."},
            {"name": "AWS / Cloud (GCP/Azure)", "level_needed": "Professional", "demand": "Very High",
             "learn_via": "AWS Skill Builder (free), Stephane Maarek Udemy courses, A Cloud Guru",
             "time_to_learn": "2–3 months to AWS SAA certification",
             "why_matters": "Nearly every SaaS product is cloud-hosted; cloud skills unlock DevOps/SRE roles."},
        ],
    },
    {
        "cluster": "Data Science & Machine Learning",
        "domain": "data_ai",
        "skills": [
            {"name": "Machine Learning (Scikit-learn)", "level_needed": "Professional", "demand": "Very High",
             "learn_via": "Hands-On ML with Scikit-Learn (Géron), fast.ai course (free), Kaggle Learn",
             "time_to_learn": "3–6 months",
             "why_matters": "Foundation of all ML roles; required for data scientist, ML engineer positions."},
            {"name": "Deep Learning (PyTorch/TensorFlow)", "level_needed": "Professional", "demand": "Very High",
             "learn_via": "fast.ai Part 1+2 (free), deeplearning.ai specialisation (Coursera), PyTorch tutorials",
             "time_to_learn": "4–6 months",
             "why_matters": "Required for computer vision, NLP, and generative AI roles."},
            {"name": "Large Language Models (LLMs)", "level_needed": "Advanced", "demand": "Extremely High (2024-25)",
             "learn_via": "Andrej Karpathy's Neural Networks Zero to Hero (free YouTube), LangChain/LlamaIndex docs",
             "time_to_learn": "2–4 months",
             "why_matters": "Generative AI is the hottest skill in 2024-25; LLM engineers earn 30-50% premium."},
            {"name": "Pandas / NumPy / Matplotlib", "level_needed": "Essential", "demand": "Universal",
             "learn_via": "Kaggle Pandas course (free), Python for Data Analysis (Wes McKinney book)",
             "time_to_learn": "3–4 weeks",
             "why_matters": "The data manipulation toolkit for any Python data role."},
            {"name": "Statistics & Probability", "level_needed": "Professional", "demand": "High",
             "learn_via": "StatQuest YouTube (free), Statistics with Python Specialisation (Coursera)",
             "time_to_learn": "2–3 months",
             "why_matters": "Underpins all ML decisions; required for data scientist interviews."},
            {"name": "MLOps (Model Deployment)", "level_needed": "Senior", "demand": "High",
             "learn_via": "Full Stack Deep Learning (free), MLflow docs, Made With ML",
             "time_to_learn": "2–3 months",
             "why_matters": "Bridges ML research and production — high-paying specialisation."},
        ],
    },
    {
        "cluster": "Business & Finance",
        "domain": "business",
        "skills": [
            {"name": "Financial Modelling (Excel)", "level_needed": "Professional", "demand": "High",
             "learn_via": "WSP (Wall Street Prep), CFI courses, Breaking Into Wall Street (BIWS)",
             "time_to_learn": "4–8 weeks",
             "why_matters": "Required for IB, PE, corporate finance, and consulting roles."},
            {"name": "Valuation (DCF, Comps, LBO)", "level_needed": "Professional", "demand": "High",
             "learn_via": "Damodaran's Valuation course (NYU, free), WSP courses",
             "time_to_learn": "6–8 weeks",
             "why_matters": "Core skill for investment banking and private equity interviews."},
            {"name": "SQL for Business Analysis", "level_needed": "Intermediate", "demand": "High",
             "learn_via": "Mode Analytics, Kaggle Learn SQL",
             "time_to_learn": "3–4 weeks",
             "why_matters": "Business analysts and consultants increasingly need SQL to self-serve data."},
            {"name": "Power BI / Tableau", "level_needed": "Professional", "demand": "High",
             "learn_via": "Microsoft Learn Power BI (free), Tableau Public tutorials",
             "time_to_learn": "4–6 weeks",
             "why_matters": "Required for analytics, business intelligence, and management consulting roles."},
            {"name": "Case Interview Skills", "level_needed": "Professional", "demand": "High for consulting",
             "learn_via": "CaseCoach, Victor Cheng's Case Interview Secrets, McKinsey Problem Solving Game",
             "time_to_learn": "2–3 months (100+ cases to be interview-ready)",
             "why_matters": "Mandatory skill for all consulting firms (McKinsey, BCG, Bain, Deloitte)."},
        ],
    },
    {
        "cluster": "Design & Creative",
        "domain": "design",
        "skills": [
            {"name": "Figma (UX/UI Design)", "level_needed": "Professional", "demand": "Very High",
             "learn_via": "Figma Academy (free), DesignCourse YouTube, Gary Simon tutorials",
             "time_to_learn": "4–6 weeks to intermediate proficiency",
             "why_matters": "Industry standard for product design; required for all UX/UI designer roles."},
            {"name": "User Research Methods", "level_needed": "Professional", "demand": "High",
             "learn_via": "IDEO Design Thinking course, Nielsen Norman Group articles (free)",
             "time_to_learn": "6–8 weeks",
             "why_matters": "Differentiates good designers from great ones; required for senior UX roles."},
            {"name": "Adobe Photoshop & Illustrator", "level_needed": "Professional", "demand": "Moderate",
             "learn_via": "Adobe tutorials (free), Pixel & Bracket YouTube",
             "time_to_learn": "6–8 weeks",
             "why_matters": "Required for graphic design, brand design, and visual communication roles."},
        ],
    },
    {
        "cluster": "Soft Skills (Universal)",
        "domain": "soft_skills",
        "skills": [
            {"name": "Communication (Written & Verbal)", "level_needed": "Essential", "demand": "Universal",
             "learn_via": "Toastmasters (public speaking), Strunk & White 'Elements of Style', daily writing practice",
             "time_to_learn": "Continuous; measurable improvement in 3–6 months",
             "why_matters": "The most career-limiting factor for technical professionals in India. Opens leadership paths."},
            {"name": "Problem Structuring / Analytical Thinking", "level_needed": "Professional", "demand": "Very High",
             "learn_via": "McKinsey Problem Solving Test prep, 'The McKinsey Way' book, logic puzzles",
             "time_to_learn": "2–4 months",
             "why_matters": "Required for consulting, product management, and strategy roles."},
            {"name": "Project Management", "level_needed": "Professional", "demand": "High",
             "learn_via": "PMP Certification (PMI), Google Project Management Certificate (Coursera, free trial)",
             "time_to_learn": "3–6 months for PMP",
             "why_matters": "Required for any leadership role in technology, engineering, or consulting."},
            {"name": "Negotiation", "level_needed": "Intermediate", "demand": "High for leadership",
             "learn_via": "Harvard Negotiation Project materials, 'Never Split the Difference' (book)",
             "time_to_learn": "1–2 months of practice",
             "why_matters": "Critical for salary negotiation, business development, and people management."},
        ],
    },
    {
        "cluster": "Digital Marketing",
        "domain": "marketing",
        "skills": [
            {"name": "Google Ads / SEA", "level_needed": "Professional", "demand": "Very High",
             "learn_via": "Google Skillshop (free certification), WordStream blog, Ahrefs Academy",
             "time_to_learn": "4–6 weeks",
             "why_matters": "Performance marketing is the highest-paying digital marketing specialisation."},
            {"name": "SEO (Search Engine Optimisation)", "level_needed": "Professional", "demand": "High",
             "learn_via": "Moz Beginner's Guide (free), Ahrefs Academy (free), Backlinko blog",
             "time_to_learn": "2–4 months to see measurable results",
             "why_matters": "Organic traffic is cheaper than paid; SEO specialists are in high demand at SaaS companies."},
            {"name": "Meta/Facebook Ads", "level_needed": "Professional", "demand": "Very High",
             "learn_via": "Meta Blueprint certification (free), D2C brand case studies",
             "time_to_learn": "4–6 weeks",
             "why_matters": "D2C brand boom in India creates massive demand for performance marketers."},
            {"name": "Content Marketing & Copywriting", "level_needed": "Professional", "demand": "High",
             "learn_via": "CopyHackers blog, Joanna Wiebe courses, Ann Handley 'Everybody Writes'",
             "time_to_learn": "3–4 months",
             "why_matters": "Content-led growth is most cost-effective; strong writers earn premium."},
        ],
    },
]


def get_skills_documents() -> list[dict]:
    docs = []
    for cluster in SKILL_CLUSTERS:
        text = _cluster_to_text(cluster)
        cluster_id = cluster["cluster"].lower().replace(" ", "_").replace("&", "and")
        docs.append({
            "id": f"skills::{cluster_id}",
            "text": text,
            "domain": "skills",
            "title": f"Skills: {cluster['cluster']}",
            "metadata": {
                "domain": "skills",
                "cluster": cluster["cluster"],
                "industry": cluster.get("domain", ""),
            },
        })
    return docs


def _cluster_to_text(cluster: dict) -> str:
    lines = [
        f"Skill cluster: {cluster['cluster']}",
        f"Domain: {cluster.get('domain', '').replace('_', ' ').title()}",
        "",
    ]
    for skill in cluster.get("skills", []):
        lines.append(f"Skill: {skill['name']}")
        lines.append(f"  Demand: {skill.get('demand', '')}")
        lines.append(f"  Level needed: {skill.get('level_needed', '')}")
        lines.append(f"  Time to learn: {skill.get('time_to_learn', '')}")
        if skill.get("why_matters"):
            lines.append(f"  Why it matters: {skill['why_matters']}")
        if skill.get("learn_via"):
            lines.append(f"  How to learn: {skill['learn_via']}")
        lines.append("")
    return "\n".join(lines)
