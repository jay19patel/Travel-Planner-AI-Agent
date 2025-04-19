import json
import re
from langchain.prompts import ChatPromptTemplate
from agent.state import AgentState

def extract_preferences(llm):
    """Node for extracting travel preferences from user input."""
    
    # Create a prompt template
    prompt = ChatPromptTemplate.from_template(
        """You are a travel agent assistant. Extract travel preferences from the user's message.
        Consider the following:
        - Budget (low, medium, high)
        - Trip duration (days)
        - Interests (e.g. beaches, food, culture)
        - Season
        - Party (solo, couple, family, group)
        - Any constraints

        User message: {user_input}

        Return only a JSON object like:
        ```json
        {{
            "budget": "medium",
            "duration": 7,
            "interests": ["beaches", "food"],
            "season": "summer",
            "party": "couple",
            "constraints": "no long flights"
        }}
        ```
        Only include fields you are confident about.
        """
    )
    
    def _extract_preferences(state: AgentState):
        # Get the latest user message
        user_message = state.history[-1]["content"]

        # Format the prompt as a plain string
        prompt_string = prompt.format(user_input=user_message)

        # Use Google's Gemini model (or any other that supports `generate_content`)
        response = llm.generate_content(prompt_string)

        # Extract the text content from the response
        try:
            response_text = response.text
        except AttributeError:
            response_text = response.candidates[0].content if hasattr(response, "candidates") else str(response)

        # Extract JSON using regex
        json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_str = response_text  # Fallback

        # Try to parse the JSON
        try:
            extracted_preferences = json.loads(json_str)
        except json.JSONDecodeError:
            extracted_preferences = {"error": "Could not parse preferences"}

        # Update the agent state
        state.preferences.update(extracted_preferences)

        # Add to conversation history
        state.history.append({
            "role": "system",
            "content": f"Extracted preferences: {extracted_preferences}"
        })

        # Acknowledge to the user
        acknowledgment = f"I understand you're looking for a {state.preferences.get('duration', 'short')} day trip "
        if "budget" in state.preferences:
            acknowledgment += f"with a {state.preferences['budget']} budget "
        if "interests" in state.preferences:
            interests = state.preferences["interests"]
            if len(interests) > 1:
                interests_str = ", ".join(interests[:-1]) + " and " + interests[-1]
            else:
                interests_str = interests[0]
            acknowledgment += f"focused on {interests_str}. "
        else:
            acknowledgment += ". "
        acknowledgment += "Let me find some suitable destinations for you."

        # Add the assistant's reply
        state.history.append({
            "role": "assistant",
            "content": acknowledgment
        })

        return state

    return _extract_preferences
