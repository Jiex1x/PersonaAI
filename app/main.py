from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from .api.routes import router as api_router
from .core.exception_handlers import validation_exception_handler, general_exception_handler
from .models.response_models import APIResponse
import os
import logging
import sys
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

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

class ResponseWrapperMiddleware(BaseHTTPMiddleware):
    """Middleware to wrap all successful responses in our standard format."""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # If the response is already a JSONResponse, don't wrap it again
        if isinstance(response, JSONResponse):
            return response
            
        # Get the response body
        body = b""
        async for chunk in response.body_iterator:
            body += chunk
        
        # Wrap the response in our standard format
        wrapped_response = APIResponse(
            success=True,
            data=body.decode() if body else None
        )
        
        return JSONResponse(
            status_code=response.status_code,
            content=wrapped_response.model_dump()
        )

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

# Add response wrapper middleware
app.add_middleware(ResponseWrapperMiddleware)

# Add exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

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
