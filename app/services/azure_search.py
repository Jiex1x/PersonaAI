import os
from typing import Dict, Any, List, Optional
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchFieldDataType,
    SearchableField
)
from azure.core.exceptions import AzureError
from dotenv import load_dotenv

load_dotenv()

class AzureSearchService:
    def __init__(self):
        """Initialize Azure Search service with credentials from environment variables."""
        self.endpoint = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")
        self.key = os.getenv("AZURE_SEARCH_ADMIN_KEY")
        self.index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")
        
        if not all([self.endpoint, self.key, self.index_name]):
            raise ValueError("Missing required Azure Search configuration")
        
        self.credential = AzureKeyCredential(self.key)
        self.index_client = SearchIndexClient(
            endpoint=self.endpoint,
            credential=self.credential
        )
        self.search_client = SearchClient(
            endpoint=self.endpoint,
            index_name=self.index_name,
            credential=self.credential
        )

    async def test_connection(self) -> Dict[str, Any]:
        """
        Test connection to Azure Search service.
        Returns a dictionary with connection status and details.
        """
        try:
            # Try to list indexes as a connection test
            list(self.index_client.list_indexes(select=['name']))
            return {
                "status": "success",
                "message": "Successfully connected to Azure Search service",
                "error": None
            }
        except AzureError as e:
            return {
                "status": "error",
                "message": "Failed to connect to Azure Search service",
                "error": str(e)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": "Unexpected error while connecting to Azure Search service",
                "error": str(e)
            }

    async def create_index(self) -> Dict[str, Any]:
        """
        Create search index with predefined schema.
        Returns a dictionary with operation status and details.
        """
        try:
            # Define the index schema
            fields = [
                SimpleField(name="id", type=SearchFieldDataType.String, key=True),
                SearchableField(name="content", type=SearchFieldDataType.String),
                SimpleField(name="category", type=SearchFieldDataType.String, filterable=True),
                SimpleField(name="timestamp", type=SearchFieldDataType.DateTimeOffset, sortable=True)
            ]
            
            index = SearchIndex(name=self.index_name, fields=fields)
            
            # Create the index
            result = self.index_client.create_or_update_index(index)
            
            return {
                "status": "success",
                "message": f"Successfully created/updated index '{self.index_name}'",
                "error": None
            }
        except AzureError as e:
            return {
                "status": "error",
                "message": f"Failed to create/update index '{self.index_name}'",
                "error": str(e)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": "Unexpected error while creating/updating index",
                "error": str(e)
            }

    async def upload_documents(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Upload documents to the search index.
        Returns a dictionary with operation status and details.
        """
        try:
            result = self.search_client.upload_documents(documents=documents)
            succeeded = sum(1 for r in result if r.succeeded)
            
            return {
                "status": "success",
                "message": f"Successfully uploaded {succeeded}/{len(documents)} documents",
                "error": None
            }
        except AzureError as e:
            return {
                "status": "error",
                "message": "Failed to upload documents",
                "error": str(e)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": "Unexpected error while uploading documents",
                "error": str(e)
            }

    async def search(self, query: str, filter: Optional[str] = None) -> Dict[str, Any]:
        """
        Search documents in the index.
        Returns a dictionary with search results and status.
        """
        try:
            results = self.search_client.search(
                search_text=query,
                filter=filter,
                include_total_count=True
            )
            
            documents = [dict(doc) for doc in results]
            
            return {
                "status": "success",
                "message": f"Found {len(documents)} results",
                "results": documents,
                "error": None
            }
        except AzureError as e:
            return {
                "status": "error",
                "message": "Failed to perform search",
                "error": str(e),
                "results": []
            }
        except Exception as e:
            return {
                "status": "error",
                "message": "Unexpected error while searching",
                "error": str(e),
                "results": []
            } 