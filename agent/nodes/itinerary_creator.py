from langchain.prompts import ChatPromptTemplate
from agent.tools.weather_api import get_weather_forecast
from agent.state import AgentState

def create_itinerary(llm):
    """Node for creating a detailed itinerary based on selected destinations."""
    
    # Create a prompt template
    prompt = ChatPromptTemplate.from_template(
        """You are a travel agent assistant. Create a detailed day-by-day itinerary for the user based on 
        their preferences and the recommended destinations.

        User preferences:
        {preferences}

        Selected destinations:
        {destinations}

        Weather forecast for the destination(s):
        {weather}

        Create a detailed itinerary with:
        1. Day-by-day breakdown
        2. Morning, afternoon, and evening activities
        3. Suggested accommodations
        4. Transportation recommendations
        5. Estimated costs for activities

        The trip should last for {duration} days based on the user's preferences.
        Format the itinerary in a clear, readable manner.
        """
    )
    
    def _create_itinerary(state):
        # If this is a follow-up, skip creating a new itinerary
        if state.is_followup and state.itinerary:
            return state
        
        # Get the top destination
        top_destination = state.destinations[0] if state.destinations else {"name": "Unknown", "country": "Unknown"}
        
        # Get weather forecast (mock)
        weather = get_weather_forecast(top_destination["name"])
        
        # Determine trip duration
        duration = state.preferences.get("duration", 7)
        
        # Generate itinerary using LLM
        message = prompt.invoke({
            "preferences": json.dumps(state.preferences, indent=2),
            "destinations": json.dumps([top_destination], indent=2),
            "weather": json.dumps(weather, indent=2),
            "duration": duration
        })
        response = llm.invoke([message])
        
        # Parse itinerary (simplified for this example)
        itinerary = {
            "destination": top_destination["name"],
            "duration": duration,
            "plan": response.content
        }
        
        # Store in state
        state.itinerary = itinerary
        
        # Add to history
        state.history.append({
            "role": "system",
            "content": f"Created itinerary for {top_destination['name']}"
        })
        
        state.history.append({
            "role": "assistant",
            "content": f"Here's your {duration}-day itinerary for {top_destination['name']}, {top_destination['country']}:\n\n{response.content}\n\nDo you have any questions about this itinerary or would you like me to modify anything?"
        })
        
        return state
    
    return _create_itinerary