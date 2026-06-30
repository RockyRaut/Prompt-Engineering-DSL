from .base_provider import BaseProvider


class OpenAIProvider(BaseProvider):
    def __init__(self, api_key: str = None):
        self.api_key = api_key

    def generate(self, prompt: str) -> str:
        # Placeholder: integrate with openai SDK if available
        return f"[openai MOCK RESPONSE for prompt length {len(prompt)}]"
