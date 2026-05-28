from pathlib import Path


def rollback_transaction(transaction):

    for operation in reversed(
        transaction.operations
    ):

        if operation["completed"]:

            target = Path(
                operation["target"]
            )

            original = Path(
                operation["original"]
            )

            if target.exists():

                target.rename(original)

    transaction.state = "ROLLED_BACK"