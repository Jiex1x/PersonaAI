from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, status
from typing import Optional
import logging
from datetime import datetime, timedelta
from ..models.input_models import PersonalBrandInput
from ..models.output_models import PersonalBrandStrategy
from ..models.user_models import UserCreate, UserLogin, Token, UserInDB
from ..models.response_models import APIResponse
from ..agents import (
    BrandIdentityAgent,
    UniqueStrengthsAgent,
    TargetAudienceAgent,
    ContentStrategyAgent,
    LaunchPlanningAgent,
    AgentOrchestrator
)
from ..services.storage import save_strategy_report, get_strategy_report
from ..services.auth import (
    get_current_user,
    create_access_token,
    verify_password,
    get_password_hash,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/token", response_model=APIResponse[Token])
async def login_for_access_token(form_data: UserLogin):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    try:
        # TODO: Get user from database
        # For now, use a mock user
        user = UserInDB(
            id="test-user-id",
            email=form_data.email,
            full_name="Test User",
            hashed_password=get_password_hash("test-password"),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        if not verify_password(form_data.password, user.hashed_password):
            return APIResponse(
                success=False,
                error="Incorrect email or password"
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=access_token_expires
        )
        return APIResponse(
            success=True,
            data={"access_token": access_token, "token_type": "bearer"}
        )
    except Exception as e:
        logger.error(f"Login failed: {str(e)}", exc_info=True)
        return APIResponse(
            success=False,
            error=f"Login failed: {str(e)}"
        )

@router.post("/generate-strategy", response_model=APIResponse[PersonalBrandStrategy])
async def generate_personal_brand_strategy(
    input_data: PersonalBrandInput,
    background_tasks: BackgroundTasks,
    current_user: UserInDB = Depends(get_current_user)
):
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
            strategy=strategy_response,
            user=current_user
        )
        
        logger.info("Strategy report scheduled for storage")
        
        return APIResponse(
            success=True,
            data=strategy_response
        )
        
    except Exception as e:
        logger.error(f"Failed to generate personal brand strategy: {str(e)}", exc_info=True)
        return APIResponse(
            success=False,
            error=f"Failed to generate personal brand strategy: {str(e)}"
        )

@router.get("/strategy/{strategy_id}", response_model=APIResponse[PersonalBrandStrategy])
async def get_strategy(
    strategy_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Retrieve a previously generated personal brand strategy by ID.
    """
    try:
        logger.info(f"Attempting to retrieve strategy with ID: {strategy_id}")
        strategy = await get_strategy_report(strategy_id, current_user)
        return APIResponse(
            success=True,
            data=strategy
        )
    except Exception as e:
        logger.error(f"Failed to retrieve strategy: {str(e)}", exc_info=True)
        return APIResponse(
            success=False,
            error=f"Failed to retrieve strategy: {str(e)}"
        ) 