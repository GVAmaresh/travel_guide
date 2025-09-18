# import os
# import logging
# import json
# import datetime
# import firebase_admin
# from firebase_admin import credentials, firestore
# from vertexai.generative_models import GenerativeModel

# import uuid

# from src.core import setup_logging, GeminiClient
# from src.interaction_formats.prompts import PromptManager

# from .tools import all_tools
# from src.core.vector_db_client import VectorDBClient 

# class TripPlannerAgent:
#     def __init__(self, user_id: str):
#         setup_logging()
#         self.prompt_manager = PromptManager()
#         self.user_id = user_id
        
#         project_id = os.environ.get("GCP_PROJECT_ID", "")
#         location = "us-central1"
#         model_name = "gemini-2.0-flash-001"
        
#         self.client = GeminiClient(
#             project_id=project_id, location=location, model_name=model_name
#         )
        
#         if not firebase_admin._apps:
#             cred = credentials.ApplicationDefault()
#             firebase_admin.initialize_app(cred, {'projectId': project_id})
#         self.db = firestore.client()
#         self.vector_client = VectorDBClient() 
        
#         self.user_profile = self._load_user_profile() 

#         system_instructions = self.prompt_manager.get_prompt("MAIN_SYSTEM")
#         self.utility_model = GenerativeModel(model_name)
        
#         logging.info("Initializing Vertex AI Agent with base system prompt and all tools...")
#         self.model = GenerativeModel(
#             model_name,
#             tools=all_tools,
#             system_instruction=system_instructions 
#         )
        
#         self.reset()
#         logging.info(f"TripPlannerAgent successfully initialized for user_id: {self.user_id}")

#     def reset(self):
#         """Resets the short-term conversation state for a new trip plan."""
#         logging.info("Resetting agent's short-term state for a new conversation.")
#         self.state = "GATHERING_DESTINATION"
#         self.plan_details = {}

#     def update_user_profile(self, new_data: dict):
#             if not isinstance(new_data, dict):
#                 logging.error("Failed to update profile: new_data is not a dictionary.")
#                 return
#             logging.info(f"Updating profile for user {self.user_id} with data: {new_data}")
#             user_ref = self.db.collection('users').document(self.user_id)
#             user_ref.set(new_data, merge=True) # merge=True is critical!
#             self.user_profile = self._load_user_profile()
#             logging.info(f"User profile refreshed: {self.user_profile}")

#     def _extract_and_save_preferences(self, user_input: str):
#         prompt = f"""
#         Analyze the following text from a user. Extract any personal preferences, facts, or constraints they mention about themselves for travel planning.
#         Return the information as a valid JSON object with keys like 'diet', 'home_airport', 'travel_style', 'interests', etc.
#         If no preferences are mentioned, return an empty JSON object {{}}.
#         User text: "{user_input}"
#         JSON:
#         """
#         try:
#             response = self.utility_model.generate_content(prompt)
#             extracted_json_str = response.text.strip().replace("```json", "").replace("```", "")
#             if extracted_json_str and extracted_json_str != "{}":
#                 preferences = json.loads(extracted_json_str)
#                 logging.info(f"Extracted preferences: {preferences}")
#                 self.update_user_profile(preferences)
#         except Exception as e:
#             logging.error(f"Could not extract or save preferences: {e}")
#     def _load_user_profile(self) -> dict:
#         logging.info(f"Loading profile for user {self.user_id}")
#         doc_ref = self.db.collection('users').document(self.user_id)
#         doc = doc_ref.get()
#         if doc.exists:
#             return doc.to_dict()
#         return {"notes": "New user, no preferences recorded yet."}

#     def _save_turn(self, user_input: str, agent_response: str):
#             logging.info(f"Saving turn for user {self.user_id}")
            
#             turn_id = str(uuid.uuid4())
            
