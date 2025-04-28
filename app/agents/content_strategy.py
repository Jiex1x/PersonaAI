from typing import Dict, List, Any
from .base import BaseAgent
from openai import AsyncOpenAI
import os

class ContentStrategyAgent(BaseAgent):
    """Agent responsible for developing content strategy and platform recommendations."""
    
    def __init__(self):
        super().__init__(
            name="ContentStrategyAgent",
            description="Develops content themes and platform strategy for personal brand"
        )
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4")
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate required input fields."""
        required_fields = [
            "content_format_preference",
            "preferred_platforms",
            "target_language",
            "target_audience_profile",    # From TargetAudienceAgent
            "audience_interests",         # From TargetAudienceAgent
            "brand_title",               # From BrandIdentityAgent
        ]
        return all(field in input_data for field in required_fields)
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process user input to develop content strategy recommendations."""
        
        prompt = f"""
        Based on the following personal brand and audience information:
        
        Brand Title: {input_data['brand_title']}
        Target Audience: {input_data['target_audience_profile']}
        Audience Interests: {', '.join(input_data['audience_interests'])}
        Preferred Content Formats: {', '.join(input_data['content_format_preference'])}
        Preferred Platforms: {', '.join(input_data['preferred_platforms'])}
        Target Language: {input_data['target_language']}
        
        Please provide:
        1. List of recommended platforms for content distribution (prioritized)
        2. 3-5 main content themes/topics to focus on
        3. Recommended content formats for each platform
        
        Format the response as a JSON object with keys:
        - recommended_platforms (array of strings)
        - content_themes (array of strings)
        - content_formats (array of strings)
        
        Ensure recommendations are practical and aligned with the target audience's preferences.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert content strategist who excels at developing engaging content strategies for professional personal brands."
                    },
                    {"role": "user", "content": prompt}
                ]
            )
            
            # In production, add proper JSON parsing
            # This is a simplified example response structure
            return {
                "recommended_platforms": [
                    "LinkedIn",
                    "Twitter",
                    "Personal Blog",
                    "YouTube"
                ],
                "content_themes": [
                    "AI Project Showcases",
                    "Technical Tutorial Series",
                    "Industry Trends Analysis",
                    "Career Growth Tips",
                    "Behind-the-Scenes Development"
                ],
                "content_formats": [
                    "Technical Blog Posts",
                    "Code Walkthrough Videos",
                    "LinkedIn Articles",
                    "Twitter Threads",
                    "Live Coding Sessions"
                ]
            }
            
        except Exception as e:
            raise Exception(f"Failed to process content strategy development: {str(e)}") 