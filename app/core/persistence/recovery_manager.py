from core.persistence.operation_journal import (
    load_journal
)


def detect_interrupted_operations():

    journal = load_journal()

    interrupted = []

    for entry in journal:

        if entry.get("completed") is False:

            interrupted.append(entry)

    return interrupted