from __future__ import annotations

from app.agents.base import AgentContext, AgentResult, BaseAgent
from app.llm.base import Message
from app.llm.prompts import SCHOLARSHIP_AGENT_SYSTEM
from app.rag.retrieval import retrieve
from app.core.config import settings


class ScholarshipAgent(BaseAgent):
    name = "scholarship"
    system_prompt = SCHOLARSHIP_AGENT_SYSTEM

    async def _execute(self, ctx: AgentContext) -> AgentResult:
        profile = ctx.student_profile
        category = profile.get("category", "General")
        income = profile.get("family_income", "")
        marks = profile.get("marks", "")
        state = profile.get("state", "")
        stream = profile.get("stream", "")

        query = f"scholarship {category} {state} {stream} students India merit"
        docs = retrieve(query, collections=[settings.COLLECTION_SCHOLARSHIPS], top_k=8)
        context = "\n".join(f"- {d.text}" for d in docs[:5])

        prompt = f"""Student Profile:
- Category: {category}
- Annual Family Income: {income or 'Not specified'}
- Marks/Score: {marks}
- State: {state or 'Not specified'}
- Stream: {stream}
- Query: {ctx.user_query}

Knowledge Base Context:
{context or 'Use general knowledge about Indian scholarships.'}

Output a JSON object with key "scholarships" — array of scholarship objects.
Each: name, provider (Central Govt/State Govt/Private/NGO/International),
amount (string in INR per year), eligibility (string),
deadline (string or "Rolling"), application_url (if known else "Apply via official portal"),
why_eligible (explain why this student qualifies), documents_required (array).
List 5-8 scholarships most relevant to this student."""

        result = await self._llm_json([
            Message(role="system", content=self.system_prompt),
            Message(role="user", content=prompt),
        ])

        sources = [{"title": d.metadata.get("title", ""), "domain": "scholarship", "score": round(d.score, 3)} for d in docs[:5]]
        return AgentResult(agent=self.name, data=result, confidence=0.85, sources=sources)
