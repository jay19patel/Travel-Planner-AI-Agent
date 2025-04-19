from langchain.prompts import ChatPromptTemplate
from agent.state import AgentState

def extract_preferences(llm):
    """Node for extracting travel preferences from user input."""
    
    # Create a prompt template
    prompt = ChatPromptTemplate.from_template(
        """You are a travel agent assistant. Extract travel preferences from the user's message.
        Consider the following aspects:
        - Budget (low, medium, high)
        - Trip duration (number of days)
        - Interests (e.g., beaches, mountains, culture, food, adventure)
        - Season or time of year
        - Traveling party (solo, couple, family, group)
        - Any constraints or special requirements

        User message: {user_message}

        Extract and return ONLY a JSON object with the preferences. For example:
        ```json
        {
            "budget": "medium",
            "duration": 7,
            "interests": ["beaches", "food"],
            "season": "summer",
            "party": "couple",
            "constraints": "no long flights"
        }
        ```
        Only include fields that you can confidently extract from the user message.
        """
    )
    
    def _extract_preferences(state):
        # Get the latest user message
        user_message = state.history[-1]["content"]
        
        # Invoke the LLM to extract preferences
        message = prompt.invoke({"user_message": user_message})
        response = llm.invoke([message])
        
        # Extract the JSON from the response
        import json
        import re
        
        json_match = re.search(r'```json\s*(.*?)\s*```', response.content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_str = response.content
        
        try:
            extracted_preferences = json.loads(json_str)
        except json.JSONDecodeError:
            # Fallback if we couldn't parse JSON
            extracted_preferences = {"error": "Could not parse preferences"}
        
        # Update state with extracted preferences
        state.preferences.update(extracted_preferences)
        
        # Add system message to history
        state.history.append({
            "role": "system",
            "content": f"Extracted preferences: {extracted_preferences}"
        })
        
        # Add assistant message acknowledging the preferences
        acknowledgment = f"I understand you're looking for a {state.preferences.get('duration', 'short')} day trip "
        if "budget" in state.preferences:
            acknowledgment += f"with a {state.preferences['budget']} budget "
        if "interests" in state.preferences:
            interests_str = ", ".join(state.preferences["interests"][:-1]) + " and " + state.preferences["interests"][-1] if len(state.preferences["interests"]) > 1 else state.preferences["interests"][0]
            acknowledgment += f"focused on {interests_str}. "
        else:
            acknowledgment += ". "
        acknowledgment += "Let me find some suitable destinations for you."
        
        state.history.append({
            "role": "assistant",
            "content": acknowledgment
        })
        
        return state
    
    return _extract_preferences