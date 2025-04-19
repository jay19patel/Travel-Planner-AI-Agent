# Import necessary libraries
import json
from langchain.prompts import ChatPromptTemplate
from agent.tools.weather_api import get_weather_forecast
from agent.state import AgentState

def create_itinerary(llm):
    """Node for creating a detailed itinerary based on selected destinations."""
    
    # Create a simple prompt template with clear variable names
    prompt = ChatPromptTemplate.from_template(
        """You are a travel agent assistant. Create a detailed day-by-day itinerary for the user based on 
        their preferences and the recommended destinations.

        User preferences:
        {user_preferences}

        Selected destinations:
        {selected_destinations}

        Weather forecast for the destination(s):
        {weather_forecast}

        Create a detailed itinerary with:
        1. Day-by-day breakdown
        2. Morning, afternoon, and evening activities
        3. Suggested accommodations
        4. Transportation recommendations
        5. Estimated costs for activities in Indian Rupees (₹)

        IMPORTANT: Always display all costs in Indian Rupees (₹) and use the budget_inr field from the destination data.
        For example: "Hotel: ₹2,500 per night", "Meal: ₹300-500 per person", "Activity: ₹1,200 per person"

        The trip should last for {trip_duration} days based on the user's preferences.
        Format the itinerary in a clear, readable manner.
        """
    )
    
    def _create_itinerary(state):
        # Step 1: Check if this is a follow-up request and we already have an itinerary
        # If so, we don't need to create a new one
        if state.is_followup and state.itinerary:
            return state
        
        # Step 2: Get the top destination from our ranked list
        # If no destinations were found, use a placeholder
        top_destination = state.destinations[0] if state.destinations else {"name": "Unknown", "country": "Unknown"}
        
        # Step 3: Get weather forecast for the destination
        # This comes from our weather API tool
        weather = get_weather_forecast(top_destination["name"])
        
        # Step 4: Get the trip duration from user preferences (default to 7 days)
        duration = state.preferences.get("duration", 7)
        
        # Step 5: Format the prompt as a plain string
        prompt_string = prompt.format(
            user_preferences=json.dumps(state.preferences, indent=2),
            selected_destinations=json.dumps([top_destination], indent=2),
            weather_forecast=json.dumps(weather, indent=2),
            trip_duration=duration
        )
        
        # Step 6: Send the prompt to the LLM to generate an itinerary
        response = llm.generate_content(prompt_string)
        
        # Extract the text content from the response
        try:
            response_content = response.text
        except AttributeError:
            response_content = response.candidates[0].content if hasattr(response, "candidates") else str(response)
        
        # Step 7: Create a simple itinerary object with the key information
        itinerary = {
            "destination": top_destination["name"],
            "duration": duration,
            "plan": response_content
        }
        
        # Step 8: Save the itinerary to the agent's state
        state.itinerary = itinerary
        
        # Step 9: Add a system message to track that we created an itinerary
        state.history.append({
            "role": "system",
            "content": f"Created itinerary for {top_destination['name']}"
        })
        
        # Step 10: Add the assistant's response with the itinerary to the conversation
        state.history.append({
            "role": "assistant",
            "content": f"Here's your {duration}-day itinerary for {top_destination['name']}, {top_destination['country']}:\n\n{response_content}\n\nDo you have any questions about this itinerary or would you like me to modify anything?"
        })
        
        # Step 11: Return the updated state
        return state
    
    return _create_itinerary