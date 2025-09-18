
import logging
from datetime import date

def find_flights(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: str,
    num_passengers: int
):
    logging.info(f"TOOL CALLED: find_flights(origin='{origin}', destination='{destination}', ...)")
    return (
        f"Found a round-trip flight for {num_passengers} passengers from {origin} to {destination}, "
        f"departing {departure_date} and returning {return_date}. "
        f"SpiceJet flight SG-456, total price ₹12,500."
    )

flight_tool = find_flights