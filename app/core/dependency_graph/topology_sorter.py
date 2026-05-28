class TopologySorter:

    def sort(self, graph):

        visited = set()

        result = []

        def visit(node):

            if node in visited:
                return

            visited.add(node)

            for dependency in node.dependencies:

                visit(dependency)

            result.append(node)

        for node in graph.all_nodes():

            visit(node)

        return reversed(result)