from core.transaction_engine.transaction import (
    RenameTransaction
)

from core.transaction_engine.atomic_executor import (
    execute_transaction
)

from core.transaction_engine.integrity_validator import (
    validate_transaction_integrity
)


class TransactionManager:

    def create_transaction(self):

        return RenameTransaction()

    def commit(self, transaction):

        valid = validate_transaction_integrity(
            transaction
        )

        if not valid:

            print(
                "Transaction integrity failed."
            )

            return False

        return execute_transaction(
            transaction
        )