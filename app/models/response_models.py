from typing import Optional, Any, TypeVar, Generic
from pydantic import BaseModel

DataT = TypeVar('DataT')

class APIResponse(BaseModel, Generic[DataT]):
    """Standard API response model."""
    success: bool
    data: Optional[DataT] = None
    error: Optional[str] = None 