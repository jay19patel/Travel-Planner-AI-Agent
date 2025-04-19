# Travel Planner AI Agent

## Overview
This project implements an AI-powered Travel Planner using LangGraph to create a conversational agent that helps users plan trips by understanding preferences, suggesting destinations, creating itineraries, and answering follow-up questions.

## Features
- Extracts travel preferences (budget, duration, interests, etc.)
- Recommends destinations based on user preferences
- Creates detailed day-by-day itineraries
- Handles follow-up questions about generated plans
- Integrates with external tools (destination database and weather API)

## Project Structure
```
travel_planner/
├── main.py                 # Entry point for the application
├── agent/
│   ├── graph.py            # LangGraph implementation
│   ├── nodes/              # Node implementations
│   │   ├── __init__.py
│   │   ├── preference_extractor.py
│   │   ├── destination_finder.py
│   │   ├── itinerary_creator.py
│   │   └── followup_handler.py
│   ├── tools/              # External tool connections
│   │   ├── __init__.py
│   │   ├── destination_db.py
│   │   └── weather_api.py
│   └── state.py            # State management
├── data/
│   └── destinations.json   # Mock destination database
├── tests/
│   └── test_agent.py       # Test cases
└── README.md               # Documentation
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/travel-planner-ai.git
cd travel-planner-ai
```

2. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the travel planner:
```bash
python main.py
```

## Development Guide

### Adding New Destinations
To add new destinations to the system, modify the `data/destinations.json` file, following the existing structure:

```json
{
  "name": "Destination Name",
  "country": "Country",
  "tags": ["tag1", "tag2", "tag3"],
  "budget_level": "low|medium|high",
  "ideal_duration": [min_days, max_days],
  "best_seasons": ["winter", "spring", "summer", "fall"]
}
```

### Extending Node Functionality
To modify the behavior of a specific node:

1. Locate the corresponding file in `agent/nodes/`
2. Update the logic while ensuring the function signature remains compatible
3. Test your changes using the test cases

### Adding New Tools
To add new external tools:

1. Create a new file in `agent/tools/`
2. Implement the tool's functionality
3. Update `graph.py` to incorporate the new tool
4. Update relevant nodes to utilize the new tool

## Testing

Run tests with:
```bash
pytest tests/
```

## Requirements
- Python 3.9+
- LangGraph
- LangChain
- OpenAI API key (set as environment variable `OPENAI_API_KEY`)