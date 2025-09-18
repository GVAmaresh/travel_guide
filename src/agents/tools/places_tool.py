
import logging

def find_points_of_interest(location: str, place_type: str):
    logging.info(f"TOOL CALLED: find_points_of_interest(location='{location}', place_type='{place_type}')")
    all_places = {
        "goa": {
            "temple": "Mangeshi Temple, Shanta Durga Temple, Mahadev Temple",
            "beach": "Baga Beach, Calangute Beach, Anjuna Beach, Palolem Beach",
            "fort": "Aguada Fort, Chapora Fort",
            "restaurant": "Britto's, Fisherman's Wharf, Martin's Corner"
        }
    }

    city_key = location.split(",")[0].lower()
    if city_key in all_places and place_type in all_places[city_key]:
        return all_places[city_key][place_type]
    else:
        return f"Sorry, I couldn't find any popular places of type '{place_type}' in {location}."

places_tool = find_points_of_interest