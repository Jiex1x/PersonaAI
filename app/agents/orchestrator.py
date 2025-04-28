from typing import Dict, List, Any
from .base import BaseAgent

class AgentOrchestrator:
    """Orchestrates the workflow between different agents in the PersonalBrand.AI system."""
    
    def __init__(self):
        self.agents: List[BaseAgent] = []
        self.workflow_results: Dict[str, Any] = {}
    
    def register_agent(self, agent: BaseAgent) -> None:
        """Register a new agent in the orchestrator."""
        self.agents.append(agent)
    
    async def execute_workflow(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the personal branding workflow using registered agents.
        
        Args:
            user_input: Dictionary containing the initial user input data
            
        Returns:
            Dictionary containing the final branding strategy report
        """
        current_context = user_input.copy()
        
        for agent in self.agents:
            if not agent.validate_input(current_context):
                raise ValueError(f"Invalid input for agent: {agent.name}")
            
            # Process data through the agent
            result = await agent.process(current_context)
            
            # Store results and update context for next agent
            self.workflow_results[agent.name] = result
            current_context.update(result)
            
            # Update agent's context
            agent.update_context(current_context)
        
        return self.generate_final_report()
    
    def generate_final_report(self) -> Dict[str, Any]:
        """Generate the final Personal Brand Strategy Report."""
        return {
            "title": "Personal Brand Strategy Report",
            "brand_identity": self.workflow_results.get("BrandIdentityAgent", {}),
            "unique_strengths": self.workflow_results.get("UniqueStrengthsAgent", {}),
            "target_audience": self.workflow_results.get("TargetAudienceAgent", {}),
            "content_strategy": self.workflow_results.get("ContentStrategyAgent", {}),
            "launch_plan": self.workflow_results.get("LaunchPlanningAgent", {})
        } 