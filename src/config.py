import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).parent.parent
PATH_TO_ENV = BASE_DIR / '.env'

load_dotenv(dotenv_path=PATH_TO_ENV)

PATH_TO_RESOURCES=BASE_DIR / 'src'/'resources'

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
TG_BOT_API_KEY = os.environ.get("TG_BOT_API_KEY")