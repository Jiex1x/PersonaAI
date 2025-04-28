from typing import List, Dict, Any
from pydantic import BaseModel, Field

class BrandIdentity(BaseModel):
    """Brand identity recommendations."""
    brand_title: str = Field(..., description="Concise professional brand title")
    brand_slogan: str = Field(..., description="Memorable brand slogan")
    core_values: List[str] = Field(..., description="Core brand values")

class UniqueStrengths(BaseModel):
    """Unique strengths and personal story."""
    unique_strengths: List[str] = Field(..., description="List of unique professional strengths")
    personal_story: str = Field(..., description="Compelling personal narrative")

class TargetAudience(BaseModel):
    """Target audience analysis."""
    target_audience_profile: str = Field(..., description="Detailed target audience description")
    audience_interests: List[str] = Field(..., description="Key audience interests and pain points")

class ContentStrategy(BaseModel):
    """Content strategy recommendations."""
    recommended_platforms: List[str] = Field(..., description="Prioritized list of content platforms")
    content_themes: List[str] = Field(..., description="Main content themes to focus on")
    content_formats: List[str] = Field(..., description="Recommended content formats")

class ContentPiece(BaseModel):
    """Individual content piece in the launch schedule."""
    content_type: str = Field(..., description="Type of content")
    topic: str = Field(..., description="Content topic")
    platform: str = Field(..., description="Platform for publication")

class WeeklyPlan(BaseModel):
    """Weekly content plan."""
    week_number: int = Field(..., description="Week number in the launch schedule")
    content: List[ContentPiece] = Field(..., description="Content pieces for the week")

class LaunchPlan(BaseModel):
    """Launch plan and schedule."""
    launch_schedule: List[WeeklyPlan] = Field(..., description="Weekly content schedule")

class PersonalBrandStrategy(BaseModel):
    """Complete personal brand strategy."""
    brand_identity: BrandIdentity = Field(..., description="Brand identity recommendations")
    unique_strengths: UniqueStrengths = Field(..., description="Unique strengths analysis")
    target_audience: TargetAudience = Field(..., description="Target audience analysis")
    content_strategy: ContentStrategy = Field(..., description="Content strategy recommendations")
    launch_plan: LaunchPlan = Field(..., description="Launch plan and schedule")
    
    class Config:
        json_schema_extra = {
            "example": {
                "brand_identity": {
                    "brand_title": "AI Developer and Tech Educator",
                    "brand_slogan": "Building AI, Inspiring Minds",
                    "core_values": ["Innovation", "Authenticity", "Growth"]
                },
                "unique_strengths": {
                    "unique_strengths": [
                        "Rapid Prototyping",
                        "Open Source Contributor",
                        "Cross-functional Team Leadership"
                    ],
                    "personal_story": "Transitioned from mechanical engineering to AI through self-learning..."
                },
                "target_audience": {
                    "target_audience_profile": "Junior AI developers and tech professionals...",
                    "audience_interests": [
                        "Learning AI fundamentals",
                        "Career growth",
                        "Technical skill development"
                    ]
                },
                "content_strategy": {
                    "recommended_platforms": ["LinkedIn", "Medium", "YouTube"],
                    "content_themes": [
                        "AI Project Showcases",
                        "Technical Tutorials",
                        "Industry Trends"
                    ],
                    "content_formats": [
                        "Technical Blog Posts",
                        "Video Tutorials",
                        "Code Walkthroughs"
                    ]
                },
                "launch_plan": {
                    "launch_schedule": [
                        {
                            "week_number": 1,
                            "content": [
                                {
                                    "content_type": "Article",
                                    "topic": "Introduction and Vision",
                                    "platform": "LinkedIn"
                                }
                            ]
                        }
                    ]
                }
            }
        } 