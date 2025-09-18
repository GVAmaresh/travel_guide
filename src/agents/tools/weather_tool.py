
import logging
import random 

def get_current_weather(location: str):
    logging.info(f"TOOL CALLED: get_current_weather(location='{location}')")
    if "goa" in location.lower():
        temp = random.randint(27, 32)
        conditions = random.choice(["sunny", "partly cloudy", "humid with a slight breeze"])
        return f"The weather in Goa, India is {temp}°C and {conditions}."
    else:
        temp = random.randint(15, 25)
        conditions = random.choice(["cool", "windy", "rainy"])
        return f"The weather in {location} is {temp}°C and {conditions}."

weather_tool = get_current_weather