import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-3.5-turbo"

    # App Settings
    APP_TITLE = "💡 Intelligent PDF Co-Pilot"
    MAX_FILE_SIZE = 200  # MB
    SUPPORTED_FILE_TYPES = ["pdf"]

    @classmethod
    def validate_config(cls):
        """Validate configuration settings."""
        errors = []
        if not cls.OPENAI_API_KEY:
            errors.append("OpenAI API Key is missing.")
        return errors


