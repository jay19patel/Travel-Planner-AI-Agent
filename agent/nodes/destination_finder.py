# Import necessary libraries
import json
import os
from langchain.prompts import ChatPromptTemplate
from agent.tools.destination_db import get_destinations
from agent.state import AgentState

def find_destinations(llm):
    """Node for finding suitable destinations based on user preferences."""
    
    # Create a simple prompt template with clear variables
    prompt = ChatPromptTemplate.from_template(
        """You are a travel agent assistant. Based on the user preferences and available destinations, 
        recommend the top 3 most suitable destinations.

        User preferences:
        {user_preferences}

        Available destinations:
        {available_destinations}

        For each recommended destination, provide:
        1. Name and country
        2. Why it's a good match for the preferences
        3. Best time to visit
        4. Estimated budget requirements in Indian Rupees (₹)

        IMPORTANT: Always display all costs in Indian Rupees (₹) and use the budget_inr field from the destination data.
        For example: "Budget: ₹15,000-40,000 for a 5-day trip"

        Return your recommendations in a well-formatted response that's ready to show to the user.
        """
    )
    
    def _find_destinations(state):
        # Step 1: Load all possible destinations from our database
        all_destinations = get_destinations()
        
        # Step 2: Prepare to score each destination based on user preferences
        filtered_destinations = []
        
        # Step 3: Score each destination based on how well it matches preferences
        for dest in all_destinations:
            score = 0
            
            # Budget matching - higher score for exact matches
            if "budget" in state.preferences:
                if state.preferences["budget"] == dest["budget_level"]:
                    # Exact budget match
                    score += 2
                # Give some points if user wants higher budget than needed
                elif (state.preferences["budget"] == "high" and dest["budget_level"] in ["medium", "low"]) or \
                     (state.preferences["budget"] == "medium" and dest["budget_level"] == "low"):
                    score += 1
            
            # Duration matching - check if destination's ideal duration includes user's preference
            if "duration" in state.preferences:
                if dest["ideal_duration"][0] <= state.preferences["duration"] <= dest["ideal_duration"][1]:
                    score += 2
            
            # Interests matching - add points for each matching interest
            if "interests" in state.preferences:
                for interest in state.preferences["interests"]:
                    # Case-insensitive matching of interests to destination tags
                    if interest.lower() in [tag.lower() for tag in dest["tags"]]:
                        score += 1
            
            # Season matching - check if user's preferred season is good for this destination
            if "season" in state.preferences:
                if state.preferences["season"].lower() in [s.lower() for s in dest["best_seasons"]]:
                    score += 2
            
            # Save the score with the destination
            dest["match_score"] = score
            filtered_destinations.append(dest)
        
        # Step 4: Sort destinations by score and take the top 5
        filtered_destinations.sort(key=lambda x: x["match_score"], reverse=True)
        top_destinations = filtered_destinations[:5]
        
        # Step 5: Save the best destinations to the agent's state
        state.destinations = top_destinations
        
        # Step 6: Format the prompt as a plain string
        prompt_string = prompt.format(
            user_preferences=json.dumps(state.preferences, indent=2),
            available_destinations=json.dumps(top_destinations, indent=2)
        )
        
        # Step 7: Send the prompt to the LLM and get recommendations
        response = llm.generate_content(prompt_string)
        
        # Extract the text content from the response
        try:
            response_content = response.text
        except AttributeError:
            response_content = response.candidates[0].content if hasattr(response, "candidates") else str(response)
        
        # Step 8: Add a system message to track selected destinations
        state.history.append({
            "role": "system",
            "content": f"Selected destinations: {[d['name'] for d in top_destinations]}"
        })
        
        # Step 9: Add the assistant's recommendations to the conversation history
        state.history.append({
            "role": "assistant",
            "content": response_content
        })
        
        # Step 10: Return the updated state
        return state
    
    return _find_destinations