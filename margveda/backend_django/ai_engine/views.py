import json
import os

import requests as http_requests
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import AssessmentResult, CareerRoadmap, AIInsight
from .scoring import (
    score_interest_assessment, score_personality_assessment,
    score_aptitude_assessment, score_readiness_assessment,
    match_careers, generate_skill_gaps, get_market_trends, calculate_career_score,
)
from .career_data import (
    INTEREST_QUESTIONS, PERSONALITY_QUESTIONS, APTITUDE_QUESTIONS,
    READINESS_QUESTIONS, CAREERS, ROADMAP_TEMPLATES, LEARNING_RESOURCES,
)


def _get_profile(user):
    try:
        return user.student_profile
    except Exception:
        return None


class AssessmentQuestionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, assessment_type):
        MAP = {
            "interest": INTEREST_QUESTIONS,
            "personality": PERSONALITY_QUESTIONS,
            "aptitude": APTITUDE_QUESTIONS,
            "readiness": READINESS_QUESTIONS,
        }
        if assessment_type not in MAP:
            return Response({"error": "Invalid assessment type."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"questions": MAP[assessment_type], "assessment_type": assessment_type})


class SubmitAssessmentView(APIView):
    permission_classes = [IsAuthenticated]

    SCORERS = {
        "interest": score_interest_assessment,
        "personality": score_personality_assessment,
        "aptitude": score_aptitude_assessment,
        "readiness": score_readiness_assessment,
    }

    def post(self, request, assessment_type):
        if assessment_type not in self.SCORERS:
            return Response({"error": "Invalid assessment type."}, status=status.HTTP_400_BAD_REQUEST)
        profile = _get_profile(request.user)
        if not profile:
            return Response({"error": "Student profile required."}, status=status.HTTP_403_FORBIDDEN)
        responses = request.data.get("responses", {})
        scores = self.SCORERS[assessment_type](responses)
        top_careers = []
        if assessment_type == "interest":
            top_careers = match_careers(scores.get("top_codes", []), profile.technical_skills or [], profile.career_interests or [])
        summary = self._build_summary(assessment_type, scores)
        result, _ = AssessmentResult.objects.update_or_create(
            student=profile, assessment_type=assessment_type,
            defaults={"responses": responses, "scores": scores, "result_summary": summary, "top_careers": top_careers},
        )
        if hasattr(profile, "career_profile"):
            cp = profile.career_profile
            if assessment_type == "interest" and top_careers:
                cp.ai_career_recommendations = [c["title"] for c in top_careers[:5]]
            if assessment_type == "personality":
                cp.personality_type = scores.get("archetype", "")
            cp.assessment_completed = profile.assessment_results.count() >= 2
            cp.career_score = calculate_career_score(profile)
            cp.save()
        self._generate_insights(profile, assessment_type, scores, top_careers)
        from notifications.models import Notification
        Notification.create(user=request.user, notification_type="ai_insight",
            title=f"{assessment_type.replace('_', ' ').title()} Assessment Complete!",
            message="Your results are ready. Check your AI career insights.", link="/student/ai-advisor")
        return Response({"result": {"id": str(result.id), "assessment_type": assessment_type,
            "scores": scores, "result_summary": summary, "top_careers": top_careers}}, status=status.HTTP_201_CREATED)

    def _build_summary(self, assessment_type, scores):
        if assessment_type == "interest":
            primary = scores.get("primary", "I")
            names = {"R": "Realistic", "I": "Investigative", "A": "Artistic", "S": "Social", "E": "Enterprising", "C": "Conventional"}
            return f"Your primary interest type is {names.get(primary, primary)}. You thrive in environments that reward logical thinking and discovery."
        elif assessment_type == "personality":
            return f"Personality archetype: {scores.get('archetype', 'Balanced Achiever')}. You bring structured thinking and collaborative energy to your work."
        elif assessment_type == "aptitude":
            total = scores.get("scores", {}).get("total", 0)
            strengths = scores.get("strengths", [])
            return f"Aptitude score: {total}%. Strengths: {', '.join(strengths) or 'general reasoning'}."
        elif assessment_type == "readiness":
            level, overall = scores.get("level", "Developing"), scores.get("overall", 0)
            return f"Career Readiness: {level} ({overall}%). Strengthen your weaker areas to accelerate your journey."
        return ""

    def _generate_insights(self, profile, assessment_type, scores, top_careers):
        if assessment_type == "interest" and top_careers:
            AIInsight.objects.update_or_create(student=profile, insight_type="career_match", defaults={
                "title": f"Top Career Match: {top_careers[0]['title']}",
                "content": f"You have a {top_careers[0]['match_pct']}% match with {top_careers[0]['title']} based on your interests.",
                "data": {"careers": top_careers[:3]}, "relevance_score": top_careers[0]["match_pct"] / 100,
            })
        gaps = generate_skill_gaps(
            (profile.target_roles or [])[0].lower().replace(" ", "_") if profile.target_roles else "software_engineer",
            profile.technical_skills or [],
        )
        if gaps:
            AIInsight.objects.update_or_create(student=profile, insight_type="skill_gap", defaults={
                "title": "Key skills to develop", "content": f"Focus on: {', '.join(gaps)}.",
                "data": {"gaps": gaps}, "relevance_score": 0.8,
            })


