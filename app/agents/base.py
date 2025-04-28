from typing import Dict, List, Any
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """Base class for all agents in the PersonalBrand.AI system."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.context: Dict[str, Any] = {}
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the input data and return the results.
        
        Args:
            input_data: Dictionary containing the input data for the agent
            
        Returns:
            Dictionary containing the processed results
        """
        pass
    
    def update_context(self, new_context: Dict[str, Any]) -> None:
        """Update the agent's context with new information."""
        self.context.update(new_context)
    
    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        Validate the input data before processing.
        
        Args:
            input_data: Dictionary containing the input data to validate
            
        Returns:
            Boolean indicating if the input is valid
        """
        pass 