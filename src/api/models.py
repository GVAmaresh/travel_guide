from pydantic import BaseModel, Field
from typing import List, Union, Optional


class FixedDates(BaseModel):
    start_date: str
    end_date: str

class FlexibleDates(BaseModel):
    month: str
    days: str

class PlanTripRequest(BaseModel):
    origin: str
    destination: str
    is_flexible: bool
    dates: Union[FixedDates, FlexibleDates]
    include_flights: bool = True

class Preferences(BaseModel):
    budget: str
    theme: List[str]
    food_preferences: List[str]
    traveling_with: str

class GenerateSummaryRequest(BaseModel):
    session_id: str
    preferences: Preferences
    additional_details: str

class UpdateSummaryRequest(BaseModel):
    session_id: str
    action: str  
    edited_summary_text: Optional[str] = None
    
class Price(BaseModel):
    currency: str
    amount: int

class FlightDetails(BaseModel):
    airport: str
    time: str

class FlightLeg(BaseModel):
    flight_id: str
    airline: str
    agent_id: str
    price: Price
    departure: FlightDetails
    arrival: FlightDetails
    duration: str
    stops: int
    layover_airport: str

class FlightCategory(BaseModel):
    best: List[FlightLeg]
    budget: List[FlightLeg]
    
class FlightOptions(BaseModel):
    onward_flights: FlightCategory
    return_flights: FlightCategory

class ConfirmFlightsRequest(BaseModel):
    session_id: str
    onward_flight: str 
    return_flight: str  
    
class ChatRequest(BaseModel):
    message: str

class Token(BaseModel):
    access_token: str
    token_type: str
class UserCreate(BaseModel):
    username: str
    password: str
    
class GetFlightsRequest(BaseModel):
    session_id: str