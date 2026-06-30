from __future__ import annotations

from app.agents.base import AgentContext, AgentResult, BaseAgent
from app.llm.base import Message
from app.llm.prompts import COLLEGE_AGENT_SYSTEM
from app.rag.retrieval import retrieve
from app.core.config import settings


class CollegeAgent(BaseAgent):
    name = "college"
    system_prompt = COLLEGE_AGENT_SYSTEM

    async def _execute(self, ctx: AgentContext) -> AgentResult:
        profile = ctx.student_profile
        stream = profile.get("stream", "")
        marks = profile.get("marks", "")
        category = profile.get("category", "General")
        budget = profile.get("budget", "")
        preferred_states = profile.get("preferred_states", [])
        target_career = profile.get("target_career", "")

        query = f"{target_career} colleges {stream} {' '.join(preferred_states)} admission cutoff {category}"
        docs = retrieve(query, collections=[settings.COLLECTION_COLLEGES, settings.COLLECTION_EXAMS], top_k=10)
        context = "\n".join(f"- {d.text}" for d in docs[:6])

        prompt = f"""Student Profile:
- Stream: {stream}
- Marks/Percentile: {marks}
- Category: {category}
- Budget (annual fees): {budget or 'Not specified'}
- Preferred States: {', '.join(preferred_states) or 'All India'}
- Target Career: {target_career or 'Not specified'}
- Query: {ctx.user_query}

Knowledge Base Context:
{context or 'No specific context. Use general knowledge about Indian colleges.'}

Output a JSON object with key "colleges" — array of college objects.
Each: name, location (city, state), tier (Tier-1/2/3), type (IIT/NIT/BITS/Private/Govt/Deemed),
cutoff_range (string, mention JEE/NEET rank or board %), fees_per_year (string in INR),
programs (array of relevant programs), why_recommended (string),
admission_process (string), placement_avg_lpa (string).
List 6-8 colleges from aspirational to safe."""

        result = await self._llm_json([
            Message(role="system", content=self.system_prompt),
            Message(role="user", content=prompt),
        ])

        sources = [{"title": d.metadata.get("title", ""), "domain": "college", "score": round(d.score, 3)} for d in docs[:5]]
        return AgentResult(agent=self.name, data=result, confidence=0.85, sources=sources)
