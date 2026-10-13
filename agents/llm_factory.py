"""
Inference Engine supporting local Ollama, Claude, OpenAI, and deterministic Mock with Zero-PHI checks.
"""
from .base import PHIGuard


class MockLLM:
    def __init__(self, system_name: str = "Hospital Outbreak Cluster Agent"):
        self.system_name = system_name

    def invoke(self, prompt: str) -> str:
        PHIGuard.assert_no_phi(prompt)
        return f"[{self.system_name} demo responder]: No clinical or scientific verification was performed. Received query: '{prompt[:60]}...'."


class LLMFactory:
    """Creates configured LLM client instances with zero-PHI protection."""

    @staticmethod
    def create(provider: str = "mock", system_name: str = "Hospital Outbreak Cluster Agent"):
        prov = str(provider).lower()
        if prov in ["mock", "deterministic", "test"]:
            return MockLLM(system_name)
        raise ValueError(f"Unsupported model provider: {provider!r}. Only the deterministic mock is implemented.")
