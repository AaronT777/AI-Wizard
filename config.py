import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# API Keys
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Model Configuration
DEFAULT_MODEL_SIZE = os.getenv("DEFAULT_MODEL_SIZE", "base")
DEFAULT_SAVE_DIR = os.getenv("DEFAULT_SAVE_DIR", str(DATA_DIR / "saved_meetings"))
DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "meta-llama/Meta-Llama-3-8B-Instruct-Lite")

# User Interface
APP_TITLE = os.getenv("APP_TITLE", "AI-Wizard: Meeting Recorder and Summarizer")
APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "Record, transcribe, and summarize meetings with AI")

# Warn if no API key is found
if not TOGETHER_API_KEY:
    print("⚠️  Warning: TOGETHER_API_KEY not found in environment variables.")
    print("   Summarization will use a placeholder implementation.")
    print("   Please copy .env.example to .env and add your API key.")