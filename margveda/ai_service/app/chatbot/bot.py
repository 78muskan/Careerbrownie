from app.models.schemas import ChatMessageRequest, ChatMessageResponse


def chat(payload: ChatMessageRequest) -> ChatMessageResponse:
    message = payload.message.lower()
    if "college" in message:
        reply = "Share your stream, score percentage, preferred location, and budget so I can suggest college matches."
        actions = ["Try college prediction", "Complete your profile"]
    elif "roadmap" in message or "career" in message:
        reply = "Tell me your target career and current level. I can turn it into a month-wise roadmap."
        actions = ["Generate roadmap", "Run skill gap analysis"]
    elif "skill" in message:
        reply = "Choose a target career and list your current skills. I will identify the missing skills."
        actions = ["Analyze skill gap", "Get recommendations"]
    else:
        reply = (
            "I am MargVedA AI. I can help with career choices, skill gaps, college prediction, "
            "roadmaps, and counselling preparation."
        )
        actions = ["Get career recommendations", "Create roadmap", "Book counsellor session"]

    return ChatMessageResponse(reply=reply, suggested_actions=actions)
