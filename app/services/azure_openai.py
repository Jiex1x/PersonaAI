import os
from typing import Optional, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class OpenAIService:
    def __init__(self):
        """Initialize OpenAI service with API key from environment variables."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
            
        self.client = OpenAI(
            api_key=self.api_key
        )
        self.model = os.getenv("OPENAI_MODEL_NAME", "gpt-4")

    async def test_connection(self) -> Dict[str, Any]:
        """Test the connection to OpenAI service"""
        try:
            # 使用实际的API调用来测试连接
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return {
                "status": "success",
                "message": "Successfully connected to OpenAI service",
                "details": {
                    "model": self.model
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to connect to OpenAI service: {str(e)}",
                "error_type": e.__class__.__name__,
                "error_details": {"message": str(e)}
            }

    async def generate_completion(self, prompt: str, max_tokens: int = 1000) -> Dict[str, Any]:
        """Generate completion using OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            return {
                "status": "success",
                "completion": response.choices[0].message.content,
                "error": None
            }
        except Exception as e:
            return {
                "status": "error",
                "message": "Failed to generate completion",
                "error": str(e)
            } 