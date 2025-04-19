import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from google.generativeai import GenerativeModel 
from agent.graph import build_travel_agent
from agent.state import AgentState

# Load environment variables
load_dotenv()

import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def main():
    # Initialize the model
    # llm = ChatOpenAI(temperature=0.7)
    llm =  GenerativeModel('gemini-1.5-pro')
    
    # Build the travel agent
    travel_agent = build_travel_agent(llm)
    
    print("Welcome to the Travel Planner AI Agent!")
    print("Tell me about your travel preferences (budget, duration, interests, etc.)")
    
    # Initialize state
    state = AgentState(
        preferences={},
        destinations=[],
        itinerary={},
        history=[],
        is_followup=False
    )
    
    # Start conversation
    user_input = input("You: ")
    # user_input = "I want a 5-day budget trip to Himachal Pradesh focused on nature and trekking."
    
    while True:
        # Add user message to history
        if hasattr(state, 'history'):
            state.history.append({"role": "user", "content": user_input})
        else:
            # If state is a dict-like object
            if 'history' in state:
                state['history'].append({"role": "user", "content": user_input})
            else:
                # Initialize history if it doesn't exist
                state['history'] = [{"role": "user", "content": user_input}]
        
        # Process through the graph
        result = travel_agent.invoke(state)
                
        # Extract the latest assistant message from the updated state
        assistant_message = "I'm processing your request..."
        
        # Try to access history in different ways
        if hasattr(result, 'history') and result.history and isinstance(result.history[-1], dict) and result.history[-1].get("role") == "assistant":
            assistant_message = result.history[-1].get("content")
        elif isinstance(result, dict) and 'history' in result and result['history'] and isinstance(result['history'][-1], dict) and result['history'][-1].get("role") == "assistant":
            assistant_message = result['history'][-1].get("content")



        print(f"Travel Agent: {assistant_message}")
        
        # Check if user wants to exit
        user_input = input("You (type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            print("Thank you for using the Travel Planner AI Agent. Goodbye!")
            break
        
        # Update state for next iteration
        state = result
        
        # Set is_followup flag based on whether state is a dict or object
        if hasattr(state, 'is_followup'):
            state.is_followup = True
        elif isinstance(state, dict):
            state['is_followup'] = True

if __name__ == "__main__":
    main()