from typing import Dict, List, Any
from .base import BaseAgent
import openai
import os

class LaunchPlanningAgent(BaseAgent):
    """Agent responsible for creating a concrete launch plan and content calendar."""
    
    def __init__(self):
        super().__init__(
            name="LaunchPlanningAgent",
            description="Develops actionable launch plan and content calendar for personal brand"
        )
        self.model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4")
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate required input fields."""
        required_fields = [
            "recommended_platforms",    # From ContentStrategyAgent
            "content_themes",          # From ContentStrategyAgent
            "content_formats",         # From ContentStrategyAgent
            "brand_title",            # From BrandIdentityAgent
            "personal_story"          # From UniqueStrengthsAgent
        ]
        return all(field in input_data for field in required_fields)
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process user input to create launch schedule and content calendar."""
        
        prompt = f"""
        Based on the following content strategy and brand information:
        
        Brand Title: {input_data['brand_title']}
        Platforms: {', '.join(input_data['recommended_platforms'])}
        Content Themes: {', '.join(input_data['content_themes'])}
        Content Formats: {', '.join(input_data['content_formats'])}
        Personal Story: {input_data['personal_story']}
        
        Please create:
        1. A 12-week launch plan with specific content pieces and timing
        2. Each week should have 2-3 content pieces across different platforms
        3. Start with introduction content and gradually build complexity
        
        Format the response as a JSON array of weekly plans, each containing:
        - week_number (int)
        - content_type (string)
        - topic (string)
        - platform (string)
        
        Ensure the plan is realistic and manageable for one person to execute.
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert content calendar strategist who excels at creating realistic and impactful launch plans."
                    },
                    {"role": "user", "content": prompt}
                ]
            )
            
            # In production, add proper JSON parsing
            # This is a simplified example response structure
            return {
                "launch_schedule": [
                    {
                        "week_number": 1,
                        "content": [
                            {
                                "content_type": "Article",
                                "topic": "Personal Introduction and Vision",
                                "platform": "LinkedIn"
                            },
                            {
                                "content_type": "Thread",
                                "topic": "My AI Journey Highlights",
                                "platform": "Twitter"
                            }
                        ]
                    },
                    {
                        "week_number": 2,
                        "content": [
                            {
                                "content_type": "Tutorial",
                                "topic": "Building Your First AI Model",
                                "platform": "Personal Blog"
                            },
                            {
                                "content_type": "Video",
                                "topic": "Code Walkthrough",
                                "platform": "YouTube"
                            }
                        ]
                    }
                    # Additional weeks would be included in production
                ]
            }
            
        except Exception as e:
            raise Exception(f"Failed to create launch plan: {str(e)}") 