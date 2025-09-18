from src.core.vertex_ai_client import GeminiClient 
import os
import json
from src.core.config import settings
gemini_client = GeminiClient(
    project_id= os.environ.get("GCP_PROJECT_ID"),
    location="us-central1",
    model_name="gemini-2.0-flash-001"
)

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