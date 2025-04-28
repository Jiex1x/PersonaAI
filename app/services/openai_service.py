import os
import openai
from typing import Dict, Any, Optional

class OpenAIService:
    def __init__(self):
        """Initialize OpenAI service with API key"""
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL_NAME", "gpt-4")

    async def test_connection(self) -> Dict[str, Any]:
        """Test connection to OpenAI API"""
        try:
            # Make a simple test request
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[{"role": "user", "content": "Test connection"}],
                max_tokens=5
            )
            return {
                "status": "ok",
                "error": None
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    async def generate_completion(
        self, 
        prompt: str,
        model: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Generate completion using OpenAI API"""
        try:
            response = await openai.ChatCompletion.acreate(
                model=model or self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return {
                "status": "success",
                "text": response.choices[0].message.content,
                "usage": response.usage
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            } 