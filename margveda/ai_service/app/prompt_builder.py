"""Prompt construction for the CareerBrownie AI assistant."""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from app.retriever import RetrievalResult

# ── Data types ────────────────────────────────────────────────────────────────

@dataclass
class Message:
    role: str
    content: str


@dataclass
class PromptPackage:
    system: str
    messages: list[dict]
    context_used: list[str]


@dataclass
class SuggestedAction:
    label: str
    value: str
    type: str = "query"


# ── System prompt ─────────────────────────────────────────────────────────────

_SYSTEM_TEMPLATE = """\
You are **CareerVeda**, the AI career counsellor for CareerBrownie — India's most \
comprehensive career guidance platform.  You serve Indian students from Class 8 through \
postgraduate level, as well as working professionals seeking career transitions.

## Knowledge domains you cover
- **Engineering & Technology**: JEE (Main + Advanced), GATE, BITSAT, entrance exams; \
  IITs, NITs, IIITs, private universities; B.Tech branches, M.Tech, research careers
- **Medical & Allied Health**: NEET-UG, NEET-PG, AIIMS; MBBS, BDS, Pharmacy, Physiotherapy, \
  Nursing, Biomedical Engineering; government and private medical colleges
- **Management & Business**: CAT, XAT, GMAT, SNAP, NMAT; IIMs, XLRI, FMS, MDI, SP Jain; \
  MBA specialisations, finance careers, consulting, entrepreneurship
- **Government & Public Sector**: UPSC Civil Services (IAS/IPS/IFS), SSC CGL/CHSL, IBPS PO/Clerk, \
  SBI PO, RBI Grade B, RRB NTPC, NDA, CDS, AFCAT, State PSC, CTET/UGC NET
- **Law**: CLAT, AILET, LSAT India; NLUs, private law schools; practice areas, LLM, judiciary
- **Design & Architecture**: NIFT, NID, CEED, JEE Advanced (B.Arch); fashion design, \
  industrial design, UX/product design, film, animation
- **Liberal Arts & Humanities**: Ashoka University, OP Jindal, BHU, Delhi University; \
  economics, political science, sociology, history, philosophy — career paths beyond academia
- **Creative & Media**: Journalism, advertising, film, content creation, social media; \
  institutes, skills, freelancing, brand management
- **Sports & Physical Education**: SAI sports academies, NIS Patiala, sports science, \
  physiotherapy, coaching certifications, sports management
- **Study Abroad**: US (F-1 visa, GRE/GMAT/SAT, Common App), UK (UCAS, Student Route visa), \
  Canada (study permit), Germany (DAAD), Australia; scholarship programs
- **Scholarships & Financial Aid**: Central Sector, PM Scholarship, INSPIRE, Post-Matric SC/ST, \
  Minority scholarships, Reliance, Tata, Fulbright, Chevening, DAAD
- **Skills & Certifications**: Programming, data science, digital marketing, finance, \
  design — online platforms, free resources, time-to-job-ready timelines
- **Salary & Job Market**: Salary by role, city, experience; top companies; hiring trends 2025

## How to respond — multi-perspective framework
For every career or education question, cover ALL relevant angles:
1. **Academic path** — eligibility, entrance exams, best colleges/universities, duration
2. **Financial reality** — fees, ROI, salary range (entry to senior), scholarship options
3. **Job market** — current demand, top employers, growth rate, remote work possibility
4. **Realistic assessment** — difficulty, competition level, backup options
5. **Actionable next steps** — what the student can do THIS WEEK to start

## Response quality rules
1. **Be a real expert, not a search engine**: synthesise information, give opinions, \
   make comparisons.  "Software engineering OR data science — which is better for you?" \
   requires judgment, not just definitions.
2. **India-first, globally aware**: salary benchmarks should be in ₹ LPA.  Mention \
   ₹ → USD conversion only when relevant (study abroad context).
3. **Cite sources from Context**: when the Context section has numbered sources [1][2], \
   reference them inline.  Example: "IIT Bombay CS requires JEE Advanced rank < 100 [1]."
4. **Specificity over vagueness**: "₹8–14 LPA for a fresh software engineer at product \
   companies in Bangalore" beats "good salary".
5. **Empathy for Indian family pressures**: acknowledge that parental expectations, \
   financial constraints, and societal pressure are real factors — not things to dismiss.
6. **Honest about difficulty**: if UPSC success rate is 0.1%, say so.  Then explain how \
   to maximise chances and what backup plans exist.
7. **Never demotivate**: hard goal ≠ impossible goal.  Always provide a realistic path.
8. **Escalate gracefully**: if a question requires personalised assessment \
   (psychological aptitude test, family financial situation review, specific college \
   application review), say: \
   "This is best discussed in a 1-on-1 session with a CareerBrownie counsellor who can \
   review your specific profile.  **Book a session** for personalised guidance."

## Format
- Use **bold** for key terms, institutions, salary figures
- Use bullet points (- item) for lists of options or steps
- Use numbered lists (1. 2. 3.) for sequential roadmaps
- Use ### Section headers only for long responses (roadmaps, comparisons)
- Keep mobile-friendly: no table syntax
- Maximum 400 words unless the question requires a roadmap or comparison
- Always end with 2–3 follow-up questions the student might want to ask next\
"""

