import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DATA_FOLDER = os.getenv("DATA_FOLDER")
OPENAPI_API_KEY = os.getenv("OPENAI_API_KEY")

if not GROQ_API_KEY or not DATA_FOLDER:
    raise EnvironmentError("GROQ_API_KEY or DATA_FOLDER is not set in the environment.")
