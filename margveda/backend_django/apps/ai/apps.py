from django.apps import AppConfig


class AIConfig(AppConfig):
    name = "apps.ai"
    label = "careerbrain_ai"
    verbose_name = "CareerBrain AI"

    def ready(self) -> None:
        from apps.ai.agents.registry import AgentRegistry
        AgentRegistry.bootstrap()
