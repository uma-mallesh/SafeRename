class CycleExecutionPlan:

    def __init__(self):

        self.operations = []

    def add_operation(

        self,

        source,

        target
    ):

        self.operations.append({

            "source": source,

            "target": target
        })