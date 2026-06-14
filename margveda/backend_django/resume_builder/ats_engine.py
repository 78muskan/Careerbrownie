"""
ATS (Applicant Tracking System) scoring engine.
Analyses resume content against job descriptions and industry standards.
"""
import re
from .resume_data import ATS_KEYWORDS, STRONG_ACTION_VERBS, WEAK_PHRASES


def extract_text_from_resume(resume) -> str:
    """Combine all resume sections into a single searchable text blob."""
    parts = []
    if resume.summary:
        parts.append(resume.summary)
    for section in resume.sections.all():
        content = section.content
        if isinstance(content, dict):
            parts.append(" ".join(str(v) for v in content.values() if v))
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    parts.append(" ".join(str(v) for v in item.values() if v))
                else:
                    parts.append(str(item))
    personal = resume.personal_info or {}
    parts.append(personal.get("title", ""))
    return " ".join(parts).lower()


def extract_keywords_from_jd(job_description: str) -> list:
    """Extract relevant keywords from a job description."""
    jd = job_description.lower()
    found = set()
    for domain_keywords in ATS_KEYWORDS.values():
        for kw in domain_keywords:
            if kw.lower() in jd:
                found.add(kw.lower())
    # Also extract single/two-word phrases from JD that look like skills
    words = re.findall(r'\b[a-z][a-z\+\#\.\/]+(?:\s+[a-z][a-z\+\#\.\/]+)?\b', jd)
    common = {"the", "and", "or", "for", "with", "this", "that", "will", "you",
              "are", "our", "your", "have", "has", "been", "can", "work", "team",
              "experience", "strong", "good", "role", "job", "position", "candidate"}
    skill_words = [w for w in set(words) if w not in common and len(w) > 3]
    found.update(skill_words[:30])
    return list(found)[:50]


def score_resume(resume, job_description: str = "", domain: str = "technology") -> dict:
    """
    Score a resume and return ATS analysis.
    Returns score (0-100), matched/missing keywords, and suggestions.
    """
    resume_text = extract_text_from_resume(resume)
    jd_keywords = extract_keywords_from_jd(job_description) if job_description else []
    domain_keywords = ATS_KEYWORDS.get(domain, ATS_KEYWORDS["general"])

    # --- Keyword matching ---
    all_target = list(set(jd_keywords + domain_keywords[:20]))
    matched = [kw for kw in all_target if kw.lower() in resume_text]
    missing = [kw for kw in all_target if kw.lower() not in resume_text]

    keyword_score = min(round(len(matched) / max(len(all_target), 1) * 40), 40)

    # --- Section completeness ---
    sections_present = {s.section_type for s in resume.sections.all()}
    core_sections = {"education", "skills"}
    has_core = all(s in sections_present for s in core_sections)
    has_experience = "experience" in sections_present or "projects" in sections_present
    has_summary = bool(resume.summary)
    section_score = (10 if has_core else 0) + (8 if has_experience else 0) + (7 if has_summary else 0)

    # --- Personal info completeness ---
    p = resume.personal_info or {}
    pi_fields = ["name", "email", "phone", "city"]
    pi_score = round(sum(1 for f in pi_fields if p.get(f)) / len(pi_fields) * 10)

    # --- Action verbs check ---
    action_verb_count = sum(1 for v in STRONG_ACTION_VERBS if v.lower() in resume_text)
    weak_phrase_count = sum(1 for w in WEAK_PHRASES if w in resume_text)
    action_score = min(action_verb_count * 2, 15) - min(weak_phrase_count * 3, 10)
    action_score = max(action_score, 0)

    # --- Length / density check ---
    word_count = len(resume_text.split())
    if 300 <= word_count <= 900:
        length_score = 10
    elif 200 <= word_count < 300 or 900 < word_count <= 1200:
        length_score = 6
    else:
        length_score = 3

    total = keyword_score + section_score + pi_score + action_score + length_score
    total = min(total, 100)

    # --- Suggestions ---
    suggestions = []
    if len(missing) > 5:
        suggestions.append(f"Add missing keywords: {', '.join(missing[:6])}.")
    if not has_summary:
        suggestions.append("Add a Professional Summary section — it's the first thing recruiters read.")
    if not has_experience:
        suggestions.append("Add Work Experience or Projects to demonstrate applied skills.")
    if weak_phrase_count > 0:
        suggestions.append("Replace weak phrases like 'responsible for' with strong action verbs (e.g., Led, Delivered, Built).")
    if action_verb_count < 5:
        suggestions.append("Use more action verbs to make bullet points impactful.")
    if word_count < 300:
        suggestions.append("Resume is too short. Expand your experience/project sections with quantified results.")
    if word_count > 1200:
        suggestions.append("Resume is too long for ATS. Aim for 1 page (fresh grad) or 2 pages (experienced).")
    if not p.get("linkedin"):
        suggestions.append("Add your LinkedIn profile URL to increase credibility.")

    grade = "A" if total >= 80 else "B" if total >= 65 else "C" if total >= 50 else "D"

    return {
        "ats_score": total,
        "grade": grade,
        "breakdown": {
            "keywords": keyword_score,
            "sections": section_score,
            "personal_info": pi_score,
            "action_verbs": action_score,
            "length": length_score,
        },
        "matched_keywords": matched[:20],
        "missing_keywords": missing[:15],
        "suggestions": suggestions,
        "word_count": word_count,
    }
