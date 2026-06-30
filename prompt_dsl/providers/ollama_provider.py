from .base_provider import BaseProvider


class OllamaProvider(BaseProvider):
    def generate(self, prompt: str) -> str:
        return f"[ollama MOCK RESPONSE for prompt length {len(prompt)}]"
