from uuid import uuid4

from core.transaction_engine.transaction_state_machine import (
    TransactionState
)


class RenameTransaction:

    def __init__(self):

        self.transaction_id = str(uuid4())

        self.operations = []

        self.state = TransactionState.PENDING

    def add_operation(

        self,

        original_path,

        target_path
    ):

        self.operations.append({

            "original": original_path,

            "target": target_path,

            "completed": False
        })