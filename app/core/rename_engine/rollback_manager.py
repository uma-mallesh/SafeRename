import json
from pathlib import Path


ROLLBACK_FILE = "logs/rollback.json"


def save_rollback(rename_operations):

    Path("logs").mkdir(exist_ok=True)

    with open(ROLLBACK_FILE, "w", encoding="utf-8") as file:

        json.dump(
            rename_operations,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_rollback():

    rollback_path = Path(ROLLBACK_FILE)

    if not rollback_path.exists():
        return []

    with open(ROLLBACK_FILE, "r", encoding="utf-8") as file:

        return json.load(file)