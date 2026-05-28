from core.dependency_graph.graph_node import (
    GraphNode
)

from core.dependency_graph.dependency_graph import (
    DependencyGraph
)


class GraphBuilder:

    def build(self, transaction):

        graph = DependencyGraph()

        operations = transaction.operations

        for operation in operations:

            node = GraphNode(

                source=operation["original"],

                target=operation["target"]
            )

            graph.add_node(node)

        # -----------------------------------------
        # BUILD DEPENDENCIES
        # -----------------------------------------

        for node in graph.all_nodes():

            for other in graph.all_nodes():

                if node == other:
                    continue

                if node.target == other.source:

                    node.dependencies.append(
                        other
                    )

        return graph