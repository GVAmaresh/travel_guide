from src.core.vertex_ai_client import GeminiClient 
import os
import json
import datetime
from src.core.config import settings
gemini_client = GeminiClient(
    project_id= os.environ.get("GCP_PROJECT_ID"),
    location="us-central1",
    model_name="gemini-2.0-flash-001"
)

def run_flexible_date_agent(destination: str, month: str, days: str) -> dict:
    current_year = datetime.date.today().year
    prompt = f"""
    A user wants to travel to {destination} for {days} days in {month} of {current_year}.
    Analyze weather patterns and local events for that month.
    Suggest the best continuous {days}-day period for the trip.
    
    Your response MUST be a valid JSON object with this exact structure:
    {{
      "start_date": "YYYY-MM-DD",
      "end_date": "YYYY-MM-DD",
      "reasoning": "A brief explanation for your date suggestion."
    }}
    """
    response_str = gemini_client.generate_content(prompt)
    return json.loads(response_str)

def run_flight_search_agent(origin: str, destination: str, start_date: str, end_date: str) -> dict:
    prompt = f"""
    Generate realistic, mock flight options from {origin} to {destination}.
    The onward journey departs on {start_date}.
    The return journey departs on {end_date}.
    Prices should be in Indian Rupees (INR).

    CRITICAL: The root of your JSON response MUST be an object with two keys: "onward_flights" and "return_flights".

    Inside each of those keys, create two lists: "best" and "budget".
    - "best" flights should have a good balance of price and convenience.
    - "budget" flights should be cheaper but may have longer layovers.

    Generate 2-3 flight options for EACH category (best/budget) in BOTH the onward and return sections.
    Make the data look real with plausible airlines, layovers, and durations.

    Follow this JSON structure EXACTLY:
    {{
      "onward_flights": {{
        "best": [{{ "flight_id": "...", "airline": "...", "price": {{...}}, "departure": {{...}}, "arrival": {{...}}, "duration": "...", "stops": ..., "layover_airport": "..." }}],
        "budget": [{{ "flight_id": "...", ... }}]
      }},
      "return_flights": {{
        "best": [{{ "flight_id": "...", ... }}],
        "budget": [{{ "flight_id": "...", ... }}]
      }}
    }}
    """
    response_str = gemini_client.generate_content(prompt)
    return json.loads(response_str)

def run_root_agent(destination: str) -> dict:
    prompt = f"""
    Analyze the destination '{destination}' for a traveler. Provide the following in a valid JSON format:
    1. A brief, enticing summary of the weather in October.
    2. One recent, interesting local news or event tidbit.
    3. A set of three relevant follow-up questions (budget, theme, food) with choices.
    
    JSON structure:
    {{
      "weather": {{"condition": "...", "temperature_range": "...", "period": "..."}},
      "local_news": "...",
      "next_questions": {{"prompt": "...", "options": [{{"id": "...", "label": "...", "choices": [...]}}]}}
    }}
    """
    response_str = gemini_client.generate_content(prompt)
    return json.loads(response_str)

def run_summary_agent(session_data: dict, preferences: dict, details: str) -> str:
    prompt = f"""
    Based on the following travel data, create a concise, first-person summary:
    - Initial Plan: {session_data}
    - User Preferences: {preferences}
    - Additional Details: {details}
    
    Generate only the summary text.
    """
    summary = gemini_client.generate_content(prompt)
    return summary.strip()

def generate_final_prompt(summary_text: str) -> str:
    prompt = f"""
    Generate a detailed, day-by-day travel itinerary based on this summary:
    "{summary_text}"
    
    The itinerary should be creative and practical.
    """
    return prompt