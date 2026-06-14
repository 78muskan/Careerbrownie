"""
Interview question bank — HR, Behavioural, Technical, and Mock categories.
"""

HR_QUESTIONS = [
    {"id": "hr_1", "question": "Tell me about yourself.", "category": "hr", "tips": "Use the Present-Past-Future formula. Keep it under 2 minutes. Focus on professional highlights."},
    {"id": "hr_2", "question": "Why do you want to work at this company?", "category": "hr", "tips": "Show research about the company. Connect their values/mission to your goals."},
    {"id": "hr_3", "question": "What are your greatest strengths?", "category": "hr", "tips": "Pick 2–3 strengths relevant to the role. Back each with a specific example."},
    {"id": "hr_4", "question": "What is your biggest weakness?", "category": "hr", "tips": "Be honest about a real weakness. Emphasise what you have done to improve it."},
    {"id": "hr_5", "question": "Where do you see yourself in 5 years?", "category": "hr", "tips": "Show ambition aligned with the company's growth path. Avoid 'at a different company'."},
    {"id": "hr_6", "question": "Why are you leaving your current job?", "category": "hr", "tips": "Keep it positive. Focus on growth opportunities, not complaints about past employer."},
    {"id": "hr_7", "question": "What is your expected salary?", "category": "hr", "tips": "Research market rates. Give a range, not a single number. Emphasise you're flexible."},
    {"id": "hr_8", "question": "Are you willing to relocate or travel?", "category": "hr", "tips": "Be honest. If flexible, say so. If not, explain your situation professionally."},
    {"id": "hr_9", "question": "How do you handle stress and pressure?", "category": "hr", "tips": "Give a concrete example. Mention specific techniques (prioritisation, time-boxing)."},
    {"id": "hr_10", "question": "Do you prefer working alone or in a team?", "category": "hr", "tips": "Show balance — able to work independently and collaboratively. Give examples of both."},
]

BEHAVIOURAL_QUESTIONS = [
    {"id": "beh_1", "question": "Tell me about a time you dealt with a difficult team member.", "category": "behavioural", "competency": "conflict_resolution", "tips": "Use STAR method. Focus on resolution, not blame. Show empathy."},
    {"id": "beh_2", "question": "Describe a situation where you had to meet a tight deadline.", "category": "behavioural", "competency": "time_management", "tips": "Show planning skills. Mention how you prioritised and what the outcome was."},
    {"id": "beh_3", "question": "Give an example of a time you showed leadership.", "category": "behavioural", "competency": "leadership", "tips": "Leadership doesn't require a title. Show initiative, decision-making, team impact."},
    {"id": "beh_4", "question": "Tell me about a failure. What did you learn from it?", "category": "behavioural", "competency": "growth_mindset", "tips": "Be specific. Don't trivialise. Show genuine learning and how you applied it later."},
    {"id": "beh_5", "question": "Describe a time you had to learn a new skill quickly.", "category": "behavioural", "competency": "adaptability", "tips": "Show your learning process. Mention resources, mentors, or methods you used."},
    {"id": "beh_6", "question": "Tell me about a time you disagreed with your manager.", "category": "behavioural", "competency": "professional_maturity", "tips": "Show you can voice disagreement professionally and still execute on the decision."},
    {"id": "beh_7", "question": "Give an example of when you went above and beyond.", "category": "behavioural", "competency": "initiative", "tips": "Quantify the impact. Show you do more than the job description requires."},
    {"id": "beh_8", "question": "Describe a time you received difficult feedback.", "category": "behavioural", "competency": "receptiveness", "tips": "Show you welcomed the feedback and what changed because of it."},
    {"id": "beh_9", "question": "Tell me about a project you are most proud of.", "category": "behavioural", "competency": "achievement_orientation", "tips": "Structure it clearly: context → your role → actions → results. Use numbers."},
    {"id": "beh_10", "question": "Describe a situation where you had to influence someone without authority.", "category": "behavioural", "competency": "influence", "tips": "Show stakeholder management skills. Explain how you built alignment."},
    {"id": "beh_11", "question": "Tell me about a time you had to handle multiple priorities at once.", "category": "behavioural", "competency": "multitasking", "tips": "Show a system: how you evaluated importance vs urgency."},
    {"id": "beh_12", "question": "Give an example of when you took a creative approach to solve a problem.", "category": "behavioural", "competency": "creativity", "tips": "Show the problem clearly. Explain WHY the conventional approach wouldn't work."},
]

