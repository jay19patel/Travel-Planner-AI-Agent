import json
import os
from langchain.prompts import ChatPromptTemplate
from agent.tools.destination_db import get_destinations
from agent.state import AgentState

def find_destinations(llm):
    """Node for finding suitable destinations based on user preferences."""
    
    prompt = ChatPromptTemplate.from_template(
        """You are a travel agent assistant. Based on the user preferences and available destinations, 
        recommend the top 3 most suitable destinations.

        User preferences:
        {preferences}

        Available destinations:
        {destinations}

        For each recommended destination, provide:
        1. Name and country
        2. Why it's a good match for the preferences
        3. Best time to visit
        4. Estimated budget requirements

        Return your recommendations in a well-formatted response that's ready to show to the user.
        """
    )
    
    def _find_destinations(state):
        # Load destinations from the mock database
        all_destinations = get_destinations()
        
        # Filter destinations based on preferences
        filtered_destinations = []
        
        # Simple filtering logic (can be made more sophisticated)
        for dest in all_destinations:
            score = 0
            
            # Budget match
            if "budget" in state.preferences:
                if state.preferences["budget"] == dest["budget_level"]:
                    score += 2
                elif (state.preferences["budget"] == "high" and dest["budget_level"] in ["medium", "low"]) or \
                     (state.preferences["budget"] == "medium" and dest["budget_level"] == "low"):
                    score += 1
            
            # Duration match
            if "duration" in state.preferences:
                if dest["ideal_duration"][0] <= state.preferences["duration"] <= dest["ideal_duration"][1]:
                    score += 2
            
            # Interests match
            if "interests" in state.preferences:
                for interest in state.preferences["interests"]:
                    if interest.lower() in [tag.lower() for tag in dest["tags"]]:
                        score += 1
            
            # Season match
            if "season" in state.preferences:
                if state.preferences["season"].lower() in [s.lower() for s in dest["best_seasons"]]:
                    score += 2
            
            # Add score to destination
            dest["match_score"] = score
            filtered_destinations.append(dest)
        
        # Sort by match score and take top matches
        filtered_destinations.sort(key=lambda x: x["match_score"], reverse=True)
        top_destinations = filtered_destinations[:5]
        
        # Store in state
        state.destinations = top_destinations
        
        # Generate recommendations using LLM
        message = prompt.invoke({
            "preferences": json.dumps(state.preferences, indent=2),
            "destinations": json.dumps(top_destinations, indent=2)
        })
        response = llm.invoke([message])
        
        # Add to history
        state.history.append({
            "role": "system",
            "content": f"Selected destinations: {[d['name'] for d in top_destinations]}"
        })
        
        state.history.append({
            "role": "assistant",
            "content": response.content
        })
        
        return state
    
    return _find_destinations