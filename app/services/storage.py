import os
import json
import uuid
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from ..models.output_models import PersonalBrandStrategy

class StorageService:
    """Service for managing strategy report storage in Azure Blob Storage."""
    
    def __init__(self):
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
        
        if not connection_string or not container_name:
            raise ValueError("Azure Storage configuration is missing")
        
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)
    
    async def save_strategy(self, strategy: PersonalBrandStrategy) -> str:
        """
        Save a strategy report to Azure Blob Storage.
        
        Args:
            strategy: The strategy report to save
            
        Returns:
            str: The unique ID of the saved strategy
        """
        try:
            # Generate unique ID for the strategy
            strategy_id = str(uuid.uuid4())
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            
            # Create blob name with timestamp
            blob_name = f"strategies/{strategy_id}/{timestamp}_strategy.json"
            
            # Convert strategy to JSON using Pydantic v2 syntax
            strategy_dict = strategy.model_dump()  # New Pydantic v2 method
            strategy_json = json.dumps(strategy_dict, indent=2)
            
            # Upload to blob storage
            blob_client = self.container_client.get_blob_client(blob_name)
            blob_client.upload_blob(strategy_json, overwrite=True)
            
            return strategy_id
            
        except Exception as e:
            raise Exception(f"Failed to save strategy to storage: {str(e)}")
    
    async def get_strategy(self, strategy_id: str) -> PersonalBrandStrategy:
        """
        Retrieve a strategy report from Azure Blob Storage.
        
        Args:
            strategy_id: The unique ID of the strategy to retrieve
            
        Returns:
            PersonalBrandStrategy: The retrieved strategy report
        """
        try:
            # List all blobs in the strategy directory
            prefix = f"strategies/{strategy_id}/"
            blobs = list(self.container_client.list_blobs(name_starts_with=prefix))
            
            if not blobs:
                raise ValueError(f"No strategy found with ID: {strategy_id}")
            
            # Get the latest version (assuming timestamp in name)
            latest_blob = max(blobs, key=lambda b: b.name)
            
            # Download the blob
            blob_client = self.container_client.get_blob_client(latest_blob.name)
            strategy_json = blob_client.download_blob().readall()
            
            # Parse JSON and convert to PersonalBrandStrategy using Pydantic v2 syntax
            strategy_dict = json.loads(strategy_json)
            return PersonalBrandStrategy.model_validate(strategy_dict)
            
        except Exception as e:
            raise Exception(f"Failed to retrieve strategy from storage: {str(e)}")

# Create singleton instance
storage_service = StorageService()

async def save_strategy_report(strategy: PersonalBrandStrategy) -> str:
    """Helper function to save strategy report."""
    return await storage_service.save_strategy(strategy)

async def get_strategy_report(strategy_id: str) -> PersonalBrandStrategy:
    """Helper function to retrieve strategy report."""
    return await storage_service.get_strategy(strategy_id) 