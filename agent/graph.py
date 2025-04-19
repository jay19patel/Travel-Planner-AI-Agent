from langchain.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph
from agent.state import AgentState
from agent.nodes.preference_extractor import extract_preferences
from agent.nodes.destination_finder import find_destinations
from agent.nodes.itinerary_creator import create_itinerary
from agent.nodes.followup_handler import handle_followup

def build_travel_agent(llm):
    """Build the Travel Planner Agent graph."""
    
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("extract_preferences", extract_preferences(llm))
    workflow.add_node("find_destinations", find_destinations(llm))
    workflow.add_node("create_itinerary", create_itinerary(llm))
    workflow.add_node("handle_followup", handle_followup(llm))
    
    # Add edges
    workflow.add_edge("extract_preferences", "find_destinations")
    workflow.add_edge("find_destinations", "create_itinerary")
    
    # Conditional edges for routing after itinerary
    def route_after_itinerary(state):
        return "handle_followup" if state.is_followup else "__end__"
    
    workflow.add_conditional_edges(
        "create_itinerary",
        route_after_itinerary
    )
    
    # Replace direct end edge with conditional edge
    def route_after_followup(state):
        return "__end__"
    
    workflow.add_conditional_edges(
        "handle_followup",
        route_after_followup
    )
    
    # Set entry point
    def get_entry_point(state):
        return "handle_followup" if state.is_followup else "extract_preferences"
    
    workflow.set_entry_point(get_entry_point)
    workflow.set_finish_point("__end__")
    
    return workflow.compile()