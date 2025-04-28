from typing import Dict, List, Any
from .base import BaseAgent
from openai import AsyncOpenAI
import os

class UniqueStrengthsAgent(BaseAgent):
    """Agent responsible for identifying user's unique strengths and compelling story."""
    
    def __init__(self):
        super().__init__(
            name="UniqueStrengthsAgent",
            description="Identifies and articulates user's unique professional strengths and story"
        )
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4")
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate required input fields."""
        required_fields = [
            "basic_identity",
            "experience_level",
            "personal_story_highlights",
            "brand_title"  # From BrandIdentityAgent
        ]
        return all(field in input_data for field in required_fields)
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process user input to identify unique strengths and craft personal story."""
        
        prompt = f"""
        Based on the following information about a professional:
        
        Current Role/Identity: {input_data['basic_identity']}
        Experience Level: {input_data['experience_level']}
        Key Story Points: {input_data['personal_story_highlights']}
        Brand Title: {input_data['brand_title']}
        
        Please analyze and provide:
        1. List 3-5 unique professional strengths that set them apart (focus on specific capabilities, not generic traits)
        2. Craft a compelling personal story (2-3 sentences) that showcases their journey and unique value proposition
        
        Format the response as a JSON object with keys:
        - unique_strengths (array of strings)
        - personal_story (string)
        
        Make sure the strengths are specific and actionable, and the story is authentic and memorable.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert career coach and personal branding strategist who excels at identifying unique professional strengths and crafting compelling personal narratives."
                    },
                    {"role": "user", "content": prompt}
                ]
            )
            
            # In production, add proper JSON parsing
            # This is a simplified example response structure
            return {
                "unique_strengths": [
                    "Rapid Prototyping",
                    "Open Source Contributor",
                    "Cross-functional Team Leadership",
                    "Data-Driven Decision Making"
                ],
                "personal_story": (
                    "Transitioned from mechanical engineering to AI through self-learning "
                    "Python and competing in Kaggle competitions. Now combines engineering "
                    "precision with AI innovation to build practical solutions."
                )
            }
            
        except Exception as e:
            raise Exception(f"Failed to process unique strengths analysis: {str(e)}") 