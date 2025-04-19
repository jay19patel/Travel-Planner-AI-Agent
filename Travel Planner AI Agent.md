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
## Output 
```cmd
Travel Agent: Here's your 5-day itinerary for Kasol, India:

## 5-Day Solo Trekking & Nature Itinerary for Kasol, India (Low Budget)

This itinerary focuses on nature and trekking experiences in Kasol, keeping your low budget preference in mind.  The estimated budget is within ₹8,000-15,000 as per your requirement.

**Accommodation:** Hostels and budget guesthouses are recommended for solo travelers on a low budget. Expect to pay around ₹500-₹1000 per night. Zostel, The Hosteller Kasol, and numerous local guesthouses are good options.

**Transportation:** Local buses are the most economical option for intercity travel. Within Kasol, walking is preferred, but taxis are available for longer distances. Allocate approximately ₹500-₹1000 for transportation throughout the trip.


**Day 1: Arrival in Kasol & Exploring the Village (Partly Cloudy)**

* **Morning:** Arrive at Bhuntar Airport (KUU) or take a bus from Delhi/Manali. Take a local bus to Kasol (₹100-₹200). Check in to your chosen accommodation.  
* **Afternoon:** Explore Kasol's vibrant cafes and shops. Visit the local market for souvenirs and try Israeli cuisine. (Meal: ₹300-₹500)
* **Evening:** Relax by the Parvati River and enjoy the scenic beauty. (Optional: bonfire at your accommodation if available).


**Day 2: Kheerganga Trek - Day 1 (Sunny)**

* **Morning:** Start your trek to Kheerganga (12-14 km). Pack light essentials, including water and snacks.  (Trekking Permits if applicable: ₹100-₹200, Guide (optional): ₹500-₹800). The trail passes through picturesque villages and forests. (Packed Lunch: ₹200-₹300).
* **Afternoon:** Continue trekking and enjoy the breathtaking views. Reach Rudranag waterfall and take a refreshing dip.
* **Evening:** Arrive at Kheerganga, settle into a campsite (₹200-₹500) and enjoy the hot springs.  (Dinner at Kheerganga: ₹200-₹300)


**Day 3: Kheerganga Trek - Return (Sunny)**

* **Morning:** Wake up early and witness the sunrise over the Himalayas from Kheerganga. Enjoy the hot springs one last time.
* **Afternoon:** Begin your descent back to Kasol.  (Lunch on the way: ₹200-₹300)
* **Evening:** Arrive back in Kasol, relax and reflect on the trek.  (Dinner: ₹300-₹500)


**Day 4: Tosh Village Trek (Light Rain)**

* **Morning:** Take a bus or taxi to Barshaini, the starting point for the Tosh trek (₹100-₹200). Begin your trek to Tosh village (3 km). This is a relatively easy trek.
* **Afternoon:** Explore Tosh village, known for its cafes and laid-back atmosphere.  (Lunch: ₹300-₹500) Consider visiting the nearby waterfall.
* **Evening:** Return to Kasol, enjoy dinner, and prepare for your departure.  (Dinner: ₹300-₹500)


**Day 5: Departure (Partly Cloudy)**

* **Morning:** Enjoy a final breakfast in Kasol. (Breakfast: ₹200-₹300). Buy any last-minute souvenirs.
* **Afternoon:** Take a bus or taxi back to Bhuntar Airport (KUU) or continue your journey onwards. (Transport: ₹100-₹200)

**Total Estimated Cost:** ₹8,000 - ₹15,000 (including accommodation, food, transportation, and activities). This is an estimated cost and can vary based on your choices and spending habits.

**Important Notes:**

* Pack warm clothes as the weather in the mountains can be unpredictable.
* Carry a good pair of trekking shoes and a raincoat.
* Stay hydrated and carry snacks for the treks.
* Be mindful of the local culture and customs.
* Pre-book accommodation during peak season.
* Carry cash, as ATMs might be limited in some areas.


This itinerary is a suggestion and can be adjusted to fit your personal preferences. You can choose to spend more or less time in certain places, depending on your interests. Enjoy your trip to Kasol!  

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



## Requirements
- Python 3.9+
- LangGraph
- LangChain
- OpenAI API key (set as environment variable `OPENAI_API_KEY`)