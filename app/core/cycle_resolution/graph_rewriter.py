from core.cycle_resolution.temp_node_generator import (
    TempNodeGenerator
)

from core.cycle_resolution.cycle_execution_plan import (
    CycleExecutionPlan
)


class GraphRewriter:

    def __init__(self):

        self.temp_generator = (
            TempNodeGenerator()
        )

    def rewrite(

        self,

        execution_order
    ):

        plan = CycleExecutionPlan()

        handled = set()

        for node in execution_order:

            if node.source in handled:
                continue

            temp_path = (

                self.temp_generator.generate(
                    node.source
                )
            )

            # -------------------------------------
            # SOURCE → TEMP
            # -------------------------------------

            plan.add_operation(

                source=node.source,

                target=temp_path
            )

            # -------------------------------------
            # TEMP → TARGET
            # -------------------------------------

            plan.add_operation(

                source=temp_path,

                target=node.target
            )

            handled.add(node.source)

        return plan