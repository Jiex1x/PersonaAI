from typing import Dict, List, Any
from .base import BaseAgent
import openai
import os

class BrandIdentityAgent(BaseAgent):
    """Agent responsible for defining the user's brand identity."""
    
    def __init__(self):
        super().__init__(
            name="BrandIdentityAgent",
            description="Helps define user's professional brand identity and positioning"
        )
        self.model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4")
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate required input fields."""
        required_fields = [
            "basic_identity",
            "branding_goal",
            "style_tone",
            "industry_focus"
        ]
        return all(field in input_data for field in required_fields)
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process user input to generate brand identity recommendations."""
        
        # Construct prompt for the LLM
        prompt = f"""
        Based on the following information about a professional seeking to build their personal brand:
        
        Background: {input_data['basic_identity']}
        Goal: {input_data['branding_goal']}
        Style/Tone: {input_data['style_tone']}
        Industry: {input_data['industry_focus']}
        
        Please provide:
        1. A concise brand title (e.g. "AI Developer and Tech Educator")
        2. A memorable brand slogan
        3. Three core brand values that align with their identity
        
        Format the response as a JSON object with keys: brand_title, brand_slogan, core_values (array)
        """
        
        # Call OpenAI API
        response = await openai.ChatCompletion.acreate(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a personal branding expert."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract and structure the response
        try:
            result = response.choices[0].message.content
            # Note: In production, add proper JSON parsing and error handling
            
            return {
                "brand_title": "Example: AI Developer and Tech Educator",  # Replace with actual parsed result
                "brand_slogan": "Example: Building AI, Inspiring Minds",   # Replace with actual parsed result
                "core_values": ["Innovation", "Authenticity", "Growth"]    # Replace with actual parsed result
            }
        except Exception as e:
            raise Exception(f"Failed to process brand identity: {str(e)}") 