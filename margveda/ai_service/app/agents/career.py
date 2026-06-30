from __future__ import annotations

from app.agents.base import AgentContext, AgentResult, BaseAgent
from app.llm.base import Message
from app.llm.prompts import CAREER_AGENT_SYSTEM
from app.rag.retrieval import retrieve
from app.core.config import settings


class CareerAgent(BaseAgent):
    name = "career"
    system_prompt = CAREER_AGENT_SYSTEM

    async def _execute(self, ctx: AgentContext) -> AgentResult:
        profile = ctx.student_profile
        interests = profile.get("interests", [])
        skills = profile.get("skills", [])
        stream = profile.get("stream", "")
        marks = profile.get("marks", "")
        budget = profile.get("budget", "")

        # Retrieve relevant career documents
        search_query = f"{stream} career options interests:{','.join(interests)} skills:{','.join(skills)}"
        docs = retrieve(search_query, collections=[settings.COLLECTION_CAREERS], top_k=8)
        context = "\n".join(f"- {d.text}" for d in docs[:5])

        prompt = f"""Student Profile:
- Stream: {stream}
- Marks/CGPA: {marks}
- Interests: {', '.join(interests) or 'Not specified'}
- Skills: {', '.join(skills) or 'Not specified'}
- Budget: {budget or 'Not specified'}
- Query: {ctx.user_query}

Knowledge Base Context:
{context or 'No specific context retrieved. Use general knowledge.'}

Output a JSON object with key "careers" containing an array of career objects.
Each object must have: title, domain, match_score (0-100), why, avg_salary_india (string in LPA), growth_outlook (High/Medium/Low), required_skills (array), entry_paths (array of strings).
Recommend 5-7 careers sorted by match_score descending."""

        result = await self._llm_json([
            Message(role="system", content=self.system_prompt),
            Message(role="user", content=prompt),
        ])

        sources = [{"title": d.metadata.get("title", ""), "domain": "career", "score": round(d.score, 3)} for d in docs[:5]]
        return AgentResult(agent=self.name, data=result, confidence=0.9, sources=sources)
