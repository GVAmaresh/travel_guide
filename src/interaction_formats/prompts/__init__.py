# import os
# import logging

# class PromptManager:
#     def __init__(self, prompts_dir=None):
#         if prompts_dir is None:
#             prompts_dir = os.path.dirname(os.path.abspath(__file__))

#         self.prompts = {}
#         logging.info(f"Loading prompts from: {prompts_dir}")

#         try:
#             for filename in os.listdir(prompts_dir):
#                 if filename.endswith(".txt"):
#                     key = filename.replace(".txt", "").upper()
#                     filepath = os.path.join(prompts_dir, filename)
#                     with open(filepath, "r", encoding="utf-8") as f:
#                         self.prompts[key] = f.read()
#                     logging.info(f"  - Loaded prompt with key: {key}")
#         except FileNotFoundError:
#             logging.error(f"Prompt directory not found at {prompts_dir}")
#             raise
            
#         if not self.prompts:
#             logging.warning("No prompt files (.txt) were found in the directory.")

#     def get_prompt(self, key: str) -> str:
#         key = key.upper()
#         if key not in self.prompts:
#             logging.error(f"Prompt with key '{key}' not found.")
#             raise KeyError(f"Prompt key '{key}' does not exist.")
#         return self.prompts[key]