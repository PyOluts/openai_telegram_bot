import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent
Path_To_ENV = BASE_DIR / '.env'

load_dotenv(Path_To_ENV)

Path_To

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
TG_BOT_API_KEY = os.environ.get("TG_BOT_API_KEY")