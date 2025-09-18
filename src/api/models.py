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