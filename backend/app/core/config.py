import os
from pathlib import Path

from dotenv import load_dotenv

# Project root directory
ROOT_DIR = Path(__file__).resolve().parents[3]

# Load environment variables
load_dotenv(ROOT_DIR / ".env", override=True)


class Settings:
    APP_NAME: str = "AstroHealth API"
    APP_VERSION: str = "1.0.0"

    DATABASE_URL: str | None = os.getenv("DATABASE_URL")

    SUPABASE_URL: str | None = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY: str | None = os.getenv("SUPABASE_ANON_KEY")

    GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")

settings = Settings()