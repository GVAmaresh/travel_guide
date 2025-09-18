import os
import logging
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig, SafetySetting

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self, project_id: str, location: str, model_name: str):

        if not project_id:
            raise ValueError("Google Cloud project_id must be provided.")
            
        logger.info(f"Initializing Vertex AI for project '{project_id}' in '{location}'")
        vertexai.init(project=project_id, location=location)

        logger.info(f"Loading Gemini model: {model_name}")
        self.model = GenerativeModel(model_name)
        self.generation_config = GenerationConfig(
            temperature=0.7,
            top_p=0.9,
            max_output_tokens=2048,
            response_mime_type="application/json" 
        )

        self.safety_settings = {
            category: SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
            for category in SafetySetting.HarmCategory
        }

    def generate_content(self, prompt: str) -> str:
        try:
            logger.debug(f"Sending prompt to Gemini: {prompt[:200]}...")
            response = self.model.generate_content(
                [prompt],
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            logger.debug("Successfully received response from Gemini.")
            return response.text
        except Exception as e:
            logger.error(f"An error occurred while calling the Gemini API: {e}")
            return '{"error": "Failed to get a response from the AI model."}'

