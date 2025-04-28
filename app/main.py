from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router as api_router
import os
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="PersonalBrand.AI API",
    description="AI-powered personal brand strategy generation API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(
    api_router,
    prefix="/api/v1",
    tags=["brand-strategy"]
)

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "PersonalBrand.AI API",
        "version": "1.0.0",
        "description": "AI-powered personal brand strategy generation",
        "documentation": "/docs",
        "redoc": "/redoc"
    }

@app.on_event("startup")
async def startup_event():
    """Validate environment variables on startup."""
    required_vars = [
        "OPENAI_API_KEY",
        "AZURE_STORAGE_CONNECTION_STRING",
        "AZURE_STORAGE_CONTAINER_NAME"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    logger.info("All required environment variables are present")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
