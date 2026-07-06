"""CBES Volume 1 unit tests — CareerBrain AI Architecture.

Tests are Django TestCase classes so the test runner picks them up automatically:
    python manage.py test apps.ai

Coverage:
  - GatewayMessage / GatewayResponse data structures
  - AIGatewayRouter: provider selection and fallback
  - AgentRegistry: register + select + bootstrap
  - CareerAgent: escalation detection and suggestion extraction
  - ConversationMemory: load / append / clear / max-turns trimming
  - CareerBrain.process: end-to-end with all externals mocked
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

from django.test import TestCase

from apps.ai.gateway.base import GatewayMessage, GatewayResponse
from apps.ai.agents.base import AgentResult


# ─── Gateway ─────────────────────────────────────────────────────────────────

class GatewayDataStructuresTest(TestCase):
    def test_gateway_message_fields(self):
        msg = GatewayMessage(role="user", content="Hello")
        self.assertEqual(msg.role, "user")
        self.assertEqual(msg.content, "Hello")

    def test_gateway_response_defaults(self):
        resp = GatewayResponse(text="Answer", model="test-model")
        self.assertEqual(resp.text, "Answer")
        self.assertEqual(resp.input_tokens, 0)
        self.assertEqual(resp.output_tokens, 0)
        self.assertFalse(resp.from_cache)


class AIGatewayRouterTest(TestCase):
    def _make_router(self, ollama_available=False, anthropic_available=False):
        from apps.ai.gateway.router import AIGatewayRouter
        router = AIGatewayRouter.__new__(AIGatewayRouter)

        ollama = MagicMock()
        ollama.name = "ollama"
        ollama.is_available = ollama_available
        ollama.complete.return_value = GatewayResponse(text="Ollama answer", model="ollama") if ollama_available else None

        anthropic = MagicMock()
        anthropic.name = "anthropic"
        anthropic.is_available = anthropic_available
        anthropic.complete.return_value = GatewayResponse(text="Anthropic answer", model="claude") if anthropic_available else None

        router._providers = [ollama, anthropic]
        return router

    def test_prefers_ollama_when_available(self):
        router = self._make_router(ollama_available=True, anthropic_available=True)
        resp = router.complete([GatewayMessage("user", "test")])
        self.assertEqual(resp.model, "ollama")

    def test_falls_back_to_anthropic_when_ollama_down(self):
        router = self._make_router(ollama_available=False, anthropic_available=True)
        resp = router.complete([GatewayMessage("user", "test")])
        self.assertEqual(resp.model, "claude")

    def test_returns_fallback_text_when_all_down(self):
        router = self._make_router(ollama_available=False, anthropic_available=False)
        resp = router.complete([GatewayMessage("user", "test")])
        self.assertEqual(resp.model, "fallback")
        self.assertIn("unable", resp.text.lower())

    def test_active_provider_name(self):
        router = self._make_router(ollama_available=True)
        self.assertEqual(router.active_provider, "ollama")

    def test_active_provider_fallback_name(self):
        router = self._make_router()
        self.assertEqual(router.active_provider, "fallback")


# ─── Agent Registry ───────────────────────────────────────────────────────────

class AgentRegistryTest(TestCase):
    def setUp(self):
        from apps.ai.agents.registry import AgentRegistry
        AgentRegistry.bootstrap()

    def tearDown(self):
        from apps.ai.agents.registry import AgentRegistry
        AgentRegistry._agents.pop("_test_agent_", None)

    def test_register_and_retrieve(self):
        from apps.ai.agents.registry import AgentRegistry
        from apps.ai.agents.base import BaseAgent

        @AgentRegistry.register("_test_agent_")
        class _TestAgent(BaseAgent):
            goal = "test"
            def run(self, **kwargs): ...

        agent = AgentRegistry().select("_test_agent_")
        self.assertIsInstance(agent, _TestAgent)

    def test_unknown_hint_returns_career_agent(self):
        from apps.ai.agents.registry import AgentRegistry
        agent = AgentRegistry().select("nonexistent")
        self.assertEqual(agent.name, "career")

    def test_bootstrap_registers_career_crm_booking(self):
        from apps.ai.agents.registry import AgentRegistry
        self.assertIn("career", AgentRegistry._agents)
        self.assertIn("crm", AgentRegistry._agents)
        self.assertIn("booking", AgentRegistry._agents)

    def test_all_names(self):
        from apps.ai.agents.registry import AgentRegistry
        names = AgentRegistry().all_names()
        self.assertIn("career", names)


# ─── Career Agent ─────────────────────────────────────────────────────────────

class CareerAgentEscalationTest(TestCase):
    def setUp(self):
        from apps.ai.agents.career.agent import CareerAgent
        self.agent = CareerAgent()

    def test_escalation_on_mental_health_keyword(self):
        self.assertTrue(self.agent._needs_escalation("I feel depressed about my career"))

    def test_escalation_on_suicid_substring(self):
        self.assertTrue(self.agent._needs_escalation("I have suicidal thoughts"))

    def test_no_escalation_on_normal_query(self):
        self.assertFalse(self.agent._needs_escalation("What is the best career after PCM?"))

    def test_no_escalation_on_mixed_case(self):
        self.assertFalse(self.agent._needs_escalation("Should I choose Mechanical or Civil Engineering?"))


class CareerAgentSuggestionExtractionTest(TestCase):
    def test_extracts_questions_as_suggestions(self):
        from apps.ai.agents.career.agent import CareerAgent
        text = (
            "Data science is growing rapidly in India.\n"
            "Would you like to explore the required skills for data science?\n"
            "Can I help you compare data science vs software engineering?\n"
            "Some static line here.\n"
            "Do you want to see a 12-month learning roadmap for data science?\n"
        )
        suggestions = CareerAgent._extract_suggestions(text)
        self.assertEqual(len(suggestions), 3)
        for s in suggestions:
            self.assertTrue(s.endswith("?"))

    def test_caps_at_three(self):
        from apps.ai.agents.career.agent import CareerAgent
        text = "\n".join([
            "Would you like to know about JEE preparation strategies?",
            "Are you interested in comparing IIT vs NIT placements?",
            "Should I help you with the NEET entrance exam timeline?",
            "Do you want a breakdown of engineering branches by salary?",
        ])
        suggestions = CareerAgent._extract_suggestions(text)
        self.assertLessEqual(len(suggestions), 3)


class CareerAgentMessageBuildTest(TestCase):
    def test_system_message_added_first(self):
        from apps.ai.agents.career.agent import CareerAgent
        msgs = CareerAgent._build_messages("my query", [], {}, "")
        self.assertEqual(msgs[0].role, "system")
        self.assertEqual(msgs[-1].role, "user")
        self.assertEqual(msgs[-1].content, "my query")

    def test_student_context_appended_to_system(self):
        from apps.ai.agents.career.agent import CareerAgent
        msgs = CareerAgent._build_messages("q", [], {"class": "12", "stream": "PCM"}, "")
        system_content = msgs[0].content
        self.assertIn("class", system_content)
        self.assertIn("stream", system_content)

    def test_rag_context_appended_to_system(self):
        from apps.ai.agents.career.agent import CareerAgent
        msgs = CareerAgent._build_messages("q", [], {}, "Relevant KB chunk here")
        self.assertIn("Relevant KB chunk here", msgs[0].content)

    def test_history_trimmed_to_last_8_turns(self):
        from apps.ai.agents.career.agent import CareerAgent
        history = [{"role": "user", "content": f"q{i}"} for i in range(20)]
        msgs = CareerAgent._build_messages("final", history, {}, "")
        user_msgs = [m for m in msgs if m.role == "user"]
        self.assertLessEqual(len(user_msgs), 9)


# ─── Conversation Memory ──────────────────────────────────────────────────────

class ConversationMemoryTest(TestCase):
    def setUp(self):
        from apps.ai.memory.short_term import ConversationMemory
        self.mem = ConversationMemory()

    def tearDown(self):
        self.mem.clear("test-session")

    def test_empty_session_returns_empty_list(self):
        result = self.mem.load("test-session")
        self.assertEqual(result, [])

    def test_append_and_load(self):
        self.mem.append("test-session", "Hello", "Hi there!")
        history = self.mem.load("test-session")
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["role"], "user")
        self.assertEqual(history[0]["content"], "Hello")
        self.assertEqual(history[1]["role"], "assistant")
        self.assertEqual(history[1]["content"], "Hi there!")

    def test_clear_removes_session(self):
        self.mem.append("test-session", "Hello", "Hi")
        self.mem.clear("test-session")
        self.assertEqual(self.mem.load("test-session"), [])

    def test_length_counts_turns_not_messages(self):
        self.mem.append("test-session", "q1", "a1")
        self.mem.append("test-session", "q2", "a2")
        self.assertEqual(self.mem.length("test-session"), 2)

    @patch("apps.ai.memory.short_term._MAX_TURNS", 2)
    def test_max_turns_trims_oldest(self):
        for i in range(4):
            self.mem.append("test-session", f"q{i}", f"a{i}")
        history = self.mem.load("test-session")
        self.assertLessEqual(len(history), 4)


# ─── CareerBrain end-to-end (mocked) ─────────────────────────────────────────

class CareerBrainProcessTest(TestCase):
    def _make_brain(self):
        from apps.ai.careerbrain.brain import CareerBrain, BrainRequest

        brain = CareerBrain.__new__(CareerBrain)

        mock_gateway = MagicMock()
        mock_gateway.active_provider = "mock"
        mock_gateway.complete.return_value = GatewayResponse(
            text="Data science is a great career choice.\nWould you like a roadmap for data science?",
            model="mock-model",
            output_tokens=50,
        )

        mock_rag = MagicMock()
        mock_rag.health.return_value = "ok"
        mock_rag.search.return_value = {"hits": []}

        mock_svc = MagicMock()
        mock_svc.gateway = mock_gateway
        mock_svc.rag = mock_rag
        mock_svc.short_mem = MagicMock()
        mock_svc.short_mem.load.return_value = []
        mock_svc.long_mem = MagicMock()
        mock_svc.long_mem.load.return_value = {}

        from apps.ai.agents.registry import AgentRegistry
        AgentRegistry.bootstrap()  # idempotent — modules already cached after first call
        brain._registry = AgentRegistry()
        brain._svc = mock_svc

        return brain, BrainRequest

    def test_process_returns_brain_response(self):
        from apps.ai.careerbrain.brain import BrainResponse
        brain, BrainRequest = self._make_brain()
        resp = brain.process(BrainRequest(query="What career after PCM?", session_id="s1"))
        self.assertIsInstance(resp, BrainResponse)
        self.assertIn("data science", resp.answer.lower())
        self.assertEqual(resp.agent_used, "career")

    def test_process_records_latency(self):
        brain, BrainRequest = self._make_brain()
        resp = brain.process(BrainRequest(query="What career after PCM?"))
        self.assertGreaterEqual(resp.latency_ms, 0)

    def test_process_saves_to_short_memory(self):
        brain, BrainRequest = self._make_brain()
        brain.process(BrainRequest(query="Hello", session_id="sess-abc"))
        brain._svc.short_mem.append.assert_called_once()
        call_args = brain._svc.short_mem.append.call_args[0]
        self.assertEqual(call_args[0], "sess-abc")
        self.assertEqual(call_args[1], "Hello")

    def test_process_skips_memory_when_no_session(self):
        brain, BrainRequest = self._make_brain()
        brain.process(BrainRequest(query="Hello"))
        brain._svc.short_mem.append.assert_not_called()

    def test_process_loads_student_profile_when_user_id_given(self):
        brain, BrainRequest = self._make_brain()
        brain.process(BrainRequest(query="Hello", user_id=99))
        brain._svc.long_mem.load.assert_called_once_with(99)

    def test_escalation_flag_propagates(self):
        brain, BrainRequest = self._make_brain()
        resp = brain.process(BrainRequest(query="I feel depressed about my future"))
        self.assertTrue(resp.needs_counselor)
