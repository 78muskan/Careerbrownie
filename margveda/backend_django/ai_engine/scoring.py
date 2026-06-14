"""
Assessment scoring engine — rule-based AI that generates personalised
career intelligence from student profile + assessment responses.
"""
from .career_data import CAREERS, RIASEC_CAREER_MAP, MARKET_TRENDS


def score_interest_assessment(responses: dict) -> dict:
    """
    responses: {question_id: riasec_code or None}
    Returns RIASEC scores and top Holland code.
    """
    from .career_data import INTEREST_QUESTIONS
    riasec = {k: 0 for k in "RIASEC"}
    for q in INTEREST_QUESTIONS:
        q_id = str(q["id"])
        if q_id not in responses:
            continue
        chosen_idx = responses[q_id]
        if isinstance(chosen_idx, int) and chosen_idx < len(q["options"]):
            opt = q["options"][chosen_idx]
            if opt.get("riasec"):
                riasec[opt["riasec"]] += opt["value"]
    total = max(sum(riasec.values()), 1)
    pct = {k: round(v / total * 100) for k, v in riasec.items()}
    top = sorted(riasec, key=riasec.get, reverse=True)[:3]
    return {"raw": riasec, "percentages": pct, "top_codes": top, "primary": top[0]}


def score_personality_assessment(responses: dict) -> dict:
    """responses: {question_id: score 1-5}"""
    traits = {
        "openness": 0, "conscientiousness": 0,
        "extraversion": 0, "agreeableness": 0, "stability": 0,
    }
    counts = {k: 0 for k in traits}
    from .career_data import PERSONALITY_QUESTIONS
    for q in PERSONALITY_QUESTIONS:
        q_id = str(q["id"])
        if q_id in responses:
            trait = q["trait"]
            traits[trait] += int(responses[q_id])
            counts[trait] += 1
    avg = {k: round(traits[k] / counts[k] * 20) if counts[k] else 50 for k in traits}

    # Personality archetype
    archetypes = []
    if avg.get("extraversion", 50) >= 60:
        archetypes.append("Leader")
    if avg.get("openness", 50) >= 65:
        archetypes.append("Innovator")
    if avg.get("conscientiousness", 50) >= 65:
        archetypes.append("Planner")
    if avg.get("agreeableness", 50) >= 65:
        archetypes.append("Collaborator")
    if not archetypes:
        archetypes.append("Balanced Achiever")

    return {"trait_scores": avg, "archetype": " + ".join(archetypes)}


def score_aptitude_assessment(responses: dict) -> dict:
    """responses: {question_id: chosen_option_index}"""
    from .career_data import APTITUDE_QUESTIONS
    scores = {"numerical": 0, "verbal": 0, "logical": 0, "total": 0}
    totals = {"numerical": 0, "verbal": 0, "logical": 0}
    for q in APTITUDE_QUESTIONS:
        q_id = str(q["id"])
        totals[q["type"]] += 1
        if q_id in responses and str(responses[q_id]) == str(q["correct"]):
            scores[q["type"]] += 1
    pct = {k: round(scores[k] / totals[k] * 100) if totals[k] else 0 for k in totals}
    pct["total"] = round(sum(pct.values()) / len(totals))
    strengths = [k for k, v in pct.items() if v >= 60 and k != "total"]
    return {"scores": pct, "strengths": strengths}


def score_readiness_assessment(responses: dict) -> dict:
    """responses: {question_id: 1-5}"""
    from .career_data import READINESS_QUESTIONS
    cats = {}
    for q in READINESS_QUESTIONS:
        q_id = str(q["id"])
        cat = q["category"]
        val = int(responses.get(q_id, 3))
        cats.setdefault(cat, []).append(val)
    cat_scores = {k: round(sum(v) / len(v) / 5 * 100) for k, v in cats.items()}
    overall = round(sum(cat_scores.values()) / len(cat_scores))
    level = "High" if overall >= 70 else "Moderate" if overall >= 45 else "Developing"
    return {"category_scores": cat_scores, "overall": overall, "level": level}


def match_careers(riasec_top_codes: list, student_skills: list = None, student_interests: list = None) -> list:
    """Return ranked career matches based on RIASEC codes."""
    scores = {}
    for code in riasec_top_codes:
        for career_key in RIASEC_CAREER_MAP.get(code, []):
            scores[career_key] = scores.get(career_key, 0) + (3 if code == riasec_top_codes[0] else 1)
    # Boost if student skills match career skills
    if student_skills:
        for key, career in CAREERS.items():
            overlap = len(set(s.lower() for s in student_skills) & set(s.lower() for s in career["key_skills"]))
            scores[key] = scores.get(key, 0) + overlap
    ranked = sorted(scores, key=scores.get, reverse=True)[:8]
    return [
        {
            "key": k,
            "match_pct": min(round(scores[k] / max(scores.values()) * 100) if scores else 50, 99),
            **{f: CAREERS[k][f] for f in ["title", "domain", "avg_salary_india", "growth_rate", "key_skills", "demand"] if f in CAREERS[k]},
        }
        for k in ranked if k in CAREERS
    ]


def generate_skill_gaps(target_career_key: str, student_skills: list) -> list:
    """Return skills the student is missing for a target career."""
    if target_career_key not in CAREERS:
        return []
    required = set(s.lower() for s in CAREERS[target_career_key]["key_skills"])
    have = set(s.lower() for s in (student_skills or []))
    missing = required - have
    return list(missing)[:5]


def get_market_trends(domains: list) -> list:
    """Return market trends relevant to the student's target domains."""
    if not domains:
        return MARKET_TRENDS[:3]
    matched = [t for t in MARKET_TRENDS if t["domain"].lower() in [d.lower() for d in domains]]
    return (matched or MARKET_TRENDS)[:4]


def calculate_career_score(profile) -> int:
    """
    Compute a 0-100 career score from profile completeness + assessment results.
    """
    score = 0
    # Profile completeness (40 pts)
    score += min(profile.profile_score * 0.4, 40)
    # Assessment completion (30 pts)
    assessment_count = profile.assessment_results.count() if hasattr(profile, "assessment_results") else 0
    score += min(assessment_count * 7.5, 30)
    # Goals set (15 pts)
    goal_count = profile.goals.filter(status__in=["pending", "in_progress"]).count() if hasattr(profile, "goals") else 0
    score += min(goal_count * 5, 15)
    # Skills added (15 pts)
    skills = profile.technical_skills or []
    score += min(len(skills) * 3, 15)
    return round(score)