TECHNICAL_QUESTIONS = {
    "technology": [
        {"id": "tech_1", "question": "Explain the difference between REST and GraphQL.", "category": "technical", "difficulty": "medium"},
        {"id": "tech_2", "question": "What is the difference between SQL and NoSQL databases?", "category": "technical", "difficulty": "easy"},
        {"id": "tech_3", "question": "Explain what happens when you type a URL into a browser.", "category": "technical", "difficulty": "medium"},
        {"id": "tech_4", "question": "What is a Docker container and how does it differ from a VM?", "category": "technical", "difficulty": "medium"},
        {"id": "tech_5", "question": "Explain SOLID principles.", "category": "technical", "difficulty": "hard"},
        {"id": "tech_6", "question": "What is the CAP theorem?", "category": "technical", "difficulty": "hard"},
        {"id": "tech_7", "question": "How does indexing work in databases?", "category": "technical", "difficulty": "medium"},
        {"id": "tech_8", "question": "What is a race condition and how do you prevent it?", "category": "technical", "difficulty": "hard"},
    ],
    "data_science": [
        {"id": "ds_1", "question": "What is the bias-variance tradeoff?", "category": "technical", "difficulty": "medium"},
        {"id": "ds_2", "question": "Explain the difference between supervised and unsupervised learning.", "category": "technical", "difficulty": "easy"},
        {"id": "ds_3", "question": "How does gradient descent work?", "category": "technical", "difficulty": "medium"},
        {"id": "ds_4", "question": "What is overfitting and how do you handle it?", "category": "technical", "difficulty": "medium"},
        {"id": "ds_5", "question": "Explain precision, recall, and F1 score.", "category": "technical", "difficulty": "medium"},
        {"id": "ds_6", "question": "What is the difference between bagging and boosting?", "category": "technical", "difficulty": "hard"},
    ],
    "finance": [
        {"id": "fin_1", "question": "Walk me through a DCF model.", "category": "technical", "difficulty": "hard"},
        {"id": "fin_2", "question": "What is working capital and why does it matter?", "category": "technical", "difficulty": "medium"},
        {"id": "fin_3", "question": "How would you value a private company with no comparable public company?", "category": "technical", "difficulty": "hard"},
        {"id": "fin_4", "question": "What is the difference between EBITDA and Free Cash Flow?", "category": "technical", "difficulty": "medium"},
        {"id": "fin_5", "question": "Explain the three financial statements and how they connect.", "category": "technical", "difficulty": "medium"},
    ],
    "marketing": [
        {"id": "mkt_1", "question": "What is Customer Lifetime Value and how do you calculate it?", "category": "technical", "difficulty": "medium"},
        {"id": "mkt_2", "question": "How would you run an A/B test for a landing page?", "category": "technical", "difficulty": "medium"},
        {"id": "mkt_3", "question": "What is the difference between SEO and SEM?", "category": "technical", "difficulty": "easy"},
        {"id": "mkt_4", "question": "How do you approach building a content marketing strategy?", "category": "technical", "difficulty": "medium"},
    ],
    "general": [
        {"id": "gen_1", "question": "What are your top 3 technical skills and how did you develop them?", "category": "technical", "difficulty": "easy"},
        {"id": "gen_2", "question": "How do you stay up-to-date with trends in your field?", "category": "technical", "difficulty": "easy"},
        {"id": "gen_3", "question": "Describe your process for solving a complex problem.", "category": "technical", "difficulty": "medium"},
    ],
}

FEEDBACK_RUBRIC = {
    "length": {
        "too_short": "Your answer is too brief. Aim for 1–3 minutes (150–400 words). Add specific examples.",
        "too_long": "Your answer is too long. Stay focused — 2 minutes max. Cut filler phrases.",
        "good": "Good length — concise and complete.",
    },
    "star_method": {
        "missing_situation": "Add more context: what was the situation or challenge?",
        "missing_action": "Be more specific about what YOU did (not the team).",
        "missing_result": "Always end with a quantified result — numbers, %, timeline.",
        "complete": "Good structure — Situation, Actions, and Result are all present.",
    },
    "keywords": {
        "weak": "Use stronger action verbs: Led, Delivered, Achieved, Built, Improved.",
        "strong": "Good use of professional language and action verbs.",
    },
}


def get_questions_by_type(interview_type: str, domain: str = "general") -> list:
    if interview_type == "hr":
        return HR_QUESTIONS
    elif interview_type == "behavioural":
        return BEHAVIOURAL_QUESTIONS
    elif interview_type == "technical":
        return TECHNICAL_QUESTIONS.get(domain, TECHNICAL_QUESTIONS["general"])
    elif interview_type == "mock":
        hr = HR_QUESTIONS[:3]
        beh = BEHAVIOURAL_QUESTIONS[:4]
        tech = TECHNICAL_QUESTIONS.get(domain, TECHNICAL_QUESTIONS["general"])[:3]
        return hr + beh + tech
    return []


def evaluate_response(question: dict, response_text: str) -> dict:
    """Basic rule-based evaluation of a text response."""
    word_count = len(response_text.split())
    text_lower = response_text.lower()

    feedback = []
    score = 50

    # Length check
    if word_count < 50:
        feedback.append(FEEDBACK_RUBRIC["length"]["too_short"])
    elif word_count > 500:
        feedback.append(FEEDBACK_RUBRIC["length"]["too_long"])
    else:
        score += 15
        feedback.append(FEEDBACK_RUBRIC["length"]["good"])

    # STAR method check (behavioural only)
    if question.get("category") == "behavioural":
        situation_cues = ["situation", "time when", "working at", "was working", "at my", "in my"]
        action_cues = ["i did", "i led", "i built", "i created", "i managed", "i decided", "i approached"]
        result_cues = ["result", "outcome", "achieved", "increased", "reduced", "improved", "resulted in", "%", "per cent"]

        if not any(c in text_lower for c in situation_cues):
            feedback.append(FEEDBACK_RUBRIC["star_method"]["missing_situation"])
        else:
            score += 10
        if not any(c in text_lower for c in action_cues):
            feedback.append(FEEDBACK_RUBRIC["star_method"]["missing_action"])
        else:
            score += 10
        if not any(c in text_lower for c in result_cues):
            feedback.append(FEEDBACK_RUBRIC["star_method"]["missing_result"])
        else:
            score += 15

    # Action verbs check
    strong_verbs = ["led", "built", "created", "achieved", "delivered", "drove", "increased",
                    "reduced", "launched", "managed", "designed", "improved", "developed"]
    verb_count = sum(1 for v in strong_verbs if v in text_lower)
    if verb_count < 2:
        feedback.append(FEEDBACK_RUBRIC["keywords"]["weak"])
    else:
        score += 10
        feedback.append(FEEDBACK_RUBRIC["keywords"]["strong"])

    return {
        "score": min(score, 100),
        "feedback": feedback,
        "word_count": word_count,
    }
