from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field

class StyleTone(str, Enum):
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    ACADEMIC = "academic"
    INNOVATIVE = "innovative"
    EDUCATIONAL = "educational"

class ContentFormat(str, Enum):
    LONG_FORM = "long_form"
    SHORT_POSTS = "short_posts"
    VIDEO = "video"
    TUTORIAL = "tutorial"
    CASE_STUDY = "case_study"

class Platform(str, Enum):
    LINKEDIN = "LinkedIn"
    TWITTER = "Twitter"
    YOUTUBE = "YouTube"
    MEDIUM = "Medium"
    PERSONAL_BLOG = "Personal Blog"
    TIKTOK = "TikTok"

class Language(str, Enum):
    ENGLISH = "english"
    CHINESE = "chinese"
    BILINGUAL = "bilingual"

class ExperienceLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"

class IndustryFocus(str, Enum):
    AI_ML = "AI/Machine Learning"
    BLOCKCHAIN = "Blockchain/Web3"
    EDTECH = "Educational Technology"
    HEALTHCARE = "Healthcare Tech"
    OTHER = "Other"

class PersonalBrandInput(BaseModel):
    """Input model for personal brand strategy generation."""
    
    # Basic Information
    basic_identity: str = Field(
        ...,
        description="Your current role and primary professional identity",
        example="AI Developer and Technical Writer"
    )
    
    branding_goal: str = Field(
        ...,
        description="What you want to achieve with your personal brand",
        example="Build thought leadership in AI and attract speaking opportunities"
    )
    
    # Preferences
    style_tone: StyleTone = Field(
        ...,
        description="Preferred tone for your content and communication"
    )
    
    content_format_preference: List[ContentFormat] = Field(
        ...,
        description="Preferred content formats",
        min_items=1
    )
    
    preferred_platforms: List[Platform] = Field(
        ...,
        description="Preferred platforms for content distribution",
        min_items=1
    )
    
    target_language: Language = Field(
        ...,
        description="Primary language for content creation"
    )
    
    # Professional Background
    experience_level: ExperienceLevel = Field(
        ...,
        description="Your current experience level in your field"
    )
    
    industry_focus: IndustryFocus = Field(
        ...,
        description="Your primary industry or technology focus"
    )
    
    # Optional Fields
    personal_story_highlights: Optional[str] = Field(
        None,
        description="Key highlights from your professional journey",
        example="Transitioned from traditional software development to AI research"
    )
    
    custom_keywords: Optional[List[str]] = Field(
        None,
        description="Specific keywords or topics you want to be known for",
        example=["MLOps", "Edge AI", "Technical Writing"]
    )

    class Config:
        json_schema_extra = {
            "example": {
                "basic_identity": "AI Developer and Technical Writer",
                "branding_goal": "Build thought leadership in AI and attract speaking opportunities",
                "style_tone": "professional",
                "content_format_preference": ["long_form", "tutorial"],
                "preferred_platforms": ["LinkedIn", "Medium"],
                "target_language": "english",
                "experience_level": "intermediate",
                "industry_focus": "AI/Machine Learning",
                "personal_story_highlights": "Transitioned from traditional software development to AI research",
                "custom_keywords": ["MLOps", "Edge AI", "Technical Writing"]
            }
        } 