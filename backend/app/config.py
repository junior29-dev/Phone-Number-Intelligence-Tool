import os
from dotenv import load_dotenv

load_dotenv()

OPENCAGE_KEY = os.getenv("OPENCAGE_KEY", "")
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",") if o.strip()]
