import os
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables.graph import MermaidDrawMethod
from dotenv import load_dotenv
from agent.state import AgentState
from agent.nodes.preference_extractor import extract_preferences
from agent.nodes.destination_finder import find_destinations
from agent.nodes.itinerary_creator import create_itinerary
from agent.nodes.followup_handler import handle_followup


def build_travel_agent(llm):
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("extract_preferences", extract_preferences(llm))
    workflow.add_node("find_destinations", find_destinations(llm))
    workflow.add_node("create_itinerary", create_itinerary(llm))
    workflow.add_node("handle_followup", handle_followup(llm))

    # Add edges
    workflow.add_edge("extract_preferences", "find_destinations")
    workflow.add_edge("find_destinations", "create_itinerary")

    def route_after_itinerary(state):
        return "handle_followup" if state.is_followup else END

    workflow.add_conditional_edges("create_itinerary", route_after_itinerary)

    def route_after_followup(state):
        return "extract_preferences" if state.is_followup else END

    workflow.add_conditional_edges("handle_followup", route_after_followup)

    workflow.set_entry_point("extract_preferences")
    return workflow.compile()
