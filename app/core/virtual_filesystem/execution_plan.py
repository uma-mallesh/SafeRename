class ExecutionPlan:

    def __init__(self):

        self.operations = []

    def add_operation(

        self,

        original,

        simulated
    ):

        self.operations.append({

            "original": original,

            "simulated": simulated
        })

    def total_operations(self):

        return len(self.operations)