# ── Counselor escalation triggers ────────────────────────────────────────────

_ESCALATION_PHRASES = [
    "i don't know", "i'm not sure", "i cannot answer", "beyond my knowledge",
    "consult a professional", "seek professional", "i'm unable", "out of my scope",
    "cannot help with this", "please see a",
]

_PERSONAL_KEYWORDS = [
    "my family", "my parents", "mental health", "depression", "anxiety",
    "suicide", "hopeless", "give up", "relationship", "personal problem",
    "i hate", "i'm scared", "i'm afraid", "financial crisis", "can't afford",
    "broke", "loan default", "abuse",
]


def needs_counselor_escalation(query: str, response_text: str, min_score: float) -> bool:
    """Return True when the query needs a human counsellor."""
    q_lower = query.lower()
    r_lower = response_text.lower()

    # Personal/emotional topics always escalate
    if any(kw in q_lower for kw in _PERSONAL_KEYWORDS):
        return True

    # LLM expressed uncertainty
    if any(phrase in r_lower for phrase in _ESCALATION_PHRASES):
        return True

    # Very low retrieval quality — couldn't find relevant context
    if min_score < 0.25:
        return True

    return False


# ── PromptBuilder ─────────────────────────────────────────────────────────────

class PromptBuilder:

    def __init__(self, max_context_chars: int = 4000) -> None:
        self._max_context_chars = max_context_chars

    def build(
        self,
        query: str,
        retrieved: list[RetrievalResult],
        history: list[Message] | None = None,
        student_profile: dict | None = None,
    ) -> PromptPackage:
        system = self._build_system(student_profile)
        context_block, used_ids = self._build_context(retrieved)
        user_message = self._build_user_message(query, context_block)
        messages = self._format_history(history or [], user_message)
        return PromptPackage(system=system, messages=messages, context_used=used_ids)

    def extract_suggestions(self, response_text: str) -> list[SuggestedAction]:
        suggestions: list[SuggestedAction] = []
        lines = response_text.splitlines()
        for line in lines:
            # Numbered items at end of response (follow-up questions)
            m = re.match(r"^\s*\d+\.\s+(.+)$", line)
            if m:
                text = m.group(1).strip(" *?")
                if 10 < len(text) < 140:
                    suggestions.append(SuggestedAction(label=text[:90], value=text, type="query"))
            # Bullet points that look like questions
            m2 = re.match(r"^\s*[-•]\s+(.+\?)$", line)
            if m2:
                text = m2.group(1).strip(" *")
                if 10 < len(text) < 140:
                    suggestions.append(SuggestedAction(label=text[:90], value=text, type="query"))

        seen: set[str] = set()
        unique: list[SuggestedAction] = []
        for s in suggestions:
            if s.value not in seen:
                seen.add(s.value)
                unique.append(s)

        return unique[:4]

    # ── Private helpers ───────────────────────────────────────────────────

    def _build_system(self, profile: dict | None) -> str:
        if not profile:
            return _SYSTEM_TEMPLATE
        parts = [_SYSTEM_TEMPLATE, "\n\n## Student profile (personalise your response)"]
        if profile.get("stream"):
            parts.append(f"- Academic stream/background: {profile['stream']}")
        if profile.get("class_level"):
            parts.append(f"- Current class/year: {profile['class_level']}")
        if profile.get("interests"):
            interests = profile["interests"]
            if isinstance(interests, list):
                interests = ", ".join(interests)
            parts.append(f"- Interests/hobbies: {interests}")
        if profile.get("goal"):
            parts.append(f"- Stated career goal: {profile['goal']}")
        if profile.get("location"):
            parts.append(f"- Location: {profile['location']}")
        if profile.get("budget"):
            parts.append(f"- Education budget: {profile['budget']}")
        parts.append("\nTailor your response specifically to this student's situation.")
        return "\n".join(parts)

    def _build_context(self, retrieved: list[RetrievalResult]) -> tuple[str, list[str]]:
        if not retrieved:
            return "", []

        blocks: list[str] = []
        used_ids: list[str] = []
        char_budget = self._max_context_chars

        for idx, result in enumerate(retrieved, start=1):
            chunk = result.text.strip()
            if not chunk:
                continue
            if len(chunk) > char_budget:
                chunk = chunk[:char_budget]
            domain = result.metadata.get("domain", "")
            title = result.metadata.get("title", result.id)
            header = f"[{idx}] **{title}**"
            if domain:
                header += f" — domain: {domain} | relevance: {result.score:.0%}"
            blocks.append(f"{header}\n{chunk}")
            used_ids.append(result.id)
            char_budget -= len(chunk)
            if char_budget <= 0:
                break

        return "\n\n---\n\n".join(blocks), used_ids

    def _build_user_message(self, query: str, context: str) -> str:
        if context:
            return (
                f"## Knowledge Base Context\n\n{context}\n\n"
                f"---\n\n"
                f"## Student Question\n\n{query}\n\n"
                f"Provide a comprehensive, multi-perspective answer covering academic path, "
                f"financial reality, job market outlook, and actionable next steps."
            )
        return (
            f"{query}\n\n"
            f"Note: No specific context was retrieved from the knowledge base for this query. "
            f"Answer from your general India-specific career knowledge. "
            f"Acknowledge if information may need verification from official sources."
        )

    @staticmethod
    def _format_history(history: list[Message], current_user_message: str) -> list[dict]:
        messages: list[dict] = []
        for msg in history[-8:]:  # keep last 4 turns (8 messages)
            if msg.role in ("user", "assistant") and msg.content.strip():
                messages.append({"role": msg.role, "content": msg.content})
        messages.append({"role": "user", "content": current_user_message})
        return messages


# ── Fallback response builder ─────────────────────────────────────────────────

def build_fallback_response(query: str, retrieved: list[RetrievalResult]) -> str:
    if not retrieved:
        return (
            "I couldn't find specific information for your query in my knowledge base.\n\n"
            "**What you can do:**\n"
            "- Rephrase your question with more specific keywords\n"
            "- **Book a 1-on-1 session** with a CareerBrownie counsellor for personalised guidance\n"
            "- Browse our career library for detailed career profiles"
        )

    top = retrieved[0]
    title = top.metadata.get("title", "")
    header = f"**{title}**\n\n" if title else ""
    body = top.text.strip()[:600]
    suffix = (
        "\n\n---\n*For a personalised roadmap tailored to your profile, "
        "[**book a counselling session**](/student/sessions/book) with a CareerBrownie expert.*"
    )
    return f"{header}{body}{suffix}"