#             utc_now = datetime.datetime.now(datetime.timezone.utc)
#             turn_data = {
#                 'turn_id': turn_id,  
#                 'user': user_input,
#                 'agent': agent_response,
#                 'timestamp': utc_now
#             }
            
#             convo_ref = self.db.collection('conversations').document(self.user_id)
#             convo_ref.set({
#                 'turns': firestore.ArrayUnion([turn_data])
#             }, merge=True)

#             text_to_embed = f"User said: '{user_input}' -> Agent responded: '{agent_response}'"
            
#             try:
#                 self.vector_client.upsert_data(
#                     doc_id=turn_id, 
#                     text_to_embed=text_to_embed
#                 )
#                 logging.info(f"Successfully queued upsert for turn_id: {turn_id}")
#             except Exception as e:
#                 logging.error(f"Failed to upsert embedding for turn_id {turn_id}: {e}")

#     def _find_relevant_memories(self, user_input: str) -> str:
#         """Finds relevant long-term memories from the vector DB."""
#         logging.info(f"Querying vector DB for relevant memories for user {self.user_id}")
#         try:
#             context = self.vector_client.query(user_input, user_id=self.user_id)
#             return context if context else "No specific long-term memories found."
#         except Exception as e:
#             logging.error(f"Failed to query vector DB: {e}")
#             return "Could not retrieve long-term memories."

#     def _determine_prompt_key(self, user_input: str) -> str:
#         if any(keyword in user_input.lower() for keyword in ["change", "instead", "actually"]):
#             return "CHANGE_OF_PLANS"
#         if any(keyword in user_input.lower() for keyword in ["towel", "pack", "plug", "visa"]):
#             return "ANCILLARY_DETAILS"
#         if self.state == "AWAITING_CONFIRMATION":
#             return "PLAN_CONFIRMATION"
#         if self.state == "FINALIZING":
#             return "FINAL_CHECKLIST"
#         return "MAIN_SYSTEM"


#     def run(self, user_input: str) -> str:

#             logging.info(f"Current state: '{self.state}'. User input: '{user_input}'")
#             self._extract_and_save_preferences(user_input)
            
#             memories = self._find_relevant_memories(user_input)
#             profile_summary = "\n".join([f"- {k}: {v}" for k, v in self.user_profile.items()])
#             prompt_key = self._determine_prompt_key(user_input)
#             special_instruction = self.prompt_manager.get_prompt(prompt_key)
            
#             augmented_input = f"""
#             ## CONTEXT FOR THIS USER ##
#             [User Profile and Preferences]
#             {profile_summary}
            
#             [Relevant Memories From Past Conversations]
#             {memories}
#             ---
#             ## SPECIAL INSTRUCTIONS FOR THIS TURN ##
#             {special_instruction}
#             ---
#             ## USER'S CURRENT MESSAGE TO PROCESS ##
#             {user_input}
#             """
            
#             response = self.model.generate_content(augmented_input)
#             response_text = response.text
#             logging.info(f"Raw agent JSON response: '{response_text}'")

#             try:
#                 cleaned_json_str = response_text.strip().lstrip("```json").rstrip("```").strip()
#                 response_json = json.loads(cleaned_json_str)
#                 if self.state == "GATHERING_DESTINATION" and "question_text" in response_json:
#                     self.plan_details['destination'] = user_input
#                     self.state = "GATHERING_DATES"
#                 elif self.state == "GATHERING_DATES" and "question_text" in response_json:
#                     self.plan_details['dates'] = user_input
#                     self.state = "GATHERING_STYLE"
                
#                 self._save_turn(user_input, response_text)
#                 return response_json

#             except json.JSONDecodeError:
#                 logging.error("Agent returned malformed JSON even after cleaning. Turn not saved.")
#                 return {"error": "The agent returned a response that could not be parsed."}
#             except Exception as e:
#                 logging.error(f"An unexpected error occurred: {e}")
#                 return {"error": "An internal error occurred."}