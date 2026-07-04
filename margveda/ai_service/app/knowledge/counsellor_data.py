"""Counsellor knowledge base — career counselling frameworks, assessment tools, and guidance methodologies."""
from __future__ import annotations

COUNSELLOR_KNOWLEDGE = [
    {
        "id": "holland_codes",
        "title": "Holland Codes (RIASEC Theory)",
        "domain": "counsellor",
        "content": """
Holland Codes (also called RIASEC) is the most widely used career assessment framework.
Developed by psychologist John Holland, it classifies people into 6 personality types:

R — Realistic: Prefer working with tools, machines, or outdoors. Careers: Engineering, Skilled trades, Agriculture, Military.

I — Investigative: Prefer analytical, intellectual, and scientific activities. Careers: Research scientist, Doctor, Data scientist, Economist.

A — Artistic: Prefer creative, expressive, and original activities. Careers: Designer, Journalist, Architect, Musician, Writer.

S — Social: Prefer helping, teaching, and working with others. Careers: Teacher, Counsellor, Nurse, HR professional, Social worker.

E — Enterprising: Prefer leading, influencing, and business activities. Careers: Entrepreneur, Manager, Lawyer, Investment banker, Sales.

C — Conventional: Prefer structured, data-based, and orderly activities. Careers: Accountant, CA, Office Manager, Financial analyst, Bank clerk.

Most people have 2-3 dominant types. The combination predicts career fit:
- SE (Social-Enterprising) → HR, Counselling, Non-profits, NGOs
- IR (Investigative-Realistic) → Engineering research, Medical science, Data science
- AE (Artistic-Enterprising) → Marketing, Brand management, Media entrepreneurship
- EC (Enterprising-Conventional) → Business, Finance, Banking, Administration

Counsellors administer Holland Code assessments using standardised tests.
Free online version: O*NET Interest Profiler at mynextmove.org
""",
    },
    {
        "id": "multiple_intelligences",
        "title": "Howard Gardner's Multiple Intelligences",
        "domain": "counsellor",
        "content": """
Howard Gardner proposed 9 types of intelligence, rejecting the idea of a single IQ score.
Counsellors use this framework to identify hidden strengths in students who may underperform academically.

1. Linguistic: Strong reading, writing, speaking. → Lawyer, Journalist, Teacher, Politician
2. Logical-Mathematical: Strong reasoning and numbers. → Engineer, Scientist, Programmer, Accountant
3. Spatial: Strong visualisation and spatial reasoning. → Architect, Surgeon, Designer, Pilot
4. Musical: Strong rhythm, music, sound patterns. → Musician, Sound engineer, Music therapist
5. Bodily-Kinesthetic: Strong body coordination and movement. → Athlete, Surgeon, Actor, Physical therapist
6. Interpersonal: Strong empathy and social understanding. → Counsellor, Teacher, Manager, Politician
7. Intrapersonal: Strong self-awareness and reflection. → Writer, Researcher, Psychologist, Entrepreneur
8. Naturalist: Strong observation of natural world. → Biologist, Geographer, Chef, Landscape designer
9. Existential: Strong philosophical questioning. → Philosopher, Religious leader, Life coach

Using MI in counselling:
- Helps students reframe "I'm not smart" → "I have a different type of intelligence"
- Particularly valuable for students who score low on standardised tests
- Pair MI results with Holland Codes for a comprehensive career match
""",
    },
    {
        "id": "career_anchors_schein",
        "title": "Career Anchors (Edgar Schein)",
        "domain": "counsellor",
        "content": """
Career Anchors are the self-concept that an individual uses as a compass when making career decisions.
Developed by MIT Professor Edgar Schein through longitudinal research on MBA graduates.

The 8 Career Anchors:
1. Technical/Functional Competence: Satisfaction from being expert in a specific field. Resist general management roles.
2. General Managerial Competence: Desire to manage, coordinate, and lead. Want the top of the hierarchy.
3. Security/Stability: Prioritise job security over advancement. Government jobs, large corporations, PSUs.
4. Entrepreneurial Creativity: Driven to build something of their own. Startups, freelancing, own business.
5. Autonomy/Independence: Resist being tied down by rules. Consultants, academics, self-employed.
6. Service/Dedication to a Cause: Motivated by helping others or making a difference. NGOs, medicine, teaching.
7. Pure Challenge: Seek challenges and novelty. Mountain climbing, special forces, problem-solving roles.
8. Lifestyle: Want to integrate career with personal values and family. Flexible work, work-life balance.

Counselling application:
- Career Anchors are discovered through career history and interview — not just self-report
- Most relevant for adults with 2+ years of work experience
- Students (Class 12) often haven't discovered their anchors yet — use Holland Codes instead
- Most reliable for identifying what people will NOT compromise on in their career
""",
    },
    {
        "id": "counselling_process",
        "title": "Career Counselling Process (Step-by-Step)",
        "domain": "counsellor",
        "content": """
A structured career counselling process for Indian students:

Step 1 — Intake (30 minutes)
- Understand student's current situation: class, stream, board marks, family background
- Ask about interests, hobbies, extracurricular activities
- Understand parental expectations and family pressures (common in India)
- Identify any academic distress signals

Step 2 — Assessment (60 minutes)
- Administer appropriate assessments:
  * Holland Codes (RIASEC): interests and personality type
  * Multiple Intelligences inventory: dominant strengths
  * Aptitude tests: verbal, numerical, spatial, logical reasoning
  * Values clarification: what matters most (money, impact, creativity, stability)
- Do NOT use DMIT (Dermatoglyphics Multiple Intelligence Test) — it is not scientifically validated

Step 3 — Career Exploration (45 minutes)
- Present 3-4 career options that align with assessment results
- Discuss each option: job roles, salary, required education, growth path
- Address common myths ("Arts students can't earn well", "Engineering is the only option")
- Use CareerBrownie database for real salary, entrance exam, and college data

Step 4 — Education Path Mapping (30 minutes)
- Identify entrance exams required for chosen career
- Map the academic timeline: Class 12 → Entrance Exam → College → Career
- Identify gaps: subjects to improve, skills to build, certifications to pursue
- Provide action plan with specific next steps for the next 30 days

Step 5 — Follow-Up (ongoing)
- Schedule follow-up session in 4-6 weeks
- Track action plan completion
- Adjust recommendations based on exam results, changing interests
- Parent counselling session: align parental expectations with student's strengths

Common Challenges in Indian Career Counselling:
- Parental pressure towards engineering/medicine: gently redirect by showing salary/growth data for alternative careers
- First-generation learners: extra support needed for information about college admissions, scholarships
- Students with anxiety/depression: refer to clinical psychologist before career counselling
- "My child is average": reframe "average" — most successful careers don't require top-1% academic performance
""",
    },
    {
        "id": "common_student_concerns",
        "title": "Common Student Questions and Counsellor Responses",
        "domain": "counsellor",
        "content": """
Frequently encountered student concerns and evidence-based counsellor responses:

Q: "I scored only 70% in Class 12. Is my career over?"
A: Absolutely not. Most successful professionals did not top their boards.
   - Many top companies do not check Class 12 marks after 2-3 years of work experience
   - Entrance exam performance (JEE, NEET, CAT) matters more than board scores
   - Skills and portfolio matter more than percentages in technology, design, entrepreneurship
   - Recommended path: identify strengths, build skills, pursue relevant certifications

Q: "My parents want me to do engineering but I want to study art/design/commerce"
A: This is the most common conflict in Indian families. Approach:
   - Show salary data: Good designers earn ₹15-60 LPA (comparable to many engineers)
   - Show job security: India's design industry is growing at 15% annually
   - Propose a compromise: arts + business = UX design, brand management, advertising
   - Suggest a structured trial: one year of pursuing the interest with measurable outcomes
   - Use Holland Code results as objective evidence for your interests

Q: "I want to become an IAS officer but my parents think it's risky"
A: UPSC success is low probability but the career impact is very high.
   - Explain the risk honestly: 0.1% selection rate, 4-6 years of preparation
   - Offer a parallel strategy: pursue graduation AND UPSC preparation simultaneously
   - Have a backup plan: CAT/MBA or corporate job if UPSC doesn't work in 3-4 attempts
   - IAS is a life-defining career; financial security is guaranteed even at failure

Q: "I failed JEE/NEET. What now?"
A: One exam does not define a career. Options:
   - Repeat year (drop year) for second attempt — works if gap year is disciplined
   - Alternative entrance exams: BITSAT, MET, VIT, COMEDK for engineering; AIIMS-like state exams for medical
   - Alternative careers: commerce/management for former PCM students; pharmacy/biotech for former PCB
   - Direct skill-based careers: Data science bootcamp, design, digital marketing (no entrance exam needed)

Q: "I don't know what I want to do"
A: "I don't know" is normal for 16-18 year olds. Process:
   - Conduct Holland Code + Multiple Intelligence assessment
   - Ask: "What do you find yourself doing when you have no homework?"
   - Explore internship/shadowing opportunities in 2-3 interest areas
   - Recommend starting with a broad Bachelor's degree (B.Sc, BBA) that keeps options open
   - Remind: Most people change careers 2-3 times; the first choice doesn't have to be perfect

Tools counsellors should NOT use or recommend:
- DMIT (Dermatoglyphics) — no scientific basis; avoid
- Graphology (handwriting analysis) — no scientific validity
- Numerology/astrology for career guidance — not evidence-based
- Guaranteed IAS coaching claims — always check track record
""",
    },
]


def get_counsellor_documents() -> list[dict]:
    docs = []
    for item in COUNSELLOR_KNOWLEDGE:
        docs.append({
            "id": f"counsellor::{item['id']}",
            "text": item["title"] + "\n" + item["content"].strip(),
            "domain": "counsellor",
            "title": item["title"],
            "metadata": {
                "domain": "counsellor",
                "knowledge_id": item["id"],
                "title": item["title"],
            },
        })
    return docs
