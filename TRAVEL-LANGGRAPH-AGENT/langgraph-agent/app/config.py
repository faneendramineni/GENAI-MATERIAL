import os

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
    DUFFEL_ACCESS_TOKEN = os.getenv("DUFFEL_ACCESS_TOKEN")

settings = Settings()