from app.models.schemas import ChatRequest, ChatResponse


class ChatbotEngine:
    def reply(self, payload: ChatRequest) -> ChatResponse:
        message = payload.message.lower()
        if "skill" in message:
            reply = "List your current skills, then compare them with one target career to get a focused gap plan."
            actions = ["Run skill gap analysis", "Generate roadmap", "Book counsellor session"]
        elif "college" in message:
            reply = "College prediction works best with academic score, stream, location, budget, and entrance exams."
            actions = ["Run college prediction", "Update profile", "Save shortlist"]
        elif "career" in message:
            reply = "Start with your interests, strengths, and preferred work style. I can turn that into career matches."
            actions = ["Get career recommendations", "Add strengths", "Open roadmap"]
        else:
            reply = "I can guide you through careers, colleges, skills, roadmaps, and counselling sessions."
            actions = ["Open recommendations", "Open chatbot", "Open dashboard"]
        return ChatResponse(reply=reply, suggested_actions=actions, confidence=0.84)
