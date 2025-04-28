from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Optional
import logging
from ..models.input_models import PersonalBrandInput
from ..models.output_models import PersonalBrandStrategy
from ..agents import (
    BrandIdentityAgent,
    UniqueStrengthsAgent,
    TargetAudienceAgent,
    ContentStrategyAgent,
    LaunchPlanningAgent,
    AgentOrchestrator
)
from ..services.storage import save_strategy_report

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/generate-strategy", response_model=PersonalBrandStrategy)
async def generate_personal_brand_strategy(
    input_data: PersonalBrandInput,
    background_tasks: BackgroundTasks
) -> PersonalBrandStrategy:
    """
    Generate a comprehensive personal brand strategy based on user input.
    
    This endpoint orchestrates multiple AI agents to create a personalized branding strategy:
    1. Brand Identity Development
    2. Unique Strengths Analysis
    3. Target Audience Definition
    4. Content Strategy Planning
    5. Launch Schedule Creation
    """
    try:
        logger.info("Starting personal brand strategy generation")
        
        # Initialize agents
        brand_identity_agent = BrandIdentityAgent()
        unique_strengths_agent = UniqueStrengthsAgent()
        target_audience_agent = TargetAudienceAgent()
        content_strategy_agent = ContentStrategyAgent()
        launch_planning_agent = LaunchPlanningAgent()
        
        logger.info("All agents initialized successfully")
        
        # Create orchestrator
        orchestrator = AgentOrchestrator()
        
        # Register agents in the correct order
        orchestrator.register_agent(brand_identity_agent)
        orchestrator.register_agent(unique_strengths_agent)
        orchestrator.register_agent(target_audience_agent)
        orchestrator.register_agent(content_strategy_agent)
        orchestrator.register_agent(launch_planning_agent)
        
        logger.info("Starting agent workflow execution")
        
        # Execute the workflow
        strategy = await orchestrator.execute_workflow(input_data.dict())
        
        logger.info("Agent workflow completed successfully")
        
        # Convert the dictionary to our Pydantic model
        strategy_response = PersonalBrandStrategy(**strategy)
        
        # Schedule background task to save the report
        background_tasks.add_task(
            save_strategy_report,
            strategy=strategy_response
        )
        
        logger.info("Strategy report scheduled for storage")
        
        return strategy_response
        
    except Exception as e:
        logger.error(f"Failed to generate personal brand strategy: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate personal brand strategy: {str(e)}"
        )

@router.get("/strategy/{strategy_id}")
async def get_strategy(strategy_id: str) -> PersonalBrandStrategy:
    """
    Retrieve a previously generated personal brand strategy by ID.
    """
    try:
        logger.info(f"Attempting to retrieve strategy with ID: {strategy_id}")
        # TODO: Implement strategy retrieval from Azure Blob Storage
        raise HTTPException(
            status_code=501,
            detail="Strategy retrieval not implemented yet"
        )
    except Exception as e:
        logger.error(f"Failed to retrieve strategy: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve strategy: {str(e)}"
        ) 