import json

from pathlib import Path


SNAPSHOT_FILE = Path(
    "data/state_snapshot.json"
)


def save_snapshot(state):

    SNAPSHOT_FILE.parent.mkdir(
        exist_ok=True
    )

    with open(SNAPSHOT_FILE, "w") as file:

        json.dump(
            state,
            file,
            indent=4
        )


def load_snapshot():

    if not SNAPSHOT_FILE.exists():

        return {}

    with open(SNAPSHOT_FILE, "r") as file:

        return json.load(file)