import json
import os

def get_destinations():
    """Load destinations from the mock database."""
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up two levels to reach the project root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
    # Path to destinations.json
    json_path = os.path.join(project_root, 'data', 'destinations.json')
    
    try:
        with open(json_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # If file not found, return sample data with Indian destinations and budget in INR
        return [
            {
                "name": "Manali",
                "country": "India",
                "tags": ["mountains", "nature", "trekking", "adventure"],
                "budget_level": "medium",
                "budget_inr": {"low": "₹15,000-25,000", "medium": "₹25,000-40,000", "high": "₹40,000+"},
                "ideal_duration": [3, 7],
                "best_seasons": ["summer", "spring"]
            },
            {
                "name": "Shimla",
                "country": "India",
                "tags": ["mountains", "colonial", "scenic"],
                "budget_level": "medium",
                "budget_inr": {"low": "₹12,000-20,000", "medium": "₹20,000-35,000", "high": "₹35,000+"},
                "ideal_duration": [2, 5],
                "best_seasons": ["summer", "spring", "autumn"]
            },
            {
                "name": "Dharamshala",
                "country": "India",
                "tags": ["mountains", "spiritual", "trekking", "culture"],
                "budget_level": "low",
                "budget_inr": {"low": "₹10,000-18,000", "medium": "₹18,000-30,000", "high": "₹30,000+"},
                "ideal_duration": [3, 6],
                "best_seasons": ["spring", "autumn"]
            },
            {
                "name": "Dalhousie",
                "country": "India",
                "tags": ["mountains", "nature", "scenic", "colonial"],
                "budget_level": "medium",
                "budget_inr": {"low": "₹12,000-20,000", "medium": "₹20,000-35,000", "high": "₹35,000+"},
                "ideal_duration": [2, 5],
                "best_seasons": ["summer", "spring"]
            },
            {
                "name": "Kasol",
                "country": "India",
                "tags": ["trekking", "nature", "adventure", "backpacking"],
                "budget_level": "low",
                "budget_inr": {"low": "₹8,000-15,000", "medium": "₹15,000-25,000", "high": "₹25,000+"},
                "ideal_duration": [3, 7],
                "best_seasons": ["spring", "autumn"]
            }
        ]