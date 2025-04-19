# Import necessary libraries
from langchain.prompts import ChatPromptTemplate
import json
from agent.state import AgentState

def handle_followup(llm):
    """Node for handling follow-up questions about the travel plan."""
    
    # Create a simple prompt template with clear variable names
    prompt = ChatPromptTemplate.from_template(
        """You are a travel agent assistant. The user has a follow-up question or request about their travel plan.
        
        User preferences:
        {user_preferences}
        
        Current itinerary:
        {current_itinerary}
        
        Conversation history:
        {conversation_history}
        
        Follow-up question/request:
        {user_question}
        
        Please respond to the follow-up in a helpful way. If they want to modify the itinerary, suggest specific changes.
        If they have questions, provide detailed answers based on the existing plan.
        """
    )
    
    def _handle_followup(state):
        # Step 1: Get the user's follow-up question from the last message
        followup_question = state.history[-1]["content"]
        
        # Step 2: Format the conversation history to provide context
        # This creates a string with each previous message in the format "role: content"
        history_formatted = "\n".join([f"{msg['role']}: {msg['content']}" for msg in state.history[:-1]])
        
        # Step 3: Format the prompt as a plain string
        prompt_string = prompt.format(
            user_preferences=json.dumps(state.preferences, indent=2),
            current_itinerary=json.dumps(state.itinerary, indent=2),
            conversation_history=history_formatted,
            user_question=followup_question
        )
        
        # Step 4: Send the prompt to the LLM to generate a response
        response = llm.generate_content(prompt_string)
        
        # Extract the text content from the response
        try:
            response_content = response.text
        except AttributeError:
            response_content = response.candidates[0].content if hasattr(response, "candidates") else str(response)
        
        # Step 5: Add the assistant's response to the conversation history
        state.history.append({
            "role": "assistant",
            "content": response_content
        })
        
        # Step 6: Return the updated state
        return state
    
    return _handle_followup