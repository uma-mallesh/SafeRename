from pathlib import Path

from core.transaction_engine.rollback_executor import (
    rollback_transaction
)

from core.transaction_engine.transaction_state_machine import (
    TransactionState
)


def execute_transaction(transaction):

    transaction.state = (
        TransactionState.EXECUTING
    )

    try:

        for operation in transaction.operations:

            original = Path(
                operation["original"]
            )

            target = Path(
                operation["target"]
            )

            original.rename(target)

            operation["completed"] = True

        transaction.state = (
            TransactionState.COMMITTED
        )

        return True

    except Exception as error:

        rollback_transaction(
            transaction
        )

        transaction.state = (
            TransactionState.FAILED
        )

        print(error)

        return False