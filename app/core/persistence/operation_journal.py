import json

from pathlib import Path


JOURNAL_FILE = Path(
    "data/operation_journal.json"
)


def write_journal(entry):

    JOURNAL_FILE.parent.mkdir(
        exist_ok=True
    )

    journal = []

    if JOURNAL_FILE.exists():

        with open(JOURNAL_FILE, "r") as file:

            journal = json.load(file)

    journal.append(entry)

    with open(JOURNAL_FILE, "w") as file:

        json.dump(
            journal,
            file,
            indent=4
        )


def load_journal():

    if not JOURNAL_FILE.exists():

        return []

    with open(JOURNAL_FILE, "r") as file:

        return json.load(file)


def clear_journal():

    if JOURNAL_FILE.exists():

        JOURNAL_FILE.unlink()