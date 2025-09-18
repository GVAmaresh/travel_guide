import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    GCP_PROJECT_ID: str = os.environ.get("GCP_PROJECT_ID")
    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY")
    ALGORITHM: str = os.environ.get("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    VECTOR_SEARCH_INDEX_ENDPOINT_ID: str = os.environ.get("VECTOR_SEARCH_INDEX_ENDPOINT_ID")
    DEPLOYED_INDEX_ID: str = os.environ.get("DEPLOYED_INDEX_ID")
    

settings = Settings()