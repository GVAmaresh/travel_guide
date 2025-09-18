# import json
# from pathlib import Path
# from typing import Dict

# class PromptManager:
#     def __init__(self):
#         self.prompts_dir = Path(__file__).parent.parent / "interaction_formats" / "prompts"
#         self.manifest: Dict = self._load_manifest()

#     def _load_manifest(self) -> Dict:
#         manifest_path = self.prompts_dir / "prompt_manifest.json"
#         try:
#             with open(manifest_path, "r", encoding="utf-8") as f:
#                 return json.load(f)
#         except FileNotFoundError:
#             raise FileNotFoundError(f"Prompt manifest not found at {manifest_path}")
#         except json.JSONDecodeError:
#             raise ValueError(f"Error decoding JSON from {manifest_path}")

#     def get_prompt(self, situation: str) -> str:
#         prompt_info = self.manifest["prompts"].get(situation)
        
#         if not prompt_info:
#             raise ValueError(f"Unknown situation '{situation}' in prompt manifest.")
            
#         prompt_file_path = self.prompts_dir / prompt_info["file"]
        
#         try:
#             with open(prompt_file_path, "r", encoding="utf-8") as f:
#                 return f.read()
#         except FileNotFoundError:
#             raise FileNotFoundError(f"Prompt file '{prompt_info['file']}' not found for situation '{situation}'.")