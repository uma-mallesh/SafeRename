from core.dependency_graph.graph_builder import (
    GraphBuilder
)

from core.dependency_graph.cycle_detector import (
    CycleDetector
)

from core.dependency_graph.topology_sorter import (
    TopologySorter
)


class ExecutionScheduler:

    def __init__(self):

        self.builder = GraphBuilder()

        self.detector = CycleDetector()

        self.sorter = TopologySorter()

    def build_execution_plan(

        self,

        transaction
    ):

        graph = self.builder.build(
            transaction
        )

        has_cycle = self.detector.detect(
            graph
        )

        execution_order = list(

            self.sorter.sort(graph)
        )

        return {

            "graph": graph,

            "has_cycle": has_cycle,

            "execution_order": execution_order
        }