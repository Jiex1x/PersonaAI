import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import Dict, Optional, List, Any
from pydantic import BaseModel
from services.azure_openai import OpenAIService
from services.azure_search import AzureSearchService

# Load environment variables
load_dotenv()

# Validate required environment variables
required_env_vars = {
    "OPENAI_API_KEY": "OpenAI API Key",
    "OPENAI_MODEL_NAME": "OpenAI Model Name",
    "AZURE_SEARCH_SERVICE_ENDPOINT": "Azure Search Service Endpoint",
    "AZURE_SEARCH_ADMIN_KEY": "Azure Search Admin Key",
    "AZURE_SEARCH_INDEX_NAME": "Azure Search Index Name"
}

missing_vars = [desc for var, desc in required_env_vars.items() if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

app = FastAPI(
    title="PersonalBrand.AI",
    description="A multi-agent collaboration platform for personal brand incubation",
    version="1.0.0"
)

# Initialize services with proper error handling
try:
    openai_service = OpenAIService()
    azure_search_service = AzureSearchService()
except Exception as e:
    raise RuntimeError(f"Failed to initialize services: {str(e)}")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CompletionRequest(BaseModel):
    prompt: str
    model: Optional[str] = None

class SearchRequest(BaseModel):
    query: str

class DocumentInput(BaseModel):
    id: str
    content: str
    category: str

@app.get("/")
async def root():
    return {"message": "Server is running"}

@app.get("/test-services")
async def test_services() -> Dict[str, Any]:
    """
    Test connections to all required services and return detailed status
    """
    services_status = {
        "overall_status": "success",
        "services": {}
    }

    # Test OpenAI connection
    openai_status = await openai_service.test_connection()
    services_status["services"]["openai"] = openai_status

    # Test Azure Search connection
    search_status = await azure_search_service.test_connection()
    services_status["services"]["azure_search"] = search_status

    # Check if any service has failed
    if any(service.get("status") == "error" for service in services_status["services"].values()):
        services_status["overall_status"] = "error"
        raise HTTPException(
            status_code=503,
            detail={
                "message": "One or more services are unavailable",
                "status": services_status
            }
        )

    return services_status

@app.post("/test-openai")
async def test_openai_completion(request: CompletionRequest) -> Dict[str, Any]:
    """Test OpenAI completion generation"""
    result = await openai_service.generate_completion(
        prompt=request.prompt
    )
    if result["status"] == "error":
        raise HTTPException(
            status_code=500,
            detail=result
        )
    return result

@app.post("/test-search-index")
async def test_search_index_creation() -> Dict[str, Any]:
    """Test Azure Search index creation"""
    result = await azure_search_service.create_index()
    if result["status"] == "error":
        raise HTTPException(
            status_code=500,
            detail=result
        )
    return result

@app.post("/test-search")
async def test_search(request: SearchRequest) -> Dict[str, Any]:
    """Test Azure Search functionality"""
    try:
        # Add some test documents first
        test_docs = [
            {
                "id": "1",
                "content": "Azure OpenAI is a powerful service for AI applications",
                "category": "AI"
            },
            {
                "id": "2",
                "content": "Azure Search provides enterprise search capabilities",
                "category": "Search"
            }
        ]
        
        # Upload test documents
        upload_result = await azure_search_service.upload_documents(test_docs)
        if upload_result["status"] == "error":
            raise HTTPException(
                status_code=500,
                detail=upload_result
            )
            
        # Perform search
        search_result = await azure_search_service.search(request.query)
        if search_result["status"] == "error":
            raise HTTPException(
                status_code=500,
                detail=search_result
            )
        return search_result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"status": "error", "message": f"Failed to perform search: {str(e)}"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8088) 