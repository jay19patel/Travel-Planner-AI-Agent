from typing import Dict, List, Any, TypedDict, Optional
from pydantic import BaseModel, Field

class AgentState(BaseModel):
    """State for the Travel Planner Agent."""
    preferences: Dict[str, Any] = Field(default_factory=dict, description="User travel preferences")
    destinations: List[Dict[str, Any]] = Field(default_factory=list, description="Suggested destinations")
    itinerary: Dict[str, Any] = Field(default_factory=dict, description="Created travel itinerary")
    history: List[Dict[str, str]] = Field(default_factory=list, description="Conversation history")
    is_followup: bool = Field(default=False, description="Whether this is a follow-up request")