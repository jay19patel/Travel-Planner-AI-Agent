def get_weather_forecast(destination):
    """Mock weather API to get forecast for a destination."""
    # In a real application, this would call an actual weather API
    # For this demo, return mock data
    
    weather_data = {
        "Paris": {
            "forecast": [
                {"day": 1, "condition": "Partly Cloudy", "temp_high": 22, "temp_low": 15},
                {"day": 2, "condition": "Sunny", "temp_high": 24, "temp_low": 16},
                {"day": 3, "condition": "Sunny", "temp_high": 23, "temp_low": 15},
                {"day": 4, "condition": "Light Rain", "temp_high": 20, "temp_low": 14},
                {"day": 5, "condition": "Partly Cloudy", "temp_high": 21, "temp_low": 14},
                {"day": 6, "condition": "Sunny", "temp_high": 23, "temp_low": 15},
                {"day": 7, "condition": "Sunny", "temp_high": 24, "temp_low": 16}
            ]
        },
        "Bali": {
            "forecast": [
                {"day": 1, "condition": "Sunny", "temp_high": 31, "temp_low": 24},
                {"day": 2, "condition": "Sunny", "temp_high": 32, "temp_low": 25},
                {"day": 3, "condition": "Partly Cloudy", "temp_high": 30, "temp_low": 24},
                {"day": 4, "condition": "Light Rain", "temp_high": 29, "temp_low": 24},
                {"day": 5, "condition": "Thunderstorm", "temp_high": 28, "temp_low": 23},
                {"day": 6, "condition": "Partly Cloudy", "temp_high": 30, "temp_low": 24},
                {"day": 7, "condition": "Sunny", "temp_high": 31, "temp_low": 25}
            ]
        },
        "Tokyo": {
            "forecast": [
                {"day": 1, "condition": "Sunny", "temp_high": 28, "temp_low": 20},
                {"day": 2, "condition": "Sunny", "temp_high": 29, "temp_low": 21},
                {"day": 3, "condition": "Partly Cloudy", "temp_high": 27, "temp_low": 20},
                {"day": 4, "condition": "Light Rain", "temp_high": 25, "temp_low": 19},
                {"day": 5, "condition": "Rain", "temp_high": 24, "temp_low": 19},
                {"day": 6, "condition": "Partly Cloudy", "temp_high": 26, "temp_low": 20},
                {"day": 7, "condition": "Sunny", "temp_high": 28, "temp_low": 21}
            ]
        }
    }
    
    # Return weather for the destination, or a generic forecast if not found
    return weather_data.get(destination, {
        "forecast": [
            {"day": i, "condition": "Sunny", "temp_high": 25, "temp_low": 18} 
            for i in range(1, 8)
        ]
    })