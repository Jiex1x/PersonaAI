from typing import Dict, List, Any
from .base import BaseAgent
from openai import AsyncOpenAI
import os

class TargetAudienceAgent(BaseAgent):
    """Agent responsible for defining and analyzing target audience."""
    
    def __init__(self):
        super().__init__(
            name="TargetAudienceAgent",
            description="Identifies and analyzes ideal target audience for personal brand"
        )
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4")
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate required input fields."""
        required_fields = [
            "branding_goal",
            "industry_focus",
            "brand_title",        # From BrandIdentityAgent
            "unique_strengths",   # From UniqueStrengthsAgent
        ]
        return all(field in input_data for field in required_fields)
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process user input to define target audience profile and interests."""
        
        prompt = f"""
        Based on the following personal brand information:
        
        Branding Goal: {input_data['branding_goal']}
        Industry Focus: {input_data['industry_focus']}
        Brand Title: {input_data['brand_title']}
        Unique Strengths: {', '.join(input_data['unique_strengths'])}
        
        Please provide:
        1. A detailed profile of the ideal target audience (who they are, their roles, career stages)
        2. List 3-5 key interests/pain points of this audience that align with the personal brand
        
        Format the response as a JSON object with keys:
        - target_audience_profile (string)
        - audience_interests (array of strings)
        
        Focus on specific, actionable insights that will help create targeted content and messaging.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert audience research analyst who excels at identifying and understanding professional audience segments."
                    },
                    {"role": "user", "content": prompt}
                ]
            )
            
            # In production, add proper JSON parsing
            # This is a simplified example response structure
            return {
                "target_audience_profile": (
                    "Junior AI developers, tech recruiters, and early-stage AI startups "
                    "looking to build practical AI solutions and grow their technical teams"
                ),
                "audience_interests": [
                    "Learning AI fundamentals and best practices",
                    "Career growth in AI/ML field",
                    "Building practical AI projects",
                    "Technical team development",
                    "Industry networking opportunities"
                ]
            }
            
        except Exception as e:
            raise Exception(f"Failed to process target audience analysis: {str(e)}") 