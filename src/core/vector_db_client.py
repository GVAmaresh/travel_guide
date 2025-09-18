# import os
# import logging
# from typing import List, Optional
# from src.core.config import settings
# import firebase_admin
# from firebase_admin import firestore
# from google.cloud import aiplatform
# from vertexai.language_models import TextEmbeddingModel

# class VectorDBClient:

#     def __init__(self):
#         project_id = os.environ.get("GCP_PROJECT_ID", "")
#         location = "us-central1"
        
#         self.index_endpoint_id = settings.VECTOR_SEARCH_INDEX_ENDPOINT_ID
#         self.deployed_index_id = settings.DEPLOYED_INDEX_ID
#         # ---

#         if "YOUR_INDEX_ENDPOINT_ID" in self.index_endpoint_id:
#             raise ValueError("You must set YOUR_INDEX_ENDPOINT_ID in VectorDBClient")

#         aiplatform.init(project=project_id, location=location)
#         self.index_endpoint = aiplatform.MatchingEngineIndexEndpoint(
#             index_endpoint_name=self.index_endpoint_id
#         )
#         self.embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
        
#         if not firebase_admin._apps:
#             from firebase_admin import credentials
#             cred = credentials.ApplicationDefault()
#             firebase_admin.initialize_app(cred, {'projectId': project_id})
#         self.db = firestore.client()

#         logging.info("VectorDBClient initialized successfully.")

#     def get_embedding(self, text: str) -> Optional[List[float]]:
#         try:
#             embeddings = self.embedding_model.get_embeddings([text])
#             return embeddings[0].values
#         except Exception as e:
#             logging.error(f"Failed to generate embedding: {e}")
#             return None

#     def upsert_data(self, doc_id: str, text_to_embed: str):
#         embedding = self.get_embedding(text_to_embed)
#         if not embedding:
#             logging.error(f"Skipping upsert for doc_id {doc_id} due to embedding failure.")
#             return

#         datapoint = aiplatform.MatchingEngineIndex.Datapoint(
#             datapoint_id=doc_id, 
#             feature_vector=embedding,
#         )
        
#         try:
#             self.index_endpoint.upsert_datapoints(datapoints=[datapoint])
#             logging.info(f"Successfully upserted datapoint for doc_id: {doc_id}")
#         except Exception as e:
#             logging.error(f"Failed to upsert datapoint for doc_id {doc_id}: {e}")


#     def query(self, user_input: str, user_id: str, num_neighbors: int = 3) -> str:
#         query_embedding = self.get_embedding(user_input)
#         if not query_embedding:
#             return "Could not process query for memory retrieval."

#         try:
#             response = self.index_endpoint.find_neighbors(
#                 queries=[query_embedding],
#                 deployed_index_id=self.deployed_index_id,
#                 num_neighbors=num_neighbors,
#             )
            
#             if not response or not response[0]:
#                 return "No relevant memories found in Vector Search."

#             match_ids = {match.id for match in response[0]} 
#             logging.info(f"Found matching memory IDs from Vector Search: {match_ids}")
#             convo_ref = self.db.collection('conversations').document(user_id)
#             conversation = convo_ref.get()

#             if not conversation.exists:
#                 return "No conversation history found in Firestore."

#             all_turns = conversation.to_dict().get("turns", [])
#             relevant_turns = [
#                 turn for turn in all_turns if turn.get("turn_id") in match_ids
#             ]

#             if not relevant_turns:
#                  return "Could not match vector IDs to conversation turns."
#             retrieved_texts = [
#                 f"User said: '{turn['user']}' -> Agent said: '{turn['agent']}'" 
#                 for turn in relevant_turns
#             ]
#             return "\n".join(retrieved_texts)

#         except Exception as e:
#             logging.error(f"Failed during vector query or Firestore fetch: {e}")
#             return "Error retrieving memories."

#         except Exception as e:
#             logging.error(f"Failed during vector query or Firestore fetch: {e}")
#             return "Error retrieving memories."