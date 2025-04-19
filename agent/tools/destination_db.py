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
        # If file not found, return sample data
        return [
            {
                "name": "Paris",
                "country": "France",
                "tags": ["romantic", "culture", "food"],
                "budget_level": "high",
                "ideal_duration": [3, 7],
                "best_seasons": ["spring", "fall"]
            },
            {
                "name": "Bali",
                "country": "Indonesia",
                "tags": ["beaches", "relaxation", "spiritual"],
                "budget_level": "medium",
                "ideal_duration": [5, 14],
                "best_seasons": ["spring", "fall"]
            },
            {
                "name": "Tokyo",
                "country": "Japan",
                "tags": ["culture", "food", "shopping"],
                "budget_level": "high",
                "ideal_duration": [5, 10],
                "best_seasons": ["spring", "fall"]
            },
            {
                "name": "Prague",
                "country": "Czech Republic",
                "tags": ["culture", "history", "architecture"],
                "budget_level": "medium",
                "ideal_duration": [2, 5],
                "best_seasons": ["spring", "summer"]
            },
            {
                "name": "Costa Rica",
                "country": "Costa Rica",
                "tags": ["nature", "adventure", "beaches"],
                "budget_level": "medium",
                "ideal_duration": [7, 14],
                "best_seasons": ["winter", "spring"]
            }
        ]