class AssessmentResultView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, assessment_type=None):
        profile = _get_profile(request.user)
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        if assessment_type:
            try:
                r = AssessmentResult.objects.get(student=profile, assessment_type=assessment_type)
                return Response({"assessment_type": r.assessment_type, "scores": r.scores,
                    "result_summary": r.result_summary, "top_careers": r.top_careers, "completed_at": r.completed_at})
            except AssessmentResult.DoesNotExist:
                return Response({"error": "Not taken yet."}, status=status.HTTP_404_NOT_FOUND)
        results = AssessmentResult.objects.filter(student=profile)
        return Response([{"assessment_type": r.assessment_type, "result_summary": r.result_summary,
            "completed_at": r.completed_at} for r in results])


class RoadmapView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = _get_profile(request.user)
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        try:
            return Response(self._serialize(profile.roadmap))
        except CareerRoadmap.DoesNotExist:
            return Response({"exists": False}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        profile = _get_profile(request.user)
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_403_FORBIDDEN)
        target = request.data.get("target_career", "").lower().replace(" ", "_")
        key = target if target in ROADMAP_TEMPLATES else "default"
        t = ROADMAP_TEMPLATES[key]
        roadmap, _ = CareerRoadmap.objects.update_or_create(student=profile, defaults={
            "target_career": request.data.get("target_career", "Career Path"),
            "plan_3_months": t["3_months"], "plan_6_months": t["6_months"],
            "plan_1_year": t["1_year"], "plan_3_years": t["3_years"], "plan_5_years": t["5_years"],
        })
        return Response(self._serialize(roadmap), status=status.HTTP_201_CREATED)

    def _serialize(self, rm):
        return {"id": str(rm.id), "target_career": rm.target_career, "generated_at": rm.generated_at,
            "plans": {"3_months": rm.plan_3_months, "6_months": rm.plan_6_months,
                "1_year": rm.plan_1_year, "3_years": rm.plan_3_years, "5_years": rm.plan_5_years}}


class AIAdvisorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = _get_profile(request.user)
        if not profile:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
        insights = AIInsight.objects.filter(student=profile)
        skill_gaps = generate_skill_gaps(
            (profile.target_roles or [])[0].lower().replace(" ", "_") if profile.target_roles else "software_engineer",
            profile.technical_skills or [],
        )
        trends = get_market_trends(profile.career_interests or [])
        career_matches = match_careers(["I", "E", "A"], profile.technical_skills or [], profile.career_interests or [])
        resources = []
        for gap in skill_gaps[:3]:
            for sname, res_list in LEARNING_RESOURCES.items():
                if sname.lower() in gap.lower():
                    resources.extend(res_list[:2])
                    break
        return Response({
            "insights": [{"type": i.insight_type, "title": i.title, "content": i.content, "data": i.data} for i in insights[:8]],
            "career_matches": career_matches[:6],
            "skill_gaps": skill_gaps,
            "market_trends": trends,
            "learning_resources": resources[:6],
            "assessments_completed": list(profile.assessment_results.values_list("assessment_type", flat=True)),
        })


class CareerDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, career_key):
        career = CAREERS.get(career_key)
        if not career:
            return Response({"error": "Career not found."}, status=status.HTTP_404_NOT_FOUND)
        profile = _get_profile(request.user)
        skill_gaps = generate_skill_gaps(career_key, profile.technical_skills if profile else [])
        resources = [r for skill in career["key_skills"][:3]
            for sname, res_list in LEARNING_RESOURCES.items()
            if sname.lower() in skill.lower() for r in res_list[:2]]
        return Response({**career, "key": career_key, "skill_gaps": skill_gaps, "learning_resources": resources[:5]})


class CareerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        domain = request.query_params.get("domain")
        return Response([
            {"key": k, "title": v["title"], "domain": v["domain"],
             "avg_salary_india": v["avg_salary_india"], "demand": v["demand"], "growth_rate": v["growth_rate"]}
            for k, v in CAREERS.items() if not domain or v["domain"].lower() == domain.lower()
        ])


class PublicChatView(APIView):
    """
    POST /api/v1/ai/public-chat/
    No authentication required — used by the public chat widget.
    Uses keyword-based RAG over career_data.py to enrich every query,
    then calls Claude Haiku. Falls back to rule-based if no API key.
    """
    permission_classes = []
    authentication_classes = []

    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

    def post(self, request):
        message = request.data.get("message", "").strip()
        if not message:
            return Response({"error": "message is required."}, status=status.HTTP_400_BAD_REQUEST)
        history = request.data.get("history", [])
        return ChatView._direct_claude_static(message, history, self.ANTHROPIC_API_KEY)


