class SchedulerOptimizer:

    def optimize(self, operations):

        return sorted(

            operations,

            key=lambda op: len(
                op["source"]
            )
        )