"""Unit tests for AI chatbot engine."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.chatbot.bot import chat
from app.models.schemas import ChatMessageRequest


def _chat(message: str):
    return chat(ChatMessageRequest(message=message))


class TestChatbotKeywordRouting:
    def test_college_keyword_triggers_college_reply(self):
        resp = _chat("I want to know about college admissions")
        assert "college" in resp.reply.lower() or "stream" in resp.reply.lower()
        assert len(resp.suggested_actions) > 0

    def test_career_keyword_triggers_roadmap_reply(self):
        resp = _chat("What career should I choose?")
        assert "career" in resp.reply.lower() or "roadmap" in resp.reply.lower()

    def test_roadmap_keyword_triggers_roadmap_reply(self):
        resp = _chat("Help me build a roadmap")
        assert "roadmap" in resp.reply.lower()

    def test_skill_keyword_triggers_skill_gap_reply(self):
        resp = _chat("Which skills should I learn?")
        assert "skill" in resp.reply.lower()

    def test_unknown_input_returns_generic_reply(self):
        resp = _chat("Tell me something random")
        assert resp.reply
        assert len(resp.suggested_actions) >= 1

    def test_reply_is_never_empty(self):
        for msg in ["", "   ", "12345", "?????????"]:
            resp = _chat(msg)
            assert resp.reply.strip()

    def test_suggested_actions_always_list(self):
        resp = _chat("hello")
        assert isinstance(resp.suggested_actions, list)

    def test_case_insensitive_matching(self):
        resp_lower = _chat("college")
        resp_upper = _chat("COLLEGE")
        assert resp_lower.reply == resp_upper.reply


class TestChatbotIntegration:
    def test_http_chatbot_endpoint(self):
        from fastapi.testclient import TestClient
        from app.main import app
        client = TestClient(app)
        r = client.post("/chatbot/chat", json={"message": "help with career"})
        assert r.status_code == 200
        assert "reply" in r.json()
        assert "suggested_actions" in r.json()
