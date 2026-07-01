from typing import Dict, Optional
import logging
from app.config.settings import settings

logger = logging.getLogger(__name__)

try:
    import openai
except ImportError:
    openai = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None


class LLMService:
    """Simple wrapper for OpenAI and Gemini conversational responses."""

    def __init__(self):
        self.provider = settings.PRIMARY_AI_PROVIDER.lower()
        self.openai_key = settings.OPENAI_API_KEY
        self.gemini_key = settings.GEMINI_API_KEY
        if self.provider == 'openai' and openai and self.openai_key:
            openai.api_key = self.openai_key
        if self.provider == 'gemini' and genai and self.gemini_key:
            genai.configure(api_key=self.gemini_key)

    def _build_prompt(self, user_message: str, context: Optional[Dict[str, object]] = None) -> str:
        if not context:
            return f"Recruiter assistant: {user_message}"
        context_text = '\n'.join([f"{key}: {value}" for key, value in context.items()])
        return f"You are an AI recruiter assistant. Use the following context:\n{context_text}\n\nUser: {user_message}"

    def generate_response(self, message: str, context: Optional[Dict[str, object]] = None) -> str:
        prompt = self._build_prompt(message, context)
        if self.provider == 'openai' and openai and self.openai_key:
            try:
                response = openai.ChatCompletion.create(
                    model=settings.OPENAI_MODEL,
                    messages=[{'role': 'user', 'content': prompt}],
                    max_tokens=300,
                )
                return response.choices[0].message.content.strip()
            except Exception as exc:
                logger.error(f"OpenAI response error: {exc}")

        if self.provider == 'gemini' and genai and self.gemini_key:
            try:
                response = genai.chat.create(
                    model=settings.OPENAI_MODEL,
                    messages=[{'role': 'user', 'content': prompt}],
                    max_output_tokens=300,
                )
                return response.last
            except Exception as exc:
                logger.error(f"Gemini response error: {exc}")

        logger.warning("No LLM provider configured or available, returning fallback response.")
        return (
            "I can help analyze candidate fit and explain rankings. "
            "Provide more detail or check the candidate ranking dashboard."
        )
