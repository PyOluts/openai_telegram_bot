from pathlib import Path

PATH_TO_RESOURCES = Path(__file__).parent / "resources"

def load_messages_for_bot(filename: str) -> str:
    """
    Load a text message from resources folder.
    """
    file_path = PATH_TO_RESOURCES / f"{filename}.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

def read_text(path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()