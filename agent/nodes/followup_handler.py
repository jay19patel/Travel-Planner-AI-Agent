from langchain.prompts import ChatPromptTemplate
import json
from agent.state import AgentState

def handle_followup(llm):
    """Node for handling follow-up questions about the travel plan."""
    
    prompt = ChatPromptTemplate.from_template(
        """You are a travel agent assistant. The user has a follow-up question or request about their travel plan.
        
        User preferences:
        {preferences}
        
        Current itinerary:
        {itinerary}
        
        Conversation history:
        {history}
        
        Follow-up question/request:
        {followup_question}
        
        Please respond to the follow-up in a helpful way. If they want to modify the itinerary, suggest specific changes.
        If they have questions, provide detailed answers based on the existing plan.
        """
    )
    
    def _handle_followup(state):
        # Get the follow-up question
        followup_question = state.history[-1]["content"]
        
        # Format conversation history for context
        history_formatted = "\n".join([f"{msg['role']}: {msg['content']}" for msg in state.history[:-1]])
        
        # Generate response using LLM
        message = prompt.invoke({
            "preferences": json.dumps(state.preferences, indent=2),
            "itinerary": json.dumps(state.itinerary, indent=2),
            "history": history_formatted,
            "followup_question": followup_question
        })
        response = llm.invoke([message])
        
        # Add to history
        state.history.append({
            "role": "assistant",
            "content": response.content
        })
        
        return state
    
    return _handle_followup