class ChatView(APIView):
    """
    POST /api/v1/ai/chat/
    Authenticated endpoint — forwards to AI microservice or falls back to Django RAG.
    """
    permission_classes = [IsAuthenticated]

    AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://localhost:9000")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

    def post(self, request):
        message = request.data.get("message", "").strip()
        if not message:
            return Response({"error": "message is required."}, status=status.HTTP_400_BAD_REQUEST)

        student_context = request.data.get("student_context", {}) or {}

        try:
            ai_resp = http_requests.post(
                f"{self.AI_SERVICE_URL}/chat",
                json={"query": message, "student_profile": student_context, "history": []},
                timeout=15,
            )
            ai_resp.raise_for_status()
            return Response(ai_resp.json())
        except Exception:
            pass

        return self._direct_claude(message, student_context)

    # ── RAG retrieval ─────────────────────────────────────────────────────────

    @staticmethod
    def _retrieve_context(message: str) -> str:
        """
        Keyword-based RAG: score every career in CAREERS against the user's query,
        return the top matches as formatted context for the LLM.
        """
        msg = message.lower()
        scored = []

        for key, career in CAREERS.items():
            score = 0
            title_lower = career["title"].lower()

            # Full title match is strongest signal
            if title_lower in msg:
                score += 12
            # Individual title words (skip short filler words)
            for word in title_lower.split():
                if len(word) > 3 and word in msg:
                    score += 3
            # Career key (e.g. "data_scientist" → "data scientist")
            if key.replace("_", " ") in msg:
                score += 10
            # Domain
            if career["domain"].lower() in msg:
                score += 2
            # Skills
            for skill in career.get("key_skills", []):
                if skill.lower() in msg:
                    score += 2
            # Companies
            for company in career.get("top_companies", []):
                if company.lower() in msg:
                    score += 1

            if score > 0:
                scored.append((score, key, career))

        scored.sort(key=lambda x: x[0], reverse=True)
        parts = []
        for _, key, career in scored[:4]:
            roadmap_hint = ""
            if key in ROADMAP_TEMPLATES:
                steps = [s["title"] for s in ROADMAP_TEMPLATES[key].get("3_months", [])[:2]]
                roadmap_hint = f"\n  First steps: {'; '.join(steps)}" if steps else ""
            parts.append(
                f"{career['title']} ({career['domain']})\n"
                f"  Salary: {career['avg_salary_india']} | Growth: {career['growth_rate']} | Demand: {career['demand']}\n"
                f"  Education: {', '.join(career['education'][:2])}\n"
                f"  Key Skills: {', '.join(career['key_skills'][:5])}\n"
                f"  Top Companies: {', '.join(career['top_companies'][:4])}"
                f"{roadmap_hint}"
            )

        return "\n\n".join(parts)

    # ── Shared Claude call (public + authenticated fallback) ──────────────────

    @staticmethod
    def _direct_claude_static(message: str, history: list, api_key: str):
        if not api_key:
            return Response(ChatView._rule_based(message))

        context = ChatView._retrieve_context(message)

        SYSTEM = (
            "You are Career Brownie AI — India's most advanced AI career counsellor.\n"
            "You serve Class 9-12 students, college students, graduates, and working professionals.\n\n"
            "About Career Brownie:\n"
            "• Founded by Muskan Sahani\n"
            "• Contact: careerbrownie@gmail.com | +91 8171557334\n"
            "• Services: Career Counselling (₹999+), University Admissions, Study Abroad, AI Career Guidance\n"
            "• Free 30-min introductory session available\n\n"
            "How to respond:\n"
            "• Be warm, specific, and practical — always India-focused\n"
            "• Quote real salary ranges, growth rates, entrance exams, and top companies when relevant\n"
            "• Keep the reply to 2-4 short paragraphs\n"
            "• End EVERY reply with exactly this line:\n"
            "  ACTIONS: [\"specific action 1\", \"specific action 2\", \"specific action 3\"]\n"
            "• Actions must be concrete next steps the user can take on Career Brownie\n"
            "  (e.g., 'Book free 30-min session', 'Take career assessment', 'Explore data science roadmap')"
        )

        user_content = message
        if context:
            user_content = (
                f"[Career Knowledge Base — top matches for this query]\n{context}\n\n"
                f"[Student question]\n{message}"
            )

        messages = []
        for entry in (history or [])[-10:]:
            if entry.get("role") in ("user", "assistant") and entry.get("content"):
                messages.append({"role": entry["role"], "content": entry["content"]})
        messages.append({"role": "user", "content": user_content})

        try:
            resp = http_requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-haiku-4-5-20251001",
                    "max_tokens": 600,
                    "system": SYSTEM,
                    "messages": messages,
                },
                timeout=25,
            )
            resp.raise_for_status()
            full_text = resp.json()["content"][0]["text"].strip()

            reply, suggested_actions = full_text, []
            if "ACTIONS:" in full_text:
                parts = full_text.rsplit("ACTIONS:", 1)
                reply = parts[0].strip()
                try:
                    suggested_actions = json.loads(parts[1].strip())
                except Exception:
                    pass

            if not suggested_actions:
                suggested_actions = ["Book free session", "Take career assessment", "Speak to a counsellor"]

            return Response({
                "reply": reply,
                "suggested_actions": suggested_actions,
                "rag_docs": len(context.split("\n\n")) if context else 0,
            })
        except Exception:
            return Response(ChatView._rule_based(message))

    def _direct_claude(self, message: str, student_context: dict):
        history = student_context.get("history") or []
        return self._direct_claude_static(message, history, self.ANTHROPIC_API_KEY)

    # ── Rule-based fallback (no API key) ──────────────────────────────────────

    @staticmethod
    def _rule_based(message: str) -> dict:
        msg = message.lower()

        # Try to pull a relevant career from the KB even without Claude
        context = ChatView._retrieve_context(message)
        if context:
            first_career = context.split("\n")[0]
            return {
                "reply": (
                    f"Great question! Based on what you asked, here's what I know about {first_career}.\n\n"
                    f"{context}\n\n"
                    "For personalised advice tailored to your scores and interests, "
                    "book a free 30-minute session with one of our expert counsellors."
                ),
                "suggested_actions": ["Book free 30-min session", "Take career assessment", "Talk to a counsellor"],
            }

        if any(w in msg for w in ("college", "iit", "nit", "iim", "university", "admission", "cut-off", "cutoff")):
            return {
                "reply": (
                    "To find the best colleges for you, I need to know your stream (PCM/PCB/Commerce/Arts), "
                    "your expected score or percentile, and your preferred state or city.\n\n"
                    "Share those details and I'll give you a personalised college shortlist. "
                    "You can also book a free counselling session for a deep-dive."
                ),
                "suggested_actions": ["Share my score for college list", "Book free counselling session", "View top colleges by stream"],
            }

        if any(w in msg for w in ("skill", "learn", "course", "certificate", "gap", "upskill")):
            return {
                "reply": (
                    "Building the right skills is the fastest way to accelerate your career. "
                    "Tell me your current skills and your target role — I'll identify the exact gaps "
                    "and recommend free + paid courses to fill them.\n\n"
                    "Our AI generates a step-by-step 12-month learning roadmap personalised to you."
                ),
                "suggested_actions": ["Generate my skill gap report", "Get a personalised roadmap", "Browse recommended courses"],
            }

        if any(w in msg for w in ("salary", "package", "lpa", "ctc", "pay", "earn")):
            return {
                "reply": (
                    "Salaries in India vary widely by role, company, and city. "
                    "For example: Software Engineers earn ₹6–25 LPA, Data Scientists ₹8–30 LPA, "
                    "MBAs ₹8–40 LPA, and Doctors ₹6–30 LPA.\n\n"
                    "Tell me which career you're targeting and I'll give you detailed salary benchmarks."
                ),
                "suggested_actions": ["Compare salaries by career", "Explore high-growth careers", "Book salary negotiation session"],
            }

        if any(w in msg for w in ("abroad", "usa", "uk", "canada", "australia", "gre", "gmat", "ielts", "toefl")):
            return {
                "reply": (
                    "We offer end-to-end study abroad support — from country and university selection "
                    "to SOP writing, visa guidance, and scholarship applications.\n\n"
                    "Popular destinations: USA (MS/MBA), UK (1-year Master's), Canada (PR pathway), "
                    "Australia (skilled migration). Book a free session to discuss your profile."
                ),
                "suggested_actions": ["Book study abroad session", "Check eligibility for USA MS", "Find scholarships for my profile"],
            }

        if any(w in msg for w in ("career", "job", "switch", "role", "path", "future", "after 12", "after graduation")):
            return {
                "reply": (
                    "Choosing the right career path is the most important decision you'll make. "
                    "I can help you explore 50+ careers across Technology, Finance, Healthcare, Law, "
                    "Design, and more — with real salary data and growth rates for India.\n\n"
                    "Take our free career assessment to discover which paths match your interests and strengths."
                ),
                "suggested_actions": ["Take free career assessment", "Explore careers by domain", "Book a counselling session"],
            }

        return {
            "reply": (
                "Hi! I'm Career Brownie AI, your personal career counsellor for Indian students. "
                "I can help with:\n"
                "• Choosing the right career after Class 12 or graduation\n"
                "• College admissions and cut-offs\n"
                "• Skill gaps and learning roadmaps\n"
                "• Study abroad guidance\n"
                "• Salary benchmarks and job market trends\n\n"
                "What would you like to explore today?"
            ),
            "suggested_actions": ["Explore careers", "Take career assessment", "Book free counselling session"],
        }
