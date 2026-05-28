from pathlib import Path


def validate_transaction_integrity(transaction):

    seen_targets = set()

    for operation in transaction.operations:

        target = operation["target"]

        if target in seen_targets:

            return False

        seen_targets.add(target)

        if not Path(
            operation["original"]
        ).exists():

            return False

    return True