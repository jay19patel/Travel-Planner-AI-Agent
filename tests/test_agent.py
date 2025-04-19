import unittest
from unittest.mock import patch, MagicMock
from agent.state import AgentState
from agent.graph import build_travel_agent

class TestTravelAgent(unittest.TestCase):
    
    def setUp(self):
        # Mock LLM
        self.mock_llm = MagicMock()
        self.mock_llm.invoke.return_value = MagicMock(content='{"budget": "medium", "duration": 7, "interests": ["beaches", "culture"]}')
        
        # Initialize agent
        self.agent = build_travel_agent(self.mock_llm)
        
        # Initialize base state
        self.base_state = AgentState(
            preferences={},
            destinations=[],
            itinerary={},
            history=[],
            is_followup=False
        )
    
    def test_preference_extraction(self):
        """Test that the agent can extract preferences from user input."""
        # Add a user message
        state = self.base_state
        state.history.append({
            "role": "user",
            "content": "I want to plan a week-long trip to somewhere with nice beaches. My budget is medium."
        })
        
        # Process through the agent
        with patch('agent.tools.destination_db.get_destinations', return_value=[]):
            result = self.agent.invoke(state)
        
        # Check that preferences were extracted
        self.assertIn("budget", result.preferences)
        self.assertIn("duration", result.preferences)
        self.assertIn("interests", result.preferences)
    
    def test_destination_finding(self):
        """Test that the agent can find suitable destinations."""
        # Create state with preferences
        state = self.base_state
        state.preferences = {
            "budget": "medium",
            "duration": 7,
            "interests": ["beaches", "culture"]
        }
        state.history.append({
            "role": "user",
            "content": "I want to plan a week-long trip to somewhere with nice beaches. My budget is medium."
        })
        
        # Mock destinations
        mock_destinations = [
            {
                "name": "Bali",
                "country": "Indonesia",
                "tags": ["beaches", "relaxation", "spiritual"],
                "budget_level": "medium",
                "ideal_duration": [5, 14],
                "best_seasons": ["spring", "fall"]
            }
        ]
        
        # Process through the agent
        with patch('agent.tools.destination_db.get_destinations', return_value=mock_destinations):
            result = self.agent.invoke(state)
        
        # Check that destinations were found
        self.assertGreater(len(result.destinations), 0)
    
    def test_followup_handling(self):
        """Test that the agent can handle follow-up questions."""
        # Create state with preferences, destinations, and an itinerary
        state = self.base_state
        state.preferences = {
            "budget": "medium",
            "duration": 7,
            "interests": ["beaches", "culture"]
        }
        state.destinations = [{
            "name": "Bali",
            "country": "Indonesia",
            "tags": ["beaches", "relaxation", "spiritual"],
            "budget_level": "medium",
            "ideal_duration": [5, 14],
            "best_seasons": ["spring", "fall"]
        }]
        state.itinerary = {
            "destination": "Bali",
            "duration": 7,
            "plan": "Sample itinerary for Bali"
        }
        state.history = [
            {"role": "user", "content": "I want to go to Bali for a week"},
            {"role": "assistant", "content": "Here's a plan for Bali..."}
        ]
        state.is_followup = True
        
        # Add a follow-up question
        state.history.append({
            "role": "user",
            "content": "What activities can I do if it rains?"
        })
        
        # Process through the agent
        result = self.agent.invoke(state)
        
        # Check that there's a new assistant response
        self.assertEqual(result.history[-1]["role"], "assistant")
        self.assertNotEqual(result.history[-1]["content"], "Here's a plan for Bali...")

if __name__ == '__main__':
    unittest.main()